# Grant Kaufmann portfolio - photo-integrated edition

This is the complete, ready-to-preview and ready-to-commit website. It uses the full multi-page portfolio as its base and preserves its visual design. The older eight-project one-page starter was not used.

The folder includes 22 project pages (the existing 21 plus a short Smart home controller entry), five experience pages, all generated HTML, all source JSON, the Python build and preview scripts, styles, JavaScript, the existing resume, and the optimized media. No npm packages or Python packages are needed to build or preview it.

## Open it locally on Windows

Extract the entire ZIP, then open PowerShell inside **Grant-Kaufmann-Portfolio-Updated**, the folder containing `index.html`, `build.py`, `serve.py`, `assets`, and `content`.

```powershell
python build.py
python serve.py
```

The preview opens in your browser at `http://localhost:8000`. Keep PowerShell open while using it. Press Ctrl+C to stop. `START-WINDOWS.bat` is a double-click alternative. On macOS/Linux, use `python3` where necessary.

The build has already been run, so `python serve.py` alone is enough to preview the supplied version. Opening `index.html` directly also works; the local server is preferable for playback and clipboard support.

A different port is available with `python serve.py --port 8001`.

**Important:** do not copy just `build.py`. It reads `content/projects.json`, `content/experience.json`, and `content/profile.json`. All three are included here. Extract or copy the whole folder so the content files stay beside the code in the expected structure.

## Update your existing GitHub repository

Copy the **contents inside** this folder into the existing local portfolio repository, replacing its old files. Keep the existing `.git` directory. Put `index.html` at the repository root rather than nesting this entire folder one level below it. Include the `assets`, `content`, `projects`, `experience`, and `scripts` folders and the `.nojekyll` file.

From PowerShell in that repository:

```powershell
python build.py
python scripts/check_site.py
git add .
git commit -m "Organize project photos and update galleries"
git push
```

The included HTML files are static; GitHub does not need to run Python. Existing GitHub Pages branch/root settings can remain unchanged. No files have been pushed to your account as part of preparing this package.

All site links and media paths are relative, so repository-subfolder hosting is supported. Do not upload the separate sorted-originals archive: the website already includes every media file it uses.

## Where the pictures live

```text
assets/
  projects/
    budget-ebike/
      img_0727.webp
      img_0727-thumb.webp
      videos/
        img_0752.mp4
    desktop-cnc/
    cybertruck-go-kart/
    hurc-mars-rover/
    ...
  experience/
    crls-robotics/
    nrotc/
    rowland/
  images/                    # Existing PDF-extracted photographs and diagrams
  illustrations/             # Retained where no confident photo match exists
content/
  projects.json              # Project covers, captions, galleries, and videos
  experience.json            # Experience pages and galleries
  profile.json               # Existing profile and contact details
  media-manifest.json        # Original filenames, assignments, and publication status
```

There are **119 newly integrated photos**, **five standalone build videos**, and **32 Live Photo clips**. One byte-identical team photo appears only once in the site. The 13 uncertain photos and their four companion clips are preserved in the separate sorted-originals package, not assigned to a guessed project page.

The sorted-originals ZIP also contains all confidently matched originals, unchanged. Open its `PHOTO-REVIEW.html` to browse every original and see the photos that need confirmation. `PHOTO-INTEGRATION.md` in this website folder summarizes the assignments.

## What changed

Project covers and catalog cards now use matching build photos. Photos open in a full-size viewer with Previous/Next controls, arrow-key navigation, Escape to close, and a full-size image link. Long galleries show eight photos initially and keep the rest under an expandable control. All photos remain accessible through the viewer.

The five standalone videos have inline players. A **Play Live Photo** control reveals each paired clip; opening the page never starts playback automatically. HURC, CRLS robotics, NROTC, and Rowland experience pages also have appropriate galleries. The HURC experience page references the same rover assets rather than duplicating them.

Images have correctly applied orientation and stripped metadata in the web copies, with small thumbnails and larger images selected responsively. Videos use browser-ready H.264 MP4. Original source files are untouched in the separate archive.

The existing zero-byte `controller-cad.webp` was removed from the gallery. Other existing images, diagrams, project links, and the resume PDF were retained. The optional resume-regeneration script and font binaries are not part of this edition; the actual resume download remains unchanged.

## Edit a photo, caption, or project

Edit the corresponding entry in `content/projects.json`, then run `python build.py`. Each new gallery item uses explicit paths:

```json
{
  "src": "assets/projects/hurc-mars-rover/img_2683.webp",
  "thumb": "assets/projects/hurc-mars-rover/img_2683-thumb.webp",
  "caption": "Rover chassis, suspension, and manipulator on a workshop stand.",
  "width": 1350,
  "height": 1800,
  "source": "IMG_2683.JPEG"
}
```

Use the actual width and height of the larger image. `thumb` is optional; when used by the supplied responsive-image code, create it with a longest edge of 640 pixels. Set `live` to a relative MP4 path to attach a Live Photo clip. `source` is an optional provenance note.

To change the card and cover, update the project's `image`, `imageThumb`, `imageAlt`, `imageType`, and `position` fields. Keep `image` equal to the selected gallery item's `src` for its responsive thumbnail to be reused on the card. Use `position` to tune the crop on cards; the full project cover and gallery viewer preserve the photograph's full aspect ratio.

Standalone build videos are objects in the project's `videos` array with `src`, `poster`, `caption`, `width`, and `height` fields. Experience galleries use the same image format in `content/experience.json`.

The builder also accepts the original `["image-name", "Caption"]` gallery format, pointing to `assets/images/image-name.webp`.

## Check before committing

```powershell
python build.py
python scripts/check_site.py
```

The offline checker validates page links, responsive images, gallery paths, video paths and posters, titles, project relationships, source-file accounting, and the resume file. See `REVIEW-NOTES.md` for the browser checks performed for this edition. `ORIGINAL-CONTENT-NOTES.md` preserves the prior edition's content-review notes as historical context; its media-gap descriptions no longer reflect this update.
