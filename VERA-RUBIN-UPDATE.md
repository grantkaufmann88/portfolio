# Vera Rubin project update - 2026-10-02

This edition promotes the Vera Rubin Observatory transducer positioning system to the first project and the micro swarming drone to the second. Both use the visible label **Currently Working On**. The HURC rover retains its existing **Ongoing** label.

## Rubin media added

- Complete two-axis actuator / transducer-array CAD views
- Custom strain-wave gearbox CAD views
- Hand-controller schematic
- Actuator/stepper-driver schematic
- Controller PCB layout and 3D render
- 17.47 s resin-printed gearbox prototype video, web-encoded for playback

## Content decisions

The Rubin page uses the October 1-2 raw narration as the primary description of the current design. It explicitly separates the 0.1 degree requirement and 0.036 degree theoretical full-step increment from measured accuracy. The planned long-baseline laser test is described as validation work still to be performed.

The schematics identify the processor as **ATtiny1604**, not ATtiny1608. The actuator schematic shows two **DRV8434A** stepper drivers. The hand-control schematic shows **CAP1298**, **CH340C**, **UCC27211**, and **IRLR7843** parts. The narration contains conflicting wording around the intended signaling rate (100 kHz vs. 100 bits/s), so the public copy describes the architecture without publishing an unverified baud-rate number.

Public observatory background was refreshed from the official Rubin Observatory and Harvard Physics pages. External links are included on the project page.

## Validation

`python build.py` and `python scripts/check_site.py` pass for this edition. The checker now expects seven referenced standalone project videos and supports per-project status labels.
