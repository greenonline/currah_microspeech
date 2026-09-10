# Currah µSpeech - ROM reading

## Preamble

Why not try to reverse engineer a Currah µSpeech ROM using an Arduino (Mega)? 

Put the ROM on a breadboard. Connect Arduino digital data pins to all pins:

 - Arduino data lines connected to ROM Address lines configured as outputs
 - Arduino data lines connected to ROM Data lines configured as inputs
 - If available, add three Arduino data lines to the ROM chip select lines, otherwise do manually HIGH and LOW:
   - Pin 18 LOW
   - Pin 20 ???
   - Pin 21 HIGH
 - Cycle through the ROM addresses (0000h - 0800h), outputing on the Arduino data lines connected to the address lines of the ROM
 - Wait 1-2 µS, even though the access time for the 9316C is only 450 nS (max.)
 - Read the ROM data, reading the Arduino data lines connected to the data lines of the ROM


## Links

 - [Unable to read older GI 9316b ROM in programmers - Suggestions?](https://www.eevblog.com/forum/microcontrollers/unable-to-read-older-gi-9316b-rom-in-programmers-suggestions/)
 - [HOW TO READ 9316 ROMS](https://www.mikesarcade.com/cgi-bin/spies.cgi?action=url&type=info&page=9316.txt)
 - [9316B Rom replacement](https://forum.allaboutcircuits.com/threads/9316b-rom-replacement.69569/)

## Notes

### Component identification


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

### Access times

From the [datasheet](https://www.datasheetarchive.com/?q=ro-3-9316b):

|Type|Access time|CS response time|
|----|-----------|----------------|
| A  |   600-850 |      200-300   |
| B  |   350-450 |      100-200   |
| C  |   250-350 |      100-200   |

### Sketch

```none
// Sketch to read 9316C ROM

void init()
{
}

void lopp()
{
}
```



