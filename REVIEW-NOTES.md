# Content review notes - monologue edition

## Source priority and scope

This edition starts from the complete Revised website, then incorporates
`Project and Website Monologue.docx`, its embedded rover photographs, the latest
resume (`Grant-Kaufmann-Resume(1).pdf`), and the newly supplied photos and video.
The earlier transcripts, project documents, presentations and image assignments
remain the basis for details not repeated in the new monologue.

The prose is written for the public project pages, not copied verbatim from the
speech transcription. Individual contributions, team work, requirements,
estimates, observations and demonstrated results are distinguished.
`content/source-map.json` records the source names; the original private working
monologue is not bundled into the public website.

## Changes that resolve earlier review notes

- The newly supplied resume has the corrected May-August 2026 SpaceX dates. It
  replaces the previous PDF byte-for-byte. The old resume mismatch is resolved.
- NROTC is explicitly past participation, ending in spring 2026. Its influence
  on leadership, preparation and fitness remains part of the background.
- The expanded Rubin description now explains the printed strain-wave drive,
  array-board work and backlash/friction tradeoff. The 0.1-degree figure is an
  aiming requirement, not measured accuracy. The project is ongoing.
- The old custom-drives URL redirects to the Rubin project, preserving the
  existing precision-angular-positioning URL rather than leaving two incomplete
  or conflicting descriptions of the same work.
- The drone uses the new roughly $22 high-volume cost estimate. Twenty minutes
  is a flight-time goal; autonomous landing, charging and coordinated tasks are
  development goals, not completed demonstrations. The 52 g figure is labeled
  as an earlier design target where retained.
- The ES125 second-place result comes from the latest monologue. The new video is
  a CAD walkthrough, not a physical drop test. Rotation and jamming of the
  carriage remain an explicit limitation.
- The HURC power-distribution board is credited to the two students Grant
  mentored. His teaching, design guidance and subsystem work are not presented
  as sole authorship of that board.

## Technical details that still need confirmation before adding specifications

1. The sound-array monologue mentions about 125 ns per update and about 20 frames
   per 40 kHz cycle. These figures do not describe the same update interval, so
   neither is published as a performance specification. The earlier poster's
   tested two-bank configuration is kept separate from the intended independent
   control of all 64 elements. A later working per-element controller would need
   a separate update describing what changed and what was tested.
2. The aircraft iteration count differs between accounts (seven recalled models,
   nine designs/iterations on the resume, and another count in an older account).
   The site describes successive iterations without inventing a reconciliation.
3. The boat's very high ignition-module voltage is not treated as a measured
   output. There is no verified voltage specification in the new description.
4. Geophone motion amplitude is a requested target. Mount FEA and the recorded
   few-hundred-hertz sensor range are not a calibrated complete-stand bandwidth.
5. The egg-drop presentation's acceleration requirement and optimization value
   differ. The narrative explains the model and its friction limitation without
   claiming either value was measured or that the ideal profile was validated.
6. The spoken collaborator name and inductor-core identifier are unclear in the
   transcription. No guessed spelling or component part number is published.
7. Supply voltage/current photographs support an approximate bench operating
   point, not measured noise, efficiency, or qualification claims.

## SpaceX and personal content

The public SpaceX page uses a short, high-level description of the Starlink
Aviation internship. Detailed part designs, test procedures, evaluation scores,
fleet counts and integration quantities are not repeated in its prose. The road
trip, hiking, roommates, intercom modification and double-decker couch are clearly
personal activities outside company work.

This is not an independent confidentiality clearance. The requested resume PDF is
included unchanged and still contains the details Grant supplied in that file.
Review the PDF itself before public distribution if any of those items should be
removed. Future Seattle or outdoor photographs can be added without publishing
placeholders or inventing images of those activities.

## Public context and media

Official Rubin Observatory, Harvard SEAS, and University Rover Challenge pages
are linked from short background notes. They explain the observatory or
competition, not Grant's individual results. The Rubin gallery is linked rather
than bundling an unavailable third-party photograph.

Two new rover science-module photos are extracted from the DOCX. The uploaded
board and frame photos and the embedded drill-CAD photo duplicate higher-quality
images already in the website; those existing versions are reused. The Rowland
screenshot has been refreshed, with only browser and desktop chrome cropped.

The prior original-photo archive remains unchanged. The other 11 previously
uncertain photos remain unpublished. `content/media-manifest.json` accounts for
all 174 files in that original collection and records the new media assignments.

## Video limitations

There are six standalone MP4 players in this edition. All six were decoded and
played with the website's controls during local browser testing. No Live Photo
controls or clips were reintroduced. YouTube tiles remain click-to-load, with
always-visible direct links. Embed creation and the supplied CNC start time were
checked, but live YouTube streaming and embedding permissions were not verified
in this environment.

## Resume integrity

All resume links point to `assets/downloads/Grant-Kaufmann-Resume.pdf`.
The expected SHA-256 is stored in `content/profile.json` as `resumeSha256`:

`f96ffb340683cef6745ab539b6660917b6362f008c76b1b3e2c3b81a7312d0ba`

When intentionally replacing the resume in a future edition, update that field
before running `python scripts/check_site.py`.
