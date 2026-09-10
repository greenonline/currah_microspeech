# Currah µSpeech - footprints 

## Preamble

The component footprints for the Currah µSpeech layout.

## Notes

### Footprints used

This was the first PCB layout attempt. The footprints used are listed below.

Capacitors:

 - `C1` 100 nF:  `Capacitor_THT:C_Disc_D5.1mm_W3.2mm_P5.00mm`

Resistors:

 - `R8` 10k: `Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal`
 - Vertical: `Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P2.54mm_Vertical`

Regulator:

 - `U4` 7805: `Package_TO_SOT_THT:TO-220F-3_Vertical`

Connector:


Diode:

 - `D2` Germanium?: `Diode_THT:D_DO-34_SOD68_P10.16mm_Horizontal`
 - `D3` Germanium?: `Diode_THT:D_DO-34_SOD68_P10.16mm_Horizontal`

Transistor:
 
  - `Q1` TO-92 2N2907 EBC: `Package_TO_SOT_THT:TO-92_Inline`
 
Header
 
 - `J1` RF/UHF Ariel: `Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical`
   - Can't be bothered to search for footprint of an RCA ariel
   - https://uk.farnell.com/pro-signal/psg01754/tv-coax-socket-pcb-pk10/dp/3383792 ???
 - `J2` 1x03: `Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical`
 - `J3` ZXSpectrum Bus: `Connector_PinHeader_2.54mm:PinHeader_2x28_P2.54mm_Vertical`

 
Variable capacitor

 - `CV1`, ???: `Potentiometer_THT:Potentiometer_Bourns_3266W_Vertical`
   - USing potentiometer, can't be bothered to find footprint. Maybe the same three pin (with right angle) arrangement








-------


-------

Capacitors:

 - `C1` 10 µF: `Capacitor_THT:CP_Radial_D5.0mm_P2.50mm`
 - `C2` 1 µF: `Capacitor_THT:CP_Radial_D5.0mm_P2.00mm`
 - `C8` 47 µF: `Capacitor_THT:CP_Radial_D6.3mm_P2.50mm`
 - `C13` 100 nF: `Capacitor_THT:C_Disc_D5.1mm_W3.2mm_P5.00mm`
 - `C9` 100 nF:  `Capacitor_THT:C_Disc_D5.1mm_W3.2mm_P5.00mm`
 - `C17` 47 pF: `Capacitor_THT:C_Disc_D3.8mm_W2.6mm_P2.50mm`
 - `C18` 22 pF: `Capacitor_THT:C_Disc_D3.8mm_W2.6mm_P2.50mm`
 - `C5` 8 pF: `Capacitor_THT:C_Disc_D3.8mm_W2.6mm_P2.50mm`
 - `C6` 8 pF: `Capacitor_THT:C_Disc_D3.8mm_W2.6mm_P2.50mm`
 - Maybe for `C5` and `C6` 8 pF (RCBUS): `Capacitor_THT:C_Disc_D3.0mm_W2.0mm_P2.50mm`

Resistors:

 - `R8` 10k: `Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal`
 - Vertical: `Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P2.54mm_Vertical`

XTAL

 - `Y1`: `Crystal:Crystal_HC49-4H_Vertical`

Switch

 - `SW1`: `Button_Switch_SMD:SW_SPST_CK_RS282G05A3`
 - Also possible: `Button_Switch_SMD:SW_Tactile_SPST_NO_Straight_CK_PTS636Sx25SMTRLFS`
 - OMRON: `???`

Headers

 - `H1`: `Connector_PinHeader_2.54mm:PinHeader_1x06_P2.54mm_Horizontal`
 - `H1` (Squires): was `Connector_PinHeader_2.54mm:PinHeader_1x06_P2.54mm_Horizontal` now `Connector_PinHeader_2.54mm:PinHeader_1x06_P2.54mm_Vertical`
 - `H2` (Squires): was `My_Components:Conn_Pin_Header_39x1_2.54mm`, now `Connector_PinHeader_2.54mm:PinHeader_1x39_P2.54mm_Horizontal`, better for less silkscreen of the pins: `Connector_PinHeader_2.54mm:PinHeader_1x39_P2.54mm_Vertical`
 - `H3` (RCBUS): `Connector_PinHeader_2.54mm:PinHeader_1x10_P2.54mm_Horizontal`
 - `H4` (RCBUS): `Connector_PinHeader_2.54mm:PinHeader_1x05_P2.54mm_Horizontal`
 - `H2` (RCBUS80): `Connector_PinHeader_2.54mm:PinHeader_1x40_P2.54mm_Vertical`
 - `H3` (RCBUS80): `Connector_PinHeader_2.54mm:PinHeader_1x40_P2.54mm_Vertical`
 - Trying to use a 2x40 but the footprint has the pins numbered odd-even when I want top to bottom. Annoying.
 - `H2` (RCBUS80/40) `Connector_PinHeader_2.54mm:PinHeader_2x40_P2.54mm_Horizontal`
 - FOr H2, it is better to use the vertical connector footprint, less silkscreen
 - `H2` (RCBUS80): `Connector_PinHeader_2.54mm:PinHeader_2x40_P2.54mm_Vertical`
 - `H2` (RCBUS40): `Connector_PinHeader_2.54mm:PinHeader_1x40_P2.54mm_Vertical`

Jumpers:

 - `J1`: `Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical`
 - `J2`: `Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical`
 - `J5`: `Connector_PinSocket_2.54mm:PinSocket_2x03_P2.54mm_Vertical`
 - `J7`: `Connector_PinSocket_2.54mm:PinSocket_1x03_P2.54mm_Vertical`
 - `J8`: `Connector_PinSocket_2.54mm:PinSocket_1x03_P2.54mm_Vertical`
 - `J6`: `Connector_PinSocket_2.54mm:PinSocket_2x08_P2.54mm_Vertical`

LED:

 - `LED1`: `LED_THT:LED_D3.0mm`

IC:

 - `U8` (GOL): `Package_DIP:DIP-14_W7.62mm_LongPads`
 - `U5` (Squires): `Package_DIP:DIP-14_W7.62mm`
 - `U6` (Squires): `Package_DIP:DIP-14_W7.62mm`
 - `U7` (Squires): `Package_DIP:DIP-14_W7.62mm`
 - `U8` (Squires): `Package_DIP:DIP-14_W7.62mm`
 - `U8` (RCBUS): `Package_DIP:DIP-14_W7.62mm`

Mounting holes:

 - `MountingHole_2.2mm_M2_DIN965_Pad`, Ref and footprint both set to not visible. REFs start top left REF1, clockwise