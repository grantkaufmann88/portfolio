# QA report - personal photos edition

## Build and local references

- Python build passed for all 34 HTML pages: 23 project pages (22 listed projects
  plus a legacy redirect), five experience pages, and six main pages.
- The included offline checker passed 2,076 local references, including image
  sources, responsive source sets, gallery links, page fragments and video paths.
- A separate local HTTP check returned HTTP 200 for all 368 unique referenced
  pages and assets beneath a `/portfolio/` repository prefix.
- The ten new photographs and their ten thumbnails are valid WebP images.
  Their actual dimensions match the content data; each thumbnail is at most
  640 pixels on its longest side.
- Every new photo appears on the page assigned in the media inventory.
- Public copies of the new photos contain no EXIF or XMP metadata. Hashes of the
  original uploads were checked again; those original files remain unchanged.

## Responsive rendering and controls

The production HTML, CSS and JavaScript were rendered in Chromium at widths of
360, 390, 768 and 1,440 pixels for each of the four updated pages: SpaceX, About,
NROTC and the go-kart. No horizontal overflow, broken images or JavaScript errors
were detected. Each new inline photo retains its aspect ratio without cropping.
Desktop and phone screenshots were visually inspected. The final preview images
were captured from fresh pages to avoid retained scroll/focus in the test fixture.

The browser environment blocks navigation to local HTTP URLs. Rendering used a
QA-only copy with local images/styles/scripts inlined; no browser URL restrictions
were changed. The shipped files retain ordinary relative URLs, responsive image
source sets and the deferred script. The separate HTTP audit above tested those
actual relative deployment paths. This is not a remote GitHub deployment test.

Passed interaction checks:

- Image viewer opening, image decoding, unique-image counts, arrow navigation,
  Escape to close, and focus return on all four pages at all four widths.
- All seven new SpaceX inline photo links, captions and full-size viewer targets.
- Unique image counts of seven on SpaceX, one on About, four on NROTC and ten on
  the go-kart page; repeated article/gallery links do not duplicate viewer images.
- Mobile menu opening and Escape-to-close behavior on both phone widths.

## Preservation and limits

A byte-level comparison against the monologue-edition ZIP confirmed:

- No previously delivered files were removed.
- All existing photo and video assets are unchanged.
- The supplied resume is unchanged and still matches its recorded SHA-256.
- The site JavaScript is unchanged.
- HTML changes are confined to the four updated pages and the self-contained
  404 page, which embeds the revised CSS. Other generated pages are unchanged.
- The original 174-file photo inventory remains intact; the ten additions are
  tracked separately under `personal_photos` in the media manifest.

Existing video playback was not re-tested in this photo-only update; the six
standalone video files, poster files, player code and YouTube links are preserved.
Live YouTube availability/playback was not verified. No remote repository write
or GitHub deployment was performed.
