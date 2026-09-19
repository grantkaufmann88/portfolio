#!/usr/bin/env python3
"""Build the static portfolio using Python's standard library.

Edit content/*.json, then run python build.py. Generated HTML is included in the
release; GitHub Pages and the local preview do not need Python to render pages.
All internal URLs are relative so the site also works inside a repository path.
"""
from __future__ import annotations

import json
import re
import sys
from html import escape
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parent


def load(name: str):
    path = ROOT / 'content' / name
    if not path.is_file():
        raise SystemExit(f'Missing {path}. Extract the entire website folder before building.')
    return json.loads(path.read_text(encoding='utf-8'))


PROJECTS = load('projects.json')
EXPERIENCE = load('experience.json')
PROFILE = load('profile.json')
BY_SLUG = {p['slug']: p for p in PROJECTS}
EX_BY_SLUG = {x['slug']: x for x in EXPERIENCE}
LISTED = [p for p in PROJECTS if p.get('listed', True)]
ARROW = '<span aria-hidden="true">&#8599;</span>'


def e(value) -> str:
    return escape(str(value), quote=True)


def write(path: str, html: str) -> None:
    out = ROOT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html + '\n', encoding='utf-8')


def local_url(path: str, prefix: str = '') -> str:
    if not path or path.startswith(('#', 'https:', 'http:', 'mailto:', 'tel:')):
        return path
    return prefix + path


def link(url: str, label: str, prefix: str = '', cls: str = '', download: bool = False) -> str:
    external = url.startswith(('https://', 'http://'))
    extra = ' target="_blank" rel="noopener noreferrer"' if external else ''
    extra += ' download' if download else ''
    return f'<a href="{e(local_url(url, prefix))}" class="{e(cls)}"{extra}>{e(label)} {ARROW if external else ""}</a>'


def paragraphs(text: str) -> str:
    return ''.join(f'<p>{e(part.strip())}</p>' for part in text.split('\n\n') if part.strip())


def normalize_media(item) -> dict:
    if isinstance(item, dict):
        return item
    name, caption = item
    return {'src': f'assets/images/{name}.webp', 'caption': caption, 'width': 1200, 'height': 900}


def image(media: dict, prefix: str = '', alt: str | None = None, cls: str = '', eager: bool = False, sizes: str = '100vw') -> str:
    src = local_url(media['src'], prefix)
    width, height = media.get('width', 1200), media.get('height', 900)
    attrs = f'src="{e(src)}"'
    if media.get('thumb'):
        thumb = local_url(media['thumb'], prefix)
        tw = media.get("thumbWidth", max(1, round(width * min(1, 640 / width, 640 / height))))
        attrs = f'src="{e(thumb)}" srcset="{e(thumb)} {tw}w, {e(src)} {width}w" sizes="{e(sizes)}"'
    loading = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy"'
    return f'<img {attrs} alt="{e(media.get("caption", "") if alt is None else alt)}" class="{e(cls)}" width="{width}" height="{height}" {loading} decoding="async">'


def cover_media(p: dict) -> dict | None:
    if not p.get('image'):
        return None
    for raw in p.get('gallery', []):
        media = normalize_media(raw)
        if media['src'] == p['image']:
            return media
    return {'src': p['image'], 'caption': p.get('imageAlt', p['title']), 'width': 1200, 'height': 900}


def fit_class(p: dict) -> str:
    if p.get('imageType') in ('CAD model', 'Application screenshot') or p['slug'] in ('gimbaling-tvc', 'transducer-phased-array', 'vacuum-tube-power-supply'):
        return ' contain'
    return ''


def header(active: str, prefix: str) -> str:
    nav = ''.join(f'<a href="{prefix}{slug}.html"' + (' aria-current="page"' if active == slug else '') + f'>{label}</a>' for slug, label in [('projects', 'Projects'), ('experience', 'Experience'), ('about', 'About'), ('contact', 'Contact')])
    return f'''<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header"><div class="wrap header-inner">
<a class="brand" href="{prefix}index.html" aria-label="Grant Kaufmann, home">Grant Kaufmann<span aria-hidden="true">.</span></a>
<button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Menu <span aria-hidden="true">+</span></button>
<nav id="site-nav" class="nav-links" aria-label="Main navigation">{nav}<a class="nav-resume" href="{e(prefix + PROFILE['resume'])}" download>R&eacute;sum&eacute; <span aria-hidden="true">&#8595;</span></a></nav>
</div></header>'''


def footer(prefix: str) -> str:
    return f'''<footer class="site-footer"><div class="wrap footer-inner"><div><a class="footer-name" href="{prefix}index.html">Grant Kaufmann</a><p>Mechanical engineering &middot; Harvard College &rsquo;28</p></div><div class="footer-links">{link('mailto:' + PROFILE['email'], 'Email')}{link(PROFILE['linkedin'], 'LinkedIn')}{link(PROFILE['youtube'], 'YouTube')}{link(PROFILE['resume'], 'R\u00e9sum\u00e9', prefix, download=True)}</div></div><div class="wrap footer-bottom"><span>&copy; 2026 Grant Kaufmann</span><a href="#top">Back to top &#8593;</a></div></footer>'''


def shell(title: str, description: str, body: str, active: str = '', prefix: str = '') -> str:
    full_title = f'{title} | Grant Kaufmann' if title != PROFILE['name'] else 'Grant Kaufmann | Mechanical Engineering'
    return f'''<!doctype html>
<html lang="en" id="top"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#ffffff"><meta name="color-scheme" content="light"><title>{e(full_title)}</title><meta name="description" content="{e(description)}"><meta property="og:title" content="{e(full_title)}"><meta property="og:description" content="{e(description)}"><meta property="og:type" content="website"><meta name="referrer" content="strict-origin-when-cross-origin"><link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="{prefix}assets/styles.css"><script src="{prefix}assets/site.js" defer></script></head><body>{header(active, prefix)}<main id="main">{body}</main>{footer(prefix)}</body></html>'''


def page_intro(kicker: str, title: str, description: str) -> str:
    return f'<section class="wrap page-intro"><p class="eyebrow">{e(kicker)}</p><h1>{e(title)}</h1><p class="intro-text">{e(description)}</p></section>'


def card(p: dict, prefix: str = '', heading: int = 3) -> str:
    href = f"{prefix}projects/{p['slug']}.html"
    media = cover_media(p)
    search = ' '.join([p['title'], p['category'], p['summary'], *p.get('tools', [])])
    photo = ''
    if media:
        photo = f'<a class="card-photo{fit_class(p)}" href="{href}" tabindex="-1" aria-hidden="true" style="--image-position:{e(p.get("position", "center"))}">{image(media, prefix, "", sizes="(max-width: 680px) 92vw, (max-width: 1000px) 44vw, 570px")}</a>'
    else:
        photo = f'<div class="card-text-cover"><span>{e(p["category"])}</span><p>{e(p["title"])}</p><span class="text-cover-detail">{e(p["role"])}</span></div>'
    return f'''<article class="project-card" data-project data-category="{e(p['category'])}" data-featured="{str(p['featured']).lower()}" data-search="{e(search)}">{photo}<div class="card-meta"><span>{e(p['category'])}</span><span class="card-date">{status_badge(p)}{e(p.get('year', ''))}</span></div><h{heading}><a href="{href}">{e(p['title'])}<span aria-hidden="true">&#8599;</span></a></h{heading}><p class="card-summary">{e(p['summary'])}</p></article>'''


def status_badge(p: dict) -> str:
    return '<span class="status-badge">Ongoing</span>' if p.get('status') == 'ongoing' else ''


def article_media(items: list, prefix: str = '../') -> str:
    """Place the actual project photographs beside the relevant discussion."""
    if not items:
        return ''
    figures = []
    for raw in items:
        media = normalize_media(raw)
        caption = media.get('caption', '')
        src = local_url(media['src'], prefix)
        photo = image(media, prefix, sizes='(max-width: 680px) 90vw, 740px')
        natural = ' natural-photo' if media.get('natural') else ''
        portrait = ' portrait-photo' if natural and media.get('height', 0) > media.get('width', 1) else ''
        figures.append(f'<figure class="article-figure{natural}{portrait}"><a class="article-image-open" href="{e(src)}" data-gallery-src="{e(src)}" data-caption="{e(caption)}" aria-label="Enlarge: {e(caption)}">{photo}<span class="expand-label" aria-hidden="true">&#8599;</span></a><figcaption>{e(caption)}</figcaption></figure>')
    layout = ' paired' if len(items) == 2 else ''
    if len(items) == 3 and all(normalize_media(item).get('natural') for item in items):
        layout = ' photo-story'
    return '<div class="article-media' + layout + '">' + ''.join(figures) + '</div>'


def resource_links(items: list, prefix: str = '../') -> str:
    if not items:
        return ''
    return '<div class="section-resource-links">' + ''.join(link(url, label, prefix) for label, url in items) + '</div>'


def context_markup(context: dict, prefix: str = '../') -> str:
    if not context:
        return ''
    return f'<aside class="context-note" aria-label="Project background"><h2>{e(context["title"])}</h2>{paragraphs(context["text"])}{resource_links(context.get("links", []), prefix)}</aside>'


def project_section(s: dict, number: int, prefix: str = '../') -> str:
    return f'<section id="section-{number}"><h2>{e(s["title"])}</h2>{paragraphs(s["text"])}{article_media(s.get("images", []), prefix)}{resource_links(s.get("links", []), prefix)}</section>'


def related(slugs: list, prefix: str = '../', title: str = 'Related projects') -> str:
    items = [BY_SLUG[s] for s in slugs if s in BY_SLUG and BY_SLUG[s].get('listed', True)]
    if not items:
        return ''
    return f'<section class="wrap section related"><div class="section-heading"><h2>{e(title)}</h2>{link("projects.html", "All projects", prefix, "inline-link")}</div><div class="project-grid related-grid">' + ''.join(card(p, prefix) for p in items) + '</div></section>'


def gallery_markup(items: list, prefix: str = '../', title: str = 'Photos & drawings') -> str:
    if not items:
        return ''
    figures = []
    for raw in items:
        media = normalize_media(raw)
        caption, src = media.get('caption', ''), local_url(media['src'], prefix)
        figures.append(f'<figure class="gallery-item"><a href="{e(src)}" class="gallery-open" data-gallery-src="{e(src)}" data-caption="{e(caption)}" aria-label="Enlarge: {e(caption)}">{image(media, prefix, sizes="(max-width: 540px) 88vw, (max-width: 800px) 43vw, 330px")}<span class="expand-label" aria-hidden="true">&#8599;</span></a><figcaption>{e(caption)}</figcaption></figure>')
    more = ''
    if len(figures) > 8:
        more = f'<details class="gallery-more"><summary>Show {len(figures) - 8} more photos</summary><div class="gallery-grid">' + ''.join(figures[8:]) + '</div></details>'
    return f'<section class="section gallery-section" id="photos"><div class="section-heading"><h2>{e(title)}</h2><span class="quiet">{len(figures)} images</span></div><div class="gallery-grid">' + ''.join(figures[:8]) + '</div>' + more + '</section>'


def lightbox() -> str:
    return '''<dialog id="lightbox" class="lightbox" aria-label="Image gallery"><div class="lightbox-toolbar"><span data-image-count aria-live="polite"></span><div><a data-original target="_blank" rel="noopener noreferrer">Open original &#8599;</a><button type="button" data-close aria-label="Close image gallery" autofocus>Close &#215;</button></div></div><div class="lightbox-image-wrap"><img class="lightbox-image" alt=""><button class="image-prev" data-prev type="button" aria-label="Previous image">&#8592;</button><button class="image-next" data-next type="button" aria-label="Next image">&#8594;</button></div><p class="lightbox-caption" aria-live="polite"></p></dialog>'''


def youtube_info(url: str) -> tuple[str, int]:
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    if parsed.hostname in ('youtu.be', 'www.youtu.be'):
        video_id = parsed.path.strip('/').split('/')[0]
    elif parsed.path.startswith(('/shorts/', '/embed/')):
        video_id = parsed.path.strip('/').split('/')[1]
    else:
        video_id = query.get('v', [''])[0]
    if not re.fullmatch(r'[A-Za-z0-9_-]{11}', video_id):
        raise ValueError(f'Invalid YouTube video URL: {url}')
    raw_time = query.get('start', query.get('t', ['0']))[0]
    if raw_time.isdigit():
        start = int(raw_time)
    else:
        start = sum(int(n) * {'h': 3600, 'm': 60, 's': 1}[unit] for n, unit in re.findall(r'(\d+)([hms])', raw_time))
    return video_id, start


def videos_markup(p: dict, prefix: str = '../') -> str:
    clips, embeds = p.get('videos', []), p.get('youtube', [])
    if not clips and not embeds:
        return ''
    cards = []
    for clip in clips:
        src, poster = local_url(clip['src'], prefix), local_url(clip['poster'], prefix)
        cap = clip['caption']
        cards.append(f'''<figure class="video-card"><div class="video-player"><video controls playsinline preload="none" poster="{e(poster)}" width="{clip['width']}" height="{clip['height']}" aria-label="{e(cap)}"><source src="{e(src)}" type="video/mp4">{link(clip['src'], 'Open video', prefix)}</video><button type="button" class="local-video-play" aria-label="Play: {e(cap)}"><span aria-hidden="true">&#9654;</span></button></div><figcaption><strong>{e(cap)}</strong>{link(clip['src'], 'Open video file', prefix, 'video-fallback')}</figcaption></figure>''')
    for item in embeds:
        video_id, start = youtube_info(item['url'])
        media = cover_media(p)
        poster = image(media, prefix, '', sizes='(max-width: 680px) 92vw, 540px') if media else '<span class="video-plain-poster">Grant Kaufmann</span>'
        if item.get('poster'):
            poster = image({'src': item['poster'], 'width': 1280, 'height': 720}, prefix, '', sizes='(max-width: 680px) 92vw, 540px')
        cards.append(f'''<figure class="video-card"><div class="video-player youtube-player" data-youtube="{video_id}" data-start="{start}" data-title="{e(item['title'])}"><a class="youtube-play" href="{e(item['url'])}" target="_blank" rel="noopener noreferrer" aria-label="Play: {e(item['title'])}">{poster}<span class="play-icon" aria-hidden="true">&#9654;</span><span class="video-source">YouTube</span></a></div><figcaption><strong>{e(item['title'])}</strong>{link(item['url'], 'Watch on YouTube', cls='video-fallback')}</figcaption></figure>''')
    return '<section class="section videos-section" id="videos"><div class="section-heading"><h2>Project videos</h2><span class="quiet">Play on click</span></div><div class="video-grid">' + ''.join(cards) + '</div></section>'


def home() -> None:
    main_p = BY_SLUG['desktop-cnc']
    hero_image = image(cover_media(main_p), eager=True, sizes='(max-width: 800px) 92vw, 540px')
    featured = ''.join(card(p) for p in LISTED if p['featured'])
    exp_rows = ''.join(f'<a class="home-experience-row" href="experience/{x["slug"]}.html"><span><strong>{e(x["org"])}</strong><span>{e(x["title"])}</span></span><span class="home-period">{e(x["period"])} {ARROW}</span></a>' for x in EXPERIENCE[:3])
    body = f'''<section class="wrap home-hero"><div class="hero-copy"><p class="eyebrow">Mechanical engineering &middot; Harvard &rsquo;28</p><h1>Grant<br>Kaufmann<span class="accent">.</span></h1><p class="hero-intro">{e(PROFILE['intro'])}</p><div class="actions">{link('projects.html', 'Explore projects', cls='button primary')}{link(PROFILE['resume'], 'Download r\u00e9sum\u00e9', cls='button', download=True)}</div><div class="hero-socials">{link(PROFILE['linkedin'], 'LinkedIn')}{link(PROFILE['youtube'], 'YouTube')}</div></div><figure class="hero-photo"><a href="projects/desktop-cnc.html" aria-label="Explore the homemade CNC mill">{hero_image}</a><figcaption><span>Built at home</span><a href="projects/desktop-cnc.html">Desktop CNC / PCB mill &#8599;</a></figcaption></figure></section>
<section class="wrap section selected-projects"><div class="section-heading"><div><p class="eyebrow">Selected work</p><h2>Projects</h2></div>{link('projects.html', 'View all projects', cls='inline-link')}</div><div class="project-grid">{featured}</div></section>
<section class="experience-band"><div class="wrap home-experience"><div><p class="eyebrow">Beyond independent projects</p><h2>Research, industry,<br>and student robotics.</h2><p>{e(PROFILE['bio'])}</p>{link('experience.html', 'Experience & leadership', cls='inline-link')}</div><div class="home-experience-list">{exp_rows}</div></div></section>
<section class="wrap contact-strip"><div><h2>Get in touch</h2><p>Questions about a project or an engineering opportunity?</p></div>{link('mailto:' + PROFILE['email'], PROFILE['email'], cls='inline-link')}</section>'''
    write('index.html', shell(PROFILE['name'], PROFILE['intro'], body))


def catalog() -> None:
    categories = list(dict.fromkeys(p['category'] for p in LISTED))
    order = ['Robotics', 'Electronics', 'Mechanisms', 'Fabrication', 'Research', 'Coursework']
    categories.sort(key=lambda x: order.index(x) if x in order else len(order))
    filters = '<button type="button" data-filter="all" aria-pressed="true">All</button>' + ''.join(f'<button type="button" data-filter="{e(c)}" aria-pressed="false">{e(c)}</button>' for c in categories)
    body = page_intro('Portfolio', 'Engineering projects', 'Machines, electronics, and experiments. The designs, iterations, and lessons behind each build.')
    body += f'''<section class="wrap catalog-section"><div class="catalog-controls" hidden><div class="filter-buttons" role="group" aria-label="Filter by project category">{filters}</div><div class="search-wrap"><label for="project-search" class="sr-only">Search projects</label><input id="project-search" type="search" placeholder="Search projects" autocomplete="off"><button type="button" data-clear-search aria-label="Clear search" hidden>&#215;</button></div></div><div class="catalog-count"><span data-project-count role="status" aria-live="polite">{len(LISTED)} projects</span></div><div class="project-grid catalog-grid">{''.join(card(p, heading=2) for p in LISTED)}</div><div class="empty-state" hidden><h2>No matching projects</h2><p>Try another search or show all projects.</p><button class="button" type="button" data-reset-filters>Reset filters</button></div></section>'''
    write('projects.html', shell('Projects', 'Explore Grant Kaufmann\'s engineering projects, including robotics, electronics, research instruments, and homemade machines.', body, 'projects'))


def project_pages() -> None:
    for p in PROJECTS:
        prefix = '../'
        if p.get('redirectTo'):
            target = BY_SLUG[p['redirectTo']]
            target_url = target['slug'] + '.html'
            body = page_intro('Project moved', p['title'], p['summary'])
            body += '<div class="wrap section">' + link('projects/' + target_url, target['title'], prefix, 'button primary') + '</div>'
            html = shell(p['title'], p['summary'], body, 'projects', prefix)
            html = html.replace('</head>', f'<meta name="robots" content="noindex"><link rel="canonical" href="{e(target_url)}"><meta http-equiv="refresh" content="0; url={e(target_url)}"></head>')
            write(f'projects/{p["slug"]}.html', html)
            continue
        media = cover_media(p)
        cover = f'<figure class="project-hero-photo{fit_class(p)}">{image(media, prefix, eager=True, sizes="(max-width: 800px) 92vw, 580px")}<figcaption>{e(p.get("imageAlt", media.get("caption", "")))}</figcaption></figure>' if media else ''
        metrics = ''
        if p.get('metrics'):
            metrics = '<dl class="metrics">' + ''.join(f'<div><dt>{e(label)}</dt><dd>{e(value)}</dd></div>' for value, label in p['metrics']) + '</dl>'
        jump = []
        if p.get('sections'):
            jump.append('<a href="#overview">Read the project &#8595;</a>')
        if p.get('videos') or p.get('youtube'):
            jump.append('<a href="#videos">Watch videos &#8595;</a>')
        if p.get('gallery'):
            jump.append('<a href="#photos">View photos &#8595;</a>')
        title_info = '<p class="eyebrow">' + e(p['category']) + (' &middot; ' + e(p['year']) if p.get('year') and p['year'] not in ('Rowland Institute', p['category']) else '') + '</p>'
        meta_items = [('Role', p.get('role')), ('Status', p.get('outcome'))]
        if p.get('experience') in EX_BY_SLUG:
            x = EX_BY_SLUG[p['experience']]
            experience_link = f'<p class="context-link">{link("experience/" + x["slug"] + ".html", x["org"], prefix)}</p>'
        else:
            experience_link = ''
        meta = '<dl class="project-meta">' + ''.join(f'<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>' for k, v in meta_items if v) + '</dl>'
        article_sections = context_markup(p.get('context', {}), prefix) + ''.join(project_section(section, i + 1, prefix) for i, section in enumerate(p['sections']))
        toc = ''.join(f'<a href="#section-{i + 1}">{e(s["title"])}</a>' for i, s in enumerate(p['sections']))
        skills = '<div class="sidebar-group"><h2>Tools &amp; skills</h2><p>' + e(', '.join(p.get('tools', []))) + '</p></div>' if p.get('tools') else ''
        resources = '<div class="sidebar-group"><h2>Resources</h2>' + ''.join(link(url, label, prefix) for label, url in p.get('links', [])) + '</div>' if p.get('links') else ''
        sidebar = f'<aside class="article-sidebar"><nav class="page-contents" aria-label="On this page"><h2>In this project</h2>{toc}</nav>{skills}{resources}</aside>'
        body = f'''<div class="wrap"><nav class="breadcrumb" aria-label="Breadcrumb"><a href="../projects.html">All projects</a><span aria-hidden="true">/</span><span aria-current="page">{e(p['title'])}</span></nav><section class="project-hero{' text-only' if not media else ''}"><div class="project-hero-copy">{title_info}{status_badge(p)}<h1>{e(p['title'])}</h1><p class="intro-text">{e(p['summary'])}</p>{meta}{experience_link}<div class="jump-links">{''.join(jump)}</div></div>{cover}</section>{metrics}{videos_markup(p)}<div class="article-layout" id="overview">{sidebar}<article class="prose" aria-label="Project description">{article_sections}</article></div>{gallery_markup(p.get('gallery', []))}</div>{related(p.get('related', []))}{lightbox() if p.get('gallery') else ''}'''
        write(f'projects/{p["slug"]}.html', shell(p['title'], p['summary'], body, 'projects', prefix))


def experiences() -> None:
    body = page_intro('Background', 'Experience & leadership', 'Research instrumentation, aircraft integration, and teams that build together.')
    rows = []
    for x in EXPERIENCE:
        rows.append(f'''<article class="experience-row"><div class="experience-period"><span>{e(x['period'])}</span><span class="eyebrow">{e(x['kind'])}</span></div><div><h2><a href="experience/{x['slug']}.html">{e(x['org'])} {ARROW}</a></h2><h3>{e(x['title'])}</h3><p>{e(x['summary'])}</p></div></article>''')
    body += '<section class="wrap experience-list" aria-label="Roles">' + ''.join(rows) + '</section>'
    write('experience.html', shell('Experience', 'Grant Kaufmann\'s research, summer 2026 SpaceX internship, robotics leadership, and past NROTC participation.', body, 'experience'))
    for x in EXPERIENCE:
        body = f'<div class="wrap"><nav class="breadcrumb" aria-label="Breadcrumb"><a href="../experience.html">All experience</a><span aria-hidden="true">/</span><span aria-current="page">{e(x["org"])}</span></nav></div>'
        body += page_intro(x['kind'] + ' / ' + x['period'], x['org'], x['title'])
        article = ''.join(f'<section><h2>{e(title)}</h2>{paragraphs(text)}{article_media(x.get("sectionMedia", {}).get(str(i), []))}</section>' for i, (title, text) in enumerate(x['sections']))
        side = '<aside class="article-sidebar"><dl class="meta-list"><div><dt>Role</dt><dd>' + e(x['title']) + '</dd></div><div><dt>Period</dt><dd>' + e(x['period']) + '</dd></div></dl>' + link(PROFILE['resume'], 'Download r\u00e9sum\u00e9', '../', 'inline-link', True) + '</aside>'
        if x['projects']:
            project_links = '<section class="experience-project-links"><h2>Projects from this work</h2><div>' + ''.join(f'<a href="../projects/{slug}.html">{e(BY_SLUG[slug]["title"])} {ARROW}</a>' for slug in x['projects'] if slug in BY_SLUG) + '</div></section>'
        else:
            project_links = ''
        body += f'<div class="wrap">{project_links}<div class="article-layout experience-article">{side}<article class="prose" aria-label="Experience description">{article}</article></div>{gallery_markup(x.get("gallery", []), title=x.get("galleryTitle", "Photos & drawings"))}</div>' + related(x['projects'], title='Explore the work') + (lightbox() if x.get('gallery') or any(x.get('sectionMedia', {}).values()) else '')
        write(f'experience/{x["slug"]}.html', shell(x['org'], x['summary'], body, 'experience', '../'))


def about() -> None:
    body = page_intro('About', 'I learn by building.', 'Mechanical engineering at Harvard College, Class of 2028. Based in Cambridge, Massachusetts.')
    sections = ''.join(f'<section><h2>{e(title)}</h2>{paragraphs(text)}{article_media(PROFILE.get("aboutSectionMedia", {}).get(str(i), []), "")}</section>' for i, (title, text) in enumerate(PROFILE['aboutSections']))
    facts = '<dl class="about-facts">' + ''.join(f'<div><dt>{e(label)}</dt><dd>{e(value)}</dd></div>' for value, label in PROFILE.get('aboutFacts', [])) + '</dl>'
    skills = ''.join(f'<div><h3>{e(title)}</h3><p>{e(text)}</p></div>' for title, text in PROFILE['aboutSkills'])
    actions = link('experience.html', 'Experience & leadership', cls='button') + link(PROFILE['resume'], 'Download r\u00e9sum\u00e9', cls='button', download=True)
    body += f'<section class="wrap about-layout"><div class="prose">{sections}{resource_links(PROFILE.get("aboutLinks", []), "")}<div class="actions">{actions}</div></div><aside class="about-skills">{facts}<h2>Tools I work with</h2>{skills}</aside></section>'
    maker = {'slug': 'maker', 'image': BY_SLUG['cybertruck-go-kart']['image'], 'gallery': BY_SLUG['cybertruck-go-kart']['gallery'], 'youtube': [{'title': 'Earlier maker portfolio', 'url': PROFILE['makerVideo']}], 'videos': []}
    body += '<div class="wrap maker-video"><div class="maker-note"><p class="eyebrow">An earlier chapter</p><h2>My maker portfolio</h2><p>An older video of the independent projects that came before my current research and college work.</p></div>' + videos_markup(maker, '') + '</div>'
    if any(PROFILE.get('aboutSectionMedia', {}).values()):
        body += lightbox()
    write('about.html', shell('About', 'Meet Grant Kaufmann, a Harvard mechanical engineering student, researcher, and independent builder.', body, 'about'))


def contact() -> None:
    body = page_intro('Contact', 'Get in touch', 'For engineering opportunities, collaborations, or questions about a project.')
    body += f'''<section class="wrap contact-layout"><div class="contact-methods"><div class="contact-row"><div><h2>Email</h2><a class="contact-value" href="mailto:{e(PROFILE['email'])}">{e(PROFILE['email'])}</a></div><button class="copy-button" type="button" data-copy="{e(PROFILE['email'])}" hidden>Copy</button></div><div class="contact-row"><div><h2>LinkedIn</h2>{link(PROFILE['linkedin'], 'grant-kaufmann-harvard', cls='contact-value')}</div></div><div class="contact-row"><div><h2>YouTube</h2>{link(PROFILE['youtube'], '@grantkprojects', cls='contact-value')}</div></div><div class="contact-row"><div><h2>Phone</h2><a class="contact-value" href="tel:{e(PROFILE['phoneHref'])}">{e(PROFILE['phone'])}</a></div></div><p class="quiet" id="copy-status" role="status" aria-live="polite">{e(PROFILE['location'])}</p></div><aside class="resume-panel"><p class="eyebrow">Education &amp; experience</p><h2>R&eacute;sum&eacute;</h2><p>My background, selected projects, and technical skills.</p>{link(PROFILE['resume'], 'Download PDF', cls='button primary', download=True)}{link(PROFILE['resume'], 'Open r\u00e9sum\u00e9', cls='inline-link')}</aside></section>'''
    write('contact.html', shell('Contact', 'Email Grant Kaufmann, connect on LinkedIn, watch his engineering projects, or download his r\u00e9sum\u00e9.', body, 'contact'))


def not_found() -> None:
    css = (ROOT / 'assets/styles.css').read_text(encoding='utf-8')
    # Relative assets cannot be relied on for a 404 at an arbitrary nested URL.
    # Keep this page self-contained and find the nearest existing site root.
    recovery = """<script>(()=>{const parts=location.pathname.split('/').filter(Boolean);if(parts.length)parts.pop();const a=document.getElementById('home-link');(async()=>{for(let i=parts.length;i>=0;i--){const base='/'+parts.slice(0,i).join('/')+(i?'/':'');try{const r=await fetch(base+'index.html');if(r.ok&&(await r.text()).includes('Grant Kaufmann')){a.href=base+'index.html';return;}}catch{}}})();})();</script>"""
    write('404.html', f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page not found | Grant Kaufmann</title><style>{css}</style></head><body><main class="wrap not-found"><p class="eyebrow">404</p><h1>Page not found.</h1><p>The page may have moved, or the address may be incomplete.</p><a class="button primary" href="./index.html" id="home-link">Back to the portfolio</a></main>{recovery}</body></html>')


def main() -> None:
    for p in PROJECTS:
        if not re.fullmatch(r'[a-z0-9-]+', p['slug']):
            raise SystemExit('Project slugs may contain only lowercase letters, numbers, and hyphens.')
        for y in p.get('youtube', []):
            youtube_info(y['url'])
    home()
    catalog()
    project_pages()
    experiences()
    about()
    contact()
    not_found()
    (ROOT / '.nojekyll').touch()
    print(f'Built {len(PROJECTS)} project pages, {len(EXPERIENCE)} experience pages, and 6 main pages.')


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, KeyError) as exc:
        print(f'Build failed: {exc}', file=sys.stderr)
        sys.exit(1)
