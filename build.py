#!/usr/bin/env python3
"""Build the static portfolio. Standard-library Python only; no packages to install.
Content: content/*.json. Design: assets/styles.css. Behavior: assets/site.js.
Generated HTML is included so viewing and GitHub Pages do not require a build.
"""
from pathlib import Path
from html import escape as e
import json

ROOT=Path(__file__).resolve().parent
PROJECTS=json.loads((ROOT/'content/projects.json').read_text(encoding='utf-8'))
EXPERIENCE=json.loads((ROOT/'content/experience.json').read_text(encoding='utf-8'))
PROFILE=json.loads((ROOT/'content/profile.json').read_text(encoding='utf-8'))
BY_SLUG={p['slug']:p for p in PROJECTS}
EX_BY_SLUG={p['slug']:p for p in EXPERIENCE}
ARROW='<span class="arrow" aria-hidden="true">↗</span>'

def text_link(href,label,extra=''):
 return f'<a class="text-link" href="{e(href)}" {extra}>{e(label)} {ARROW}</a>'
def button(href,label,primary=False,extra=''):
 return f'<a class="button{ " primary" if primary else ""}" href="{e(href)}" {extra}>{e(label)} {ARROW}</a>'
def ext(href,label):
 return f'<a href="{e(href)}" target="_blank" rel="noopener noreferrer">{e(label)} <span aria-hidden="true">↗</span><span class="sr-only"> (opens in a new tab)</span></a>'
def header(active,prefix):
 links=''.join(f'<a href="{prefix}{slug}.html"'+(' aria-current="page"' if slug==active else '')+f'>{name}</a>' for slug,name in [('projects','Projects'),('experience','Experience'),('about','About'),('contact','Contact')])
 return f'''<a class="skip-link" href="#main">Skip to content</a><header class="site-header"><div class="wrap header-inner"><a class="brand" href="{prefix}index.html" aria-label="Grant Kaufmann home"><span class="brand-mark" aria-hidden="true">GK.</span>Grant Kaufmann</a><button class="menu-toggle js-only" aria-expanded="false" aria-controls="site-nav">Menu +</button><nav class="nav" id="site-nav" aria-label="Main navigation">{links}<a class="resume-link" href="{prefix}{PROFILE['resume']}" download>Résumé ↓</a></nav></div></header>'''
def footer(prefix):
 return f'''<footer class="footer"><div class="wrap"><div class="footer-top"><div><div class="eyebrow">Have something in mind?</div><h2>Let’s build something.</h2></div>{button(prefix+'contact.html','Get in touch')}</div><div class="footer-bottom"><span>© 2026 Grant Kaufmann · Cambridge, MA</span><div class="footer-links">{ext(PROFILE['linkedin'],'LinkedIn')}{ext(PROFILE['youtube'],'YouTube')}<a href="mailto:{PROFILE['email']}">Email ↗</a><a href="#top">Back to top ↑</a></div></div></div></footer>'''
def shell(title,description,body,active='',prefix='',extra=''):
 return f'''<!doctype html>
<html lang="en" id="top"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#f8f7f3"><title>{e(title)} | Grant Kaufmann</title><meta name="description" content="{e(description)}"><meta property="og:title" content="{e(title)} | Grant Kaufmann"><meta property="og:description" content="{e(description)}"><meta property="og:type" content="website"><link rel="icon" type="image/svg+xml" href="{prefix}assets/favicon.svg"><link rel="stylesheet" href="{prefix}assets/styles.css"><script src="{prefix}assets/site.js" defer></script>{extra}</head><body>{header(active,prefix)}<main id="main">{body}</main>{footer(prefix)}</body></html>'''
def write(path,html):
 out=ROOT/path;out.parent.mkdir(parents=True,exist_ok=True);out.write_text(html+'\n',encoding='utf-8')
def card(p,prefix='',featured_layout=False):
 badge='<span class="badge featured">Selected project</span>' if p['featured'] else ('<span class="badge">Brief entry</span>' if p['brief'] else '')
 link=f"{prefix}projects/{p['slug']}.html"
 search=' '.join([p['title'],p['category'],p['summary'],*p['tools']])
 cover=next((normalize_media(m) for m in p['gallery'] if normalize_media(m)['src']==p['image']), {'src':p['image']})
 image_attrs=responsive_attrs(cover,prefix,'(max-width: 620px) 90vw, (max-width: 960px) 45vw, 640px')
 return f'''<article class="project-card" data-project data-category="{e(p['category'])}" data-featured="{str(p['featured']).lower()}" data-search="{e(search)}"><a class="card-image-link" href="{link}" tabindex="-1" aria-hidden="true"><img class="card-image" {image_attrs} alt="" width="600" height="460" loading="lazy" style="object-position:{p['position']}">{badge}</a><div class="card-copy"><div class="card-meta mono"><span>{e(p['category'])}</span><span class="year">{e(p['year'])}</span></div><h3><a href="{link}">{e(p['title'])}</a></h3><p>{e(p['summary'])}</p>{'<div class="card-cta">'+text_link(link,'Explore the project')+'</div>' if featured_layout else ''}</div></article>'''
def intro(kicker,title,description):
 return f'<section class="wrap page-intro"><div class="eyebrow accent">{kicker}</div><h1>{title}</h1><p>{description}</p></section>'
def note():
 return '''<div class="work-note"><div class="eyebrow">A note from the workbench</div><span class="note-mark" aria-hidden="true">+</span><blockquote>“Building tools and components has given me a deeper understanding of making.”</blockquote><div class="note-bottom eyebrow">Grant Kaufmann</div></div>'''


def normalize_media(item):
 """Accept both explicit image objects and the original [name, caption] entries."""
 if isinstance(item, dict):
  return item
 name, caption = item
 return {'src': 'assets/images/' + name + '.webp', 'caption': caption, 'width': 1200, 'height': 900}

def responsive_attrs(media, prefix, sizes):
 """Width descriptors use actual proportional image widths, including portraits."""
 src=prefix+media['src']; thumb=media.get('thumb')
 if not thumb:
  return f'src="{e(src)}"'
 width=media.get('width',1800);height=media.get('height',1800)
 thumb_width=max(1,round(width*min(1,640/width,640/height)))
 return f'src="{e(prefix+thumb)}" srcset="{e(prefix+thumb)} {thumb_width}w, {e(src)} {width}w" sizes="{e(sizes)}"'

def gallery_markup(items, prefix='../', title='From the build.'):
 if not items:
  return ''
 figures=[]
 for raw in items:
  media=normalize_media(raw)
  src=prefix+media['src']; caption=media['caption']
  attrs=responsive_attrs(media,prefix,'(max-width: 620px) 43vw, (max-width: 960px) 30vw, 340px')
  live=''
  if media.get('live'):
   live_src=prefix+media['live'];poster=prefix+media.get('thumb',media['src'])
   live=f'<details class="live-photo"><summary>Play Live Photo</summary><video controls playsinline preload="none" poster="{e(poster)}" aria-label="Live Photo: {e(caption)}"><source src="{e(live_src)}" type="video/mp4"><a href="{e(live_src)}">Open the video</a></video></details>'
  figures.append(f'<figure><a class="gallery-open" href="{e(src)}" data-gallery-src="{e(src)}" data-caption="{e(caption)}" aria-label="Enlarge image: {e(caption)}"><img {attrs} alt="{e(caption)}" width="{media.get("width",1200)}" height="{media.get("height",900)}" loading="lazy" decoding="async"><span class="gallery-expand" aria-hidden="true">+</span></a><figcaption>{e(caption)}</figcaption>{live}</figure>')
 visible=''.join(figures[:8]);more=''
 if len(figures)>8:
  more=f'<details class="gallery-more"><summary>View {len(figures)-8} more photos <span aria-hidden="true">+</span></summary><div class="gallery">'+''.join(figures[8:])+'</div></details>'
 return f'<section class="gallery-section" id="build-photos"><div class="gallery-heading"><h2>{e(title)}</h2><span class="mono">{len(figures)} photos</span></div><p class="gallery-help">Select any photo to open the full-size gallery.</p><div class="gallery">{visible}</div>{more}</section>'

def video_markup(items,prefix='../'):
 if not items:return ''
 figures=[]
 for media in items:
  src=prefix+media['src'];poster=prefix+media['poster'];caption=media['caption']
  figures.append(f'<figure class="video-figure"><video controls playsinline preload="none" poster="{e(poster)}" width="{media["width"]}" height="{media["height"]}" aria-label="{e(caption)}"><source src="{e(src)}" type="video/mp4"><a href="{e(src)}">Open the video</a></video><figcaption>{e(caption)}</figcaption></figure>')
 return '<section class="video-section" id="build-videos"><h2>See it in motion.</h2><div class="video-gallery">'+''.join(figures)+'</div></section>'

def lightbox_markup():
 return '<dialog id="lightbox" class="lightbox" aria-label="Project image viewer"><div class="lightbox-toolbar"><span data-image-count aria-live="polite"></span><div class="lightbox-actions"><a data-original target="_blank" rel="noopener noreferrer">Open full-size photo</a><button data-close aria-label="Close image viewer" autofocus>Close &times;</button></div></div><img class="lightbox-image" alt=""><div class="lightbox-bottom"><p class="lightbox-caption" aria-live="polite"></p><div class="lightbox-controls"><button data-prev aria-label="Previous image">&larr;</button><button data-next aria-label="Next image">&rarr;</button></div></div></dialog>'

def home():
 affiliation=''.join(f'<a href="experience/{slug}.html">{name}<small>{role}</small></a>' for slug,name,role in [('spacex','SpaceX','Engineering intern'),('rowland','Harvard Rowland','Research assistant'),('hurc','HURC','Vice president'),('nrotc','NROTC','Midshipman')])
 rows=''
 for ex in EXPERIENCE[:4]:
  rows+=f'''<a class="experience-row" href="experience/{ex['slug']}.html"><span class="org-mark" aria-hidden="true">{ex['mark']}</span><span class="org">{e(ex['org'])}</span><span class="role">{e(ex['title'])}</span><span class="period mono">{e(ex['period'])}</span>{ARROW}</a>'''
 selected=''.join(card(p,featured_layout=True) for p in PROJECTS if p['featured'])
 body=f'''<div class="wrap"><section class="hero"><div class="hero-copy reveal"><div class="eyebrow"><span class="status-dot"></span>Mechanical engineer. Lifelong maker.</div><h1>I make things<br>that <em>move.</em></h1><p>{e(PROFILE['intro'])}</p><div class="actions">{button('projects.html','Explore my projects',True)}{text_link('about.html','A little about me')}</div></div><figure class="hero-visual reveal"><img class="hero-image" src="assets/images/cnc-milling.webp" alt="My homemade CNC mill cutting traces into a copper circuit board" width="800" height="850" fetchpriority="high"><span class="image-corner mono">FROM MY WORKBENCH / 01</span><div class="hero-detail" aria-hidden="true"><img src="assets/images/motor-stator.webp" alt="" width="135" height="132"><span class="mono">DESIGN. BUILD. ITERATE.</span></div><figcaption class="hero-caption mono"><span>Custom PCB on my homemade CNC mill</span><span>Cambridge, MA ↗</span></figcaption><span class="hero-cross" aria-hidden="true">+</span></figure></section><div class="affiliations"><div class="eyebrow">Learning by doing.<br>In good company.</div>{affiliation}</div><section class="section"><div class="section-head"><div><div class="eyebrow accent">01 / Selected work</div><h2>From idea to something real.</h2></div>{text_link('projects.html',f'All {len(PROJECTS)} projects')}</div><div class="project-grid selected-grid">{selected}</div></section></div><section class="experience-band section"><div class="wrap"><div class="section-head"><div><div class="eyebrow">02 / Beyond my own workbench</div><h2>Built with others.</h2></div><a class="text-link" href="experience.html">Explore my experience {ARROW}</a></div>{rows}</div></section><section class="wrap section about-teaser two-col"><div><div class="eyebrow accent">03 / A little more human</div><h2 style="margin-top:22px">Curiosity doesn’t<br>clock out.</h2><p>Sometimes that means one more prototype. Sometimes it means a long hike in Maine, playing violin, or running along the Charles with my dog. I like a challenge—and the people I get to share it with.</p>{text_link('about.html','Beyond engineering')}</div>{note()}</section>'''
 write('index.html',shell('Mechanical engineer & maker',PROFILE['intro'],body,extra='<link rel="preload" as="image" href="assets/images/cnc-milling.webp">'))

def catalog():
 filters=''.join(f'<button class="filter" data-filter="{cat}" aria-pressed="{str(cat=="All").lower()}">{cat}</button>' for cat in ['All','Featured','Robotics','Electronics','Mechanisms','Fabrication','Research','Software','Coursework'])
 body=intro('The project archive','Made. Tested. Reimagined.', 'A collection of mechanisms, electronics, and things I wanted to understand by building. Start with a featured project, or follow your curiosity.')
 body+=f'''<section class="wrap catalog" aria-label="Projects"><div class="catalog-controls js-only"><div class="filters" role="group" aria-label="Filter projects by category">{filters}</div><label class="search-box"><span aria-hidden="true">⌕</span><span class="sr-only">Search projects</span><input id="project-search" type="search" placeholder="Search projects…" autocomplete="off"></label></div><div class="catalog-status"><span id="result-count" aria-live="polite" aria-atomic="true">{len(PROJECTS)} projects</span><span>Brief entries have more documentation on the way.</span></div><div class="project-grid" data-catalog>{''.join(card(p) for p in PROJECTS)}</div><div id="empty-state" class="empty-state" hidden><h2>No projects found.</h2><p>Try a different term or explore the full collection.</p><button class="button" id="reset-filters">Reset filters <span aria-hidden="true">↗</span></button></div></section>'''
 write('projects.html',shell('Projects',f'Explore {len(PROJECTS)} projects in robotics, electronics, mechanical design, fabrication, and research.',body,'projects'))

def related(slugs,prefix='../'):
 if not slugs:return ''
 return f'''<section class="wrap related"><div class="section-head"><div><div class="eyebrow accent">Keep exploring</div><h2>Connected projects.</h2></div>{text_link(prefix+'projects.html','The full collection')}</div><div class="project-grid">{''.join(card(BY_SLUG[s],prefix) for s in slugs)}</div></section>'''

def project_pages():
 for p in PROJECTS:
  pre='../';is_ill=p['imageType']=='Project illustration'
  title=p['title'];tags=''.join(f'<span class="tag">{e(t)}</span>' for t in p['tools'])
  links=''.join(ext(url,label) for label,url in p['links'])
  if p.get('experience'):
   ex=EX_BY_SLUG[p['experience']];links+=f'<a href="../experience/{ex["slug"]}.html">Related experience: {e(ex["org"])} ↗</a>'
  side=f'''<aside class="detail-sidebar" aria-label="Project information"><dl class="meta-list"><dt>Context</dt><dd>{e(p['role'])}</dd><dt>Project period</dt><dd>{e(p['year'])}</dd><dt>Focus</dt><dd><div class="tag-list">{tags}</div></dd></dl><div class="side-links">{links}<a href="../contact.html">Ask me about this project ↗</a></div></aside>'''
  metrics=''
  if p.get('metrics'):metrics='<div class="metrics">'+''.join(f'<div><strong>{e(value)}</strong><span>{e(label)}</span></div>' for value,label in p['metrics'])+'</div>'
  notice='<div class="brief-notice"><div class="eyebrow">Project brief</div><p>Full build documentation is on the way.</p></div>' if p['brief'] else ''
  prose=''.join(f'<section><h2>{e(s["title"])}</h2><p>{e(s["text"])}</p></section>' for s in p['sections'])
  gallery=gallery_markup(p['gallery'])
  video_section=video_markup(p.get('videos',[]))
  gallery_dialog=lightbox_markup() if p['gallery'] else ''
  media_links=[]
  if p['gallery']:media_links.append(text_link('#build-photos',f"View {len(p['gallery'])} photos"))
  if p.get('videos'):media_links.append(text_link('#build-videos','Watch the build'))
  jump_links='<div class="media-jumps">'+''.join(media_links)+'</div>' if media_links else ''
  body=f'''<section class="wrap detail-intro"><nav class="breadcrumb" aria-label="Breadcrumb"><a href="../index.html">Home</a><span aria-hidden="true">/</span><a href="../projects.html">Projects</a><span aria-hidden="true">/</span><span aria-current="page">{e(title)}</span></nav><div class="eyebrow accent">{e(p['category'])} / {e(p['year'])}</div><h1>{e(title)}.</h1><p class="lead">{e(p['summary'])}</p>{jump_links}</section><div class="wrap"><figure class="detail-cover{' illustration' if is_ill else ' photograph'}"><img src="../{p['image']}" alt="{e(p['imageAlt'])}" width="1280" height="540" style="object-position:{p['position']}" fetchpriority="high"><figcaption>{'Conceptual illustration · Build photos to follow' if is_ill else e(p['imageAlt'])}</figcaption></figure><div class="detail-body">{side}<div class="prose">{notice}{metrics}{prose}{gallery}{video_section}</div></div></div>{related(p['related'])}{gallery_dialog}'''
  write(f"projects/{p['slug']}.html",shell(title,p['summary'],body,'projects','../'))

def experiences():
 items=''
 for x in EXPERIENCE:
  items+=f'''<a class="experience-item" href="experience/{x['slug']}.html"><span class="org-mark" aria-hidden="true">{x['mark']}</span><div><div class="eyebrow">{e(x['kind'])} / {e(x['period'])}</div><h2>{e(x['org'])}</h2><div class="job-title">{e(x['title'])}</div></div><p>{e(x['summary'])}</p>{ARROW}</a>'''
 body=intro('Experience','Different settings.<br>The same curiosity.', 'Research, industry, student robotics, and service. The teams and places that have shaped how I work.')+f'<section class="wrap experience-list" aria-label="Experience">{items}</section>'
 write('experience.html',shell('Experience','Research at Harvard Rowland, a SpaceX internship, robotics leadership, and NROTC.',body,'experience'))
 for x in EXPERIENCE:
  experience_gallery=gallery_markup(x.get('gallery',[]),title='A closer look.')
  experience_dialog=lightbox_markup() if x.get('gallery') else ''
  body=f'''<section class="wrap detail-intro"><nav class="breadcrumb" aria-label="Breadcrumb"><a href="../index.html">Home</a><span aria-hidden="true">/</span><a href="../experience.html">Experience</a><span aria-hidden="true">/</span><span aria-current="page">{e(x['org'])}</span></nav><div class="eyebrow accent">{e(x['kind'])} / {e(x['period'])}</div><h1>{e(x['title'])}.</h1><p class="lead">{e(x['org'])}</p></section><div class="wrap"><div class="experience-detail-mark"><span class="large-mark" aria-hidden="true">{x['mark']}</span><div><div class="eyebrow">{e(x['kind'])}</div><div class="org-name">{e(x['org'])}</div></div></div><div class="detail-body"><aside class="detail-sidebar"><dl class="meta-list"><dt>Role</dt><dd>{e(x['title'])}</dd><dt>Period</dt><dd>{e(x['period'])}</dd></dl><div class="side-links"><a href="../{PROFILE['resume']}" download>Download résumé ↓</a><a href="../contact.html">Get in touch ↗</a></div></aside><div class="prose">{''.join(f'<section><h2>{e(t)}</h2><p>{e(s)}</p></section>' for t,s in x['sections'])}{experience_gallery}</div></div></div>{related(x['projects'])}{experience_dialog}'''
  write('experience/'+x['slug']+'.html',shell(x['title']+' at '+x['org'],x['summary'],body,'experience','../'))

def about():
 body=intro('About Grant','Engineer by training.<br>Maker by nature.', 'Harvard College ’28 · Mechanical Engineering · Cambridge, Massachusetts')
 body+=f'''<section class="wrap about-opening"><div><p class="lead">I like understanding how things work. My favorite way to find out is to build them.</p><p>{e(PROFILE['intro'])} {e(PROFILE['bio'])}</p><p>Before college, I learned much of my engineering through independent projects at home and at Cambridge Rindge and Latin. Building my own tools, stretching a small budget, and chasing questions outside the classroom shaped how I approach a problem.</p><p>I’m especially interested in the point where mechanics and electronics meet—and in making useful technology affordable enough for more people to use.</p><div class="actions" style="margin-top:28px">{text_link('experience.html','My experience')}{text_link(PROFILE['resume'],'Download résumé','download')}</div></div>{note()}</section><section class="wrap skills-section"><div class="eyebrow accent">A practical toolkit</div><h2 style="margin-top:17px">Across the workbench.</h2><div class="skills-grid"><div><h3>Design & fabrication</h3><p>Onshape, Fusion 360, FDM and SLA printing, CNC milling, welding, and carpentry.</p></div><div><h3>Electronics & code</h3><p>PCB design, soldering, Arduino, motor control, C/C++, Python, and hands-on troubleshooting.</p></div><div><h3>Working with people</h3><p>Student robotics leadership, project-based teaching, mentoring, and communication in English and Spanish.</p></div></div></section><section class="outside"><div class="wrap"><div class="eyebrow accent">Away from the workbench</div><h2>There’s a whole world outside.</h2><svg class="trail-line" viewBox="0 0 550 90" fill="none" aria-hidden="true"><path d="M0 76l36-8 31-30 22 18 47-46 43 50 25-15 28 25 33-35 35 13 27-35 43 46 33-20 23 26 24-13 38 24 42-19 20 15" stroke="#8b9787"/><path d="M18 79q112-31 176-13t132-2 167 15" stroke="#b54828" stroke-dasharray="4 6"/><circle cx="18" cy="79" r="4" fill="#b54828"/><circle cx="493" cy="79" r="4" fill="#b54828"/></svg><div class="outside-stories"><div><h3>Maine, on foot and by canoe.</h3><p>In 2023, I spent 22 days hiking 216 miles of the Appalachian Trail in Maine with friends. I’ve also paddled the Allagash Wilderness Waterway. Mud, rain, and headwinds have a way of creating the stories we keep telling—and the space to come back with a clearer head.</p></div><div><h3>Music, a dog, and a different pace.</h3><p>I play violin and enjoy running along the Charles with my dog. I grew up speaking English and Spanish in a dual-language school, and I like helping people feel at home in a classroom or workshop. Making things is a big part of my life; sharing it with people is just as much a part.</p></div></div></div></section>'''
 write('about.html',shell('About','Meet Grant Kaufmann: Harvard mechanical engineering student, maker, researcher, and outdoor enthusiast.',body,'about'))

def contact():
 body=intro('Contact','Good work starts<br>with a conversation.', 'Have a project, an opportunity, or a question about something I’ve built? I’d love to hear from you.')
 body+=f'''<section class="wrap contact-layout"><div><div class="contact-list"><div class="contact-row"><div><div class="eyebrow">Email</div><a href="mailto:{PROFILE['email']}">{PROFILE['email']}</a></div><button class="copy-button js-only" data-copy="{PROFILE['email']}" aria-label="Copy email address">Copy</button></div><div class="contact-row"><div><div class="eyebrow">Phone</div><a href="tel:{PROFILE['phoneHref']}">{PROFILE['phone']}</a></div>{ARROW}</div><div class="contact-row"><div><div class="eyebrow">Professional</div>{ext(PROFILE['linkedin'],'Connect on LinkedIn')}</div></div><div class="contact-row"><div><div class="eyebrow">Builds in motion</div>{ext(PROFILE['youtube'],'Watch my projects')}</div></div></div><p class="contact-message" id="copy-status" role="status" aria-live="polite">Based in Cambridge, Massachusetts.</p></div><aside class="contact-aside"><div class="eyebrow accent">The short version</div><h2>Take my résumé<br>with you.</h2><p>Education, experience, selected projects, and the tools I work with, in one page.</p>{button(PROFILE['resume'],'Download résumé',True,'download')}<p style="font-size:11px;margin:16px 0 0">PDF · September 2026</p></aside></section>'''
 write('contact.html',shell('Contact','Contact Grant Kaufmann by email, phone, or LinkedIn and download his résumé.',body,'contact'))

if __name__=='__main__':
 home();catalog();project_pages();experiences();about();contact()
 body='<section class="wrap not-found"><div class="eyebrow accent">404 / A wrong turn</div><h1>Back to the workbench.</h1><p>This page isn’t here. Let’s get you back to the projects.</p>'+button('./index.html','Go home',True)+'</section>'
 recovery="""<script>(async()=>{const parts=location.pathname.split('/').filter(Boolean);if(parts.at(-1)?.includes('.'))parts.pop();for(let i=parts.length;i>=0;i--){const base='/'+parts.slice(0,i).join('/')+(i?'/':'');try{const r=await fetch(base+'index.html');if(r.ok&&(await r.text()).includes('Grant Kaufmann')){document.querySelector('a').href=base+'index.html';break;}}catch{}}})();</script>"""
 css=(ROOT/'assets/styles.css').read_text(encoding='utf-8')
 write('404.html','<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page not found | Grant Kaufmann</title><style>'+css+'</style><body><main>'+body+'</main>'+recovery+'</body></html>')
 (ROOT/'.nojekyll').touch()
 print(f'Built {len(list(ROOT.rglob("*.html")))} static pages.')
