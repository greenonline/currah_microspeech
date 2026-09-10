# Currah µSpeech - layout

## Notes

### Determining layout/traces from photos

Layout and routing mostly taken from these two images: [front](xtras/images/hw.jpg) and [rear](xtras/images/hw_back.jpg):

[![Front of PCB][1]][1]

[![Rear of PCB][2]][2]

This video also has some good clear views of portions of the PCB, [Sinclair ZX Spectrum Currah Microspeech & Sound Output](https://www.youtube.com/watch?v=PdAvMTof0jo).

### General layout

Improving component IDs:

```none
----------------------------------------------------           
VC1             R12 C1                  U3         J3
    R16 R15 C4  R13 D2                             J3
    C5  R17 R9  R10 R14 L5 R11          U2         J3
        Q1                                         J3
                R7                      U1         J3
J1              R7  D1                             J3
                R6    R8      C2        U4_OUT     J3
                R6    R3      R5        U4_GND     J3
                      D3      R2        U4_IN      J3
J2                    R4      R1        C3         J3
----------------------------------------------------           
```


Headers:

 - J1 is the RF/UHF push connector
 - J2 is the three wire flying audio cable
 - J3 is the ZX Spectrum bus

Discrete:

 - Q1 2N2907 EBC
 - D1 1N914

ICs:

 - U1 SP0256A-AL2 (28 pin)
 - U2 ROM 9316C (24 pin)
 - U3 ULA LA05-147 (28 pin)
 - U4 7805

### ZX Spectrum bus

#### Front side

```none
 Bus 01a - ULA 12
 Bus 02a - x
 Bus 03a - ROM 17
 Bus 04a - x
 Bus 05a - blank
 Bus 06a - SP0256 18
 Bus 07a - SP0256 17
 Bus 08a - SP0256 16 & ROM 10
 Bus 09a - ROM 14
 Bus 10a - SP0256 13 & ROM 9
 Bus 11a - ROM 13
 Bus 12a - SP0256 pin 14
 Bus 13a - x
 Bus 14a - x
 Bus 15a - x
 Bus 16a - x
 Bus 17a - x
 Bus 18a - x
 Bus 19a - ULA 26
 Bus 20a - x
 Bus 21a - x
 Bus 22a - x
 Bus 23a - x
 Bus 24a - x
 Bus 25a - x
 Bus 26a - via ULA 22
 Bus 27a - ULA 21
 Bus 28a - ULA 16
```
 
#### Rear side

```none
 Bus 01b - via ULA 13
 Bus 02b - via ULA 11
 Bus 03b - x  (normally 5V)
 Bus 04b - 9V
 Bus 05b - blank
 Bus 06b - GND
 Bus 07b - GND
 Bus 08b - x
 Bus 09b - ULA 4 & ROM 8  (A0)
 Bus 10b - ULA 5 & ROM 23 (A1)
 Bus 11b - ULA 6 & ROM 22 (A2)
 Bus 12b - ULA 8 & ROM 19 (A3)
 Bus 13b - x 1
 Bus 14b - x 2
 Bus 15b - x 3
 Bus 16b - x 4
 Bus 17b - x 5
 Bus 18b - x 6
 Bus 19b - x 7
 Bus 20b - ULA 25 (/RESET)
 Bus 21b - ULA 24 (A7)
 Bus 22b - ULA 23 (A6)
 Bus 23b - ULA 20 (A5)
 Bus 24b - ULA 19 (A4)
 Bus 25b - ULA 15 (/ROMCS)
 Bus 26b - x
 Bus 27b - ULA 17
 Bus 28b - ULA 18
```
 

### R11

Interestingly, this photo, from [Sinclair ZX Spectrum Currah Microspeech & Sound Output](https://www.youtube.com/watch?v=PdAvMTof0jo), shows R11 unpopulated:

[![R11 unpopulated][3]][3]

From this image, taken from [CURRAH MICRO SPEECH (USPEECH)](https://blog.bisinternet.com/index.php/sinclair/zx-spectrum/currah-micro-speech-uspeech/), it can be seen that R11 does *not* actually go to pin 26 of the SP0256

[![R11 not going to pin 26][5]][5]

From this image, taken from [currah_uspeech_tests](https://maziac.github.io/currah_uspeech_tests/), it looked as if R11 did, as well as going to pin 1 of the ULA (but now I am not even sure of that):

[![Annotated hardware][6]][6]

### Bodged resistor

This photo, from the same video, shows a bodged resistor between pin 9 ULA and a pin on the ZXSpectrum bus?

[![Bodged resistor][4]][4]

### PCB revision

This latter photo is also of a different revision of the PCB, or in better condition. The traces are much more defined and not so "bubbly and crinkled", as the traces on the PCB in the [currah_uspeech_tests](https://maziac.github.io/currah_uspeech_tests) blog.

### Determining layout/traces by physical device

By this point, I had managed to get hold of a physical device from eBay (£21.50, maybe expensive for an untested and case broken open unit, but I didn't feel that smashing open a working unit was appropriate, seeing as they are not being made anymore. I got it for half of the asking price anyway), which should makes things easier. 


### ULA connections from bus are all inputs?

Would it make sense that the ULA only decodes info from the bus, to direct action on the PCB? Therefore, all bus connections to the ULA would be just input.

Or would the ULA need to signal back to the CPU?

See [Currah µSpeech - reverse engineering](Currah%20µSpeech%20-%20reverse%20engineering.md) for details about the ULA.

### ZX bus for reference


```none
 A15   - 01a Bus 01b - A14
 A13   - 02a Bus 02b - A12
 D2    - 03a Bus 03b - 5V
 NC    - 04a Bus 04b - 9V
 blank - 05a Bus 05b - blank
 D0    - 06a Bus 06b - GND
 D1    - 07a Bus 07b - GND
 D2    - 08a Bus 08b - CLK
 D6    - 09a Bus 09b - A0
 D5    - 10a Bus 10b - A1
 D3    - 11a Bus 11b - A2
 D4    - 12a Bus 12b - A3
 /INT  - 13a Bus 13b - /IORQGE
 /NMI  - 14a Bus 14b - GND
 /HALT - 15a Bus 15b - VIDEO
 /MREQ - 16a Bus 16b - Y
 /IORQ - 17a Bus 17b - V
 /RD   - 18a Bus 18b - U
 /WR   - 19a Bus 19b - /BUSRQ
 -5V   - 20a Bus 20b - /RESET
 /WAIT - 21a Bus 21b - A7
 +12V  - 22a Bus 22b - A6
 12VAC - 23a Bus 23b - A5
 /M1   - 24a Bus 24b - A4
 /RFSH - 25a Bus 25b - /ROMCS
 A8    - 26a Bus 26b - /BUSACK
 A10   - 27a Bus 27b - A9
 NC    - 28a Bus 28b - A11
```

See also [ZX Spectrum Expansion Bus Overview](https://www.scribd.com/document/717386736/The-expansion-bus-on-the-ZX-Spectrum)

<!-- Images -->

  [1]: ../xtras/images/hw.jpg "Front of PCB"
  [2]: ../xtras/images/hw_back.jpg "Rear of PCB"
  [3]: ../xtras/images/R11%20unpopulated.png "R11 unpopulated"
  [4]: ../xtras/images/Bodged%20resistor.png "Bodged resistor"
  [5]: ../xtras/images/currah-speech-modified-768x433.jpg "R11 not going to pin 26"
  [6]: ../xtras/images/hw.jpg "Annotated hardware"


  
  
  
  
