# Transmitter schematic: build report (Part 1 final)

Source of truth: `docs/design-hardware.md` section 2 (pin map). Project: KiCad 9.0.2, root `transmitter.kicad_sch` plus sheets MCU, Radio, Power, Inputs, Peripherals. Custom symbols in `transmitter_custom.kicad_sym` (Black Pill STM32F411, nRF24L01+ PA/LNA module, ST7735 module), registered in `sym-lib-table`.

## Facts kept from the first build
- Built with the `kicad` MCP server (v2.9.0, swig backend). Cross-sheet signals use global labels.
- The MCP server writes KiCad 10 format (header `(version 20260101)`, `(generator_version "10.0")`, plus `(body_style N)` and `(in_pos_files ...)` tokens in placed symbols). KiCad 9 rejects it (`Failed to load schematic`). No MCP tool changes the format. After any MCP edit, re-apply in `hardware/`:
  ```
  sed -i 's/(version 20260101)/(version 20250114)/; s/(generator_version "10.0")/(generator_version "9.0")/; /(body_style [0-9]*)/d; /(in_pos_files [a-z]*)/d' *.kicad_sch
  ```
  Check with `grep -c "body_style\|in_pos_files\|20260101" *.kicad_sch` (all 0).
- First-build ERC: 0 errors. 124 `lib_symbol_issues` warnings appear only because `~/.config/kicad/9.0/` has no global `sym-lib-table`; with KiCad's default table (`KICAD_CONFIG_HOME=<dir>` where `<dir>/9.0/sym-lib-table` is a copy of `/usr/share/kicad/template/sym-lib-table`) ERC reports 0 violations.
- Fixes made then: removed a duplicate GND PWR_FLAG on the MCU sheet; added PWR_FLAGs FLG104 (VINA_F) and FLG105 (RF_LDO_IN), rails fed through a resistor or ferrite.
- Library substitutions: TPS63000 for TPS63020, TPS2051C for TPS2553 (check 0.5 A limit), TLV75533, BQ24074. No footprints assigned.
- Baseline netlist: 104 nets, saved in `.agents/tasks/run/baseline.net`. Compare with `.agents/tasks/run/compare_nets.py`.

## Open [verify] items (carried over)
- PROVISIONAL / still to verify: OQ-29 ratiometric analog, antenna connectors J301/J302 (OQ-24 chose the stock module antenna), Black Pill regulator and 32.768 kHz crystal on PC14/PC15.
- Round 3 (decided): OQ-02 one TCA9555PWR (U404, I2C 0x20) on I2C1 (U1 pads 14 SCL and 15 SDA, pull-ups R427/R428) replaces the three 74HC165; NRF_CE moved to U1 pad 23 (PC14), NRF_IRQ to pad 35 (PB1), HOST_OC on pad 24 (PC15); SD_CD removed (J501 pin 9 DET is no-connect); OQ-03 J202 is a 5-pin SWD header (GND, SWCLK, SWDIO, 3V3 sense through R203 1k, NRST). ERC 0 violations; netlist delta recorded in `.agents/tasks/run3/allowed_deltas.json`.
- MCU: PA0 KEY button, PA9/PA10 bootloader, PA15/PB3-PB5 AF map, PC14/PC15 drive, PB2/BOOT1 pull-down, USB-C back-feed.
- Radio: module minimum supply, ripple under 50 mV p-p, LDO PSRR, single antenna only.
- Power: TPS63000 ripple and 600 mA, cell protection at 1.2 A peak, BQ24074 ILIM/ISET/TMR/ITERM/TS values (R105 placeholder), feedback dividers, SW101 placement.
- Inputs: CHG_STAT, PGOOD, OC polarity; connector pinouts; ANA_3V3 versus VDDA.
- Peripherals: ST7735 variant and offsets, backlight polarity, SD detect polarity, TPS2051C limit, buzzer 30 mA.

## Module pinouts (custom symbols, redrawn from real boards)
- Black Pill STM32F411 (U1, 44 pins + pad B0): pins 1-20 = header P2.1-P2.20 (left), 21-40 = P1.20..P1.1 (right), 41-44 = SWD header P3.1-P3.4 (3V3, SWDIO, SWCLK, GND). Sources: https://github.com/hojoonch/BlackPill_WeAct-BlackPill-STM32F411CEU6-KiCad-Library (validation/pinout_and_geometry.csv), https://github.com/WeActStudio/WeActStudio.MiniSTM32F4x1, https://stm32world.com/wiki/Black_Pill. Old pads 38-40 (PA13, PA14, BOOT0) were wrong: they are 3V3, GND, 5V. SWDIO/SWCLK moved to pads 42/43. BOOT0 has no header pin; it sits on pad `B0` (button pad). [verify] BOOT0 route (solder to button pad or USB DFU) and which long edge is "left".
- nRF24L01+PA+LNA (U301): 1 GND, 2 VCC, 3 CE, 4 CSN, 5 SCK, 6 MOSI, 7 MISO, 8 IRQ, unchanged. Drawn with even pins left, odd pins right. Sources: https://shillehtek.com/blogs/shillehtek-product-manuals/nrf24l01-pa-lna-wireless-transceiver-module-antenna-1100m-range-manual and the module datasheets https://cdn.shopify.com/s/files/1/0837/4340/8415/files/10335312609567.pdf?v=1770237957 and https://5.imimg.com/data5/SELLER/Doc/2024/12/475734627/DR/VN/KR/5030312/nrf24l01-pa-lna-sma-wireless-transceiver-antenna.pdf . [verify] which header row holds the odd pins.
- ST7735 1.8in (U501): 1 VCC, 2 GND, 3 CS, 4 RESET, 5 A0, 6 SDA, 7 SCK, 8 LED (was GND VCC SCK SDA RES DC CS BL). Sources: https://lcdwiki.com/1.8inch_SPI_Module_ST7735S_SKU:MSP1803, https://github.com/alepao821/driver-ST7735S. [verify] the purchased module is the 8-pin no-SD variant.
## Status (Part 1 final)
- Pass-2 layout done. Exports regenerated with `.agents/tasks/run/export_all.sh`: `hardware/transmitter/transmitter-schematic.pdf` and `hardware/transmitter/images/<sheet>.svg` + `.png` (3600 px wide) for the root and the MCU, Radio, Power, Inputs, Peripherals sheets, all newer than the `.kicad_sch` files.
- ERC: 0 errors, 231 warnings, all `lib_symbol_issues` (no global `sym-lib-table`, see above). 0 violations with the default table.
- Netlist: baseline 104 nets, new 105 nets, only the 11 allow-listed deltas (`.agents/tasks/run/allowed_deltas.json`: re-pinning, extra 3V3/GND/5V header pins).
- Remaining [verify] items: the lists above, plus Black Pill BOOT0 route and long-edge orientation, nRF24 header row of odd pins, ST7735 8-pin no-SD variant.

## BOM
- Run `python3 hardware/tools/make_bom.py` from any directory (needs `kicad-cli` on PATH).
- It exports all sheets of `transmitter.kicad_sch` and writes `hardware/transmitter/BOM.md`, grouped into sections.
- Edit the `RULES` table at the top of the script to change sections; re-run after schematic changes.

## Receiver
- `hardware/receiver/receiver.kicad_sch` (single sheet, generated by `.agents/tasks/run3/make_receiver.py`): Nano, nRF24 PA/LNA module on its own MIC5219-3.3 LDO, 5 V BEC from the pack, Schottky D1 to the logic rail, pack divider 100k/6.2k on A0, 8 servo headers, CH9/CH10 header, bind button. ERC: 0 violations. BOM: `receiver/BOM.md`. Open: BEC part (>= 20 V in), footprints, whether the Nano MISO/IRQ levels need a buffer.
