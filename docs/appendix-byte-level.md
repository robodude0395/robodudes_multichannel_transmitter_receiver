# Appendix: byte-level detail (v5)

Companion to [design.md](design.md). The design files say what happens; this file holds the exact bytes, layouts and test vectors. Figures tagged **[verify]** are unchecked.

## A1. Radio packets (see [design-radio-link.md](design-radio-link.md) section 2)

Transmitter to receiver, 17 bytes, little-endian.

| Byte | Field | Content |
|---|---|---|
| 0 | `type_flags` | bits 0-1 type (0 control, 1 bind, 2 failsafe set, 3 receiver command); bit 2 TX low battery; bits 3-6 `hop_idx` (0 while hopping is off); bit 7 `sweep` |
| 1 | `seq` | increments per packet, wraps at 255; loss counting and `seq_echo` validation only |
| 2-15 | payload | type 0: 10 channels x 11 bits (110 bits in 14 bytes, CH1 in the lowest bits) |
| 16 | `check` | `crc8(bytes 0..15) XOR (bind_id & 0xFF)`; CRC-8/SMBUS (poly 0x07, init 0, no reflection); key 0 for bind packets |

Channel to packet: `pkt = ((s + 1000) * 2047 + 1000) / 2000` (s = -1000 gives 0, 0 gives 1024, +1000 gives 2047). Receiver pulse: `1000 + round(pkt * 1000 / 2047)` us.

| Type | Bytes | Content |
|---|---|---|
| 1 bind | 2-5 / 6 / 7 / 8 / 9 / 10 / 11-15 | `bind_id` / `rf_channel` (0..80) / `channel_count` (10) / `rate_code` (0 = 100 Hz, 1 = 50 Hz) / `proto_version` (1) / `link_cfg` / zero |
| 2 failsafe | 2-4 / 5-14 / 15 | 2 bits per channel mode (0 preset, 1 hold, 2 no pulse) / 8-bit preset per channel / zero |
| 3 command | 2 / 3 / 4-5 / 6-7 / 8-11 / 12-15 | `cmd` (1 calibrate, 2 mark not fitted) / `step` (0 arm, 1 apply) / `nonce` / `ref_mv` / `bind_id` / zero |

`link_cfg` (byte 10) carries what the receiver must match from the radio profile: bits 0-1 data rate (0 = 250 kbps, 1 = 1 Mbps, 2 = 2 Mbps), bit 2 CRC length (0 = 2 bytes, 1 = 1 byte), bits 3-4 address width (0 = 5 bytes, 1 = 4, 2 = 3), bits 5-7 zero. Zero means the defaults of A2, so a packet from a transmitter that left the byte zero decodes unchanged and `proto_version` stays 1. The bind packet itself always goes out on the rendezvous settings (250 kbps, 5-byte address, 2-byte CRC). PA level, ARC and ARD are transmitter-only and are not sent.

Failsafe packing: `v = (value + 1000) * 255 / 2000`; unpack `pkt = v * 2047 / 255`. Value 0 gives v = 127 and pkt = 1019 (5 counts under centre, accepted).

ACK payload, receiver to transmitter, 6 bytes: byte 0 `ack_type` (0 telemetry, 1 bind ack, 2 failsafe stored, 3 command result), byte 1 `seq_echo`.

| `ack_type` | Bytes 2-5 |
|---|---|
| 0 | 2-3 `rx_mv` (pack voltage in mV, 0xFFFF = no sensor), 4 `lqi` (% of last 100), 5 `rx_flags` (bit 0 failsafe, bit 1 low voltage (below 3.3 V per cell), bit 2 sense fitted, bit 3 sense calibrated, bits 4-5 detected cells minus 1 (1 = 2S, 2 = 3S, 3 = 4S, 0 = unknown)) |
| 1 | 2-4 `receiver_id` (24-bit), 5 `rx_caps` (bit 0 sense fitted, bit 1 sense calibrated, bits 4-7 servo output count) |
| 2 | 2 CRC-8 of the stored failsafe block, 3-5 zero |
| 3 | 2 `status` (0 applied, 1 armed, 2 range error, 3 state error, 4 link error, 5 EEPROM error, 6 marked not fitted), 3 low byte of `nonce`, 4-5 uncalibrated mV (status 1) or new `vscale_q15` (status 0) |

Replies (types 1, 2, 3) are loaded for the receiver's next 10 ACKs, because an ACK payload must be queued before the packet it accompanies.

## A2. nRF24 register set (transmitter)

`EN_AA` pipe 0; `EN_RXADDR` pipe 0; `SETUP_AW` 5 bytes; `SETUP_RETR` ARD = 750 us (code 2), ARC = 0; `FEATURE` = `EN_DPL | EN_ACK_PAY`; `DYNPD` = `DPL_P0`; `CONFIG` = `EN_CRC | CRCO | PWR_UP`, `MASK_RX_DR` = 1, `MASK_TX_DS` = 0, `MASK_MAX_RT` = 0; `RF_SETUP` 250 kbps (`RF_DR_LOW`) plus PA level; `RF_CH` 0..80. ARD 750 us is required for ACK payloads under 8 bytes at 250 kbps [checked: nRF24L01+ PS]. Receiver masks: `RX_DR` unmasked, `TX_DS` and `MAX_RT` masked. Airtime: TX frame 209 bits (about 0.84 ms), ACK 121 bits (about 0.48 ms), about 1.6 ms of each 10 ms slot including settling [verify on hardware].

## A3. Address derivation and known-answer vectors

Shared header `common/protocol.h`. FNV-1a 32-bit (basis 2166136261, prime 16777619). Hash input (6 bytes): `bind_id` as 4 little-endian bytes, `counter` (starts 0), `salt` (0x01 for `h1`, 0x02 for `h2`). Address `a0..a3` = `h1` little-endian, `a4` = low byte of `h2`. Reject and retry with `counter + 1` if any byte is 0x00 or 0xFF, all five bytes are equal, every byte is 0x55 or 0xAA, or `a0` is 0x55 or 0xAA.

| bind_id | counter used | h1 | h2 | address a0..a4 |
|---|---|---|---|---|
| 0xDEADBEEF | 0 | 0x4A5D46B0 | 0x4D5D4B69 | B0 46 5D 4A 69 |
| 0xA1B2C3D4 | 1 (counter 0 gave AA 4A C7 D4 17, rejected: a0 = 0xAA) | 0xB0C4D367 | 0xB1C4D4FA | 67 D3 C4 B0 FA |
| 0x00000001 | 0 | 0x84219137 | 0x852192CA | 37 91 21 84 CA |

These vectors were recomputed for v5 with an independent script and match.

## A4. Receiver EEPROM map (ATmega328P, 1 KB)

| Address | Size | Content |
|---|---|---|
| 0 / 1 | 1 / 1 | magic 0xA5 / layout version 1 |
| 2-5 / 6 / 7 / 8 | 4 / 1 / 1 / 1 | `bind_id` / `rf_channel` / `rate_code` / `channel_count` |
| 9-11 / 12-21 | 3 / 10 | failsafe modes (2 bits per channel) / preset values (8 bit) |
| 22 | 1 | CRC-8 of addresses 2 to 21 |
| 23 | 1 | `sense_state`: 0 not fitted, 1 fitted not calibrated, 2 fitted and calibrated (0xFF = build default) |
| 24-25 / 26 | 2 / 1 | `vscale_q15` (32768 = 1.0) / CRC-8 of 23 to 25 |
| 27 / 28 | 1 / 1 | `cell_count_override` (0 or 0xFF = auto, 2 to 4) / CRC-8 of address 27 |

One byte is written per main-loop pass when `eeprom_is_ready()` (3.4 ms per byte [checked]); interrupts stay on so servo pulses stay clean. Voltage maths without overflow (pack divider 100k over 6.2k, ratio 6.2/106.2, taken before the BEC; 32-bit): `pin_mv = raw * 1100 / 1023` (at most 1100); `pack_mv = pin_mv * 106200 / 6200` (the product is at most 116,820,000 and `pack_mv` at most 18,843, both fit `uint32_t`); `reported_mv = pack_mv * scale_q15 / 32768` (the product is at most 771,000,000, fits `uint32_t`). 16.8 V gives about 0.981 V at the pin. Cell count at power-up: `n = (pack_mv + 4249) / 4250` (ceiling of `pack_mv / 4250`), clamped to 2 to 4, accepted only if `pack_mv / n >= 2500`; `cell_count_override` replaces `n` when set. Low-voltage flag: `pack_mv < n * rx_alarm_mv` (`rx_alarm_mv` per cell, default 3300). Calibrate command: `scale_q15 = ref_mv * 32768 / uncalibrated_mv`, accepted 26214 to 40960 (0.80 to 1.25), reference 5000 to 17000 mV.

## A5. Settings and persisted structs

`Settings` is the snapshot the tick reads (two static buffers, `static_assert(sizeof <= 2048)`). Hand count 976 B; the `static_assert` is the authority. `TrainerCfg` and `MixerCfg` are gone in v5; nothing is reserved for a mixer.

```cpp
struct Failsafe   { uint8_t mode; uint8_t pad; int16_t value; };           // mode 0 preset, 1 hold, 2 no pulse; permille. 4 B
struct ModelHeader { uint32_t bind_id; char name[13];
                     uint8_t has_bind_id; uint8_t rf_channel; uint8_t rate_code; uint8_t pad[4]; };   // 24 B
struct ChannelCfg { uint8_t source /*0xFF none*/; uint8_t reverse; int16_t ep_lo, ep_hi; Failsafe fs; };  // 10 B x10
struct InputCfg   { int16_t rate_hi, rate_lo, expo, trim; uint8_t rate_switch /*0xFF none*/; uint8_t flags; };  // 10 B x64, axes and pots only
struct RadioCfg   { uint8_t profile /*0 Safe, 1 Medium, 2 Extreme, 3 Custom*/, hop_enabled /*reserved 0*/; uint16_t rx_alarm_mv /*per cell, 0 off*/;
                    uint8_t c_pa /*0..3*/, c_rate /*0 250k, 1 1M, 2 2M*/, c_arc /*0..15*/, c_ard /*(n+1)*250 us*/,
                    c_rf_channel /*0..80, 0xFF from bind scan*/, c_addr_w /*3..5*/, c_crc_len /*1 or 2*/, pad;
                    uint8_t c_hop[16]; };                                 // 28 B; c_* used only when profile == 3
struct CalRecord  { uint16_t min, centre, max; uint8_t centring, deadband_pm /*default 20*/; uint16_t crc; };  // 10 B x16
struct GlobalCfg  { uint32_t last_bind_id; uint8_t last_slot, last_rf_channel, last_rate_code;
                    uint8_t module_type /*0 standard, 1 PA/LNA*/, extreme_ack, medium_pa[2] /*per module type*/, power_measured;
                    int8_t power_dbm[4], antenna_gain_dbi_x2;
                    uint8_t brightness, volume, mute, display_rotation, pad[3]; };   // 24 B
// Settings: ModelHeader 24 + ch[10] 100 + in[64] 640 + radio 28 + cal[16] 160 + global 24 = 976 B
// cal[0..7] = onboard analog axes and pots, cal[8..15] = first 8 axes of the connected USB gamepad.
struct Tone { uint16_t freq_hz, dur_ms; uint8_t critical, pad; };           // 6 B
struct FactoryRecord { uint32_t magic /*0xFAC70001*/; uint16_t battery_cal_q15 /*29491..36045*/, battery_ref_mv;
                       uint8_t cells /*1*/, flags /*bit0 battery, bit1 stick wizard*/; uint16_t redo_count; uint8_t reserved[2]; uint16_t crc; };  // 16 B
```

The effective bind trio is `(bind_id, rf_channel, rate_code)` read as one unit: the model's if `has_bind_id`, else `GlobalCfg`'s. Freeze rule: the layout and packet format freeze at Phase 1 exit with later-gated fields (failsafe, curves, bind, `hop_enabled`, `hop_idx`/`sweep` bits, command packet) present at their defaults; a later change bumps the JSON `schema` and the protocol version and ships a migration.

## A6. Flash layout and write rules (STM32F411 Black Pill) [verify against RM0383]

| Item | Value |
|---|---|
| Flash | 512 KB, sectors 0 to 3 (16 KB), 4 (64 KB), 5 to 7 (128 KB) [verify] |
| Key-value store | two alternating 128 KB sectors, 6 and 7 (0x08040000 and 0x08060000) [verify] |
| Firmware image limit | 256 KB (240 KB with the optional 16 KB SD bootloader in sector 0, app at 0x08004000 with `VTOR` set) |
| Shared constant | `kv_region.h`, included by the linker script fragment and the KV driver; the build fails if the image exceeds the limit |
| Records | sequence number and CRC per record; factory record two copies, copied verbatim on compaction and verified before the old sector is erased |
| Erase time | a 128 KB sector erase takes on the order of 1 to 2 s [verify]; the IWDG reload is extended to about 4 s nominal around it, one sector per operation, only while TX is muted or has not started; deferred in flight |
| RAM | 128 KB, all DMA-capable, no CCM [verify] |

## A7. Reset flags and resume (STM32F4 RCC_CSR) [verify RM0383]

Several flags set together (power-on sets `PORRSTF`, `BORRSTF` and `PINRSTF`; IWDG and software resets also set `PINRSTF`). Read RCC_CSR, then clear with `RMVF` and clear the magic value. First match wins:

| Order | Test | Result |
|---|---|---|
| 1 | `PORRSTF` | Normal (full startup checks, then transmit at once; no mute) |
| 2 | `IWDGRSTF` | Resume |
| 3 | `SFTRSTF` and no-init magic valid | Resume (UI-hang reset) |
| 4 | `BORRSTF` | Resume |
| 5 | `PINRSTF`, or `SFTRSTF` without magic | Normal |
| 6 | none | Normal |

`Boot decide(uint32_t csr_flags, bool magic_ok)` is a pure function; the unit test is the full truth table. Resume restores `Settings` from a two-slot no-init RAM mirror (each slot: sequence number and CRC-16; the main loop writes the older slot, sequence number last); a corrupt mirror or invalid flash data gives a normal start; three resets in 10 s stop resuming. CRC-16 of 976 B takes about 24 us table-driven at 168 MHz; at 100 MHz expect about 40 us [estimate]. Outage budget (watchdog case): detect up to 190 ms (LSI -47 % to +45 % [verify]), clocks and RAM 20 ms, nRF24 init 10 ms, mirror and flash CRC 5 ms, first packet 10 ms: about 45 ms after reset release, about 235 ms in total against the 500 ms failsafe.

## A8. Battery percent table (per cell, 1S)

| Cell V | 4.20 | 4.10 | 4.00 | 3.90 | 3.80 | 3.70 | 3.60 | 3.50 | 3.40 | 3.30 |
|---|---|---|---|---|---|---|---|---|---|---|
| % | 100 | 90 | 80 | 68 | 55 | 40 | 25 | 12 | 5 | 0 |

Typical Li-ion values, tune from a real discharge log. Linear interpolation, 1 s smoothing, 1 % hysteresis. Divider 100k/100k (ratio 0.5, 2.10 V at 4.2 V, source impedance 50 kohm, so 100 nF at the pin and the longest sample time; halve both resistors if the error is too large [verify]). `battery_cal_q15 = reference_mv * 32768 / raw_displayed_mv`, clamped 29491 to 36045.

## A9. ST7735 orientation

MADCTL (0x36) bits: MY 0x80, MX 0x40, MV 0x20, RGB/BGR 0x08 [checked: Adafruit ST7735 library]. Landscape needs MV.

| `display_rotation` | RGB-order panel | BGR-order panel [verify] |
|---|---|---|
| 0 | 0xA0 | 0xA8 |
| 180 | 0x60 | 0x68 |

Column and row offsets are per module variant in `kPanelOffset[variant][rotation]`, defaulted from the library. [verify on your module]: draw a 1 px border and corner markers in both rotations.

## A10. Receiver pin map (Nano class) and LDO

| Function | Pin |
|---|---|
| nRF24 SCK, MISO, MOSI, CSN, CE, IRQ | D13, D12, D11, D10, D9, D2 (INT0) |
| Servo outputs 1 to 6 | D3, D4, D5, D6, D7, D8 |
| Servo outputs 7 and 8 | A1, A2 |
| Pack voltage sense (only if fitted) | A0, 100k/6.2k divider from the pack before the BEC, 100 nF at the pin, internal 1.1 V reference [checked] |
| Bind button | A3 to GND, pull-up |
| CH9 and CH10 digital outputs (if OQ-05 option B) | A4, A5 |

Receiver power: battery pack (2S to 4S, up to 16.8 V) into a 5 V buck BEC (at least 20 V input [verify the part]) that feeds the Nano 5 V pin. nRF24 supply: own MIC5219-3.3 LDO from the BEC 5 V rail, 100 uF polymer plus 10 uF ceramic, 100 nF at the module. nRF24 inputs tolerate 5 V only while its VDD is 2.7 to 3.3 V [checked]. Its MISO and IRQ high level meets the ATmega328P input-high level (0.6 VCC = 3.0 V) with no guaranteed margin, so measure at the Nano pin (target 3.2 V or more); a 74HCT125-class buffer is the fix [checked, [verify] HCT thresholds].
