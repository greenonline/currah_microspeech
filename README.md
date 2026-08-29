
# currah_microspeech

Schematic and PCB layout of the Currah µSpeech for the Sinclair ZX Spectrum

## Preamble

Inspired by [AY-3-8910 Soundcard and Music Generator for ZX Spectrum](https://www.youtube.com/watch?v=XaY5Ca7vKt8)

 - [Sinclair ZX Spectrum Melodik2 AY Interface PCB](https://www.ebay.co.uk/itm/197944545954)
Melodik2
 - [Melodik2 AY Interface](https://hw.speccy.cz/melodik2.html)
Similar to [Solving a 30-Year-Old Amiga Mystery](https://www.youtube.com/watch?v=aBnO_6cKC0c), no ZN447/8/9E

If you close your eyes and listen to these Speech Synths, you will have absolutely no idea what they are saying... However, if you can see the text, then yes, the "noise" starts to make sense.

## Links

 - [Currah uSpeech user guide](https://k1.spdns.de/Vintage/Sinclair/82/Peripherals/Currah%20uSpeech/Manual.pdf)

### Videos

 - [Sinclair ZX Spectrum Currah Microspeech & Sound Output](https://www.youtube.com/watch?v=PdAvMTof0jo)
 - [Commodore 64 (C64) Currah Speech 64 (Voice Messenger) Cart Repair](https://www.youtube.com/watch?v=vUIuqzf1G7I)
 - [Your Spectrum can talk! Let’s look at the Currah Microspeech](https://www.youtube.com/watch?v=UcAVrcGmlvw)
   - Sounds better than the SweetTalker


### Useful links

 - [Currah%20uSpeech](https://k1.spdns.de/Vintage/Sinclair/82/Peripherals/Currah%20uSpeech/)
 - [ZXDocs](https://problemkaputt.de/zxdocs.htm)
 - [currah_uspeech_tests](https://maziac.github.io/currah_uspeech_tests/)
 - [CURRAH MICRO SPEECH (USPEECH)](https://blog.bisinternet.com/index.php/sinclair/zx-spectrum/currah-micro-speech-uspeech/)

### Comparing

 - [hardware speech synthesyzer comparison thread](https://www.vogons.org/viewtopic.php?t=46335)
 - [Talkback: Speech Units Assessed!](https://www.everygamegoing.com/larticle/Talkback-Speech-Units-Assessed-000/35097)
 - [Spectrum Speakers](http://www.users.globalnet.co.uk/~jg27paw4/yr09/yr09_52.htm)

### Images

Two images of the PCB:

 - [Top](https://k1.spdns.de/Vintage/Sinclair/82/Peripherals/Currah%20uSpeech/Currah%20%C2%B5Speech%20-%20open%20(redclash).jpg)
 - [Bottom](https://k1.spdns.de/Vintage/Sinclair/82/Peripherals/Currah%20uSpeech/Currah%20%C2%B5Speech%20-%20PCB%20rear%20side%20(redclash).jpg)

### Emulator for FUSE

[Currah µSpeech emulation](https://sourceforge.net/p/fuse-emulator/patches/142/?page=1)


### ebay

 - [Currah MicroSlot / uSlot - Expansion Port Doubler / Extender - ZX Spectrum Range](https://www.ebay.co.uk/itm/315353994325), £104.65

 - [Currah μSpeech MicroSpeech – Tested Working – ZX Spectrum Speech Unit + Tape](https://www.ebay.co.uk/itm/116894306778), £31.89+£3.71
 - [ZX Spectrum Bundle Includes ZX Printer Currah Speech Synthesiser Joystick Games](https://www.ebay.co.uk/itm/317818350461), £104.70
 - [Sinclair ZX Spectrum Currah Speech And Sound](https://www.ebay.co.uk/itm/177796470984), £37.10

## Notes


Two photos of the PCB, from [currah_uspeech_tests](https://maziac.github.io/currah_uspeech_tests/):

 [![front][1]][1]

 [![rear][2]][2]

It might be possible to derive a partial schematic from the two images.

From [Sinclair ZX Spectrum Currah Microspeech & Sound Output](https://www.youtube.com/watch?v=PdAvMTof0jo):

 - [SP0256-AL2](http://www.bitsavers.org/components/gi/speech/General_Instrument_-_SP0256A-AL2_datasheet_(Radio_Shack_276-1784)_-_Apr1984.pdf)
 - ULA
 - ROM

For the reverse-engineering of the board, please see [Currah µSpeech - reverse engineering](documentation/Currah%20µSpeech%20-%20reverse%20engineering.md).

## Cheetah Sweet Talker

It is also worth considering the Cheetah SweetTalker, which also uses the SP0256-AL2:

 - [Retro Tech Nibble: A Sweet Talking 1983 Micro Computer](https://www.youtube.com/watch?v=H2lNiB58c34)
   - Sounds terrible!
 - [Cheetah Sweet Talker Speech Synthesis Module for the ZX Spectrum](https://www.youtube.com/watch?v=p275k1khzZk)
 - [Sinclair ZX Spectrum 32k Cheetah and Sweet Talker Bundle 1983](https://www.ebay.co.uk/itm/306735764428), £31.89
 - [Sweet talking Beeb](https://chrisacorns.computinghistory.org.uk/docs/Mags/AU/AU_May85_CheetahSweetTalker.pdf) 
 - [Sinclair ZX81 & Spectrum Computers](https://lannerchronicle.wordpress.com/2024/06/05/sinclair-zx81-spectrum-computers/)


The Acorn version of PCB seems more minimalistic than the Currah µSpeech, only two ICs: 

 - [Bottom](https://commons.wikimedia.org/wiki/File:Cheetah_Sweet_talker_(bottom).jpg)
 - [Top](https://chrisacorns.computinghistory.org.uk/8bit_Upgrades/Cheetah_SweetTalkerD.jpg)

[Cheetah Sweet Talker](https://chrisacorns.computinghistory.org.uk/8bit_Upgrades/Cheetah_SweetTalker.html)


Not to be confused with Micro Mint Sweet Talker for the Apple II, which uses the SSI 263.



<!-- Images -->

  [1]: https://k1.spdns.de/Vintage/Sinclair/82/Peripherals/Currah%20uSpeech/Currah%20%C2%B5Speech%20-%20open%20(redclash).jpg "Front"
  [2]: https://k1.spdns.de/Vintage/Sinclair/82/Peripherals/Currah%20uSpeech/Currah%20%C2%B5Speech%20-%20PCB%20rear%20side%20(redclash).jpg "Rear"
