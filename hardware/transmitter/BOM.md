# Bill of Materials

- Generated: 2026-11-22
- Source: `hardware/transmitter/transmitter.kicad_sch` (all sheets)
- Regenerate: `python3 hardware/tools/make_bom.py`

## Summary

| Section | Lines | Parts |
|---|---|---|
| Modules | 3 | 3 |
| ICs | 9 | 9 |
| Resistors | 15 | 51 |
| Capacitors | 6 | 34 |
| Inductors and ferrites | 4 | 4 |
| Diodes and transistors | 3 | 3 |
| Connectors | 14 | 14 |
| Switches | 1 | 1 |
| Buzzer/audio | 1 | 1 |
| **Total** | **56** | **120** |

## Modules

| Qty | Value | Description | References | Footprint |
|---|---|---|---|---|
| 1 | Black Pill STM32F411 | WeAct Black Pill STM32F411CEU6 (v3.x). Pins 1-20 = header P2.1-P2.20 (left), 21-40 = P1.20..P1.1 (right), 41-44 = SWD header P3.1-P3.4, B0 = BOOT0 button pad (no header pin). Source: github.com/hojoonch/BlackPill_WeAct-BlackPill-STM32F411CEU6-KiCad-Library validation/pinout_and_geometry.csv. [verify] left/right edge. | U1 | - |
| 1 | nRF24L01+ PA/LNA module | nRF24L01+PA+LNA SMA module, 2x4 header. Pin order 1 GND 2 VCC 3 CE 4 CSN 5 SCK 6 MOSI 7 MISO 8 IRQ (odd pins right, even pins left in this symbol). [verify] which header row holds the odd pins. | U301 | - |
| 1 | ST7735 160x128 landscape | 1.8in 128x160 ST7735S SPI TFT, 8-pin header VCC GND CS RESET A0 SDA SCK LED (no SD slot variant, LCDwiki MSP1803). [verify] header order of the purchased module. | U501 | - |

## ICs

| Qty | Value | Description | References | Footprint |
|---|---|---|---|---|
| 1 | BQ24074RGT | USB-Friendly Li-Ion Battery Charger and Power-Path Management, VQFN-16 | U101 | Package_DFN_QFN:VQFN-16-1EP_3x3mm_P0.5mm_EP1.6x1.6mm |
| 1 | TCA9555PWR | 16-bit I/O expander, I2C and SMBus interface, interrupts, w/ pull-ups, TSSOP-24 package | U404 | - |
| 1 | TLV75533 | 500mA Low Dropout Voltage Regulator, Fixed Output 3.3V, SOT-23-5 | U104 | Package_TO_SOT_SMD:SOT-23-5 |
| 1 | TPS7A2033 | 300 mA Low Dropout Voltage Regulator, Fixed Output, 1.6..6.0Vin, Low-Noise (7μV RMS), 6.5μA IQ LDO, X2SON-5 | U105 | Package_SON:Texas_X2SON-4_1x1mm_P0.65mm |
| 1 | TPS2051C (0.5 A class switch) | 0.5A Current limited power switch, single channel, output discharge, reverse blocking, SOT-23-5 | U502 | Package_TO_SOT_SMD:SOT-23-5 |
| 1 | TPS63000 | Buck-Boost Converter, 1.8-5.5V Input Voltage, 1.8A Switch Current, Adjustable 1.2-5.5V Output Voltage, VSON-10 | U103 | Package_SON:Texas_DRC0010J_ThermalVias |
| 1 | TPS63060 | Buck-Boost Converter, 2.5-12V Input Voltage, 2-A Switch Current, Adjustable 2.5-8V Output Voltage, S-PWSON-N10 | U106 | Package_SON:Texas_S-PWSON-N10_ThermalVias |
| 1 | USBLC6-2P6 | Very low capacitance ESD protection diode, 2 data-line, SOT-666 | U102 | Package_TO_SOT_SMD:SOT-666 |
| 1 | USBLC6-2P6 (ESD on D+/D-) | Very low capacitance ESD protection diode, 2 data-line, SOT-666 | U503 | Package_TO_SOT_SMD:SOT-666 |

## Resistors

| Qty | Value | Description | References | Footprint |
|---|---|---|---|---|
| 1 | 10R | Resistor | R110 | - |
| 9 | 100R | Resistor | R419-R426, R501 | - |
| 2 | 1k | Resistor | R203, R503 | - |
| 1 | 1.5k | Resistor | R103 | - |
| 1 | 1.8k | Resistor | R104 | - |
| 2 | 4.7k | Resistor | R427, R428 | - |
| 2 | 5.1k | Resistor | R101, R102 | - |
| 23 | 10k | Resistor | R105, R107, R401-R414, R416-R418, R502, R505-R507 | - |
| 1 | 10k (BOOT0 pull-down) | Resistor | R202 | - |
| 1 | 49.9k | Resistor | R106 | - |
| 1 | 62k | Resistor | R112 | - |
| 4 | 100k | Resistor | R109, R113, R114, R504 | - |
| 1 | 100k (PB2/BOOT1 pull-down) | Resistor | R201 | - |
| 1 | 560k | Resistor | R111 | - |
| 1 | 620k | Resistor | R108 | - |

## Capacitors

| Qty | Value | Description | References | Footprint |
|---|---|---|---|---|
| 13 | 100nF | Unpolarized capacitor | C104, C116, C301, C402, C404-C411, C501 | - |
| 5 | 1uF | Unpolarized capacitor | C101, C108, C109, C111, C302 | - |
| 2 | 4.7uF | Unpolarized capacitor | C102, C103 | - |
| 8 | 10uF | Unpolarized capacitor | C105, C110, C112, C113, C303, C412, C502, C503 | - |
| 4 | 22uF | Unpolarized capacitor | C106, C107, C114, C115 | - |
| 2 | 100uF | Polarized capacitor | C304, C504 | - |

## Inductors and ferrites

| Qty | Value | Description | References | Footprint |
|---|---|---|---|---|
| 1 | 1.5uH | Inductor | L101 | - |
| 1 | 2.2uH | Inductor | L102 | - |
| 1 | Ferrite 600R@100MHz | Ferrite bead | FB101 | - |
| 1 | Ferrite (analog 3V3, match VDDA) | Ferrite bead | FB401 | - |

## Diodes and transistors

| Qty | Value | Description | References | Footprint |
|---|---|---|---|---|
| 1 | 2N7002 (backlight switch) | N-MOSFET transistor | Q501 | - |
| 1 | Flyback | Schottky diode | D501 | - |
| 1 | MMBT3904 (buzzer driver) | 0.2A Ic, 40V Vce, Small Signal NPN Transistor, SOT-23 | Q502 | Package_TO_SOT_SMD:SOT-23 |

## Connectors

| Qty | Value | Description | References | Footprint |
|---|---|---|---|---|
| 1 | Gimbal 1 (3V3 GND X Y Z) | Generic connector, single row, 01x05, script generated (kicad-library-utils/schlib/autogen/connector/) | J403 | - |
| 1 | Gimbal 2 (3V3 GND X Y Z) | Generic connector, single row, 01x05, script generated (kicad-library-utils/schlib/autogen/connector/) | J404 | - |
| 1 | microSD (SPI2) | Micro SD Card Socket with one card detection pin | J501 | - |
| 1 | Module IPEX/U.FL jumper | coaxial connector (BNC, SMA, SMB, SMC, Cinch/RCA, LEMO, ...) | J302 | - |
| 1 | Pot 1 | Generic connector, single row, 01x03, script generated (kicad-library-utils/schlib/autogen/connector/) | J405 | - |
| 1 | Pot 2 | Generic connector, single row, 01x03, script generated (kicad-library-utils/schlib/autogen/connector/) | J406 | - |
| 1 | Program port | Generic connector, single row, 01x05, script generated (kicad-library-utils/schlib/autogen/connector/) | J201 | - |
| 1 | Protected 18650 (PROVISIONAL cell make) | Generic connector, single row, 01x02, script generated (kicad-library-utils/schlib/autogen/connector/) | J102 | - |
| 1 | SMA bulkhead | coaxial connector (BNC, SMA, SMB, SMC, Cinch/RCA, LEMO, ...) | J301 | - |
| 1 | SWD (GND CLK DIO 3V3sense NRST) | Generic connector, single row, 01x05, script generated (kicad-library-utils/schlib/autogen/connector/) | J202 | - |
| 1 | Switch bank 1 (GND + 8) | Generic connector, single row, 01x09, script generated (kicad-library-utils/schlib/autogen/connector/) | J401 | - |
| 1 | Switch bank 2 (GND + 6 d-pad) | Generic connector, single row, 01x07, script generated (kicad-library-utils/schlib/autogen/connector/) | J402 | - |
| 1 | USB-A host (weird port) | USB Type A connector | J502 | - |
| 1 | USB-C charge port | USB Power-Only 6P Type-C Receptacle connector | J101 | - |

## Switches

| Qty | Value | Description | References | Footprint |
|---|---|---|---|---|
| 1 | Hard power switch | Single Pole Single Throw (SPST) switch | SW101 | - |

## Buzzer/audio

| Qty | Value | Description | References | Footprint |
|---|---|---|---|---|
| 1 | Buzzer (30 mA peak) | Buzzer, polarized | LS501 | - |
