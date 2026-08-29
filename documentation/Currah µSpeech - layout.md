# Currah µSpeech - layout


Layout and routing mostly taken from these two images: [front](hw.jpg) and [rear](hw_back.jpg).

This video also has some good clear views of portions of the PCB, [Sinclair ZX Spectrum Currah Microspeech & Sound Output](https://www.youtube.com/watch?v=PdAvMTof0jo).


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


J3 is bus

```none
 Bus 01b - via
 Bus 02b - via
 Bus 03b - 5V (n/c?)
 Bus 04b - 9V
 Bus 05b - blank
 Bus 06b - GND
 Bus 07b - GND
 Bus 08b - x
 Bus 09b - ULA 4 & ROM 8
 Bus 10b - ULA 5 & ROM 23
 Bus 11b - ULA 6 & ROM 22
 Bus 12b - ULA 8 & ROM 19
 Bus 13b - x 1
 Bus 14b - x 2
 Bus 15b - x 3
 Bus 16b - x 4
 Bus 17b - x 5
 Bus 18b - x 6
 Bus 19b - x 7
 Bus 20b - ULA 25
 Bus 21b - ULA 24
 Bus 22b - ULA 23
 Bus 23b - ULA 20
 Bus 24b - ULA 19
 Bus 25b - ULA 15
 Bus 26b - x
 Bus 27b - ULA 17
 Bus 28b - ULA 18
```
 

Discrete:

 - Q1 2N2907 EBC
 - D1 1N914

ICs:

 - U1 SP0256A-AL2 (28 pin)
 - U2 ROM 9316C (24 pin)
 - U3 ULA LA05-147 (28 pin)


Interestingly, this photo, from [Sinclair ZX Spectrum Currah Microspeech & Sound Output](https://www.youtube.com/watch?v=PdAvMTof0jo), shows R11 unpopulated:

[![R11 unpopulated][1]][1]

This photo, from the same video, shows a bodged resistor between pin 9 ULA and a pin on the ZXSpectrum bus?

[![Bodged resistor][2]][2]

It is also a different revision of the PCB, or in better condition. The traces are much more defined and not so "bubbly and crinkled", as the traces on the PCB in the [currah_uspeech_tests](https://maziac.github.io/currah_uspeech_tests) blog.

From this image, taken from [CURRAH MICRO SPEECH (USPEECH)](https://blog.bisinternet.com/index.php/sinclair/zx-spectrum/currah-micro-speech-uspeech/), it can be seen that R11 does *not* actually go to pin 26 of the SP0256

[![R11 not going to pin 26][3]][3]

From this image, taken from [currah_uspeech_tests](https://maziac.github.io/currah_uspeech_tests/), it looked as if R11 did, as well as going to pin 1 of the ULA (but now I am not even sure of that):

[![Annotted hardware][4]][4]



<!-- Images -->

  [1]: ../xtras/images/R11%20unpopulated.png "R11 unpopulated"
  [2]: ../xtras/images/Bodged%20resistor.png "Bodged resistor"
  [3]: ../xtras/images/currah-speech-modified-768x433.jpg "R11 not going to pin 26"
  [4]: ../xtras/images/hw.jpg "Annotted hardware"


  
  
  
  
