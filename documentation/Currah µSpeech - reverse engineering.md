# Currah µSpeech - reverse engineering the schematic and PCB layout

## Preamble

Why not try to reverse engineer a Currah µSpeech? 

The Cheetah and [dk'tronics speech](https://vintagecomputermuseum.com/collection/dktronics-speech-synthesiser/) units could also be worth a go.

## Links

 - [currah_uspeech_tests](https://maziac.github.io/currah_uspeech_tests/)
 - [SP0256 PDF](https://www.100y.com.tw/pdf_file/SPO256.pdf)
 - [Currah Microspeech (Currah µSpeech)](https://k1.spdns.de/Vintage/Sinclair/82/Peripherals/Currah%20uSpeech/)
 - [Tech notes](https://problemkaputt.de/zxdocs.htm#aboutthisdocument)


## Notes

### Component identification

From [this image](https://maziac.github.io/currah_uspeech_tests/pics/hw.jpg), taken from [currah_uspeech_tests](https://maziac.github.io/currah_uspeech_tests/):

[![Annotted hardware][2]][2]


 - (`U1`) [SP0256A-AL2 SemiConductor - DIP24 - Littelfuse](https://www.ebay.co.uk/itm/175559442527), £39.99+£4.99
 - [SP0256-AL2](https://en.wikipedia.org/wiki/General_Instrument_SP0256)
 - (`U2`) 2kB ROM - 9316C 
   - [HOW TO READ 9316 ROMS](https://www.mikesarcade.com/cgi-bin/spies.cgi?action=url&type=info&page=9316.txt)
   - ROM code?
   - Pinout?
   - AKA 2316 or RO-3-9316C
 - (`U3`) ULA - LA05-147 (IC code from [this image](https://i.ebayimg.com/images/g/y~sAAeSwXudqgWE~/s-l1600.webp), from [Currah MicroSpeech ZX Spectrum Speech Sound Device Untested for Parts Or Repair](https://www.ebay.co.uk/itm/227477894410)

   [![ULA IC code][1]][1]

   - ULA code??? TTL equivalent circuit?


### Sourcing the unit and parts

Please see [Currah µSpeech - purchasing](documentation/Currah%20µSpeech%20-%20purchasing.md).

### Discrete components

32 components + 2 connectors (bus and video)

 - 7805 5V regulator (U4)
 - Resistors:
   - at least 16? + 1 x big red
   - 2 x dark brown: (brown green orange gold): 1, 5, 3, 0.1 = 15.3 Ohm??? => 15k (R1, R2)
   - 1 x pink (blue blue orange red red): 6, 6, 3, 10, ±1% = 6k6
     - (red red orange silver silver): 2, 2, 3, 0.01, ±10% = 2R2 (R3)
     - (red red orange grey grey): 2, 2, 3, 100M, ±0.05, = 22300M
   - 6 x green 
     - 2 x (red red red silver gold): 2, 2, 2, 0.01, ±5% = 2.2 Ohm (R4, R5)
     - 3 x (brown black black gold black): 1, 0 , 0, 0.1, ? = 10 Ohm (R6, R7, R8)
     - 1 x (brown red black gold black): 1, 2, 0, 0.1, ? = 12 Ohm (R9)
   - 7 x light brown 
     - 2 x (blue grey brown gold): 6, 8, 1, 0.1 = 68 Ohm => 680R (R10, R11)
     - 2 x (brown black green gold): 1, 0, 5, 0.1 = 10.5 Ohm => 1M (R12, R13)
     - 1 x (red red red gold): 2, 2, 2, 0.1 = 22.2 Ohm => 2k2 (R14)
     - 1 x (brown black orange gold): 1, 0, 3, 0.1 = 10.3 Ohm => 10k (R15)
     - 1 x (red red orange gold): 2, 2, 3, 0.1 = 22.3 Ohm => 22k (R16)
   - 1 x big red (brown red black silver?): 1, 2, 0, 0.01 = 1.2 Ohm => 12R (not 120R???) (R17)
 - Variable cap (CV1)
 - 2 x small blue (inductor/choke?) (L1->C4, L2->C5) (maybe capacitor
 - Big black (inductor/choke?) (L5), is this a big capacitor (C6)?
 - Diodes
   - 1 x red IN4014? (D1)
   - 2 x black/yellow (germanium?) (small signal or zener? schottky?) (D2, D3)
 - Transistor (Q1)
   - PNP in datasheet of SPO256 2N2907
   - EBC
 - Cap
   - 1 x Bypass on ULA, 100 nF - 1 µF (C1)
 - Two smooth light brown cylinders - inductors? (L3->C2, L4->C3) (maybe capacitors?) L3 100 nF, L4 330 nF for a typical 7805 application


Note:

 - [Resistor chart](https://www.thegeekpub.com/calculators/resistor-calculator-calculate-the-value-of-resistors/) - wrong for 4 bands
 - [Resistor color code](https://www.physics-and-radio-electronics.com/electronic-devices-and-circuits/passive-components/resistors/resistorcolorcode.html) - better for four band

The placement of the two smooth brown cylindrical components, next to the regulator, make one think that they are actually capacitors.

Also, the two smooth brown cylindrical components at the bottom of this photo:

[![Hardware][3]][3]
 
have been replaced with two more small blue components, in this photo
 
[![More blue components, including the bypass capacitor - capacitors][4]][4]
 
What is more, the bypass capacitor for the ULA has also been replaced by a small blue component.

Therefore is is safe to conclude that the small blue components and the smooth brown cylindrical components are actually capacitors, probably in the 100 nF to 1 µF range.


### Pinout

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

