# Future features and deferred work (v5)

Part of [design.md](design.md). This file lists features that were dropped from the current scope or deferred, why, and which decision did it. Nothing here is built, tested or reserved in the packet or `Settings` layouts unless it says so. Items are removed from this file when they move into the roadmap.

## 1. Dropped from scope

### Mixer (OQ-20)
- **What:** up to 8 mix entries per model with the ops `Add`, `AddConst`, `MulConst`, `MulSrc` and `Set`, each with a source (an on-air channel before reverse, or any input id) and an optional switch condition with an invert flag; examples were a throttle hold on a toggle and a toggle that adds an offset; safe mode disabled it; a global `mixer_allowed` switch existed; a "Mixer" screen and a `mixer` key in the profile JSON.
- **Why dropped:** you moved mixing out of scope for this project and left it for a later iteration (OQ-20). The design keeps the pipeline stage hook between the channel map and reverse/endpoints (design-ui-profiles.md section 1), so a stage can be added without touching the core. No mixer fields are reserved in the layouts.
- **What a later version needs:**
  1. Re-introduce `MixerCfg` (`enabled`, `count`, entries) in `Settings` (appendix A5, about 66 B for 8 entries) and a `mixer` object in the profile JSON.
  2. Bump the JSON `schema` and the `Settings` layout version, and ship a migration that fills the new block with "disabled, empty" for every existing profile and for the key-value store. The radio protocol does not change if the mixer only works on channel values before packing, so the protocol version stays unless a new packet field is added.
  3. Add the pipeline stage between the channel map and reverse/endpoints, identity-bypassable, with load-time validation in the UI context and no heap or blocking calls in the tick.
  4. Add the Mixer screen and its SavePrompt flow, the safe-mode bypass, and the host tests (each op, bad data, disabled mixer leaves channels unchanged).
  5. Decide the throttle-safety rules again: with no designated throttle channel (see below) the earlier rule "reject `Add`, `MulSrc` and `MulConst` onto the throttle channel and check all switch combinations against `L + 200`" has nothing to attach to, so a later version needs a way to mark a channel as safety-critical.

## 2. Deferred safety features (OQ-25)
- **Startup mute:** the radio waking up muted until you unmute it. Dropped because you want it ready at power-up and on until muted. A later version could offer it as a setting.
- **Boot throttle-high lockout and designated throttle channel:** a `throttle_channel` in the model and a refusal to transmit while throttle was above `L + 200` after map, reverse and endpoints (`L = -ep_lo`). Dropped because there is no designated throttle channel; the receiver failsafe also never guesses one.
- **Confirm step before transmitting uncalibrated data:** today an invalid calibration shows "UNCALIBRATED", uses nominal values and keeps transmitting; a later version may require a confirmation first.
- **Throttle-low check for "Send failsafe" and receiver calibration:** replaced by a green link and on-screen confirmation.

## 3. Deferred or replaced options from other decisions
| Item | What | Why | Decision |
|---|---|---|---|
| Regional power cap and region setting | A `region` field with an EIRP cap, US level 0 only, "Allow mixer" on the region screen | Replaced by four radio profiles (Safe, Medium, Extreme, Custom) with a module type setting | OQ-08, OQ-34 |
| Hopping | Table hopping with sync-sweep behind `RadioLink` | The earlier failure's root cause is unknown, so it waits for a review and the host simulation (Phase 5c) | OQ-09 |
| Code refactoring and ponytail-style cleanup | A cleanup pass over the code once it exists | You do not want it now; the design document is the reference and refactoring is left for later | your last answer |
| Per-input reverse | A reverse flag per input applied before the curves, alone or together with per-channel reverse | Per-channel reverse only | OQ-30 |
| Endpoint overtravel to 120 % | Packet mapping `pkt = ((out + 1200) * 2047 + 1200) / 2400` and a receiver clamp (880 to 2120 us) | Endpoints limited to 100 % | OQ-31 |
| Hold-Back-to-save and the Back state machine | Tap Back cancels, a 700 ms hold saves, with progress bar and tones | Replaced by the Xbox-style button map (X saves) | OQ-16 (supersedes OQ-41) |
| Interrupt line from the input expander | An INT pin and an EXTI handler to read the expander only on change | Polling in the control tick is enough and every GPIO is used | OQ-02 |
| Second input expander | Another I2C expander (addresses 0x21 to 0x27) for more inputs | Not needed; one TCA9555 is enough | OQ-02 |
| SD card-detect signal | A detect pin on the SD socket | The module has no detect pin; presence is found by mount attempt and polling | OQ-02 |
| MCP23017 as the expander | The part you first chose | Only 14 usable inputs for 17 signals (GPA7 and GPB7 are output-only) | OQ-02 |
| SMA bulkhead antenna | An external whip on a bulkhead connector | You use the module's own antenna (the schematic still has J301 and J302) | OQ-24 |
| Trainer/PPM port | A PPM trainer connector | Out of scope | OQ-06 |
| Renode or QEMU firmware emulation | Running the real firmware on a desktop | The emulator is GUI and UX only | OQ-43 |
| Fourth gimbal axis | A fourth analog axis per gimbal | Three axes plus a button | OQ-28 |
| Wireless and Bluetooth gamepads | Adapters beyond wired USB | Out of scope | OQ-04 |
| Xbox One (GIP) driver | A driver behind a time-boxed spike | May fail without affecting anything else (Phase 5b) | OQ-04 |
| SD firmware update | A 16 KB bootloader that flashes from the SD card | Optional extra (Phase 5d) | OQ-03 |
