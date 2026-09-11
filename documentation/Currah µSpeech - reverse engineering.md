# Currah µSpeech - reverse engineering the schematic and PCB layout

## Preamble

Why not try to reverse engineer a Currah µSpeech? 

The Cheetah and [dk'tronics speech](https://vintagecomputermuseum.com/collection/dktronics-speech-synthesiser/) units could also be worth a go.

## Links

 - [currah_uspeech_tests](https://maziac.github.io/currah_uspeech_tests/)
 - [SP0256 PDF](https://www.100y.com.tw/pdf_file/SPO256.pdf)
 - [Currah Microspeech (Currah µSpeech)](https://k1.spdns.de/Vintage/Sinclair/82/Peripherals/Currah%20uSpeech/)
 - [Tech notes](https://problemkaputt.de/zxdocs.htm#aboutthisdocument)
 - [Speech with an SP0256-AL2](https://www.rehsdonline.com/post/speech-with-an-sp0256-al2)


## Notes

### Component identification

From [this image](https://maziac.github.io/currah_uspeech_tests/pics/hw.jpg), taken from [currah_uspeech_tests](https://maziac.github.io/currah_uspeech_tests/):

[![Annotted hardware][2]][2]


 - (`U1` 28 pins) [SP0256A-AL2 SemiConductor - DIP24 - Littelfuse](https://www.ebay.co.uk/itm/175559442527), £39.99+£4.99
 - [SP0256-AL2](https://en.wikipedia.org/wiki/General_Instrument_SP0256)
 - (`U2` 24 pins) 2kB ROM - 9316C 
   - [HOW TO READ 9316 ROMS](https://www.mikesarcade.com/cgi-bin/spies.cgi?action=url&type=info&page=9316.txt)
   - ROM code?
   - Pinout?
   - AKA 2316 or RO-3-9316C
 - (`U3` 28 pins) ULA - LA05-147 (IC code from [this image](https://i.ebayimg.com/images/g/y~sAAeSwXudqgWE~/s-l1600.webp), from [Currah MicroSpeech ZX Spectrum Speech Sound Device Untested for Parts Or Repair](https://www.ebay.co.uk/itm/227477894410)

   [![ULA IC code][1]][1]

   - ULA code??? TTL equivalent circuit?


### Sourcing the unit and parts

Please see [Currah µSpeech - purchasing](documentation/Currah%20µSpeech%20-%20purchasing.md).

### Discrete components

32 components + 2 connectors (bus and video)

 - 7805 5V regulator (U4)
 - Resistors:
   - at least 16? + 1 x big red
   - 2 x dark brown: (brown green orange gold): 1, 5, 3, 0.1 = 15.3 Ohm??? => 15k (`R1`, `R2`)
   - 1 x pink (blue blue orange red red): 6, 6, 3, 10, ±1% = 6k6
     - (red red orange silver silver): 2, 2, 3, 0.01, ±10% = 2R2 (`R3`)
     - (red red orange grey grey): 2, 2, 3, 100M, ±0.05, = 22300M
   - 6 x green 
     - 2 x (red red red silver gold): 2, 2, 2, 0.01, ±5% = 2.2 Ohm (`R4`, `R5`)
     - 3 x (brown black black gold black): 1, 0 , 0, 0.1, ? = 10 Ohm (`R6`, `R7`, `R8`)
     - 1 x (brown red black gold black): 1, 2, 0, 0.1, ? = 12 Ohm (`R9`)
   - 7 x light brown 
     - 2 x (blue grey brown gold): 6, 8, 1, 0.1 = 68 Ohm => 680R (`R10`, `R11`)
     - 2 x (brown black green gold): 1, 0, 5, 0.1 = 10.5 Ohm => 1M (`R12`, `R13`)
     - 1 x (red red red gold): 2, 2, 2, 0.1 = 22.2 Ohm => 2k2 (`R14`)
     - 1 x (brown black orange gold): 1, 0, 3, 0.1 = 10.3 Ohm => 10k (`R15`)
     - 1 x (red red orange gold): 2, 2, 3, 0.1 = 22.3 Ohm => 22k (`R16`)
   - 1 x big red (brown red black silver?): 1, 2, 0, 0.01 = 1.2 Ohm => 12R (not 120R???) (`R17`)
 - Variable cap (`CV1`)
 - 2 x small blue (inductor/choke?) (L1->`C4`, L2->`C5`) (maybe capacitor
 - Big black (inductor/choke?) (L5->`C6`), is this a big capacitor?
 - Diodes
   - 1 x red IN4014? (`D1`)
   - 2 x black/yellow (germanium?) (small signal or zener? schottky?) (`D2`, `D3`)
 - Transistor (`Q1`)
   - PNP in datasheet of SPO256 2N2907
   - EBC
 - Cap
   - 1 x Bypass on ULA, 100 nF - 1 µF (`C1`)
 - Two smooth light brown cylinders - inductors? (L3->`C2`, L4->`C3`) (maybe capacitors?) L3 100 nF, L4 330 nF for a typical 7805 application


Note:

 - [Resistor chart](https://www.thegeekpub.com/calculators/resistor-calculator-calculate-the-value-of-resistors/) - wrong for 4 bands
 - [Resistor color code](https://www.physics-and-radio-electronics.com/electronic-devices-and-circuits/passive-components/resistors/resistorcolorcode.html) - better for four band

#### The mystery blue and brown components are capacitors

The placement of the two smooth brown cylindrical components, next to the regulator, makes one think that they are actually capacitors.

Also, the two smooth brown cylindrical components at the bottom of this photo:

[![Hardware][3]][3]
 
have been replaced with two more small blue components, in this photo:
 
[![More blue components, including the bypass capacitor - capacitors][4]][4]
 
What is more, the bypass capacitor for the ULA has also been replaced by a small blue component.

Therefore is is safe to conclude that the small blue components and the smooth brown cylindrical components are actually capacitors, probably in the 100 nF to 1 µF range.


### Pinout

#### SP0256

```none
          +---v---+
   GND  1 |       | 28  OSC2
 RESET  2 |       | 27  OSC1
ROMDIS  3 |       | 26  ROMCLK
    C1  4 |       | 25  /SBY_RESET
    C2  5 |       | 24  DIGITAL_OUT
    C3  6 |       | 23  VDI
   VCC  7 |       | 22  TEST
   SBY  8 |       | 21  SER_IN
  /LRQ  9 |       | 20  /ALD
    A8 10 |       | 19  SE
    A7 11 |       | 18  A1
SEROUT 12 |       | 17  A2
    A6 13 |       | 16  A3
    A5 14 |       | 15  A4
          +-------+
```

Note that `/LRQ` and `SBY` are outputs (as specified in the datasheet).

Note thqt in this PCB, the SP0256 is always operating in MODE 1, as SE is tied to 5V.


#### ULA

ULA_LA05_147

```none
          +---v---+
        1 |       | 28  Vcc (+5V)
        2 |       | 27  
        3 |       | 26  
        4 |       | 25  
        5 |       | 24  
        6 |       | 23  
        7 |       | 22  
        8 |       | 21  
        9 |       | 20  
       10 |       | 19  
       11 |       | 18  
       12 |       | 17  
       13 |       | 16  
   GND 14 |       | 15  
          +-------+
```

Note: Pins 14 & 27 tied to ground

Inputs and outputs:

 - Pin 1 must be an output as conected to /ALD which is an input
 - Pin 2 must be an input as connected to SBY which is an output
 - Pin 4 must be an input to A0 on BUS (also A0 on ROM) 
 - Pin 5 must be an input to A1 on BUS (also A8 on ROM)
 - Pin 6 must be an input to A2 on BUS (also A9 on ROM)
 - Pin 7 must be an output to CS1 on ROM only?
 - Pin 8 must be an input to A3 on BUS (also A10 on ROM)
 - Pin 11 must be an input to A12 on BUS
 - Pin 13 must be an input to A14 on BUS
 - Pin 15 must be an output to [/ROMCS](https://sinclair.wiki.zxnet.co.uk/wiki/ZX_Spectrum_edge_connector#ROM_disable_pins) on BUS
 - Pin 16 must be an xxx? to NC? on BUS
 - Pin 17 must be an input to A9 on BUS (also A1 on ROM)
 - Pin 18 must be an input to A11 on BUS
 - Pin 19 must be an input to A4 on BUS (also A2 on ROM)
 - Pin 20 must be an input to A5 on BUS (also A3 on ROM)
 - Pin 21 must be an input to A10 on BUS (also A4 on ROM)
 - Pin 22 must be an input to A8 on BUS (also A5 on ROM)
 - Pin 23 must be an input to A6 on BUS (also A6 on ROM)
 - Pin 24 must be an input to A7 on BUS (also A7 on ROM)
 - Pin 25 could be an output as connected to RESET on SP0256 which is an input?
 - Pin 26 must be an input to /WR on BUS
 - Pin 27 must be an input if tied to GND


Note: The address lines could also be ULA inputs, *if* also coming from the ZX Spectrum bus.

One column

| Pin | IOPut |
|-----|-------|
|     |       |
|  1  | Output|
|  2  | Input |
|  3  |       |
|  4  | Input |
|  5  | Input |
|  6  | Input |
|  7  | Output|
|  8  | Input |
|  9  |  NC?  |
| 10  |  NC?  |
| 11  | Input |
| 12  |  NC?  |
| 13  | Input |
| 14  |  GND  |
| 15  |Output |
| 16  | NC?   |
| 17  | Input |
| 18  | Input |
| 19  | Input |
| 20  | Input |
| 21  | Input |
| 22  | Input |
| 23  | Input |
| 24  | Input |
| 25  |Output?|
| 26  | Input |
| 27  |  Input|
| 28  |  VCC  |

Two columns

| Pin | IOPut | Pin | IOPut |
|-----|-------|-----|-------|
|     |       |     |       |
|  1  | Output|  28 | VCC   |
|  2  | Input |  27 | Input |
|  3  |       |  26 | Input |
|  4  | Input |  25 |Output?|
|  5  | Input |  24 | Input |
|  6  | Input |  23 | Input |
|  7  | Output|  22 | Input |
|  8  | Input |  21 | Input |
|  9  | NC?   |  20 | Input |
| 10  | NC?   |  19 | Input |
| 11  | Input |  18 | Input |
| 12  | NC?   |  17 | Input |
| 13  | Input |  16 | to NC?|
| 14  | GND   |  15 | Output|
|     |       |     |       |

Two columns with connections (for convenience)

| Pin | IOPut | Conn. | Pin | IOPut | Conn. |
|-----|-------|-------|-----|-------|-------|
|     |       |       |     |       |       |
|  1  | Output| /ALD  |  28 | VCC   | +5V   |
|  2  | Input | SBY   |  27 | Input | GND   |
|  3  |       | R13   |  26 | Input | /WR   |
|  4  | Input | A0    |  25 |Output?| RESET |
|  5  | Input | A1    |  24 | Input | A7    |
|  6  | Input | A2    |  23 | Input | A6    |
|  7  | Output| CS1   |  22 | Input | A8    |
|  8  | Input | A3    |  21 | Input | A10   |
|  9  | NC?   | NC?   |  20 | Input | A5    |
| 10  | NC?   | NC?   |  19 | Input | A4    |
| 11  | Input | A12   |  18 | Input | A11   |
| 12  | NC?   | NC?   |  17 | Input | A9    |
| 13  | Input | A14   |  16 | to NC?| BUS NC|
| 14  | GND   | GND   |  15 | Output| /ROMCS|
|     |       |       |     |       |       |

#### 9316C

```none
          +---v---+
    A7  1 |       | 24  Vcc (+5V)
    A6  2 |       | 23  A8
    A5  3 |       | 22  A9
    A4  4 |       | 21  CS3 (Chip Select 3)*
    A3  5 |       | 20  CS1 (Chip Select 1)*
    A2  6 |       | 19  A10
    A1  7 |       | 18  CS2 (Chip Select 2)*
    A0  8 |       | 17  D7 (Data 7)
    D0  9 |       | 16  D6 (Data 6)
    D1 10 |       | 15  D5 (Data 5)
    D2 11 |       | 14  D4 (Data 4)
   GND 12 |       | 13  D3 (Data 3)
          +-------+
```

EPROM/EEPROM equivalent?

Use a [OneROM](https://onerom.org/buy/)!!!? See [Emulate a 9316C ROM for Currah Microspeech (µSpeech) #301](https://github.com/piersfinlayson/one-rom/discussions/301). As pointed out in the discussion, the logic of the ROM's three chip select lines needs to be determined (active high or low):

Pins select (wrong):

 - 18 - CS2 - ? (no *visible* connection)
 - 20 - CS1 - ULA pin 22 (confused pin 1, pin 22 is opposite pin 7)
 - 21 - CS3 - Regulated 5V

Recheck:

 - 18 - CS2 - GND
 - 20 - CS1 - Pin 7 ULA
 - 21 - CS3 - Regulated 5V

##### 2716 EPROM

From [eprom data](https://www.unitechelectronics.com/EPROM_data.htm)	

Inverted logic on two of the enable pins, and the VPP replaces CS3
          
```none
          +---v---+
    A7  1 |       | 24  Vcc (+5V)
    A6  2 |       | 23  A8
    A5  3 |       | 22  A9
    A4  4 |       | 21  VPP
    A3  5 |       | 20  /OE
    A2  6 |       | 19  A10
    A1  7 |       | 18  /CE
    A0  8 |       | 17  D7 (Data 7)
    D0  9 |       | 16  D6 (Data 6)
    D1 10 |       | 15  D5 (Data 5)
    D2 11 |       | 14  D4 (Data 4)
   GND 12 |       | 13  D3 (Data 3)
          +-------+
```


From [HOW TO READ 9316 ROMS](https://www.mikesarcade.com/cgi-bin/spies.cgi?action=url&type=info&page=9316.txt)

> I made an adapter for 9316 to 2716 as follows:
> 
> 1. Obtain a 24 Pin wire wrap socket.
> 2. Cut pin 21, leaving enough of a stub to solder to.
> 3. Solder a wire from Pin 24 to pin 18.
> 4. Solder a wire from Pin 12 to the stub pin 21.

Also, [9316B Rom replacement](https://forum.allaboutcircuits.com/threads/9316b-rom-replacement.69569/)


> For the base I am using a 2kb cartridge that contained a 9316B rom and I have replaced it with an at28c16 eeprom. I have successfully written to the eeprom using an arduino but for the life of me I can't get it to work. I have seen various sources quoting that the 9316B and 2716 are pin compatible (hence the 2816 should be too right?) and others saying pins 18 and 21 need to be swapped. I have tried both of these layouts and had no success.



<!-- Images -->


  [1]: ../xtras/images/Currah%20internals.png "ULA IC code"
  [2]: ../xtras/images/hw.jpg "Annotted hardware"
  [3]: ../xtras/images/hw.jpg "Hardware"
  [4]: ../xtras/images/Currah%20internals.png "More blue components, including the bypass capacitor - capacitors"

