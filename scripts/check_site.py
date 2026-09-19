#!/usr/bin/env python3
"""Validate the static deliverable without installing anything or accessing the network."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json
ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
 def __init__(self):
  super().__init__();self.ids=set();self.links=[];self.images=[];self.title='';self.h1=0;self.in_title=False;self.errors=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:
   if a['id'] in self.ids:self.errors.append('Duplicate ID '+a['id'])
   self.ids.add(a['id'])
  if tag=='title':self.in_title=True
  if tag=='h1':self.h1+=1
  if tag in ('a','link') and a.get('href'):self.links.append(a['href'])
  if tag in ('img','script') and a.get('src'):self.links.append(a['src'])
  if tag=='img':
   self.images.append(a)
   if 'alt' not in a:self.errors.append('Missing image alt attribute')
  if tag=='a' and a.get('target')=='_blank' and 'noopener' not in a.get('rel',''):self.errors.append('External link missing noopener')
 def handle_endtag(self,tag):
  if tag=='title':self.in_title=False
 def handle_data(self,data):
  if self.in_title:self.title+=data
pages={};errors=[]
for f in ROOT.rglob('*.html'):
 p=Page();p.feed(f.read_text(encoding='utf-8'));pages[f]=p
 if p.h1!=1:errors.append(f'{f.relative_to(ROOT)}: {p.h1} H1 headings')
 errors += [f'{f.relative_to(ROOT)}: {x}' for x in p.errors]
titles=[p.title for p in pages.values()]
if len(set(titles))!=len(titles):errors.append('Duplicate page titles')
references=0
for f,p in pages.items():
 for href in p.links:
  u=urlsplit(href)
  if u.scheme or u.netloc:continue
  references+=1
  if u.path.startswith('/'):errors.append(f'Root-relative link breaks repository hosting: {href}')
  dest=(f.parent/unquote(u.path)).resolve() if u.path else f
  if not dest.exists():errors.append(f'{f.relative_to(ROOT)}: missing {href}')
  if u.fragment and dest in pages and u.fragment not in pages[dest].ids:errors.append(f'{f.relative_to(ROOT)}: missing fragment {href}')
projects=json.loads((ROOT/'content/projects.json').read_text(encoding='utf-8'))
slugs=[p['slug'] for p in projects]
assert len(slugs)==len(set(slugs)), 'Duplicate project slugs'
for p in projects:
 for slug in p['related']:
  if slug not in slugs:errors.append(f'Unknown related project {slug}')
 for name,caption in p['gallery']:
  if not (ROOT/'assets/images'/f'{name}.webp').exists():errors.append(f'Missing gallery image {name}')
 if not (ROOT/'projects'/f'{p["slug"]}.html').exists():errors.append('Missing project page '+p['slug'])
 if p['imageType']=='Project illustration' and 'CONCEPTUAL ILLUSTRATION' not in (ROOT/p['image']).read_text():errors.append('Unlabeled illustration')
resume=ROOT/'assets/downloads/Grant-Kaufmann-Resume.pdf'
assert resume.read_bytes().startswith(b'%PDF-'), 'Invalid resume PDF'
assert (ROOT/'.nojekyll').exists()
if errors:
 print('\n'.join(errors));raise SystemExit(1)
print(f'PASS: {len(pages)} pages, {references} local references, {len(projects)} projects, unique titles, image labels, content relationships, and resume PDF.')
