# Handover: nRF24 multichannel transmitter design

Read this first in a new session. Written 2026-11-13, updated after the round 3 answers (all open questions decided; see Status).

## Project
Custom RC transmitter. nRF24L01+ PA/LNA radio, STM32F411 Black Pill, 1.8" ST7735 (160x128, landscape), SD card profiles (JSON), buzzer, two 3-axis gimbals, 2 pots, 2 toggles, 2 triggers, two d-pads (8 buttons), USB "weird port" for gamepads. Receiver: Arduino Nano class (ATmega328P, 5 V), servo PWM out, optional voltage telemetry.

## Files
- `design-brief.md` (this folder): the user's original notes. Never modify.
- `docs/design.md` and the topic files it indexes: the v5 design, updated with the round 3 answers. `docs/design-future-features.md` lists dropped and deferred features.
- `docs/open-questions.md`: tracked decisions OQ-01..OQ-43, each with its `Decision:` line. `docs/open-questions-answers.md`: your answers, verbatim.
- `hardware/transmitter/` and `hardware/receiver/`: the KiCad schematics, BOMs and rendered images (updated for the TCA9555 expander, the 5-pin SWD header and the re-pinned nRF24 CE/IRQ).
- `docs/.review/`: latest independent review output.

## Decisions made by the user
- Radio: stay with nRF24L01+ PA. ELRS and Crossfire are ruled out (different chips).
- Battery: 1S Li-ion/LiPo (recommended by me, user agreed). Round 3: a protected cell bank of about 2000 mAh (about 21 h); make and protection board are yours (generic). The protection must allow about 1.5 A, because a USB gamepad can draw about 0.7 to 0.8 A from the cell.
- MCU: STM32F411 Black Pill (the user owns one).
- Receiver: Nano/Pro Mini class. The nRF24 inputs tolerate 5 V, so no level shifter. The radio still needs its own 3.3 V supply, since the Nano 3V3 pin is too weak.
- Trainer/PPM port: dropped (out of scope).
- Emulator: GUI and UX only, built from the shared UI and profile code. It does not run the control loop, radio, USB or ADC. Renode/QEMU is dropped.
- Calibration: one-time factory calibration of battery voltage on both ends. The receiver reports voltage only if a divider is fitted. Stick calibration stays user-redoable.
- Weird port: per-device drivers (HID gamepad first, Xbox 360, Xbox One later). Unplugged inputs read as neutral.
- UI: the screen map is approved. Button map (OQ-16): left d-pad moves the cursor (Left/Right also switch tabs), right d-pad in Xbox layout (A accept, B back, X save, Y options; on Home Y opens the main menu); there are no long presses. `display_rotation` flag (0 or 180) with a boot button combo to fix a flipped screen.
- IRQ pin: used on both ends, with polling as a fallback.
- Gimbals (OQ-28 decided): 3 analog pots each (x, y, twist-yaw) plus one digital button at the top of the stick. Analog budget is 9 inputs (6 axes, 2 pots, 1 battery sense). No fourth-axis contingency is needed.
- Testing: mostly manual.
- Code practices: DRY, KISS, SOLID, decoupled features, core first.

## Round 3 decisions (all open questions are now decided)
- Input expansion (OQ-02, 21): one **TCA9555** I2C expander (address 0x20, I2C1 on PB6/PB7, polled in the control tick, no interrupt line) replaces the three 74HC165. The MCP23017 you asked for has output-only GPA7/GPB7, so it has 14 usable inputs for 17 signals; you chose the pin-compatible TCA9555 and the re-pin (nRF24 CE on PC14, IRQ on PB1, HOST_OC on PC15). SD card-detect is removed.
- SWD header (OQ-03): 5 pins GND, SWCLK, SWDIO, 3V3 sense (1 kohm, sense only), NRST. The UART program port stays.
- Radio (OQ-08, 34): four profiles Safe, Medium, Extreme (warning and opt-in), Custom; module type standard or PA/LNA selects the stored Medium PA level (to be confirmed by measurement). The regional cap is gone. Not legal advice.
- Power (OQ-07, 38): 1S cell bank of about 2000 mAh (about 21 h), generic protected cell and protection board that you supply; the radio has its own LDO and the Black Pill USB-C stays unused while the battery path is on.
- Receiver (OQ-27): monitors a 2S to 4S pack through a 5 V BEC, divider 100k/6.2k before the BEC, cell auto-detect, 3.3 V per cell warning.
- Startup (OQ-25, 32): the radio does not start muted, no throttle lockout; reset policy (b) resume at once, at most 3 resets in 10 s. Flash writes wait for a mute (OQ-35).
- Mixer (OQ-20) is out of scope; Phase 5 is removed and the later phases are 5a to 5d. See `docs/design-future-features.md`.

## Still open
- No design decisions are open. Open items are facts to verify and hardware to choose: the Black Pill regulator and 32.768 kHz crystal on PC14/PC15 (probably harmless, see design-hardware.md section 2), module datasheet PA figures, and whether to keep the SMA bulkhead J301 and U.FL jumper J302 in the schematic (you chose the stock module antenna). Hopping (OQ-09) is deferred to Phase 5c; its root cause is unknown.

## Status
- The v5 docs and the KiCad schematics are updated for round 3. Earlier states are in git history.
- The receiver schematic and BOM are in `hardware/receiver/` (Nano, nRF24 module with its own LDO, 5 V BEC, pack divider, 8 servo headers, CH9/CH10 header, bind button). Design: `docs/design-hardware.md` section 6 and appendix A4 and A10.

## Notes for the next session
- Keep briefs short: point agents at files, not long pasted text.
- Review gate: block only on HIGH findings, list MEDIUMs for later.
- Figures tagged [verify] are unchecked, including STM32F4 flash and reset specifics, the Black Pill USB-C VBUS wiring, module power figures and the ST-Link behaviour with an unpowered target.
- Code refactoring is deferred by choice (see the future-features file).

## Phases (summary)
0 decisions and bring-up. 1 core link (inputs to radio to channels, text screen, buzzer), with the GUI emulator work in parallel. 2 receiver, telemetry, battery. 3 mapping, reverse, trim, rates, SD profiles. 4 UI polish and animations. 5 optional work: 5a USB HID host, 5b Xbox drivers, 5c hopping, 5d SD firmware update.
