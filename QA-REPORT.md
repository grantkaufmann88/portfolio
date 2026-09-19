# QA report - monologue edition

## Build and source checks

- Python build completes from the included JSON and assets.
- Offline audit passes: 34 HTML files (22 listed projects, one legacy redirect,
  five experience pages, and six main pages), with 1,981 local references.
- Each HTML page has one H1 and a unique title; local paths, fragments, image
  attributes, external-link protections and related-project slugs are checked.
- All 174 original source files remain accounted for in the media inventory.
- No Live Photo UI, bundled fonts, broken image paths or empty referenced files.
- The served resume matches the newly supplied PDF byte-for-byte.

## Browser rendering and controls

Chromium rendered the site's HTML, CSS and JavaScript with local assets inlined
for testing. The container's browser URL restrictions were left unchanged. This
is a rendering/test fixture only; the shipped pages retain their ordinary relative
asset URLs and deferred script. Deployment paths were separately checked over a
local HTTP server.

The normal pages were checked at desktop and phone widths. Updated project,
experience and personal pages were re-rendered after their assets decoded and
visually inspected. Narrow-phone and tablet checks cover representative pages.
No horizontal overflow was detected in those checks.

Passed functional checks:

- Search, category filters, combined no-results state, reset, three ongoing badges.
- Inline lightbox, 9 unique images from 12 links, arrow navigation, Escape, focus restored.
- Expandable photo gallery.
- Six actual local MP4s decoded and played through the production play controls.
- YouTube click-to-embed URL, start time and title checked; live playback not tested.
- Mobile menu toggle/Escape and readable clipboard result.
- No-JavaScript content, navigation, and video-file fallback.

## Local HTTP and media

- 348 unique page/asset URLs returned HTTP 200 under a `/portfolio/` repository prefix.
- New media is served with the expected WebP / MP4 content types.
- All six MP4 files have their playback metadata before media data (fast start).
- The six local videos decoded and advanced playback through the production
  play controls, including the new ES125 CAD walkthrough.

## Limits

Live YouTube playback was not checked. Availability, embedding permission,
network filters and browser policy can affect external players independently of
this website. Their direct YouTube links remain available without JavaScript.
No real GitHub deployment or remote-repository write was performed. Source
precision and confidentiality review notes are in `REVIEW-NOTES.md`.
