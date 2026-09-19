# Grant Kaufmann - engineering portfolio

A complete static website with project pages, experience pages, organized images,
click-to-play videos, and the supplied resume. No npm, framework, paid service,
or third-party Python package is needed.

## Preview locally

Extract the **entire ZIP**. Open PowerShell or a terminal in the folder containing
`build.py`, `serve.py`, `content`, and `assets`, then run:

```powershell
python serve.py
```

Open `http://localhost:8000`. Keep the terminal open while viewing the site.
Press Ctrl+C to stop the server. `START-WINDOWS.bat` and `START-MAC.command` are
also included.

The HTML is already built. To rebuild after changing text or media:

```powershell
python build.py
python scripts/check_site.py
python serve.py
```

If port 8000 is in use, run `python serve.py --port 8001`.
Opening `index.html` directly works for reading most of the site, but use the
local server for normal testing and embedded videos. YouTube requires internet
access and can block embedding independently of this website.

## Update the existing GitHub repository

Copy the **contents** of this folder into your repository's website root,
replacing existing files. Keep the repository's `.git` directory. Do not put the
entire extracted folder inside another website folder by mistake. The directory
served by GitHub Pages should contain `index.html` and `assets` at the same level.

Then use your normal commit/push workflow, for example:

```powershell
git add .
git commit -m "Add road-trip, Seattle, hiking, and Navy photos"
git push
```

The generated pages are included, so no server-side build is required. Internal
paths are relative and support a project URL such as `/portfolio/` as well as a
site root. `.nojekyll` is included. Nothing has been deployed automatically.

Replacing files does not delete old, unreferenced media already in your
repository. They will not appear in the new interface. This ZIP omits the Live
Photo clips, but preserves the six standalone project videos.

## Edit the content

- `content/profile.json`: introduction, About sections, contact links, resume path, maker video.
- `content/projects.json`: project descriptions, photos, video URLs, and metadata.
- `content/experience.json`: research, internship, and leadership descriptions.
- `assets/styles.css`: responsive layout and visual design.
- `assets/site.js`: filters, mobile navigation, photo viewer, and video controls.
- `build.py`: generates all 34 HTML pages from the JSON files.

After editing the JSON or templates, run `python build.py` again. Editing only the
CSS or JavaScript does not require rebuilding, except that the 404 page embeds
its own CSS and will pick up style changes on the next build.

### Add a photo

Put the image in `assets/projects/<project-slug>/` and add a gallery object:

```json
{
  "src": "assets/projects/desktop-cnc/example.webp",
  "caption": "An accurate description of this stage of the build.",
  "width": 1600,
  "height": 1200
}
```

An optional `thumb` field points to a smaller copy with a maximum dimension of
640 pixels. Provide the actual full-image dimensions so responsive image sizing
is correct. Keep images of circuits and CAD readable; the viewer opens the larger
image without cropping it.

### Add a YouTube video

Use a `youtube` list on the project:

```json
"youtube": [
  {"title": "Build demonstration", "url": "https://www.youtube.com/watch?v=VIDEO_ID"}
]
```

The generator accepts watch, youtu.be, and Shorts links. It preserves supported
start-time parameters. Videos load into the page only after a click; a direct
YouTube link remains below each player. A project image is used as the preview,
not a downloaded YouTube thumbnail. An optional local `poster` image can override
that preview.

For a standalone MP4, use the existing `videos` entries as a template. Include a
poster image, caption, and the video's actual width and height. No Live Photo
controls are generated.

### Keep draft entries off the index

`"listed": false` keeps an entry out of the project grid. The old custom-drives
entry now also uses `"redirectTo": "precision-angular-positioning"`, preserving
its URL while directing visitors to the complete Rubin Observatory project.
Use `"status": "ongoing"` for a visible current-work badge on a card and page.

### Put a photo beside the relevant explanation

A project section may include an `images` list using the same objects as its
`gallery`. A section may also include `links` as `[label, URL]` pairs. Keep the
image in the main gallery too: the viewer deduplicates it automatically.

Experience pages can use a `sectionMedia` object whose keys are zero-based
section numbers, as shown on the HURC experience page. The About page is driven
by `aboutSections`, `aboutFacts`, and `aboutSkills` in `profile.json`.
Use `aboutSectionMedia` with the same zero-based section-number keys to place
photos in the About text. Its images open in the same accessible viewer.
A `galleryTitle` on an experience can customize its gallery heading.

For personal photos, `"natural": true` preserves the full image framing in the
article. Three such images appear as one large image above a pair on desktop;
all stack on mobile. Single portrait photos are kept at a readable width.

## Files and checks

`content/source-map.json` records the source documents used for each write-up.
`content/media-manifest.json` tracks 25 additional images/drawings, the latest
media assignments, all 174 files in the earlier original-photo archive,
and the ten additions listed under `personal_photos`. `PERSONAL-PHOTOS.md` maps
each new upload to its folder and page.
The original photo bytes remain in the separate originals archive; this website
contains web-ready copies. Do not upload the originals ZIP as part of the site.

`PROJECT-COPY.md` is an easy-to-read export of the project/experience/About text.
Edit the JSON rather than that export to change the actual website.
`REVIEW-NOTES.md` lists remaining source ambiguities and the SpaceX scope.
`QA-REPORT.md` records the testing and external-playback limitation.

The included resume is the exact new `Grant-Kaufmann-Resume(1).pdf`. It replaces
the old PDF and contains the correct May-August 2026 SpaceX timeline. Its SHA-256
is stored in `content/profile.json`; update `resumeSha256` when deliberately
replacing the PDF, then run the checker again.

This folder is a complete replacement website, not a patch. All generated HTML,
content JSON, media, build scripts, and preview scripts are included.
