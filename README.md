# Grant Kaufmann — engineering portfolio

A complete static website for local review and GitHub Pages. Includes 21 project pages, five experience pages, an about page, contact links, and a one-page résumé. All images, styles, and scripts are local. No npm install, API keys, account, or paid hosting are required.

## Preview on your computer

1. Extract this ZIP completely. Open the `grant-kaufmann-portfolio` folder.
2. On Windows, double-click `START-WINDOWS.bat`. A browser should open automatically.
3. Alternatively, open a terminal in this folder and run:

   ```sh
   python serve.py
   ```

   On macOS/Linux use `python3 serve.py` if needed. Python 3 is the only requirement for the server.
4. Visit **http://localhost:8000**. Keep the terminal window open while reviewing. Press **Ctrl+C** to stop.

If port 8000 is busy, run `python serve.py --port 8001` and open http://localhost:8001.

**Without Python:** double-click `index.html`. The pages, navigation, project filters, and galleries work directly from the folder. Copy-to-clipboard may require the local server; the email link remains usable.

The server binds to your computer only (`127.0.0.1`). It does not publish the website. After editing a stylesheet or script, refresh the browser. After editing JSON content or templates, run `python build.py` and refresh.

## What to review first

- Home: overall visual direction, introduction, and selected projects.
- Projects: search, categories, project descriptions, galleries, and linked videos.
- Experience: your role titles, dates, and preferred level of detail.
- About: your voice, interests, and biographical details.
- Contact: email, phone, LinkedIn, and the downloadable résumé.

See `REVIEW-NOTES.md` for the specific content gaps and assumptions. The résumé is newly assembled from your supplied materials and needs your review; it is not the old high-school CV.

## Publish on GitHub Pages when ready

These instructions follow [GitHub's Pages guide](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site).

1. Create a GitHub repository. For your primary site, name it `YOUR-USERNAME.github.io`. For a project site, a name such as `portfolio` also works.
2. Upload the **contents** of this folder to the repository root. `index.html` must be at the root, not inside another `grant-kaufmann-portfolio` folder. Include `assets`, `projects`, `experience`, and `.nojekyll`.
3. In the repository, open **Settings → Pages**.
4. Under **Build and deployment**, choose **Deploy from a branch**, then **main** and **/ (root)**. Save.
5. GitHub displays the site address after deployment. A project site will look like `https://YOUR-USERNAME.github.io/portfolio/`.

There is no build step on GitHub. The generated HTML is already included, and relative links support both root and repository-subfolder hosting. To publish later edits, rebuild locally if you changed the JSON, then upload/commit the updated files.

For command-line Git users, from inside this extracted folder, after creating your empty repository:

```sh
git init
git add .
git commit -m "Add engineering portfolio"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

Replace the uppercase values with your account and repository names. No site has been published as part of this delivery.

## Edit the website

| File | Purpose |
| --- | --- |
| `content/profile.json` | Name, intro, contact information, social links, résumé path |
| `content/projects.json` | All project descriptions, dates, tools, images, galleries, related links |
| `content/experience.json` | Experience roles, descriptions, and related projects |
| `assets/styles.css` | Colors, type sizes, spacing, and responsive layouts |
| `assets/site.js` | Filters, search, menu, gallery lightbox, and email copy |
| `build.py` | Shared page templates and static HTML generator |
| `assets/images/` | Optimized photos extracted from your supplied project PDF |
| `assets/illustrations/` | Original line-art covers for projects without supplied photos |
| `assets/downloads/Grant-Kaufmann-Resume.pdf` | Downloadable résumé; replace with your final version |

### Add or update a project

Edit `content/projects.json` in a text editor. Copy an existing entry when adding a project. Give it a unique `slug`; this becomes its page filename. Each section has a `title` and a `text`. Put related projects' slugs in `related`. Set `featured` to `true` to include it on the homepage and in the Featured filter. Set `brief` to `false` once it has a proper write-up.

The initial homepage layout is optimized for three selected projects. If you add more, they appear in the same grid. The featured project count and catalog total are generated from the content.

Then run:

```sh
python build.py
```

Use `python3` on platforms where necessary. The generator uses only Python's standard library.

### Replace an illustration with a real photo

1. Add a photo under `assets/images`, preferably a 1200–1600px WebP or JPEG.
2. In the project entry, set `image` to its relative path, e.g. `assets/images/rover.webp`.
3. Set `imageAlt` to a useful description and `imageType` to `Prototype photograph`.
4. Set `position` to an object-position such as `50% 40%` to tune the card crop.
5. Add gallery entries like `["rover-detail", "Caption describing this photograph."]`. The current gallery template expects `.webp` files in `assets/images`.
6. Run `python build.py`.

Images in galleries expand at their full aspect ratio. Cover images crop deliberately to preserve the layout. The line drawings are labeled conceptual illustrations and do not claim to depict your actual hardware.

### Replace the résumé

Overwrite `assets/downloads/Grant-Kaufmann-Resume.pdf` with your current résumé using the same filename. All links will keep working. The optional `scripts/make_resume.py` recreates the supplied draft PDF using ReportLab and the bundled DejaVu fonts; it is not needed to run, build, or host the website.

## Technical notes

- Real, independent HTML pages: links and refreshes work without SPA routing.
- Progressive enhancement: all content is in the HTML; JavaScript adds interactions.
- Responsive layouts with keyboard focus styles, a skip link, reduced-motion support, native dialog focus management, descriptive image text, and labeled controls.
- No analytics, remote fonts, tracking scripts, embedded YouTube players, or third-party runtime requests. Videos open on YouTube when selected.
- Contact actions use email and telephone links. There is no pretend form or backend.
- Browser page search and the project filter both work; project filter state is reflected in the URL on HTTP hosting.
- Historical numbers are labeled as targets, estimates, or documented test results.
- A self-contained 404 page searches parent paths for the site homepage, including repository-subfolder deployments.

## Verification

Run `python scripts/check_site.py` for an offline audit of generated links, image references, unique page titles, and content relationships. It uses only Python's standard library. Desktop/mobile visual and interaction checks are documented in `REVIEW-NOTES.md`.
