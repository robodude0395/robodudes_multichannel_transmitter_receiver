# Receiver BOM (Nano class)

Generated from `receiver.kicad_sch` (ERC clean). Footprints are not assigned yet, as in the transmitter. Part values marked [verify] need checking against the parts you buy.

| Qty | Value | Description | Refs |
|---|---|---|---|
| 1 | 470uF 10V | Servo rail bulk capacitor [verify] | C1 |
| 1 | 100nF | ADC input capacitor | C2 |
| 1 | 10uF 10V | LDO input | C3 |
| 1 | 470pF | LDO bypass | C4 |
| 1 | 10uF 10V | LDO output | C5 |
| 1 | 100uF 6.3V polymer | Radio bulk capacitor at the module [verify] | C6 |
| 1 | 100nF | Radio decoupling at the module | C7 |
| 1 | SS14 | Schottky: keeps USB 5 V from back-feeding the BEC | D1 |
| 1 | Pack 2S-4S (+, -) | Battery pack connector (XT30 or JST) | J1 |
| 8 | Servo header 1x3 | Servo header: pin 1 GND, pin 2 +5V, pin 3 signal | J2, J3, J4, J5, J6, J7, J8, J9 |
| 1 | Servo header 1x3 | On/off outputs A4 (CH9) and A5 (CH10) | J10 |
| 1 | 100k | Divider top, 1% | R1 |
| 1 | 6.2k | Divider bottom, 1% | R2 |
| 1 | Bind | Bind button, A3 to GND (internal pull-up) | SW1 |
| 1 | 5V BEC | Buck BEC, 5 V, input >= 20 V [verify part] | U1 |
| 1 | Arduino Nano | Arduino Nano v3 class board | U2 |
| 1 | MIC5219-3.3 | 3.3 V 500 mA LDO for the radio only | U3 |
| 1 | nRF24L01+ PA/LNA | nRF24L01+PA+LNA module, stock antenna | U4 |
