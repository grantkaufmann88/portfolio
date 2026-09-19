#!/usr/bin/env python3
"""Offline audit of pages, responsive images, galleries, videos, and content.
Run from any working directory: python scripts/check_site.py
Python standard library only.
"""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json
import hashlib
import re

ROOT = Path(__file__).resolve().parents[1]

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.links = []
        self.title = ''
        self.h1 = 0
        self.in_title = False
        self.errors = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            if a['id'] in self.ids:
                self.errors.append('Duplicate ID: ' + a['id'])
            self.ids.add(a['id'])
        if tag == 'title':
            self.in_title = True
        if tag == 'h1':
            self.h1 += 1
        if tag in ('a', 'link') and a.get('href'):
            self.links.append(a['href'])
        if tag in ('img', 'script', 'source', 'video') and a.get('src'):
            self.links.append(a['src'])
        if tag == 'video' and a.get('poster'):
            self.links.append(a['poster'])
        if a.get('data-gallery-src'):
            self.links.append(a['data-gallery-src'])
        if a.get('srcset'):
            self.links.extend(part.strip().split()[0] for part in a['srcset'].split(','))
        if tag == 'img' and 'alt' not in a:
            self.errors.append('Image missing alt attribute')
        if tag == 'video' and 'controls' not in a:
            self.errors.append('Video missing playback controls')
        if tag == 'a' and a.get('target') == '_blank' and 'noopener' not in a.get('rel', ''):
            self.errors.append('External link missing noopener')

    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data


def main():
    errors = []
    pages = {}
    for path in ROOT.rglob('*.html'):
        page = Page()
        page.feed(path.read_text(encoding='utf-8'))
        pages[path] = page
        if page.h1 != 1:
            errors.append(f'{path.relative_to(ROOT)}: expected one H1, got {page.h1}')
        errors.extend(f'{path.relative_to(ROOT)}: {error}' for error in page.errors)
    titles = [page.title for page in pages.values()]
    if len(set(titles)) != len(titles):
        errors.append('Duplicate page titles')
    references = 0
    for path, page in pages.items():
        for href in page.links:
            url = urlsplit(href)
            if url.scheme or url.netloc:
                continue
            references += 1
            if url.path.startswith('/'):
                errors.append('Root-relative link breaks repository hosting: ' + href)
            destination = (path.parent / unquote(url.path)).resolve() if url.path else path
            if not destination.exists():
                errors.append(f'{path.relative_to(ROOT)}: missing {href}')
            elif destination.is_file() and destination.stat().st_size == 0:
                errors.append(f'{path.relative_to(ROOT)}: empty file {href}')
            if url.fragment and destination in pages and url.fragment not in pages[destination].ids:
                errors.append(f'{path.relative_to(ROOT)}: missing fragment {href}')

    projects = json.loads((ROOT / 'content/projects.json').read_text(encoding='utf-8'))
    experiences = json.loads((ROOT / 'content/experience.json').read_text(encoding='utf-8'))
    slugs = [project['slug'] for project in projects]
    if len(slugs) != len(set(slugs)):
        errors.append('Duplicate project slugs')
    for project in projects:
        for slug in project['related']:
            if slug not in slugs:
                errors.append('Unknown related project: ' + slug)
        if not (ROOT / 'projects' / (project['slug'] + '.html')).exists():
            errors.append('Missing project page: ' + project['slug'])
        image = ROOT / project['image'] if project.get('image') else None
        if image is not None and not image.is_file():
            errors.append('Missing project cover: ' + project['image'])
        elif image is not None and project['imageType'] == 'Project illustration' and 'CONCEPTUAL ILLUSTRATION' not in image.read_text():
            errors.append('Unlabeled illustration: ' + project['image'])
    for item in projects + experiences:
        for media in item.get('gallery', []):
            if isinstance(media, list):
                media = {'src': f'assets/images/{media[0]}.webp'}
            if 'live' in media:
                errors.append('Live Photo control data remains in a gallery')
            for key in ('src', 'thumb'):
                if key in media and not (ROOT / media[key]).is_file():
                    errors.append(f'Missing {key} media: {media[key]}')
        for video in item.get('videos', []):
            for key in ('src', 'poster'):
                if not (ROOT / video[key]).is_file():
                    errors.append(f'Missing video {key}: {video[key]}')

    media_record = json.loads((ROOT / 'content/media-manifest.json').read_text(encoding='utf-8'))
    manifest = media_record['original_photo_inventory']
    for record in media_record['new_images']:
        for key in ('src', 'thumb'):
            if not (ROOT / record[key]).is_file():
                errors.append('Missing added image: ' + record[key])
    if len(manifest) != 174 or len({record['file'] for record in manifest}) != 174:
        errors.append('Source inventory must account for all 174 original files')
    for record in manifest:
        if record['published']:
            for key in ('web_path', 'thumbnail_path'):
                if key in record and not (ROOT / record[key]).is_file():
                    errors.append('Missing published media: ' + record[key])
        elif record['folder'].startswith('needs-review/') and record.get('web_path'):
            errors.append('Unconfirmed original was published: ' + record['file'])
    for image in ROOT.rglob('*.webp'):
        with image.open('rb') as stream:
            head = stream.read(12)
        if head[:4] != b'RIFF' or head[8:12] != b'WEBP':
            errors.append('Invalid WebP image: ' + str(image.relative_to(ROOT)))
    resume = ROOT / 'assets/downloads/Grant-Kaufmann-Resume.pdf'
    if not resume.read_bytes().startswith(b'%PDF-'):
        errors.append('Invalid resume PDF')
    expected_resume_sha256 = json.loads((ROOT / 'content/profile.json').read_text(encoding='utf-8'))['resumeSha256']
    if hashlib.sha256(resume.read_bytes()).hexdigest() != expected_resume_sha256:
        errors.append('Resume differs from the user-supplied PDF for this edition')
    video_sources = {video['src'] for project in projects for video in project.get('videos', [])}
    actual_videos = {path.relative_to(ROOT).as_posix() for path in ROOT.rglob('*.mp4')}
    if actual_videos != video_sources or len(video_sources) != 6:
        errors.append('Expected six referenced standalone project videos, with no orphan files')
    for project in projects:
        if project.get('status') == 'ongoing':
            html = (ROOT / 'projects' / (project['slug'] + '.html')).read_text(encoding='utf-8')
            if 'class="status-badge">Ongoing</span>' not in html:
                errors.append('Missing current-project badge: ' + project['slug'])
        if project.get('redirectTo') and project['redirectTo'] not in slugs:
            errors.append('Unknown redirect destination: ' + project['slug'])
        gallery_urls = [m['src'] for m in project.get('gallery', []) if isinstance(m, dict)]
        if len(gallery_urls) != len(set(gallery_urls)):
            errors.append('Duplicate gallery photo in ' + project['slug'])
    for path in pages:
        text = path.read_text(encoding='utf-8')
        if re.search(r'Play Live Photo|View moving picture|A note from the workbench|CONCEPTUAL ILLUSTRATION|Brief entry', text, re.I):
            errors.append('Obsolete UI content in ' + str(path.relative_to(ROOT)))
    for path in ROOT.rglob('*'):
        if path.suffix.lower() in {'.woff', '.woff2', '.otf', '.ttf'}:
            errors.append('Unexpected bundled font: ' + str(path.relative_to(ROOT)))
    if not (ROOT / '.nojekyll').exists():
        errors.append('Missing .nojekyll file')
    if errors:
        print('\n'.join(errors))
        raise SystemExit(1)
    print(f'PASS: {len(pages)} pages, {references} local references, {len(projects)} projects, '
          f'{len(manifest)} source files accounted for; galleries, videos, titles, links, '
          'image headers, content relationships, and resume checked.')

if __name__ == '__main__':
    main()
