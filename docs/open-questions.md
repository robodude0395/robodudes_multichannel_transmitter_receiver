# Open Questions and Decisions Tracker (v5)

Companion to [design.md](design.md) (v5). Each item is a choice the notes left open. Nothing in the design is silently decided: a default that was needed is the **Recommendation** below.

**Status key.** `decided` (your decision is in `Decision`). `open` (needs your decision). `superseded` means a later decision replaced it. `open, provisional` (no longer used) meant you left it blank, the design uses the recommended default so work can continue, and **it stays open until you confirm it** (label: *provisional default, user to confirm*). Mark an item decided by writing the decision in its `Decision` line.

**Phase gates** (phases in [design-roadmap.md](design-roadmap.md)). Every question is now decided, so none blocks a phase; the lists record what each phase relies on. Phase 0 exit relies on OQ-02, 07 (cell), 21, 22, 24 and 38. Phase 1 entry relies on OQ-03, 05, 08, 14, 16, 19, 23, 25, 29, 30, 31, 32, 33, 34 and 35. OQ-30 and OQ-31 fix the layout and packet mapping; OQ-19 is built in Phase 1 as the key-value store. **Freeze rule:** the packet format and `Settings` layout freeze at Phase 1 exit with later-gated fields at their defaults; a later change bumps the schema and protocol version with a migration. Phase 2 relies on OQ-11, 15, 26, 27; Phase 3 on OQ-12, 13, 18; Phase 4 on OQ-17; Phase 5c on OQ-09 (deferred there). There is no Phase 5 mixer (OQ-20).

**Verification.** Facts checked against datasheets, vendor documents or source are tagged [checked] in the design files; unchecked ones stay [verify].

## Index

| ID | Topic | Blocks | Status |
|----|-------|--------|--------|
| OQ-01 | MCU choice | none | decided: STM32F411 Black Pill |
| OQ-02 | Digital input expansion (pin budget), SD card-detect | Phase 0 exit | decided |
| OQ-03 | Programming port and firmware update path | Phase 1 | decided |
| OQ-04 | Gamepad / Xbox scope for the weird port | 5a, 5b | decided |
| OQ-05 | Channel count | Phase 1 | decided |
| OQ-06 | Trainer / PPM port | none | decided: dropped |
| OQ-07 | Battery: cell count, then cell make and capacity | Phase 0 exit | decided |
| OQ-08 | nRF24 data rate, packet rate, retransmit | Phase 1 | decided |
| OQ-09 | Frequency hopping: past failures and scheme | Phase 5c | decided: deferred to 5c |
| OQ-10 | ELRS / Crossfire | none | decided |
| OQ-11 | Failsafe behaviour and values | Phase 2 | decided |
| OQ-12 | Pipeline stage order (trim) | Phase 3 | decided |
| OQ-13 | Expo / dual-rate / endpoint maths | Phase 3 | decided |
| OQ-14 | Palette (black on black) and Theme | Phase 1 / 4 | decided |
| OQ-15 | Top bar layout | Phase 2 | decided |
| OQ-16 | D-pad role mapping, safe-mode button, name entry | Phase 1 | decided |
| OQ-17 | Mascot and animation budget | Phase 4 | decided |
| OQ-18 | Profile slot model and default semantics | Phase 3 | decided |
| OQ-19 | Storage safety | Phase 1 | decided |
| OQ-20 | Mixer scope and semantics | none (out of scope) | decided: out of scope |
| OQ-21 | Scheduling model and SPI topology | Phase 0 exit | decided |
| OQ-22 | Language, build system, UI library, emulator stack | Phase 0 exit | decided |
| OQ-23 | Buzzer type | Phase 1 | decided |
| OQ-24 | Enclosure, antenna placement, power switch | Phase 0 exit | decided |
| OQ-25 | Safety behaviours | Phase 1 | decided |
| OQ-26 | Binding method and model-match | Phase 2 | decided |
| OQ-27 | What receiver voltage measures | Phase 2 | decided |
| OQ-28 | Gimbal hardware specification | none | decided |
| OQ-29 | ADC accuracy, reference, battery calibration | Phase 1 | decided |
| OQ-30 | Reverse semantics | Phase 1 | decided |
| OQ-31 | Endpoint range above 100 % | Phase 1 | decided |
| OQ-32 | Reset-reason policy and in-flight resume | Phase 1 | decided |
| OQ-33 | Input ids, default channel map, default yaw axis | Phase 1 | decided |
| OQ-34 | Radio profiles (replaces region and power cap), measured power table | Phase 1 | decided |
| OQ-35 | Model switching and flash-write policy | Phase 1 | decided |
| OQ-36 | One-time factory calibration (transmitter battery) | Phase 1, 2 | decided |
| OQ-37 | Receiver voltage calibrate command | Phase 2 | decided |
| OQ-38 | Power architecture (pre-regulator, quiet radio LDO) | Phase 0 exit | decided |
| OQ-39 | nRF24 IRQ pin use on both ends | Phase 1 | decided |
| OQ-40 | Receiver hardware | Phase 2 | decided |
| OQ-41 | Back button: tap cancels, hold saves | none | superseded by OQ-16 |
| OQ-42 | Display rotation and blind recovery | Phase 1 | decided |
| OQ-43 | Run the real firmware in Renode or QEMU | none | decided: dropped |

---

## OQ-01 MCU choice
- **Status:** decided
- **Decision:** STM32F411 Black Pill (HANDOVER: you own one). Consequences: 100 MHz, 512 KB flash, 128 KB RAM, no CCM, no hardware RNG, about 32 exposed GPIO with none spare. The nRF24 uses SPI1 on PB3 to PB5 so PA0 to PA7 stay ADC pins. The F405, Nucleo-F411RE, G4, H7, ESP32-S3 and RP2040 options are closed. Detail: design-hardware.md section 2 [verify the pin map against the board schematic].

## OQ-02 Digital input expansion
- **Question:** How are the 14 digital inputs read on a pin-starved Black Pill?
- **Options:** (a) direct GPIO (not possible: no spare pins). (b) Button matrix. (c) 74HC165 shift registers (the earlier recommendation, replaced). (d) MCP23S17 SPI expander. (e) One I2C expander: MCP23017 (your first choice) or TCA9555/PCA9555.
- **Findings (round 3):** the MCP23017 has only 14 usable inputs (GPA7 and GPB7 are output-only [checked: Microchip DS20001952]) for 17 signals, and the three GPIO freed by dropping the shift registers (PC14, PC15, PB1) have no I2C function while every I2C-capable pin was taken. Alternatives A to F were reported; you chose B (re-pin I2C1 to PB6/PB7) with A (a 16-input TCA9555).
- **Status:** decided
- **Decision:** One TCA9555PWR (TSSOP-24) at I2C address 0x20 (A0 to A2 low) on I2C1 (PB6 SCL, PB7 SDA, 4.7 kohm pull-ups, 400 kHz), polled in the control tick without blocking and with a bus timeout, no interrupt line. The 14 controls plus charger STAT and USB power-good use its 16 inputs; host over-current goes to PC15. The nRF24 CE moved to PC14 and IRQ to PB1 to free PB6/PB7. SD card-detect is removed. No second expander. You chose alternatives B and A of the round 3 report. Detail: design-hardware.md sections 2 and 7.

## OQ-03 Programming port and firmware update path
- **Question:** UART or USB for the external program port?
- **Options:** (a) UART on the STM32 ROM bootloader (USART1 PA9/PA10 [verify AN2606]) with BOOT0 and NRST on a connector. (b) USB DFU on the OTG port, which is the same PA11/PA12 pair as the weird port and as the Black Pill USB-C. (c) SWD only. (d) Later: SD-card update with a 16 KB bootloader.
- **Recommendation (earlier):** (a) with SWD pads inside the case; the OTG port belongs to the weird port. The Black Pill USB-C connector is bench power or DFU only and is never connected together with the weird port [verify the board's USB-C VBUS wiring]. Add (d) in Phase 5d as an option.
- **Status:** decided
- **Decision:** Two ways in: the UART port J201 stays, and a 5-pin SWD header J202 is added: GND, SWCLK, SWDIO, 3V3 sense (1 kohm series resistor, sense only, never powers or back-feeds the board) and NRST. The receiver programming adapter must not feed 5 V into a pack-powered receiver. SD-card update stays an optional Phase 5d item. Detail: design-hardware.md section 3.

## OQ-04 Gamepad / Xbox scope
- **Status:** decided
- **Decision:** Your answer 6: per-device drivers that identify the controller and translate it to normalised axes and buttons. Generic HID first (5a), DualShock and DualSense as HID (5a), Xbox 360 wired (5b), Xbox One/GIP later behind a spike. Wireless adapters and Bluetooth out of scope. Unplugged inputs read as neutral and are invalid as mixer sources. Detail: design-ui-profiles.md section 3.6. TinyUSB dwc2 host on the F411 is the first Phase 5a task [verify].

## OQ-05 Channel count
- **Question:** How many channels, given the Nano drives 8 servo outputs?
- **Options:** (A) 10 in the packet, CH9 and CH10 ignored. (B) 10 in the packet, CH9 and CH10 as on/off digital outputs on A4 and A5. (C) 8 in the packet.
- **Recommendation:** (B).
- **Status:** decided
- **Decision:** 10 channels in the packet, 8 servo outputs, CH9 and CH10 as on/off digital outputs on A4 and A5. The receiver firmware is generic with a board-capability layer so another board with more outputs needs no change to shared code.

## OQ-06 Trainer / PPM port
- **Status:** decided
- **Decision:** HANDOVER: the trainer/PPM port is dropped (out of scope). It replaces the earlier "PPM out first" answer. Telemetry already travels over the radio. All PPM, mini-DIN, TIM2 and `TrainerCfg` content is removed from v5; the FlySky PPM facts stay unchecked [verify] if the port is ever revived.

## OQ-07 Battery: cell count, then cell make and capacity
- **Cell count:** decided, 1S Li-ion/LiPo. The 2S power tree is removed.
- **Capacity:** decided, a protected cell bank of about 2000 mAh. Runtime about 21 h typical [estimate: 2000 mAh x 0.9 / 80 mA at the cell is 22.5 h, rounded down]. A USB gamepad can draw about 0.7 to 0.8 A from the cell [verify], so the protection must allow at least 1.5 A. Charging: 1S power-path charger on its own charge port.
- **Cell and protection board:** you supply your own; the design assumes a generic protected 1S cell (nothing to decide).
- **Status:** decided
- **Decision:** 1S bank of about 2000 mAh (about 21 h); a generic protected cell and protection board, which you supply.

## OQ-08 nRF24 data rate, packet rate, retransmit, chip requirement
- **Recommendation:** 250 kbps (about -94 dBm against about -85 dBm at 1 Mbps [verify]), 100 Hz or 50 Hz as a bind-time property, auto-ack, ARD 750 us (required for ACK payloads under 8 bytes [checked]), ARC 0, ACK payload with dynamic length, 16-bit CRC. Needs the nRF24L01+; a boot readback detects the original chip, not every clone. Detail: design-radio-link.md section 2.
- **Status:** decided
- **Decision:** Four radio profiles: Safe (baseline, 250 kbps, ARC 0, PA level 0 or 1), Medium, Extreme (PA level 3, opt-in with an on-screen warning) and Custom. Detail: OQ-34 and design-radio-link.md sections 2 and 3.

## OQ-09 Frequency hopping
- **Question:** What went wrong in earlier hopping attempts, and which scheme is used?
- **Root-cause questions for you (still unanswered):** (1) Did link loss occur at start or after seconds of operation? (2) How did the receiver find the channel after a missed packet? (3) Was ACK payload used while hopping (a stale preloaded ACK payload is a common failure)? (4) Hop every packet or every N packets? (5) Was PLL settling (about 130 us) respected? (6) Was the same channel table used on both sides after power cycles? (7) Was there any clock resync?
- **Recommendation:** fixed channel in Phases 1 to 4; table hopping in Phase 5c behind `RadioLink` with `hop_idx` in the packet as the source of truth, sync-sweep recovery, and a mandatory host simulation before hardware (design-radio-link.md section 6). `hop_enabled` is reserved in the frozen layout.
- **Status:** decided: deferred
- **Decision:** The root cause is unknown (the earlier code was AI-generated and not reviewed). Fixed channel until Phase 5c; hopping is designed behind `RadioLink` and starts only after a root-cause review.

## OQ-10 ELRS / Crossfire
- **Status:** decided
- **Decision:** Ruled out; stay with nRF24L01+ PA/LNA. `RadioLink` stays as plain good design.

## OQ-11 Failsafe behaviour and values
- **Recommendation:** 500 ms timeout; per channel preset, hold or no pulse; factory failsafe is no pulse on all channels until a type 2 packet is stored; no output until the first valid packet; "Send failsafe" with confirmation, 3 attempts.
- **Status:** decided
- **Decision:** The receiver failsafe stays as designed, and the failsafe-programming message ("Send failsafe") stays in the design as long as it never interferes with the transmitter's core function. With no throttle channel, "Send failsafe" needs a green link and on-screen confirmation instead of a low-throttle check.

## OQ-12 Pipeline stage order
- **Recommendation:** trim after the curve (centre shifts by the same amount whatever the expo); order: calibration, curves, trim, map, reverse and endpoints. This deviates slightly from the order in your notes.
- **Status:** decided
- **Decision:** Trim is applied after the curve and only shifts the centre, as per-side scaling so endpoints stay reachable; operations must not affect each other indirectly. Math in design-ui-profiles.md section 3.2.

## OQ-13 Expo / dual-rate / endpoint maths
- **Recommendation:** integer permille; rate 0 to 1000; expo -500 to +1000 via `y = ((1000 - e) * x_r + e * x3) / 1000`; trim -250 to +250; endpoints 0 to 1000 per side; truncation toward zero; no float or lookup table. Two rate sets chosen by a switch. Curves per axis and pot input, endpoints per channel. Deadband 20 permille on centring axes. Design-ui-profiles.md section 3.2.
- **Status:** decided
- **Decision:** Endpoint math accepted. The rates/expo and endpoints editors draw the input curve with a crosshair at the channel's live input, like the FlySky GUI.

## OQ-14 Palette (black on black) and Theme
- **Question:** "Black background, white borders, black text within elements" makes text invisible on a black fill.
- **Options:** (a) idle black fill, white border, white text; focused white fill with black text. (b) White-filled elements with black text. (c) Grey fills.
- **Recommendation:** (a), Theme in RGB565: `0x0000` background, `0xFFFF` border, text and focus, accent `0x07FF`, green `0x07E0`, red `0xF800`, amber `0xFD20`, disabled `0x7BEF`; contrast 4.5:1 or better; status never colour only. Confirm on the real panel [verify].
- **Status:** decided
- **Decision:** Option (a): idle black fill, white border and text, focused white fill with black text.

## OQ-15 Top bar layout
- **Recommendation:** left cluster (battery icon, percent, TX dot, RX dot), model name of 8 characters in the centre, receiver volts and SD icon on the right; 6x8 font.
- **Status:** decided
- **Decision:** Top bar as recommended; the right cluster shows an SD icon for mounted or not mounted.

## OQ-16 D-pad role mapping
- **Earlier recommendation (replaced by the Decision):** left d-pad Up/Down moves the cursor, Left/Right switches tabs; right d-pad Up/Down changes values, Left is Back (tap cancels, hold saves), Right is OK; long-press OK on Home opens the menu; safe mode is left d-pad Down held at power-on; name entry uses left d-pad for the cursor and right d-pad Up/Down for the character. Timings: 20 ms debounce, 600 ms long press, repeat after 400 ms then every 100 ms. The screen map itself is approved.
- **Status:** decided
- **Decision:** Left d-pad: cursor (Left/Right also switch tabs when no field is being edited). Right d-pad in Xbox layout: A bottom accept, B right back or cancel, X left save on editing screens, Y top options (on Home it opens the main menu). Editing a field: A enters edit mode, left pad Up/Down +-1 and Left/Right +-10, A confirms, B reverts. No long presses. Boot combinations stay. This supersedes OQ-41. Detail: design-ui-profiles.md section 4.4.

## OQ-17 Mascot and animation budget
- **Recommendation:** an original catgirl-style character (not a copy of the Flipper Zero dolphin); code-drawn placeholders first; later sprites up to 64x64 at 8 to 12 fps from SD, drawn only in the UI context; a PC tool converts GIF/PNG to RGB565 strips.
- **Status:** decided
- **Decision:** Assets load from the SD card as 16-bit BMP files, with a built-in code-drawn fallback; the mascot is an original character with placeholders first.

## OQ-18 Profile slot model and default semantics
- **Recommendation:** built-in read-only DEFAULT in flash plus user slots M01 to M50 on SD; "Reset to defaults" copies DEFAULT; edits to DEFAULT always "Save as".
- **Status:** decided
- **Decision:** As recommended: read-only DEFAULT plus user slots M01 to M50 on SD.

## OQ-19 Storage safety
- **Recommendation:** DEFAULT fallback; atomic SD writes with stale-file cleanup; schema versioning; calibration and radio-global settings in an internal-flash key-value store (two alternating 128 KB sectors, 6 and 7 on the F411 [verify]); the factory record in the same store (OQ-36); minimal store built in Phase 1. Layout: appendix-byte-level.md A6.
- **Status:** decided
- **Decision:** As recommended. Only calibration and radio-global settings use internal flash; profiles and trims go to SD.

## OQ-20 Mixer scope and semantics
- **Earlier recommendation (replaced by the Decision):** up to 8 entries; ops `Add`, `AddConst`, `MulConst`, `MulSrc`, `Set`; `src_kind` channel or input; optional switch condition; one isolated stage, default empty and disabled; `effective_mixer = mixer_allowed AND model.mixer.enabled`; throttle-safety validation by enumeration; safe mode disables it. Design-ui-profiles.md section 3.3.
- **Status:** decided: out of scope
- **Decision:** Mixing is out of scope. Phase 5 is removed, the later phases are renumbered 5a to 5d, the pipeline stage hook stays, and no mixer fields are reserved. The mixer design and what a later version needs are in design-future-features.md.

## OQ-21 Scheduling model and SPI topology
- **Recommendation:** bare-metal; TIM5 pends PendSV for the 100 Hz tick; non-blocking nRF24 state machine; nRF24 alone on SPI1, LCD and SD on SPI2; SD, FatFs and USB never in PendSV. Revisit an RTOS only if USB host plus FatFs make the main loop hard to reason about.
- **Status:** decided
- **Decision:** Bare-metal, interrupt-driven; nRF24 alone on SPI1, LCD and SD on SPI2. The digital inputs are on I2C1 (OQ-02), not on SPI2, and are polled in the control tick without blocking.

## OQ-22 Language, build system, UI library, emulator stack
- **Recommendation:** C++17 (no exceptions, RTTI or heap in the control path), CMake with arm-none-eabi-gcc, STM32 HAL/LL, FatFs, a small JSON library [verify licence and version], a small custom widget layer (not LVGL), GoogleTest, SDL2 for the GUI-only emulator, `-ffp-contract=off` on host builds.
- **Status:** decided
- **Decision:** As recommended.

## OQ-23 Buzzer type
- **Recommendation:** passive piezo or magnetic buzzer on TIM1 PWM (PA8) so tunes are possible; transistor drive if current exceeds the pin rating; beeps in Phase 1, tunes in Phase 4.
- **Status:** decided
- **Decision:** Passive piezo buzzer on TIM1 PWM.

## OQ-24 Enclosure, antenna placement, power switch
- **Earlier recommendation (replaced by the Decision):** antenna on top on an SMA bulkhead with a 2.4 GHz whip, away from battery and metal; hard power switch between cell and regulators; charge, program and weird ports reachable from outside; mechanical sketch in Phase 0.
- **Status:** decided
- **Decision:** You handle the enclosure and mechanical design; the module's own antenna is used; the hard power switch between cell and regulators stays.

## OQ-25 Safety behaviours
- **Earlier recommendation (replaced by the Decision):** muted start; throttle-high judged on the final value above `L + 200` with `L = -ep_lo`; calibration validity rules; TX and RX dot semantics with `seq_echo` validation. Design-radio-link.md section 6.
- **Status:** decided
- **Decision:** Calibration is done first, with the radio muted (the wizard mutes it): release the stick for the centre, then sweep both extremes; the centre step applies only to spring-centre axes, and pots and toggles need no centre. There is no designated throttle channel and no boot throttle lockout. The radio does not start muted: it wakes up ready and stays on until you mute it. Other proposed safety features are deferred (design-future-features.md). TX and RX dot semantics stay.

## OQ-26 Binding method and model-match
- **Recommendation:** bind on channel 76 with address `BIND1` at PA level 0, 30 s timeout, scan for the quietest channel, bind ID chosen from UID, ADC noise and cycle counter (no RNG on the F411); the operating address derived by the shared FNV-1a function with rejection rules and known-answer vectors (appendix A3); the bind trio stored together globally and per model; Phase 1 uses DEV constants.
- **Status:** decided
- **Decision:** The binding method is accepted and is built after the transmitter works with a receiver. Phase 1 keeps fixed development constants.

## OQ-27 What receiver voltage measures
- **Earlier recommendation (replaced by the Decision):** the receiver's own supply rail, 22k/4.7k on A0 against the internal 1.1 V reference [checked]; reported only if the divider is fitted; value in millivolts so a pack divider (68k/8.2k for 2S) also works.
- **Status:** decided
- **Decision:** The receiver monitors the battery pack that feeds it, 2S to 4S (16.8 V maximum), through a 5 V buck BEC to the Nano. The divider (100k/6.2k) is taken from the pack before the BEC and sized so 16.8 V stays under the 1.0 V minimum reference. Cell count is auto-detected at power-up (override available). The low-voltage warning is 3.3 V per cell. Detail: design-hardware.md section 6, appendix A4 and A10.

## OQ-28 Gimbal hardware specification
- **Status:** decided
- **Decision:** Each gimbal has 3 analog potentiometers (x, y, twist-yaw) plus one digital button at the top of the stick. Analog budget is 9 inputs (6 axes, 2 pots, 1 battery sense). No fourth-axis contingency. Pot values and part numbers still need confirming before PCB work, but nothing else depends on them.

## OQ-29 ADC accuracy, reference and battery calibration
- **Recommendation:** pots fed from the same filtered 3.3 V as VDDA (ratiometric), 12-bit DMA scan, 16x oversampling, 100 ohm plus 100 nF per input, VREFINT correction, battery divider 100k/100k after the hard switch, reading ignored while USB power is present. The Black Pill's VDDA feed is unchecked; Phase 0 measures ADC noise [verify]. The per-unit scale is the factory step of OQ-36.
- **Status:** decided
- **Decision:** As recommended.

## OQ-30 Reverse semantics
- **Question:** Does reverse flip the input before curves (per input) or the servo output (per channel)?
- **Options:** (a) per channel. (b) per input. (c) both.
- **Recommendation:** (a): matches servo reverse on FlySky-style radios. Choose (c) if you also want the stick sense reversed for curves and trim.
- **Status:** decided
- **Decision:** Option (a): reverse is per channel.

## OQ-31 Endpoint (EPA) range above 100 %
- **Options:** (a) limit to 0..100 %. (b) allow ±120 % with a packet remap and a receiver clamp.
- **Recommendation:** (a). Overtravel changes the packet format, so decide before Phase 1 exit if you want (b).
- **Status:** decided
- **Decision:** Option (a): endpoints limited to 0 to 100 %.

## OQ-32 Reset-reason policy and in-flight resume
- **Options:** (a) every boot is a fresh muted start. (b) resume at once after IWDG, brown-out and UI-hang resets from a CRC-guarded no-init RAM mirror.
- **Recommendation:** (b) with guards: fixed flag evaluation order, host-testable `decide()`, two-slot mirror, no resume after three resets in 10 s, a "RESET: resumed" warning. Outage about 235 ms against the 500 ms failsafe; bench pass level gap at most 300 ms. Appendix A7 [verify the F4 reset flags].
- **Status:** decided
- **Decision:** Option (b): after an IWDG, brown-out or UI-hang reset the transmitter resumes transmitting at once (gap about 235 ms), at most 3 resets in 10 s. Power-on and user reboots start normally and also transmit as soon as init is done.

## OQ-33 Input ids, default channel map, default yaw axis
- **Recommendation:** ids 0 to 5 axes, 6 and 7 pots, 8 and 9 toggles, 10 to 13 momentary, 16 to 23 d-pads (UI only), 32 to 63 USB. Default map: CH1 `stick_r_x`, CH2 `stick_r_y`, CH3 `stick_l_y` (throttle), CH4 `stick_l_twist` (yaw), CH5 `stick_l_x`, CH6 `stick_r_twist`, CH7 `pot_1`, CH8 `pot_2`, CH9 `toggle_1`, CH10 `toggle_2`. Alternative: mode-2 AETR with yaw on `stick_l_x`.
- **Status:** decided
- **Decision:** As recommended: yaw on `stick_l_twist` with the default map in design-ui-profiles.md section 2.

## OQ-34 Radio profiles and measured power table (was: region and power cap)
- **Options:** (a) fixed PA level, no knowledge of the module's output. (b) measured table, cap on conducted power plus antenna gain, region setting.
- **Earlier recommendation (replaced by the Decision):** (b). Region EU by default, cap 20 dBm EIRP [verify EN 300 328]; duty is 8.4 % at 100 Hz against a roughly 10 % limit [verify]. US row is level 0 only until hopping or a compliance check [verify FCC 15.247 and 15.249]. Only levels 0 and 1 until measured. Not legal advice.
- **Status:** decided
- **Decision:** Four radio profiles replace the regional cap and region setting: Safe (standard non-PA/LNA modules: 250 kbps, ARC 0, PA levels 0 and 1 only); Medium (pushes the module toward the EU 20 dBm EIRP limit; you select the module type, standard or PA/LNA, and each type has a stored Medium PA level from datasheets, confirmed by measurement); Extreme (PA level 3 at 250 kbps, needs an explicit opt-in with an on-screen warning that it can exceed legal limits); Custom (PA level, data rate, retry count and delay, channel, address width, CRC length, hop table). Not legal advice. Detail: design-radio-link.md section 3.

## OQ-35 Model switching and flash-write policy
- **Recommendation:** flash is written only while the radio is muted; a model switch mutes it; the IWDG reload is extended to about 4 s around a sector erase (up to about 2 s [verify]); UI settings stay in RAM while transmitting and commit at the next mute point.
- **Status:** decided
- **Decision:** Internal flash is written only while the radio is muted or has not started transmitting; a write needed in flight is deferred until you mute. Only calibration and radio-global settings use internal flash; profiles and trims go to SD.

## OQ-36 One-time factory calibration (transmitter battery)
- **Status:** decided
- **Decision:** Your answer 1: calibrate once, as a factory step, so the end user never has to. A protected `FactoryRecord` in the flash key-value store (two copies, unlock token, copied forward on compaction); a hidden menu can redo it. Stick calibration stays user-redoable. Without a record the scale is 1.0 and the icon shows "?".

## OQ-37 Receiver voltage calibrate command and safety rules
- **Status:** decided
- **Decision:** Your answer 1 (receiver part): the receiver sends voltage only if it actually reads a battery, and calibrates once, deliberately. Capability flags in the bind ACK and every telemetry payload; a two-step arm and apply command with a nonce, bound-only, healthy link, one apply per 5 s. Design-radio-link.md section 7.

## OQ-38 Power architecture
- **Question:** Which topology feeds the MCU and the nRF24 PA module, and are the LM2596 or AMS1117 suitable?
- **Options:** (a) one 3.3 V converter plus a ferrite and capacitor branch to the radio. (b) 1S buck-boost to 3.6 V, then separate digital and quiet radio LDOs. (c) LM2596 or AMS1117.
- **Recommendation:** (b). The LM2596 is buck-only with 4.5 V minimum input and 5 to 10 mA quiescent; the AMS1117 has 1.1 to 1.3 V dropout and cannot make 3.3 V from a 1S cell [checked]. Feed the Black Pill's 3V3 pin from our digital LDO rather than its onboard regulator [verify the board]. Ripple at the module under 50 mV peak-to-peak is a Phase 0 measurement. The 2S tree is removed.
- **Status:** decided
- **Decision:** Option (b): the radio has its own LDO with ferrite and bulk capacitance and the MCU never shares its rail; under 50 mV peak-to-peak stays a Phase 0 gate. The Black Pill 3V3 is fed from the digital LDO, not from the radio LDO. Black Pill USB-C stays unused while the battery path is on (finding in design-hardware.md section 3).

## OQ-39 nRF24 IRQ pin use on both ends
- **Status:** decided
- **Decision:** Use IRQ on both ends (transmitter PB7, receiver D2), with polling as the fallback.

## OQ-40 Receiver hardware
- **Status:** decided
- **Decision:** Your answer 2: an Arduino Nano or Mini class board with 5 V logic, so no logic converter. Nano class chosen; the nRF24 gets its own 3.3 V LDO (the Nano 3V3 pin is too weak); bench-check the nRF24 output high level at the Nano pins.

## OQ-41 Back button: tap cancels, hold saves
- **Status:** superseded by OQ-16 (button map)
- **Decision:** Your answer 8: a long Back press of about 700 ms (600 to 800 ms range, with progress bar and tone) saves and leaves editing screens; a short press cancels or leaves without saving. Superseded in round 3: the Xbox-style button map of OQ-16 replaces hold-Back-to-save; there are no long presses.

## OQ-42 Display rotation and blind recovery
- **Status:** decided
- **Decision:** Your answer 9: landscape display with a radio-global `display_rotation` (0 or 180) applied at init, changeable live on SetDisplay, with a boot combo (left and right d-pad Up) to fix an upside-down screen blind.

## OQ-43 Run the real firmware in Renode or QEMU
- **Status:** decided
- **Decision:** Dropped (HANDOVER). The emulator is GUI and UX only, built from the shared UI and profile code, and does not run the control loop, radio, USB or ADC.

---

## Appendix: v5 change list

Applied from HANDOVER and `input`: 1S battery (OQ-07), STM32F411 Black Pill (OQ-01), trainer/PPM dropped (OQ-06), GUI-only emulator and Renode/QEMU dropped (OQ-43), 3-axis gimbals with a top button (OQ-28), plus the earlier answers kept as decided (OQ-04, 10, 36 to 42).

Round 3 (your answers to the open questions, in `open-questions-answers.md`): every question is decided. Design effects: one TCA9555 I2C expander replaces the three 74HC165 (nRF24 CE and IRQ re-pinned to PC14 and PB1, HOST_OC on PC15, SD card-detect removed); 5-pin SWD header with a sense-only 3V3 pin; four radio profiles replace the regional cap (`GlobalCfg` and `RadioCfg` change, bind packet byte 10 carries the link settings); trim as per-side scaling; receiver pack monitor (2S to 4S, BEC, cell auto-detect); Xbox-style button map; no startup mute and no throttle lockout; flash writes wait for a mute; mixer and Phase 5 removed, later phases renumbered 5a to 5d (`Settings` is 976 B); dropped and deferred features are in design-future-features.md.

Earlier effects still in force: pin map for the 48-pin Black Pill (nRF24 on SPI1 PB3 to PB5, no spare GPIO); flash key-value store in F411 sectors 6 and 7; 2S power tree removed; trainer, PPM timer, `TrainerCfg` and SetTrainer removed; three Black Pill risks (no spare GPIO, USB-C sharing PA11/PA12 with the weird port, ADC feed noise). Older review logs are not carried forward; v4 files are in `docs/backup-v4/`.
