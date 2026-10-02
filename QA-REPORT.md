# QA report - Vera Rubin actuator edition

Date: 2026-10-02

- `python build.py`: PASS - 23 project pages, 5 experience pages, 6 main pages.
- `python scripts/check_site.py`: PASS - 34 HTML pages, 2,136 local references, 23 projects, 174 historical source files accounted for.
- New Rubin media paths: PASS.
- Standalone project videos: PASS - 7 referenced MP4 files, no orphan MP4s.
- Current-work labels: Rubin and micro swarming drone render **Currently Working On**; HURC retains **Ongoing**.
- Project ordering: Rubin first, drone second in `content/projects.json` and the project catalog.
- Resume checksum and local links: PASS.
- Image headers, gallery/lightbox references, and video poster/source references: PASS.

Browser screenshot automation is blocked in this execution environment, so this edition relies on the unchanged responsive templates/CSS plus structural site checks rather than a new browser-render screenshot pass.
