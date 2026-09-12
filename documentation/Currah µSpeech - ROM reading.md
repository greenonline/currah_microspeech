# Currah µSpeech - ROM reading

## Preamble

Why not try to reverse engineer a Currah µSpeech ROM using an Arduino (Mega)? 

## Process

 - Put the ROM on a breadboard. 
 - Add VCC and GND from the Arduino. 
 - Connect Arduino digital data pins to all pins:

   - Arduino data lines connected to ROM Address lines configured as outputs
   - Arduino data lines connected to ROM Data lines configured as inputs
   - If available, add three Arduino data lines to the ROM chip select lines, otherwise do manually HIGH and LOW:
     - `CS2`: Pin 18 LOW
     - `CS1`: Pin 20 ??? (it turned out that `CS1` is active `LOW`)
     - `CS3`: Pin 21 HIGH
   - Cycle through the ROM addresses (0000h - 0800h), outputing on the Arduino data lines connected to the address lines of the ROM
   - Wait 1-2 µS, even though the access time for the 9316C is only 450 nS (max.)
   - Read the ROM data, reading the Arduino data lines connected to the data lines of the ROM

The same process can be applied to the ULA.

## Fritzing

Note: the 9316 is wider than shown in the digram below. I had to modify an AD5206, which was the only 24 pin DIP that I could find in the [beta version](https://github.com/fritzing/fritzing-app/releases/tag/CD-498) of Fritzing that I was using:

[![Fritzing of the 9316 ROM reader][1]][1]

  [1]: ../xtras/images/9316C_reading_bb2.jpg "Fritzing of the 9316 ROM reader"

## Links

 - [Unable to read older GI 9316b ROM in programmers - Suggestions?](https://www.eevblog.com/forum/microcontrollers/unable-to-read-older-gi-9316b-rom-in-programmers-suggestions/)
 - [HOW TO READ 9316 ROMS](https://www.mikesarcade.com/cgi-bin/spies.cgi?action=url&type=info&page=9316.txt)
 - [9316B Rom replacement](https://forum.allaboutcircuits.com/threads/9316b-rom-replacement.69569/)
 - [Datasheet 9316](https://www.datasheetarchive.com/?q=ro-3-9316b)

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
// ROMread_9316
// Sketch to read 9316C ROM (from Currah µSpeech)

// Delay in microseconds - only really needs to be 1, if at all...
unsigned int delayTime = 50;

// Use bit-shift method for bit detection
#define __USE_BITSHIFT__
// Use bitRead() method for bit detection (causes warning)
//#define __USE_BITREAD__

// Use hex output - one line one byte
//#define __USE_HEX_SINGLE__
// Use hex output - one line eight bytes
#define __USE_HEX_ROW__

// Address lines
int romA0;
int romA1;
int romA2;
int romA3;
int romA4;
int romA5;
int romA6;
int romA7;
int romA8;
int romA9;
int romA10;

// Chip select lines
int romCS1;
int romCS2;
int romCS3;

// Data lines
int romD0;
int romD1;
int romD2;
int romD3;
int romD4;
int romD5;
int romD6;
int romD7;

void setup()
{

  const int kMega = 0;             // Mega
  const int kUno = 1;              // Uno
  const int flgPlatform = kMega;   // Mega

  if (flgPlatform == kMega) {
    // Arduino Mega End bus - start
    // Address lines
    romA0 = 22;
    romA1 = 24;
    romA2 = 26;
    romA3 = 28;
    romA4 = 30;
    romA5 = 32;
    romA6 = 34;
    romA7 = 36;
    romA8 = 38;
    romA9 = 40;
    romA10 = 42;

    // Chip select lines
    romCS1 = 44; //44;
    romCS2 = 46; //46;
    romCS3 = 48; //48;

    // Data lines
    romD0 = 23;
    romD1 = 25;
    romD2 = 27;
    romD3 = 29;
    romD4 = 31;
    romD5 = 33;
    romD6 = 35;
    romD7 = 37;
    // Arduino Mega End bus - end
  }

  if (flgPlatform == kUno) {
    // Arduino Uno - start
    // Address lines
    romA0 = A0;
    romA1 = A1;
    romA2 = A2;
    romA3 = A3;
    romA4 = A4;
    romA5 = A5;
    romA6 = 11;
    romA7 = 12;
    romA8 = 13;
    romA9 = 1;
    romA10 = 2;

    // Chip select lines - on Uno must physically set due to lack of pins
    //romCS1 = 0;  // or 11
    //romCS2 = 1;  // or 12
    //romCS3 = 2;  // or 13

    // Data lines
    romD0 = 3;
    romD1 = 4;
    romD2 = 5;
    romD3 = 6;
    romD4 = 7;
    romD5 = 8;
    romD6 = 9;
    romD7 = 10;
    // Arduino Uno - end
  }

  // Address lines
  pinMode(romA0, OUTPUT);    // A0
  pinMode(romA1, OUTPUT);    // A1
  pinMode(romA2, OUTPUT);    // A2
  pinMode(romA3, OUTPUT);    // A3
  pinMode(romA4, OUTPUT);    // A4
  pinMode(romA5, OUTPUT);    // A5
  pinMode(romA6, OUTPUT);    // A6
  pinMode(romA7, OUTPUT);    // A7
  pinMode(romA8, OUTPUT);    // A8
  pinMode(romA9, OUTPUT);    // A9
  pinMode(romA10, OUTPUT);    // A10

  if (flgPlatform != kUno) {
  // Chip select lines
    pinMode(romCS1, OUTPUT);    // CS1
    pinMode(romCS2, OUTPUT);    // CS2
    pinMode(romCS3, OUTPUT);    // CS3
  }

  // Data lines
  pinMode(romD0, INPUT);     // D0
  pinMode(romD1, INPUT);     // D1
  pinMode(romD2, INPUT);     // D2
  pinMode(romD3, INPUT);     // D3
  pinMode(romD4, INPUT);     // D4
  pinMode(romD5, INPUT);     // D5
  pinMode(romD6, INPUT);     // D6
  pinMode(romD7, INPUT);     // D7

  if (flgPlatform != kUno) {
    // Set ROM chip select lines
    digitalWrite(romCS1, LOW);    // Currah CS1  active LOW
    //digitalWrite(romCS1, HIGH); // To disable chip
    digitalWrite(romCS2, LOW);    // Currah tied to GND
    digitalWrite(romCS3, HIGH);   // Currah tied to VCC
  }

  Serial.begin(9600);
}

void loop()
{
  int byteCount = 1;
  int outByteOld = 0;
  int inByteOld[8] = { -1, -1, -1, -1, -1, -1, -1, -1};

  // Byte to read
  int inD0;
  int inD1;
  int inD2;
  int inD3;
  int inD4;
  int inD5;
  int inD6;
  int inD7;
  int inByte;

#if (!defined __USE_BITREAD__)  &&  !defined(__USE_BITSHIFT__)

  // For old skool method
  int outA0;
  int outA1;
  int outA2;
  int outA3;
  int outA4;
  int outA5;
  int outA6;
  int outA7;
  int outA8;
  int outA9;
  int outA10;

#endif

  // Loop 2^11 times = 0-2047
  for (int outByte = 0; outByte < 2048; outByte++)
  {

#if (!defined __USE_BITREAD__)  &&  !defined(__USE_BITSHIFT__)

    // Old skool method
    outA0 = outByte % 2;
    if (outByte > 1023) {
      outA10 = 1;
      outByte = outByte - 1024;
    }
    if (outByte > 511) {
      outA9 = 1;
      outByte = outByte - 512;
    }
    if (outByte > 255) {
      outA8 = 1;
      outByte = outByte - 256;
    }
    if (outByte > 127) {
      outA7 = 1;
      outByte = outByte - 128;
    }
    if (outByte > 63) {
      outA6 = 1;
      outByte = outByte - 64;
    }
    if (outByte > 31) {
      outA5 = 1;
      outByte = outByte - 32;
    }
    if (outByte > 15) {
      outA4 = 1;
      outByte = outByte - 16;
    }
    if (outByte > 7) {
      outA3 = 1;
      outByte = outByte - 8;
    }
    if (outByte > 3) {
      outA2 = 1;
      outByte = outByte - 4;
    }
    if (outByte > 1) {
      outA2 = 1;
      outByte = outByte - 2;
    }

#endif

#ifdef __USE_BITSHIFT__

    // From https://stackoverflow.com/questions/523724/c-c-check-if-one-bit-is-set-in-i-e-int-variable
    byte outA0 = outByte & (1 << 0);
    byte outA1 = outByte & (1 << 1);
    byte outA2 = outByte & (1 << 2);
    byte outA3 = outByte & (1 << 3);
    byte outA4 = outByte & (1 << 4);
    byte outA5 = outByte & (1 << 5);
    byte outA6 = outByte & (1 << 6);
    byte outA7 = outByte & (1 << 7);
    byte outA8 = outByte & (1 << 8);
    byte outA9 = outByte & (1 << 9);
    byte outA10 = outByte & (1 << 10);

#endif

#ifdef __USE_BITREAD__

    // Causes warning:
    // warning: right shift count >= width of type [-Wshift-count-overflow]
    // ...
    // #define bitRead(value, bit) (((value) >> (bit)) & 0x01)
    // byte outA9 = bitRead(outByte, 89);

    // From [Convert int to binary Array](https://forum.arduino.cc/t/convert-int-to-binary-array/116781/2)
    byte outA0 = bitRead(outByte, 0);
    byte outA1 = bitRead(outByte, 1);
    byte outA2 = bitRead(outByte, 2);
    byte outA3 = bitRead(outByte, 3);
    byte outA4 = bitRead(outByte, 4);
    byte outA5 = bitRead(outByte, 5);
    byte outA6 = bitRead(outByte, 6);
    byte outA7 = bitRead(outByte, 7);
    byte outA8 = bitRead(outByte, 8);
    byte outA9 = bitRead(outByte, 89);
    byte outA10 = bitRead(outByte, 10);

#endif

    digitalWrite(romA0, outA0);
    digitalWrite(romA1, outA1);
    digitalWrite(romA2, outA2);
    digitalWrite(romA3, outA3);
    digitalWrite(romA4, outA4);
    digitalWrite(romA5, outA5);
    digitalWrite(romA6, outA6);
    digitalWrite(romA7, outA7);
    digitalWrite(romA8, outA8);
    digitalWrite(romA9, outA9);
    digitalWrite(romA10, outA10);

    delayMicroseconds(delayTime);  // not really needed

    inD0 = digitalRead(romD0);
    inD1 = digitalRead(romD1);
    inD2 = digitalRead(romD2);
    inD3 = digitalRead(romD3);
    inD4 = digitalRead(romD4);
    inD5 = digitalRead(romD5);
    inD6 = digitalRead(romD6);
    inD7 = digitalRead(romD7);

    inByte = (128 * inD7) + (64 * inD6) + (32 * inD5) + (16 * inD4) + (8 * inD3) + (4 * inD2) + (2 * inD1) + inD0;

#if !defined(__USE_HEX_SINGLE__)  && !defined(__USE_HEX_ROW__)

    Serial.print (outByte);
    Serial.print (" : ");
    Serial.println (inByte);

#endif

#if defined(__USE_HEX_SINGLE__)

    // from https://forum.arduino.cc/t/serial-print-value-hex/463868/5

    Serial.print("0x");
    Serial.print(outByte < 16 ? "0" : "");
    Serial.print(outByte, HEX);
    Serial.print(" : ");
    Serial.print("0x");
    Serial.print(inByte < 16 ? "0" : "");
    Serial.print(inByte, HEX);
    Serial.print(" : ");
    Serial.println (inByte);

#endif

#if defined(__USE_HEX_ROW__)

    if (byteCount == 1) {
      outByteOld = outByte;
    }

    inByteOld[byteCount - 1] = inByte;

    if (byteCount == 8) {
      Serial.print(outByteOld < 4096 ? "0" : "");
      Serial.print(outByteOld < 256 ? "0" : "");
      Serial.print(outByteOld < 16 ? "0" : "");
      Serial.print(outByteOld, HEX);
      Serial.print(" : ");
      for (int n = 0; n < 8; n++) {
        Serial.print(inByteOld[n] < 16 ? "0" : "");
        Serial.print(inByteOld[n], HEX);
        Serial.print(" ");
        inByteOld[n] = -1;  // clear old value
      }
      Serial.println();
      byteCount = 0;
    }
    byteCount++;

#endif

  }
}
```

Also, in [ROMread_9316.ino](../xtras/ROMread_9316.ino)

### ROM Contents

```none
0000 : A5 1E BF 2A 2F 10 5D 44 
0008 : 00 05 3E EB 00 0F AF 98 
0010 : 06 06 0B 08 65 05 61 1C 
0018 : 2B 41 A5 67 7D 5F 22 E8 
0020 : 61 0C 02 DB 60 3F 04 9F 
0028 : 40 4A 00 D3 F8 3F D8 D3 
0030 : 42 68 57 40 66 E8 C4 FB 
0038 : 01 68 72 29 01 67 4B 66 
0040 : 00 0F 90 61 FF F0 4C 44 
0048 : 57 60 40 6C D0 D5 0D 60 
0050 : DF 8B 4B 66 68 00 CA CF 
0058 : 64 C4 E5 D0 09 0A 0E 0A 
0060 : 61 0C 02 DB 60 3F 04 9F 
0068 : DA 7F EB DA 66 96 01 F8 
0070 : E4 1F 6A 04 2D 08 63 1A 
0078 : EE 05 62 85 07 09 62 85 
0080 : 1E 1F 0E 2F 41 20 AF 09 
0088 : DA 40 60 F8 6D 1E 49 09 
0090 : 0A 68 DA 67 8E 41 09 3D 
0098 : 47 C4 6A E8 09 6F 0A 09 
00A0 : 22 DA 2F 60 E7 DB 61 15 
00A8 : D0 DB 6F D8 62 F8 21 61 
00B0 : 61 E8 00 08 66 4B 00 FF 
00B8 : 70 67 00 0F 18 06 00 00 
00C0 : 00 2D 72 EB 1E 03 9C D3 
00C8 : DA 40 60 F8 6D 1E 49 09 
00D0 : 2F 4F 91 72 49 2B C4 B1 
00D8 : 74 49 63 1A 67 67 68 45 
00E0 : 61 06 65 07 1E 66 3A 14 
00E8 : 1E 3F 7D 57 09 43 4B 04 
00F0 : 84 3A 00 10 62 67 00 00 
00F8 : 2F 45 00 00 63 0C FF F0 
0100 : A5 1E BF 2A 2F 22 BF 08 
0108 : 00 05 3E EB 00 0F AF 98 
0110 : 06 06 0B 08 65 05 61 1C 
0118 : 2B 41 A5 67 7D 5F 22 E8 
0120 : 61 0C 02 DB 60 3F 04 9F 
0128 : 40 4A 00 D3 F8 3F D8 D3 
0130 : 42 68 57 40 66 E8 C4 FB 
0138 : 01 68 72 29 01 67 4B 66 
0140 : 00 0F 90 61 FF F0 4C 44 
0148 : 57 60 40 6C D0 D5 0D 60 
0150 : DF 8B 4B 66 68 00 CA CF 
0158 : 64 C4 E5 D0 09 0A 0E 0A 
0160 : 61 0C 02 DB 60 3F 04 9F 
0168 : DA 7F EB DA 66 96 01 F8 
0170 : E4 1F 6A 04 2D 08 63 1A 
0178 : EE 05 62 85 07 09 62 85 
0180 : 1E 1F 0E 2F 41 20 AF 09 
0188 : DA 40 60 F8 6D 1E 49 09 
0190 : 2F 4F 91 72 49 2B C4 B1 
0198 : 47 C4 6A E8 09 6F 0A 09 
01A0 : 22 DA 2F 60 E7 DB 61 15 
01A8 : D0 DB 6F D8 62 F8 21 61 
01B0 : 61 E8 00 08 66 4B 00 FF 
01B8 : 70 67 00 0F 18 06 00 00 
01C0 : 00 2D 72 EB 1E 03 9C D3 
01C8 : DA 40 60 F8 6D 1E 49 09 
01D0 : 2F 4F 91 72 49 2B C4 B1 
01D8 : 74 49 63 1A 67 67 68 45 
01E0 : 61 06 65 07 1E 66 3A 14 
01E8 : 1E 3F 7D 57 09 43 4B 04 
01F0 : 84 3A 00 10 62 67 00 00 
01F8 : 2F 45 00 00 63 0C FF F0 
0200 : A5 1E BF 2A 2F 22 BF 08 
0208 : 00 05 3E EB 00 0F AF 98 
0210 : 06 06 0B 08 65 05 61 1C 
0218 : 2B 41 A5 67 7D 5F 22 E8 
0220 : 61 0C 02 DB 60 3F 04 9F 
0228 : 40 4A 00 D3 F8 3F D8 D3 
0230 : 42 68 57 40 66 E8 C4 FB 
0238 : 01 68 72 29 01 67 4B 66 
0240 : 00 0F 90 61 FF F0 4C 44 
0248 : 57 60 40 6C D0 D5 0D 60 
0250 : DF 8B 4B 66 68 00 CA CF 
0258 : 64 C4 E5 D0 09 0A 0E 0A 
0260 : 61 0C 02 DB 60 3F 04 9F 
0268 : DA 7F EB DA 66 96 01 F8 
0270 : E4 1F 6A 04 2D 08 63 1A 
0278 : EE 05 62 85 07 09 62 85 
0280 : 1E 1F 0E 2F 41 20 AF 09 
0288 : DA 40 60 F8 6D 1E 49 09 
0290 : 0A 68 DA 67 49 2B C4 B1 
0298 : 47 C4 6A E8 09 6F 0A 09 
02A0 : 22 DA 2F 60 E7 DB 61 15 
02A8 : 1E 3F 7D 57 09 43 4B 04 
02B0 : 61 E8 00 08 66 4B 00 FF 
02B8 : 70 67 00 0F 18 06 00 00 
02C0 : 00 2D 72 EB 1E 03 9C D3 
02C8 : DA 40 60 F8 6D 1E 49 09 
02D0 : 2F 4F 91 72 49 2B C4 B1 
02D8 : 74 49 63 1A 67 67 68 45 
02E0 : 61 06 65 07 1E 66 3A 14 
02E8 : 1E 3F 7D 57 09 43 4B 04 
02F0 : 84 3A 00 10 62 67 00 00 
02F8 : 2F 45 00 00 63 0C FF F0 
0300 : A5 1E BF 2A 2F 22 BF 08 
0308 : 00 05 3E EB 00 0F AF 98 
0310 : 06 06 0B 08 65 05 61 1C 
0318 : 2B 41 A5 67 7D 5F 22 E8 
0320 : F8 B3 D1 D0 6C BF 09 61 
0328 : 40 4A 00 D3 F8 3F D8 D3 
0330 : 42 68 57 40 66 E8 C4 FB 
0338 : 01 68 72 29 01 67 4B 66 
0340 : 00 0F 90 61 FF F0 4C 44 
0348 : 57 60 40 6C D0 D5 0D 60 
0350 : DF 8B 4B 66 68 00 CA CF 
0358 : 64 C4 E5 D0 09 0A 0E 0A 
0360 : 61 0C 02 DB 60 3F 04 9F 
0368 : DA 7F EB DA 66 96 01 F8 
0370 : E4 1F 6A 04 2D 08 63 1A 
0378 : EE 05 62 85 07 09 62 85 
0380 : 1E 1F 0E 2F 41 20 AF 09 
0388 : DA 40 60 F8 6D 1E 49 09 
0390 : 0A 68 DA 67 8E 41 09 3D 
0398 : 47 C4 6A E8 09 6F 0A 09 
03A0 : 61 06 65 07 1E 66 3A 14 
03A8 : D0 DB 6F D8 62 F8 21 61 
03B0 : 61 E8 00 08 66 4B 00 FF 
03B8 : 70 67 00 0F 18 06 00 00 
03C0 : 00 2D 72 EB 1E 03 9C D3 
03C8 : DA 40 60 F8 6D 1E 49 09 
03D0 : 2F 4F 91 72 49 2B C4 B1 
03D8 : 74 49 63 1A 67 67 68 45 
03E0 : 61 06 65 07 1E 66 3A 14 
03E8 : 1E 3F 7D 57 09 43 4B 04 
03F0 : 84 3A 00 10 62 67 00 00 
03F8 : 2F 45 00 00 63 0C FF F0 
0400 : 00 0F 90 61 FF F0 4C 44 
0408 : 00 05 3E EB 00 0F AF 98 
0410 : 06 06 0B 08 65 05 61 1C 
0418 : 2B 41 A5 67 7D 5F 22 E8 
0420 : F8 B3 D1 D0 6C BF 09 61 
0428 : 40 4A 00 D3 F8 3F D8 D3 
0430 : 42 68 57 40 66 E8 C4 FB 
0438 : 01 68 72 29 01 67 4B 66 
0440 : 00 0F 90 61 FF F0 4C 44 
0448 : 57 60 40 6C D0 D5 0D 60 
0450 : DF 8B 4B 66 68 00 CA CF 
0458 : 64 C4 E5 D0 09 0A 0E 0A 
0460 : 61 0C 02 DB 60 3F 04 9F 
0468 : DA 7F EB DA 66 96 01 F8 
0470 : E4 1F 6A 04 2D 08 63 1A 
0478 : EE 05 62 85 07 09 62 85 
0480 : 1E 1F 0E 2F 41 20 AF 09 
0488 : DA 40 60 F8 6D 1E 49 09 
0490 : 0A 68 DA 67 8E 41 09 3D 
0498 : 47 C4 6A E8 09 6F 0A 09 
04A0 : 61 06 65 07 1E 66 3A 14 
04A8 : D0 DB 6F D8 62 F8 21 61 
04B0 : 61 E8 00 08 66 4B 00 FF 
04B8 : 70 67 00 0F 18 06 00 00 
04C0 : 00 2D 72 EB 1E 03 9C D3 
04C8 : DA 40 60 F8 6D 1E 49 09 
04D0 : 2F 4F 91 72 49 2B C4 B1 
04D8 : 74 49 63 1A 67 67 68 45 
04E0 : 61 06 65 07 1E 66 3A 14 
04E8 : 1E 3F 7D 57 09 43 4B 04 
04F0 : 84 3A 00 10 62 67 00 00 
04F8 : 2F 45 00 00 63 0C FF F0 
0500 : 00 0F 90 61 FF F0 4C 44 
0508 : 00 05 3E EB 00 0F AF 98 
0510 : 06 06 0B 08 65 05 61 1C 
0518 : 2B 41 A5 67 7D 5F 22 E8 
0520 : F8 B3 D1 D0 6C BF 09 61 
0528 : 40 4A 00 D3 F8 3F D8 D3 
0530 : 42 68 57 40 66 E8 C4 FB 
0538 : 01 68 72 29 01 67 4B 66 
0540 : 00 0F 90 61 FF F0 4C 44 
0548 : 57 60 40 6C D0 D5 0D 60 
0550 : DF 8B 4B 66 68 00 CA CF 
0558 : 64 C4 E5 D0 09 0A 0E 0A 
0560 : 61 0C 02 DB 60 3F 04 9F 
0568 : DA 7F EB DA 66 96 01 F8 
0570 : E4 1F 6A 04 2D 08 63 1A 
0578 : EE 05 62 85 07 09 62 85 
0580 : 1E 1F 0E 2F 41 20 AF 09 
0588 : DA 40 60 F8 6D 1E 49 09 
0590 : 0A 68 DA 67 8E 41 09 3D 
0598 : 47 C4 6A E8 09 6F 0A 09 
05A0 : 61 06 65 07 1E 66 3A 14 
05A8 : D0 DB 6F D8 62 F8 21 61 
05B0 : 61 E8 00 08 66 4B 00 FF 
05B8 : 70 67 00 0F 18 06 00 00 
05C0 : 00 2D 72 EB 1E 03 9C D3 
05C8 : DA 40 60 F8 6D 1E 49 09 
05D0 : 2F 4F 91 72 49 2B C4 B1 
05D8 : 74 49 63 1A 67 67 68 45 
05E0 : 61 06 65 07 1E 66 3A 14 
05E8 : 1E 3F 7D 57 09 43 4B 04 
05F0 : 84 3A 00 10 62 67 00 00 
05F8 : 2F 45 00 00 63 0C FF F0 
0600 : 00 0F 90 61 FF F0 4C 44 
0608 : 00 05 3E EB 00 0F AF 98 
0610 : 06 06 0B 08 65 05 61 1C 
0618 : 2B 41 A5 67 7D 5F 22 E8 
0620 : 61 0C 02 D1 6C BF 09 61 
0628 : 40 4A 00 D3 F8 3F D8 D3 
0630 : 42 68 57 40 66 E8 C4 FB 
0638 : 01 68 72 29 01 67 4B 66 
0640 : 00 0F 90 61 FF F0 4C 44 
0648 : 57 60 40 6C D0 D5 0D 60 
0650 : DF 8B 4B 66 68 00 CA CF 
0658 : 64 C4 E5 D0 09 0A 0E 0A 
0660 : 61 0C 02 DB 60 3F 04 9F 
0668 : DA 7F EB DA 66 96 01 F8 
0670 : E4 1F 6A 04 2D 08 63 1A 
0678 : EE 05 62 85 07 09 62 85 
0680 : 1E 1F 0E 2F 41 20 AF 09 
0688 : DA 40 60 F8 6D 1E 49 09 
0690 : 0A 68 DA 67 8E 41 09 3D 
0698 : 47 C4 6A E8 09 6F 0A 09 
06A0 : 61 06 65 07 1E 66 3A 14 
06A8 : D0 DB 6F D8 62 F8 21 61 
06B0 : 61 E8 00 08 66 4B 00 FF 
06B8 : 70 67 00 0F 18 06 00 00 
06C0 : 00 2D 72 EB 1E 03 9C D3 
06C8 : DA 40 60 F8 6D 1E 49 09 
06D0 : 2F 4F 91 72 49 2B C4 B1 
06D8 : 74 49 63 1A 67 67 68 45 
06E0 : 61 06 65 07 1E 66 3A 14 
06E8 : 1E 3F 7D 57 09 43 4B 04 
06F0 : 84 3A 00 10 62 67 00 00 
06F8 : 2F 45 00 00 63 0C FF F0 
0700 : A5 1E 90 61 FF F0 4C 44 
0708 : 00 05 3E EB 00 0F AF 98 
0710 : 06 06 0B 08 65 05 61 1C 
0718 : 2B 41 A5 67 7D 5F 22 E8 
0720 : 61 0C 02 DB 60 3F 04 9F 
0728 : 40 4A 00 D3 F8 3F D8 D3 
0730 : 42 68 57 40 66 E8 C4 FB 
0738 : 01 68 72 29 01 67 4B 66 
0740 : 00 0F 90 61 FF F0 4C 44 
0748 : 57 60 40 6C D0 D5 0D 60 
0750 : DF 8B 4B 66 68 00 CA CF 
0758 : 64 C4 E5 D0 09 0A 0E 0A 
0760 : 61 0C 02 DB 60 3F 04 9F 
0768 : DA 7F EB DA 66 96 01 F8 
0770 : E4 1F 6A 04 2D 08 63 1A 
0778 : EE 05 62 85 07 09 62 85 
0780 : 1E 1F 0E 2F 41 20 AF 09 
0788 : 29 A5 60 2A C9 24 DA 40 
0790 : 08 68 DA 67 8E 41 09 3D 
0798 : 47 C4 6A E8 09 6F 0A 09 
07A0 : 22 DA 2F 60 E7 DB 61 15 
07A8 : D0 DB 6F D8 62 F8 21 61 
07B0 : 61 E8 00 08 66 4B 00 FF 
07B8 : 70 67 00 0F 18 06 00 00 
07C0 : 00 2D 72 EB 1E 03 9C D3 
07C8 : DA 40 60 F8 6D 1E 49 09 
07D0 : 2F 4F 91 72 49 2B C4 B1 
07D8 : 74 49 63 1A 67 67 68 45 
07E0 : 61 06 65 07 1E 66 3A 14 
07E8 : 1E 3F 7D 57 09 43 4B 04 
07F0 : 84 3A 00 10 62 67 00 00 
07F8 : 2F 45 00 00 63 0C FF F0 
```

Also, in [ROM.txt](../xtras/ROM.txt)

### Disassemble

Use this:

 - [z80dismblr](https://github.com/maziac/z80dismblr)

The ROM file needs to be in  `SNA` format, or a binary `.bin` file.

#### BIN file

Python script to adapt:

```none
# Create an array of bytes you want in your ROM
# Example: 16 Kilobytes filled with 0xFF (often used as padding)
rom_size = 2 * 1024
data = bytearray([0xFF] * rom_size)

# Insert your custom data or machine instructions at specific offsets
data[0] = 0x41  # 'A'
data[1] = 0x42  # 'B' (An example custom header)

# Write the data to a .bin file
with open("my_custom_rom.bin", "wb") as f:
    f.write(data)
```

This script creates a binary file:


```none
import re

#hexaPattern = re.compile(r'\s([0-9a-fA-F]+))?\s')
hexaPattern = re.compile(r'([0-9a-fA-F]{2})\s([0-9a-fA-F]{2})\s([0-9a-fA-F]{2})\s([0-9a-fA-F]{2})\s([0-9a-fA-F]{2})\s([0-9a-fA-F]{2})\s([0-9a-fA-F]{2})\s([0-9a-fA-F]{2})\s')

# Create an array of bytes you want in your ROM
# Example: 16 Kilobytes filled with 0xFF (often used as padding)
rom_size = 2 * 1024
data = bytearray([0xFF] * rom_size)

# Read the ROM text file
count = 0
# https://stackoverflow.com/questions/9282967/how-to-open-a-file-using-the-open-with-statement
with open("rom.txt", "rt") as infile:
    #f.read(line)
    for line in infile:
        # https://stackoverflow.com/questions/10270407/regular-expression-for-hexadecimal-string-in-python-not-working
        m = re.search(hexaPattern, line)
        if m:
           print("found a match:", m.group(1), m.group(2), m.group(3), m.group(4), m.group(5), m.group(6), m.group(7), m.group(8))
           shortline = m.group(1)+ m.group(2)+ m.group(3)+ m.group(4)+ m.group(5)+ m.group(6)+ m.group(7)+ m.group(8)
           print("shortline:", shortline)

     
        # from https://stackoverflow.com/questions/5649407/how-to-convert-hexadecimal-string-to-bytes-in-python
        bytes = bytearray.fromhex(shortline)  # remove the address from the start of the line first?
        data[count] = bytes[0]
        data[count+1] = bytes[1]
        data[count+2] = bytes[2]
        data[count+3] = bytes[3]
        data[count+4] = bytes[4]
        data[count+5] = bytes[5]
        data[count+6] = bytes[6]
        data[count+7] = bytes[7]
        count = count + 8

# Insert your custom data or machine instructions at specific offsets
#data[0] = 0x41  # 'A'
#data[1] = 0x42  # 'B' (An example custom header)

# Write the data to a .bin file
with open("rom.bin", "wb") as f:
    f.write(data)
```

Python script available here, [tobin.py](../xtras/tobin.py)

Binary file available here, [rom.bin](../xtras/rom.bin)

### Disassembly for real

```none
./z80dismblr-macos --bin 0 rom.bin --codelabel 0x000 MAIN_START --out roms.list
```

gives

```none
; EQU:
; Data addresses used by the opcodes that point to uninitialized memory areas.
SUB02:       equ  0840h	; 2112. Subroutine. Called by: SUB01[078Eh].
DATA1:       equ  1000h	; 4096. Data accessed by: 00F1h(in RST36), 02F1h(in SUB01), 01F1h(in RST36), 03F1h(in SUB01), 04F1h(in SUB01), 05F1h(in SUB01), 06F1h(in SUB01), 07F1h(in SUB01)
DATA2:       equ  102Fh	; 4143. Data accessed by: 0003h(in MAIN_START)
DATA3:       equ  1E14h	; 7700. Data accessed by: 00E6h(in RST36), 02E6h(in SUB01), 01E6h(in RST36), 03E6h(in SUB01), 04E6h(in SUB01), 05E6h(in SUB01), 06E6h(in SUB01), 07E6h(in SUB01)
DATA4:       equ  222Fh	; 8751. Data accessed by: 0203h(in SUB01), 0103h(in RST36), 0303h(in SUB01)
DATA5:       equ  24C9h	; 9417. Data accessed by: 078Bh(in SUB01)
DATA6:       equ  2FDAh	; 12250. Data accessed by: 00A0h(in RST36), 02A0h(in SUB01), 01A0h(in RST36), 07A0h(in SUB01)
SUB03:       equ  47B1h	; 18353. Subroutine. Called by: SUB01[0296h], RST36[0196h].
SUB04:       equ  4967h	; 18791. Subroutine. Called by: SUB01[0292h].
SUB05:       equ  6040h	; 24640. Subroutine. Called by: RST36[0088h], SUB01[0288h], RST36[0188h], SUB01[0388h], SUB01[0488h], SUB01[0588h], SUB01[0688h].
DATA7:       equ  61E8h	; 25064. Data accessed by: 001Eh(in RST1E), 021Eh(in SUB01), 011Eh(in RST36), 061Eh(in SUB01), 071Eh(in SUB01)
SUB06:       equ  64CFh	; 25807. Subroutine. Called by: RST36[0056h], SUB01[0256h], RST36[0156h], SUB01[0356h], SUB01[0456h], SUB01[0556h], SUB01[0656h], SUB01[0756h].
SUB07:       equ  74B1h	; 29873. Subroutine. Called by: RST36[00D6h], SUB01[02D6h], RST36[01D6h], SUB01[03D6h], SUB01[04D6h], SUB01[05D6h], SUB01[06D6h], SUB01[07D6h].
SUB08:       equ  8E67h	; 36455. Subroutine. Called by: RST36[0092h], SUB01[0392h], SUB01[0492h], SUB01[0592h], SUB01[0692h], SUB01[0792h].
SUB09:       equ  9666h	; 38502. Subroutine. Called by: RST36[006Bh], SUB01[026Bh], RST36[016Bh], SUB01[036Bh], SUB01[046Bh], SUB01[056Bh], SUB01[066Bh], SUB01[076Bh].
DATA8:       equ  D014h	; 53268. Data accessed by: 03A6h(in SUB01), 04A6h(in SUB01), 05A6h(in SUB01), 06A6h(in SUB01)
SUB10:       equ  D0E5h	; 53477. Subroutine. Called by: RST36[0059h], SUB01[0259h], RST36[0159h], SUB01[0359h], SUB01[0459h], SUB01[0559h], SUB01[0659h], SUB01[0759h].
SUB11:       equ  E86Ah	; 59498. Subroutine. Called by: RST36[0099h], SUB01[0299h], RST36[0199h], SUB01[0399h], SUB01[0499h], SUB01[0599h], SUB01[0699h], SUB01[0799h].
SUB12:       equ  EB7Fh	; 60287. Subroutine. Called by: RST36[0068h], SUB01[0268h], RST36[0168h], SUB01[0368h], SUB01[0468h], SUB01[0568h], SUB01[0668h], SUB01[0768h].
DATA9:       equ  F8E8h	; 63720. Data accessed by: 031Eh(in SUB01), 041Eh(in SUB01), 051Eh(in SUB01)


             org 0000h; 0000h


; Subroutine: Size=24, CC=1.
; Called by: -
; Calls: -
0000 MAIN_START:
0000              and  l      
0001              ld   e,BFh  	; 191,  -65
0003              ld   hl,(DATA2) 	; 102Fh
0006              ld   e,l    
0007              ld   b,h    
0008              nop         
0009              dec  b      
000A              ld   a,EBh  	; 235,  -21
000C              nop         
000D              rrca        
000E              xor  a      
000F              sbc  a,b    
0010              ld   b,06h  	; 6
0012              dec  bc     
0013              ex   af,af' 
0014              ld   h,l    
0015              dec  b      
0016              ld   h,c    
0017              inc  e      


; Restart: Size=6, CC=1.
; Called by: RST36[0050h], SUB01[0250h], RST36[0150h], SUB01[0350h], SUB01[0450h], SUB01[0550h], SUB01[0650h], SUB01[0750h].
; Calls: -
0018 RST18:
0018              dec  hl     
0019              ld   b,c    
001A              and  l      
001B              ld   h,a    
001C              ld   a,l    
001D              ld   e,a    


; Restart: Size=24, CC=3.
; Called by: RST36[00A4h], SUB01[02A4h], RST36[01A4h], SUB01[07A4h].
; Calls: -
001E RST1E:
001E              ld   (DATA7),hl 	; 61E8h


0021              inc  c      
0022              ld   (bc),a 
0023              in   a,(0060h) 	; 96
0025              ccf         
0026              inc  b      
0027              sbc  a,a    
0028              ld   b,b    
0029              ld   c,d    
002A              nop         
002B              out  (00F8h),a 	; 248
002D              ccf         
002E              ret  c      
002F              out  (0042h),a 	; 66
0031              ld   l,b    
0032              ld   d,a    
0033              ld   b,b    
0034              ld   h,(hl) 
0035              ret  pe     


; Restart: Recursive, Size=441, CC=40.
; Called by: self[0044h], self[00B7h], SUB01[01FEh], SUB01[0244h], SUB01[02B7h], self[00FEh], self[0144h], self[01B7h], SUB01[02FEh], SUB01[0344h], SUB01[03B7h], SUB01[03FEh], SUB01[0404h], SUB01[0444h], SUB01[04B7h], SUB01[04FEh], SUB01[0504h], SUB01[0544h], SUB01[05B7h], SUB01[05FEh], SUB01[0604h], SUB01[0644h], SUB01[06B7h], SUB01[06FEh], SUB01[0704h], SUB01[0744h], SUB01[07B7h], SUB01[07FEh].
; Calls: RST18, RST36, SUB01, SUB03, SUB05, SUB06, SUB07, SUB08, SUB09, SUB10, SUB11, SUB12, RST1E.
0036 RST36:
0036              call nz,SUB01 	; 01FBh
0039              ld   l,b    
003A              ld   (hl),d 
003B              add  hl,hl  
003C              ld   bc,4B67h 	; 19303
003F              ld   h,(hl) 
0040              nop         
0041              rrca        
0042              sub  b      
0043              ld   h,c    
0044              rst  38h    
0045              ret  p      
0046              ld   c,h    
0047              ld   b,h    
0048              ld   d,a    
0049              ld   h,b    
004A              ld   b,b    
004B              ld   l,h    
004C              ret  nc     
004D              push de     
004E              dec  c      
004F              ld   h,b    
0050              rst  18h    
0051              adc  a,e    
0052              ld   c,e    
0053              ld   h,(hl) 
0054              ld   l,b    
0055              nop         
0056              jp   z,SUB06 	; 64CFh
0059              call nz,SUB10 	; D0E5h
005C              add  hl,bc  
005D              ld   a,(bc) 
005E              ld   c,0Ah  	; 10
0060              ld   h,c    
0061              inc  c      
0062              ld   (bc),a 
0063              in   a,(0060h) 	; 96
0065              ccf         
0066              inc  b      
0067              sbc  a,a    
0068              jp   c,SUB12 	; EB7Fh
006B              jp   c,SUB09 	; 9666h
006E              ld   bc,E4F8h 	; 58616,  -6920
0071              rra         
0072              ld   l,d    
0073              inc  b      
0074              dec  l      
0075              ex   af,af' 
0076              ld   h,e    
0077              ld   a,(de) 
0078              xor  05h    	; 5
007A              ld   h,d    
007B              add  a,l    
007C              rlca        
007D              add  hl,bc  
007E              ld   h,d    
007F              add  a,l    
0080              ld   e,1Fh  	; 31
0082              ld   c,2Fh  	; 47, '/'
0084              ld   b,c    
0085              jr   nz,RST36 	; 0036h
0087              add  hl,bc  
0088              jp   c,SUB05 	; 6040h
008B              ret  m      
008C              ld   l,l    
008D              ld   e,49h  	; 73, 'I'
008F              add  hl,bc  
0090              ld   a,(bc) 
0091              ld   l,b    
0092              jp   c,SUB08 	; 8E67h
0095              ld   b,c    
0096              add  hl,bc  
0097              dec  a      
0098              ld   b,a    
0099              call nz,SUB11 	; E86Ah
009C              add  hl,bc  
009D              ld   l,a    
009E              ld   a,(bc) 
009F              add  hl,bc  
00A0              ld   (DATA6),hl 	; 2FDAh
00A3              ld   h,b    
00A4              rst  20h    
00A5              in   a,(0061h) 	; 97
00A7              dec  d      
00A8              ret  nc     
00A9              in   a,(006Fh) 	; 111
00AB              ret  c      
00AC              ld   h,d    
00AD              ret  m      
00AE              ld   hl,6161h 	; 24929
00B1              ret  pe     
00B2              nop         
00B3              ex   af,af' 
00B4              ld   h,(hl) 
00B5              ld   c,e    
00B6              nop         
00B7              rst  38h    
00B8              ld   (hl),b 
00B9              ld   h,a    
00BA              nop         
00BB              rrca        
00BC              jr   .rst36_l1 	; 00C4h


00BE              defb 00h    	; 0
00BF              defb 00h    	; 0
00C0              defb 00h    	; 0
00C1              defb 2Dh    	; 45, '-'
00C2              defb 72h    	; 114, 'r'
00C3              defb EBh    	; 235,  -21


00C4 .rst36_l1:
00C4              ld   e,03h  	; 3
00C6              sbc  a,h    
00C7              out  (00DAh),a 	; 218
00C9              ld   b,b    
00CA              ld   h,b    
00CB              ret  m      
00CC              ld   l,l    
00CD              ld   e,49h  	; 73, 'I'
00CF              add  hl,bc  
00D0              cpl         
00D1              ld   c,a    
00D2              sub  c      
00D3              ld   (hl),d 
00D4              ld   c,c    
00D5              dec  hl     
00D6              call nz,SUB07 	; 74B1h
00D9              ld   c,c    
00DA              ld   h,e    
00DB              ld   a,(de) 
00DC              ld   h,a    
00DD              ld   h,a    
00DE              ld   l,b    
00DF              ld   b,l    
00E0              ld   h,c    
00E1              ld   b,65h  	; 101, 'e'
00E3              rlca        
00E4              ld   e,66h  	; 102, 'f'
00E6              ld   a,(DATA3) 	; 1E14h
00E9              ccf         
00EA              ld   a,l    
00EB              ld   d,a    
00EC              add  hl,bc  
00ED              ld   b,e    
00EE              ld   c,e    
00EF              inc  b      
00F0              add  a,h    
00F1              ld   a,(DATA1) 	; 1000h
00F4              ld   h,d    
00F5              ld   h,a    
00F6              nop         
00F7              nop         
00F8              cpl         
00F9              ld   b,l    
00FA              nop         
00FB              nop         
00FC              ld   h,e    
00FD              inc  c      
00FE              rst  38h    
00FF              ret  p      
0100              and  l      
0101              ld   e,BFh  	; 191,  -65
0103              ld   hl,(DATA4) 	; 222Fh
0106              cp   a      
0107              ex   af,af' 
0108              nop         
0109              dec  b      
010A              ld   a,EBh  	; 235,  -21
010C              nop         
010D              rrca        
010E              xor  a      
010F              sbc  a,b    
0110              ld   b,06h  	; 6
0112              dec  bc     
0113              ex   af,af' 
0114              ld   h,l    
0115              dec  b      
0116              ld   h,c    
0117              inc  e      
0118              dec  hl     
0119              ld   b,c    
011A              and  l      
011B              ld   h,a    
011C              ld   a,l    
011D              ld   e,a    
011E              ld   (DATA7),hl 	; 61E8h
0121              inc  c      
0122              ld   (bc),a 
0123              in   a,(0060h) 	; 96
0125              ccf         
0126              inc  b      
0127              sbc  a,a    
0128              ld   b,b    
0129              ld   c,d    
012A              nop         
012B              out  (00F8h),a 	; 248
012D              ccf         
012E              ret  c      
012F              out  (0042h),a 	; 66
0131              ld   l,b    
0132              ld   d,a    
0133              ld   b,b    
0134              ld   h,(hl) 
0135              ret  pe     
0136 .rst36_loop:
0136              call nz,SUB01 	; 01FBh
0139              ld   l,b    
013A              ld   (hl),d 
013B              add  hl,hl  
013C              ld   bc,4B67h 	; 19303
013F              ld   h,(hl) 
0140              nop         
0141              rrca        
0142              sub  b      
0143              ld   h,c    
0144              rst  38h    
0145              ret  p      
0146              ld   c,h    
0147              ld   b,h    
0148              ld   d,a    
0149              ld   h,b    
014A              ld   b,b    
014B              ld   l,h    
014C              ret  nc     
014D              push de     
014E              dec  c      
014F              ld   h,b    
0150              rst  18h    
0151              adc  a,e    
0152              ld   c,e    
0153              ld   h,(hl) 
0154              ld   l,b    
0155              nop         
0156              jp   z,SUB06 	; 64CFh
0159              call nz,SUB10 	; D0E5h
015C              add  hl,bc  
015D              ld   a,(bc) 
015E              ld   c,0Ah  	; 10
0160              ld   h,c    
0161              inc  c      
0162              ld   (bc),a 
0163              in   a,(0060h) 	; 96
0165              ccf         
0166              inc  b      
0167              sbc  a,a    
0168              jp   c,SUB12 	; EB7Fh
016B              jp   c,SUB09 	; 9666h
016E              ld   bc,E4F8h 	; 58616,  -6920
0171              rra         
0172              ld   l,d    
0173              inc  b      
0174              dec  l      
0175              ex   af,af' 
0176              ld   h,e    
0177              ld   a,(de) 
0178              xor  05h    	; 5
017A              ld   h,d    
017B              add  a,l    
017C              rlca        
017D              add  hl,bc  
017E              ld   h,d    
017F              add  a,l    
0180              ld   e,1Fh  	; 31
0182              ld   c,2Fh  	; 47, '/'
0184              ld   b,c    
0185              jr   nz,.rst36_loop 	; 0136h
0187              add  hl,bc  
0188              jp   c,SUB05 	; 6040h
018B              ret  m      
018C              ld   l,l    
018D              ld   e,49h  	; 73, 'I'
018F              add  hl,bc  
0190              cpl         
0191              ld   c,a    
0192              sub  c      
0193              ld   (hl),d 
0194              ld   c,c    
0195              dec  hl     
0196              call nz,SUB03 	; 47B1h
0199              call nz,SUB11 	; E86Ah
019C              add  hl,bc  
019D              ld   l,a    
019E              ld   a,(bc) 
019F              add  hl,bc  
01A0              ld   (DATA6),hl 	; 2FDAh
01A3              ld   h,b    
01A4              rst  20h    
01A5              in   a,(0061h) 	; 97
01A7              dec  d      
01A8              ret  nc     
01A9              in   a,(006Fh) 	; 111
01AB              ret  c      
01AC              ld   h,d    
01AD              ret  m      
01AE              ld   hl,6161h 	; 24929
01B1              ret  pe     
01B2              nop         
01B3              ex   af,af' 
01B4              ld   h,(hl) 
01B5              ld   c,e    
01B6              nop         
01B7              rst  38h    
01B8              ld   (hl),b 
01B9              ld   h,a    
01BA              nop         
01BB              rrca        
01BC              jr   .rst36_l2 	; 01C4h


01BE              defb 00h    	; 0
01BF              defb 00h    	; 0
01C0              defb 00h    	; 0
01C1              defb 2Dh    	; 45, '-'
01C2              defb 72h    	; 114, 'r'
01C3              defb EBh    	; 235,  -21


01C4 .rst36_l2:
01C4              ld   e,03h  	; 3
01C6              sbc  a,h    
01C7              out  (00DAh),a 	; 218
01C9              ld   b,b    
01CA              ld   h,b    
01CB              ret  m      
01CC              ld   l,l    
01CD              ld   e,49h  	; 73, 'I'
01CF              add  hl,bc  
01D0              cpl         
01D1              ld   c,a    
01D2              sub  c      
01D3              ld   (hl),d 
01D4              ld   c,c    
01D5              dec  hl     
01D6              call nz,SUB07 	; 74B1h
01D9              ld   c,c    
01DA              ld   h,e    
01DB              ld   a,(de) 
01DC              ld   h,a    
01DD              ld   h,a    
01DE              ld   l,b    
01DF              ld   b,l    
01E0              ld   h,c    
01E1              ld   b,65h  	; 101, 'e'
01E3              rlca        
01E4              ld   e,66h  	; 102, 'f'
01E6              ld   a,(DATA3) 	; 1E14h
01E9              ccf         
01EA              ld   a,l    
01EB              ld   d,a    
01EC              add  hl,bc  
01ED              ld   b,e    
01EE              ld   c,e    
01EF              inc  b      
01F0              add  a,h    
01F1              ld   a,(DATA1) 	; 1000h
01F4              ld   h,d    
01F5              ld   h,a    
01F6              nop         
01F7              nop         
01F8              cpl         
01F9              ld   b,l    
01FA              nop         


; Subroutine: Recursive, Size=1505, CC=128.
; Called by: RST36[0036h], self[0236h], RST36[0136h], self[0336h], self[0436h], self[0536h], self[0636h], self[0736h].
; Calls: RST18, RST36, SUB01, SUB02, SUB03, SUB04, SUB05, SUB06, SUB07, SUB08, SUB09, SUB10, SUB11, SUB12, RST1E.
01FB SUB01:
01FB              nop         
01FC              ld   h,e    
01FD              inc  c      
01FE              rst  38h    
01FF              ret  p      
0200              and  l      
0201              ld   e,BFh  	; 191,  -65
0203              ld   hl,(DATA4) 	; 222Fh
0206              cp   a      
0207              ex   af,af' 
0208              nop         
0209              dec  b      
020A              ld   a,EBh  	; 235,  -21
020C              nop         
020D              rrca        
020E              xor  a      
020F              sbc  a,b    
0210              ld   b,06h  	; 6
0212              dec  bc     
0213              ex   af,af' 
0214              ld   h,l    
0215              dec  b      
0216              ld   h,c    
0217              inc  e      
0218              dec  hl     
0219              ld   b,c    
021A              and  l      
021B              ld   h,a    
021C              ld   a,l    
021D              ld   e,a    
021E              ld   (DATA7),hl 	; 61E8h
0221              inc  c      
0222              ld   (bc),a 
0223              in   a,(0060h) 	; 96
0225              ccf         
0226              inc  b      
0227              sbc  a,a    
0228              ld   b,b    
0229              ld   c,d    
022A              nop         
022B              out  (00F8h),a 	; 248
022D              ccf         
022E              ret  c      
022F              out  (0042h),a 	; 66
0231              ld   l,b    
0232              ld   d,a    
0233              ld   b,b    
0234              ld   h,(hl) 
0235              ret  pe     
0236 .sub01_loop1:
0236              call nz,SUB01 	; 01FBh
0239              ld   l,b    
023A              ld   (hl),d 
023B              add  hl,hl  
023C              ld   bc,4B67h 	; 19303
023F              ld   h,(hl) 
0240              nop         
0241              rrca        
0242              sub  b      
0243              ld   h,c    
0244              rst  38h    
0245              ret  p      
0246              ld   c,h    
0247              ld   b,h    
0248              ld   d,a    
0249              ld   h,b    
024A              ld   b,b    
024B              ld   l,h    
024C              ret  nc     
024D              push de     
024E              dec  c      
024F              ld   h,b    
0250              rst  18h    
0251              adc  a,e    
0252              ld   c,e    
0253              ld   h,(hl) 
0254              ld   l,b    
0255              nop         
0256              jp   z,SUB06 	; 64CFh
0259              call nz,SUB10 	; D0E5h
025C              add  hl,bc  
025D              ld   a,(bc) 
025E              ld   c,0Ah  	; 10
0260              ld   h,c    
0261              inc  c      
0262              ld   (bc),a 
0263              in   a,(0060h) 	; 96
0265              ccf         
0266              inc  b      
0267              sbc  a,a    
0268              jp   c,SUB12 	; EB7Fh
026B              jp   c,SUB09 	; 9666h
026E              ld   bc,E4F8h 	; 58616,  -6920
0271              rra         
0272              ld   l,d    
0273              inc  b      
0274              dec  l      
0275              ex   af,af' 
0276              ld   h,e    
0277              ld   a,(de) 
0278              xor  05h    	; 5
027A              ld   h,d    
027B              add  a,l    
027C              rlca        
027D              add  hl,bc  
027E              ld   h,d    
027F              add  a,l    
0280              ld   e,1Fh  	; 31
0282              ld   c,2Fh  	; 47, '/'
0284              ld   b,c    
0285              jr   nz,.sub01_loop1 	; 0236h
0287              add  hl,bc  
0288              jp   c,SUB05 	; 6040h
028B              ret  m      
028C              ld   l,l    
028D              ld   e,49h  	; 73, 'I'
028F              add  hl,bc  
0290              ld   a,(bc) 
0291              ld   l,b    
0292              jp   c,SUB04 	; 4967h
0295              dec  hl     
0296              call nz,SUB03 	; 47B1h
0299              call nz,SUB11 	; E86Ah
029C              add  hl,bc  
029D              ld   l,a    
029E              ld   a,(bc) 
029F              add  hl,bc  
02A0              ld   (DATA6),hl 	; 2FDAh
02A3              ld   h,b    
02A4              rst  20h    
02A5              in   a,(0061h) 	; 97
02A7              dec  d      
02A8              ld   e,3Fh  	; 63, '?'
02AA              ld   a,l    
02AB              ld   d,a    
02AC              add  hl,bc  
02AD              ld   b,e    
02AE              ld   c,e    
02AF              inc  b      
02B0              ld   h,c    
02B1              ret  pe     
02B2              nop         
02B3              ex   af,af' 
02B4              ld   h,(hl) 
02B5              ld   c,e    
02B6              nop         
02B7              rst  38h    
02B8              ld   (hl),b 
02B9              ld   h,a    
02BA              nop         
02BB              rrca        
02BC              jr   .sub01_l1 	; 02C4h


02BE              defb 00h    	; 0
02BF              defb 00h    	; 0
02C0              defb 00h    	; 0
02C1              defb 2Dh    	; 45, '-'
02C2              defb 72h    	; 114, 'r'
02C3              defb EBh    	; 235,  -21


02C4 .sub01_l1:
02C4              ld   e,03h  	; 3
02C6              sbc  a,h    
02C7              out  (00DAh),a 	; 218
02C9              ld   b,b    
02CA              ld   h,b    
02CB              ret  m      
02CC              ld   l,l    
02CD              ld   e,49h  	; 73, 'I'
02CF              add  hl,bc  
02D0              cpl         
02D1              ld   c,a    
02D2              sub  c      
02D3              ld   (hl),d 
02D4              ld   c,c    
02D5              dec  hl     
02D6              call nz,SUB07 	; 74B1h
02D9              ld   c,c    
02DA              ld   h,e    
02DB              ld   a,(de) 
02DC              ld   h,a    
02DD              ld   h,a    
02DE              ld   l,b    
02DF              ld   b,l    
02E0              ld   h,c    
02E1              ld   b,65h  	; 101, 'e'
02E3              rlca        
02E4              ld   e,66h  	; 102, 'f'
02E6              ld   a,(DATA3) 	; 1E14h
02E9              ccf         
02EA              ld   a,l    
02EB              ld   d,a    
02EC              add  hl,bc  
02ED              ld   b,e    
02EE              ld   c,e    
02EF              inc  b      
02F0              add  a,h    
02F1              ld   a,(DATA1) 	; 1000h
02F4              ld   h,d    
02F5              ld   h,a    
02F6              nop         
02F7              nop         
02F8              cpl         
02F9              ld   b,l    
02FA              nop         
02FB              nop         
02FC              ld   h,e    
02FD              inc  c      
02FE              rst  38h    
02FF              ret  p      
0300              and  l      
0301              ld   e,BFh  	; 191,  -65
0303              ld   hl,(DATA4) 	; 222Fh
0306              cp   a      
0307              ex   af,af' 
0308              nop         
0309              dec  b      
030A              ld   a,EBh  	; 235,  -21
030C              nop         
030D              rrca        
030E              xor  a      
030F              sbc  a,b    
0310              ld   b,06h  	; 6
0312              dec  bc     
0313              ex   af,af' 
0314              ld   h,l    
0315              dec  b      
0316              ld   h,c    
0317              inc  e      
0318              dec  hl     
0319              ld   b,c    
031A              and  l      
031B              ld   h,a    
031C              ld   a,l    
031D              ld   e,a    
031E              ld   (DATA9),hl 	; F8E8h
0321              or   e      
0322              pop  de     
0323              ret  nc     
0324              ld   l,h    
0325              cp   a      
0326              add  hl,bc  
0327              ld   h,c    
0328              ld   b,b    
0329              ld   c,d    
032A              nop         
032B              out  (00F8h),a 	; 248
032D              ccf         
032E              ret  c      
032F              out  (0042h),a 	; 66
0331              ld   l,b    
0332              ld   d,a    
0333              ld   b,b    
0334              ld   h,(hl) 
0335              ret  pe     
0336 .sub01_loop2:
0336              call nz,SUB01 	; 01FBh
0339              ld   l,b    
033A              ld   (hl),d 
033B              add  hl,hl  
033C              ld   bc,4B67h 	; 19303
033F              ld   h,(hl) 
0340              nop         
0341              rrca        
0342              sub  b      
0343              ld   h,c    
0344              rst  38h    
0345              ret  p      
0346              ld   c,h    
0347              ld   b,h    
0348              ld   d,a    
0349              ld   h,b    
034A              ld   b,b    
034B              ld   l,h    
034C              ret  nc     
034D              push de     
034E              dec  c      
034F              ld   h,b    
0350              rst  18h    
0351              adc  a,e    
0352              ld   c,e    
0353              ld   h,(hl) 
0354              ld   l,b    
0355              nop         
0356              jp   z,SUB06 	; 64CFh
0359              call nz,SUB10 	; D0E5h
035C              add  hl,bc  
035D              ld   a,(bc) 
035E              ld   c,0Ah  	; 10
0360              ld   h,c    
0361              inc  c      
0362              ld   (bc),a 
0363              in   a,(0060h) 	; 96
0365              ccf         
0366              inc  b      
0367              sbc  a,a    
0368              jp   c,SUB12 	; EB7Fh
036B              jp   c,SUB09 	; 9666h
036E              ld   bc,E4F8h 	; 58616,  -6920
0371              rra         
0372              ld   l,d    
0373              inc  b      
0374              dec  l      
0375              ex   af,af' 
0376              ld   h,e    
0377              ld   a,(de) 
0378              xor  05h    	; 5
037A              ld   h,d    
037B              add  a,l    
037C              rlca        
037D              add  hl,bc  
037E              ld   h,d    
037F              add  a,l    
0380              ld   e,1Fh  	; 31
0382              ld   c,2Fh  	; 47, '/'
0384              ld   b,c    
0385              jr   nz,.sub01_loop2 	; 0336h
0387              add  hl,bc  
0388              jp   c,SUB05 	; 6040h
038B              ret  m      
038C              ld   l,l    
038D              ld   e,49h  	; 73, 'I'
038F              add  hl,bc  
0390              ld   a,(bc) 
0391              ld   l,b    
0392              jp   c,SUB08 	; 8E67h
0395              ld   b,c    
0396              add  hl,bc  
0397              dec  a      
0398              ld   b,a    
0399              call nz,SUB11 	; E86Ah
039C              add  hl,bc  
039D              ld   l,a    
039E              ld   a,(bc) 
039F              add  hl,bc  
03A0              ld   h,c    
03A1              ld   b,65h  	; 101, 'e'
03A3              rlca        
03A4              ld   e,66h  	; 102, 'f'
03A6              ld   a,(DATA8) 	; D014h
03A9              in   a,(006Fh) 	; 111
03AB              ret  c      
03AC              ld   h,d    
03AD              ret  m      
03AE              ld   hl,6161h 	; 24929
03B1              ret  pe     
03B2              nop         
03B3              ex   af,af' 
03B4              ld   h,(hl) 
03B5              ld   c,e    
03B6              nop         
03B7              rst  38h    
03B8              ld   (hl),b 
03B9              ld   h,a    
03BA              nop         
03BB              rrca        
03BC              jr   .sub01_l2 	; 03C4h


03BE              defb 00h    	; 0
03BF              defb 00h    	; 0
03C0              defb 00h    	; 0
03C1              defb 2Dh    	; 45, '-'
03C2              defb 72h    	; 114, 'r'
03C3              defb EBh    	; 235,  -21


03C4 .sub01_l2:
03C4              ld   e,03h  	; 3
03C6              sbc  a,h    
03C7              out  (00DAh),a 	; 218
03C9              ld   b,b    
03CA              ld   h,b    
03CB              ret  m      
03CC              ld   l,l    
03CD              ld   e,49h  	; 73, 'I'
03CF              add  hl,bc  
03D0              cpl         
03D1              ld   c,a    
03D2              sub  c      
03D3              ld   (hl),d 
03D4              ld   c,c    
03D5              dec  hl     
03D6              call nz,SUB07 	; 74B1h
03D9              ld   c,c    
03DA              ld   h,e    
03DB              ld   a,(de) 
03DC              ld   h,a    
03DD              ld   h,a    
03DE              ld   l,b    
03DF              ld   b,l    
03E0              ld   h,c    
03E1              ld   b,65h  	; 101, 'e'
03E3              rlca        
03E4              ld   e,66h  	; 102, 'f'
03E6              ld   a,(DATA3) 	; 1E14h
03E9              ccf         
03EA              ld   a,l    
03EB              ld   d,a    
03EC              add  hl,bc  
03ED              ld   b,e    
03EE              ld   c,e    
03EF              inc  b      
03F0              add  a,h    
03F1              ld   a,(DATA1) 	; 1000h
03F4              ld   h,d    
03F5              ld   h,a    
03F6              nop         
03F7              nop         
03F8              cpl         
03F9              ld   b,l    
03FA              nop         
03FB              nop         
03FC              ld   h,e    
03FD              inc  c      
03FE              rst  38h    
03FF              ret  p      
0400              nop         
0401              rrca        
0402              sub  b      
0403              ld   h,c    
0404              rst  38h    
0405              ret  p      
0406              ld   c,h    
0407              ld   b,h    
0408              nop         
0409              dec  b      
040A              ld   a,EBh  	; 235,  -21
040C              nop         
040D              rrca        
040E              xor  a      
040F              sbc  a,b    
0410              ld   b,06h  	; 6
0412              dec  bc     
0413              ex   af,af' 
0414              ld   h,l    
0415              dec  b      
0416              ld   h,c    
0417              inc  e      
0418              dec  hl     
0419              ld   b,c    
041A              and  l      
041B              ld   h,a    
041C              ld   a,l    
041D              ld   e,a    
041E              ld   (DATA9),hl 	; F8E8h
0421              or   e      
0422              pop  de     
0423              ret  nc     
0424              ld   l,h    
0425              cp   a      
0426              add  hl,bc  
0427              ld   h,c    
0428              ld   b,b    
0429              ld   c,d    
042A              nop         
042B              out  (00F8h),a 	; 248
042D              ccf         
042E              ret  c      
042F              out  (0042h),a 	; 66
0431              ld   l,b    
0432              ld   d,a    
0433              ld   b,b    
0434              ld   h,(hl) 
0435              ret  pe     
0436 .sub01_loop3:
0436              call nz,SUB01 	; 01FBh
0439              ld   l,b    
043A              ld   (hl),d 
043B              add  hl,hl  
043C              ld   bc,4B67h 	; 19303
043F              ld   h,(hl) 
0440              nop         
0441              rrca        
0442              sub  b      
0443              ld   h,c    
0444              rst  38h    
0445              ret  p      
0446              ld   c,h    
0447              ld   b,h    
0448              ld   d,a    
0449              ld   h,b    
044A              ld   b,b    
044B              ld   l,h    
044C              ret  nc     
044D              push de     
044E              dec  c      
044F              ld   h,b    
0450              rst  18h    
0451              adc  a,e    
0452              ld   c,e    
0453              ld   h,(hl) 
0454              ld   l,b    
0455              nop         
0456              jp   z,SUB06 	; 64CFh
0459              call nz,SUB10 	; D0E5h
045C              add  hl,bc  
045D              ld   a,(bc) 
045E              ld   c,0Ah  	; 10
0460              ld   h,c    
0461              inc  c      
0462              ld   (bc),a 
0463              in   a,(0060h) 	; 96
0465              ccf         
0466              inc  b      
0467              sbc  a,a    
0468              jp   c,SUB12 	; EB7Fh
046B              jp   c,SUB09 	; 9666h
046E              ld   bc,E4F8h 	; 58616,  -6920
0471              rra         
0472              ld   l,d    
0473              inc  b      
0474              dec  l      
0475              ex   af,af' 
0476              ld   h,e    
0477              ld   a,(de) 
0478              xor  05h    	; 5
047A              ld   h,d    
047B              add  a,l    
047C              rlca        
047D              add  hl,bc  
047E              ld   h,d    
047F              add  a,l    
0480              ld   e,1Fh  	; 31
0482              ld   c,2Fh  	; 47, '/'
0484              ld   b,c    
0485              jr   nz,.sub01_loop3 	; 0436h
0487              add  hl,bc  
0488              jp   c,SUB05 	; 6040h
048B              ret  m      
048C              ld   l,l    
048D              ld   e,49h  	; 73, 'I'
048F              add  hl,bc  
0490              ld   a,(bc) 
0491              ld   l,b    
0492              jp   c,SUB08 	; 8E67h
0495              ld   b,c    
0496              add  hl,bc  
0497              dec  a      
0498              ld   b,a    
0499              call nz,SUB11 	; E86Ah
049C              add  hl,bc  
049D              ld   l,a    
049E              ld   a,(bc) 
049F              add  hl,bc  
04A0              ld   h,c    
04A1              ld   b,65h  	; 101, 'e'
04A3              rlca        
04A4              ld   e,66h  	; 102, 'f'
04A6              ld   a,(DATA8) 	; D014h
04A9              in   a,(006Fh) 	; 111
04AB              ret  c      
04AC              ld   h,d    
04AD              ret  m      
04AE              ld   hl,6161h 	; 24929
04B1              ret  pe     
04B2              nop         
04B3              ex   af,af' 
04B4              ld   h,(hl) 
04B5              ld   c,e    
04B6              nop         
04B7              rst  38h    
04B8              ld   (hl),b 
04B9              ld   h,a    
04BA              nop         
04BB              rrca        
04BC              jr   .sub01_l3 	; 04C4h


04BE              defb 00h    	; 0
04BF              defb 00h    	; 0
04C0              defb 00h    	; 0
04C1              defb 2Dh    	; 45, '-'
04C2              defb 72h    	; 114, 'r'
04C3              defb EBh    	; 235,  -21


04C4 .sub01_l3:
04C4              ld   e,03h  	; 3
04C6              sbc  a,h    
04C7              out  (00DAh),a 	; 218
04C9              ld   b,b    
04CA              ld   h,b    
04CB              ret  m      
04CC              ld   l,l    
04CD              ld   e,49h  	; 73, 'I'
04CF              add  hl,bc  
04D0              cpl         
04D1              ld   c,a    
04D2              sub  c      
04D3              ld   (hl),d 
04D4              ld   c,c    
04D5              dec  hl     
04D6              call nz,SUB07 	; 74B1h
04D9              ld   c,c    
04DA              ld   h,e    
04DB              ld   a,(de) 
04DC              ld   h,a    
04DD              ld   h,a    
04DE              ld   l,b    
04DF              ld   b,l    
04E0              ld   h,c    
04E1              ld   b,65h  	; 101, 'e'
04E3              rlca        
04E4              ld   e,66h  	; 102, 'f'
04E6              ld   a,(DATA3) 	; 1E14h
04E9              ccf         
04EA              ld   a,l    
04EB              ld   d,a    
04EC              add  hl,bc  
04ED              ld   b,e    
04EE              ld   c,e    
04EF              inc  b      
04F0              add  a,h    
04F1              ld   a,(DATA1) 	; 1000h
04F4              ld   h,d    
04F5              ld   h,a    
04F6              nop         
04F7              nop         
04F8              cpl         
04F9              ld   b,l    
04FA              nop         
04FB              nop         
04FC              ld   h,e    
04FD              inc  c      
04FE              rst  38h    
04FF              ret  p      
0500              nop         
0501              rrca        
0502              sub  b      
0503              ld   h,c    
0504              rst  38h    
0505              ret  p      
0506              ld   c,h    
0507              ld   b,h    
0508              nop         
0509              dec  b      
050A              ld   a,EBh  	; 235,  -21
050C              nop         
050D              rrca        
050E              xor  a      
050F              sbc  a,b    
0510              ld   b,06h  	; 6
0512              dec  bc     
0513              ex   af,af' 
0514              ld   h,l    
0515              dec  b      
0516              ld   h,c    
0517              inc  e      
0518              dec  hl     
0519              ld   b,c    
051A              and  l      
051B              ld   h,a    
051C              ld   a,l    
051D              ld   e,a    
051E              ld   (DATA9),hl 	; F8E8h
0521              or   e      
0522              pop  de     
0523              ret  nc     
0524              ld   l,h    
0525              cp   a      
0526              add  hl,bc  
0527              ld   h,c    
0528              ld   b,b    
0529              ld   c,d    
052A              nop         
052B              out  (00F8h),a 	; 248
052D              ccf         
052E              ret  c      
052F              out  (0042h),a 	; 66
0531              ld   l,b    
0532              ld   d,a    
0533              ld   b,b    
0534              ld   h,(hl) 
0535              ret  pe     
0536 .sub01_loop4:
0536              call nz,SUB01 	; 01FBh
0539              ld   l,b    
053A              ld   (hl),d 
053B              add  hl,hl  
053C              ld   bc,4B67h 	; 19303
053F              ld   h,(hl) 
0540              nop         
0541              rrca        
0542              sub  b      
0543              ld   h,c    
0544              rst  38h    
0545              ret  p      
0546              ld   c,h    
0547              ld   b,h    
0548              ld   d,a    
0549              ld   h,b    
054A              ld   b,b    
054B              ld   l,h    
054C              ret  nc     
054D              push de     
054E              dec  c      
054F              ld   h,b    
0550              rst  18h    
0551              adc  a,e    
0552              ld   c,e    
0553              ld   h,(hl) 
0554              ld   l,b    
0555              nop         
0556              jp   z,SUB06 	; 64CFh
0559              call nz,SUB10 	; D0E5h
055C              add  hl,bc  
055D              ld   a,(bc) 
055E              ld   c,0Ah  	; 10
0560              ld   h,c    
0561              inc  c      
0562              ld   (bc),a 
0563              in   a,(0060h) 	; 96
0565              ccf         
0566              inc  b      
0567              sbc  a,a    
0568              jp   c,SUB12 	; EB7Fh
056B              jp   c,SUB09 	; 9666h
056E              ld   bc,E4F8h 	; 58616,  -6920
0571              rra         
0572              ld   l,d    
0573              inc  b      
0574              dec  l      
0575              ex   af,af' 
0576              ld   h,e    
0577              ld   a,(de) 
0578              xor  05h    	; 5
057A              ld   h,d    
057B              add  a,l    
057C              rlca        
057D              add  hl,bc  
057E              ld   h,d    
057F              add  a,l    
0580              ld   e,1Fh  	; 31
0582              ld   c,2Fh  	; 47, '/'
0584              ld   b,c    
0585              jr   nz,.sub01_loop4 	; 0536h
0587              add  hl,bc  
0588              jp   c,SUB05 	; 6040h
058B              ret  m      
058C              ld   l,l    
058D              ld   e,49h  	; 73, 'I'
058F              add  hl,bc  
0590              ld   a,(bc) 
0591              ld   l,b    
0592              jp   c,SUB08 	; 8E67h
0595              ld   b,c    
0596              add  hl,bc  
0597              dec  a      
0598              ld   b,a    
0599              call nz,SUB11 	; E86Ah
059C              add  hl,bc  
059D              ld   l,a    
059E              ld   a,(bc) 
059F              add  hl,bc  
05A0              ld   h,c    
05A1              ld   b,65h  	; 101, 'e'
05A3              rlca        
05A4              ld   e,66h  	; 102, 'f'
05A6              ld   a,(DATA8) 	; D014h
05A9              in   a,(006Fh) 	; 111
05AB              ret  c      
05AC              ld   h,d    
05AD              ret  m      
05AE              ld   hl,6161h 	; 24929
05B1              ret  pe     
05B2              nop         
05B3              ex   af,af' 
05B4              ld   h,(hl) 
05B5              ld   c,e    
05B6              nop         
05B7              rst  38h    
05B8              ld   (hl),b 
05B9              ld   h,a    
05BA              nop         
05BB              rrca        
05BC              jr   .sub01_l4 	; 05C4h


05BE              defb 00h    	; 0
05BF              defb 00h    	; 0
05C0              defb 00h    	; 0
05C1              defb 2Dh    	; 45, '-'
05C2              defb 72h    	; 114, 'r'
05C3              defb EBh    	; 235,  -21


05C4 .sub01_l4:
05C4              ld   e,03h  	; 3
05C6              sbc  a,h    
05C7              out  (00DAh),a 	; 218
05C9              ld   b,b    
05CA              ld   h,b    
05CB              ret  m      
05CC              ld   l,l    
05CD              ld   e,49h  	; 73, 'I'
05CF              add  hl,bc  
05D0              cpl         
05D1              ld   c,a    
05D2              sub  c      
05D3              ld   (hl),d 
05D4              ld   c,c    
05D5              dec  hl     
05D6              call nz,SUB07 	; 74B1h
05D9              ld   c,c    
05DA              ld   h,e    
05DB              ld   a,(de) 
05DC              ld   h,a    
05DD              ld   h,a    
05DE              ld   l,b    
05DF              ld   b,l    
05E0              ld   h,c    
05E1              ld   b,65h  	; 101, 'e'
05E3              rlca        
05E4              ld   e,66h  	; 102, 'f'
05E6              ld   a,(DATA3) 	; 1E14h
05E9              ccf         
05EA              ld   a,l    
05EB              ld   d,a    
05EC              add  hl,bc  
05ED              ld   b,e    
05EE              ld   c,e    
05EF              inc  b      
05F0              add  a,h    
05F1              ld   a,(DATA1) 	; 1000h
05F4              ld   h,d    
05F5              ld   h,a    
05F6              nop         
05F7              nop         
05F8              cpl         
05F9              ld   b,l    
05FA              nop         
05FB              nop         
05FC              ld   h,e    
05FD              inc  c      
05FE              rst  38h    
05FF              ret  p      
0600              nop         
0601              rrca        
0602              sub  b      
0603              ld   h,c    
0604              rst  38h    
0605              ret  p      
0606              ld   c,h    
0607              ld   b,h    
0608              nop         
0609              dec  b      
060A              ld   a,EBh  	; 235,  -21
060C              nop         
060D              rrca        
060E              xor  a      
060F              sbc  a,b    
0610              ld   b,06h  	; 6
0612              dec  bc     
0613              ex   af,af' 
0614              ld   h,l    
0615              dec  b      
0616              ld   h,c    
0617              inc  e      
0618              dec  hl     
0619              ld   b,c    
061A              and  l      
061B              ld   h,a    
061C              ld   a,l    
061D              ld   e,a    
061E              ld   (DATA7),hl 	; 61E8h
0621              inc  c      
0622              ld   (bc),a 
0623              pop  de     
0624              ld   l,h    
0625              cp   a      
0626              add  hl,bc  
0627              ld   h,c    
0628              ld   b,b    
0629              ld   c,d    
062A              nop         
062B              out  (00F8h),a 	; 248
062D              ccf         
062E              ret  c      
062F              out  (0042h),a 	; 66
0631              ld   l,b    
0632              ld   d,a    
0633              ld   b,b    
0634              ld   h,(hl) 
0635              ret  pe     
0636 .sub01_loop5:
0636              call nz,SUB01 	; 01FBh
0639              ld   l,b    
063A              ld   (hl),d 
063B              add  hl,hl  
063C              ld   bc,4B67h 	; 19303
063F              ld   h,(hl) 
0640              nop         
0641              rrca        
0642              sub  b      
0643              ld   h,c    
0644              rst  38h    
0645              ret  p      
0646              ld   c,h    
0647              ld   b,h    
0648              ld   d,a    
0649              ld   h,b    
064A              ld   b,b    
064B              ld   l,h    
064C              ret  nc     
064D              push de     
064E              dec  c      
064F              ld   h,b    
0650              rst  18h    
0651              adc  a,e    
0652              ld   c,e    
0653              ld   h,(hl) 
0654              ld   l,b    
0655              nop         
0656              jp   z,SUB06 	; 64CFh
0659              call nz,SUB10 	; D0E5h
065C              add  hl,bc  
065D              ld   a,(bc) 
065E              ld   c,0Ah  	; 10
0660              ld   h,c    
0661              inc  c      
0662              ld   (bc),a 
0663              in   a,(0060h) 	; 96
0665              ccf         
0666              inc  b      
0667              sbc  a,a    
0668              jp   c,SUB12 	; EB7Fh
066B              jp   c,SUB09 	; 9666h
066E              ld   bc,E4F8h 	; 58616,  -6920
0671              rra         
0672              ld   l,d    
0673              inc  b      
0674              dec  l      
0675              ex   af,af' 
0676              ld   h,e    
0677              ld   a,(de) 
0678              xor  05h    	; 5
067A              ld   h,d    
067B              add  a,l    
067C              rlca        
067D              add  hl,bc  
067E              ld   h,d    
067F              add  a,l    
0680              ld   e,1Fh  	; 31
0682              ld   c,2Fh  	; 47, '/'
0684              ld   b,c    
0685              jr   nz,.sub01_loop5 	; 0636h
0687              add  hl,bc  
0688              jp   c,SUB05 	; 6040h
068B              ret  m      
068C              ld   l,l    
068D              ld   e,49h  	; 73, 'I'
068F              add  hl,bc  
0690              ld   a,(bc) 
0691              ld   l,b    
0692              jp   c,SUB08 	; 8E67h
0695              ld   b,c    
0696              add  hl,bc  
0697              dec  a      
0698              ld   b,a    
0699              call nz,SUB11 	; E86Ah
069C              add  hl,bc  
069D              ld   l,a    
069E              ld   a,(bc) 
069F              add  hl,bc  
06A0              ld   h,c    
06A1              ld   b,65h  	; 101, 'e'
06A3              rlca        
06A4              ld   e,66h  	; 102, 'f'
06A6              ld   a,(DATA8) 	; D014h
06A9              in   a,(006Fh) 	; 111
06AB              ret  c      
06AC              ld   h,d    
06AD              ret  m      
06AE              ld   hl,6161h 	; 24929
06B1              ret  pe     
06B2              nop         
06B3              ex   af,af' 
06B4              ld   h,(hl) 
06B5              ld   c,e    
06B6              nop         
06B7              rst  38h    
06B8              ld   (hl),b 
06B9              ld   h,a    
06BA              nop         
06BB              rrca        
06BC              jr   .sub01_l5 	; 06C4h


06BE              defb 00h    	; 0
06BF              defb 00h    	; 0
06C0              defb 00h    	; 0
06C1              defb 2Dh    	; 45, '-'
06C2              defb 72h    	; 114, 'r'
06C3              defb EBh    	; 235,  -21


06C4 .sub01_l5:
06C4              ld   e,03h  	; 3
06C6              sbc  a,h    
06C7              out  (00DAh),a 	; 218
06C9              ld   b,b    
06CA              ld   h,b    
06CB              ret  m      
06CC              ld   l,l    
06CD              ld   e,49h  	; 73, 'I'
06CF              add  hl,bc  
06D0              cpl         
06D1              ld   c,a    
06D2              sub  c      
06D3              ld   (hl),d 
06D4              ld   c,c    
06D5              dec  hl     
06D6              call nz,SUB07 	; 74B1h
06D9              ld   c,c    
06DA              ld   h,e    
06DB              ld   a,(de) 
06DC              ld   h,a    
06DD              ld   h,a    
06DE              ld   l,b    
06DF              ld   b,l    
06E0              ld   h,c    
06E1              ld   b,65h  	; 101, 'e'
06E3              rlca        
06E4              ld   e,66h  	; 102, 'f'
06E6              ld   a,(DATA3) 	; 1E14h
06E9              ccf         
06EA              ld   a,l    
06EB              ld   d,a    
06EC              add  hl,bc  
06ED              ld   b,e    
06EE              ld   c,e    
06EF              inc  b      
06F0              add  a,h    
06F1              ld   a,(DATA1) 	; 1000h
06F4              ld   h,d    
06F5              ld   h,a    
06F6              nop         
06F7              nop         
06F8              cpl         
06F9              ld   b,l    
06FA              nop         
06FB              nop         
06FC              ld   h,e    
06FD              inc  c      
06FE              rst  38h    
06FF              ret  p      
0700              and  l      
0701              ld   e,90h  	; 144, -112
0703              ld   h,c    
0704              rst  38h    
0705              ret  p      
0706              ld   c,h    
0707              ld   b,h    
0708              nop         
0709              dec  b      
070A              ld   a,EBh  	; 235,  -21
070C              nop         
070D              rrca        
070E              xor  a      
070F              sbc  a,b    
0710              ld   b,06h  	; 6
0712              dec  bc     
0713              ex   af,af' 
0714              ld   h,l    
0715              dec  b      
0716              ld   h,c    
0717              inc  e      
0718              dec  hl     
0719              ld   b,c    
071A              and  l      
071B              ld   h,a    
071C              ld   a,l    
071D              ld   e,a    
071E              ld   (DATA7),hl 	; 61E8h
0721              inc  c      
0722              ld   (bc),a 
0723              in   a,(0060h) 	; 96
0725              ccf         
0726              inc  b      
0727              sbc  a,a    
0728              ld   b,b    
0729              ld   c,d    
072A              nop         
072B              out  (00F8h),a 	; 248
072D              ccf         
072E              ret  c      
072F              out  (0042h),a 	; 66
0731              ld   l,b    
0732              ld   d,a    
0733              ld   b,b    
0734              ld   h,(hl) 
0735              ret  pe     
0736 .sub01_loop6:
0736              call nz,SUB01 	; 01FBh
0739              ld   l,b    
073A              ld   (hl),d 
073B              add  hl,hl  
073C              ld   bc,4B67h 	; 19303
073F              ld   h,(hl) 
0740              nop         
0741              rrca        
0742              sub  b      
0743              ld   h,c    
0744              rst  38h    
0745              ret  p      
0746              ld   c,h    
0747              ld   b,h    
0748              ld   d,a    
0749              ld   h,b    
074A              ld   b,b    
074B              ld   l,h    
074C              ret  nc     
074D              push de     
074E              dec  c      
074F              ld   h,b    
0750              rst  18h    
0751              adc  a,e    
0752              ld   c,e    
0753              ld   h,(hl) 
0754              ld   l,b    
0755              nop         
0756              jp   z,SUB06 	; 64CFh
0759              call nz,SUB10 	; D0E5h
075C              add  hl,bc  
075D              ld   a,(bc) 
075E              ld   c,0Ah  	; 10
0760              ld   h,c    
0761              inc  c      
0762              ld   (bc),a 
0763              in   a,(0060h) 	; 96
0765              ccf         
0766              inc  b      
0767              sbc  a,a    
0768              jp   c,SUB12 	; EB7Fh
076B              jp   c,SUB09 	; 9666h
076E              ld   bc,E4F8h 	; 58616,  -6920
0771              rra         
0772              ld   l,d    
0773              inc  b      
0774              dec  l      
0775              ex   af,af' 
0776              ld   h,e    
0777              ld   a,(de) 
0778              xor  05h    	; 5
077A              ld   h,d    
077B              add  a,l    
077C              rlca        
077D              add  hl,bc  
077E              ld   h,d    
077F              add  a,l    
0780              ld   e,1Fh  	; 31
0782              ld   c,2Fh  	; 47, '/'
0784              ld   b,c    
0785              jr   nz,.sub01_loop6 	; 0736h
0787              add  hl,bc  
0788              add  hl,hl  
0789              and  l      
078A              ld   h,b    
078B              ld   hl,(DATA5) 	; 24C9h
078E              jp   c,SUB02 	; 0840h
0791              ld   l,b    
0792              jp   c,SUB08 	; 8E67h
0795              ld   b,c    
0796              add  hl,bc  
0797              dec  a      
0798              ld   b,a    
0799              call nz,SUB11 	; E86Ah
079C              add  hl,bc  
079D              ld   l,a    
079E              ld   a,(bc) 
079F              add  hl,bc  
07A0              ld   (DATA6),hl 	; 2FDAh
07A3              ld   h,b    
07A4              rst  20h    
07A5              in   a,(0061h) 	; 97
07A7              dec  d      
07A8              ret  nc     
07A9              in   a,(006Fh) 	; 111
07AB              ret  c      
07AC              ld   h,d    
07AD              ret  m      
07AE              ld   hl,6161h 	; 24929
07B1              ret  pe     
07B2              nop         
07B3              ex   af,af' 
07B4              ld   h,(hl) 
07B5              ld   c,e    
07B6              nop         
07B7              rst  38h    
07B8              ld   (hl),b 
07B9              ld   h,a    
07BA              nop         
07BB              rrca        
07BC              jr   .sub01_l6 	; 07C4h


07BE              defb 00h    	; 0
07BF              defb 00h    	; 0
07C0              defb 00h    	; 0
07C1              defb 2Dh    	; 45, '-'
07C2              defb 72h    	; 114, 'r'
07C3              defb EBh    	; 235,  -21


07C4 .sub01_l6:
07C4              ld   e,03h  	; 3
07C6              sbc  a,h    
07C7              out  (00DAh),a 	; 218
07C9              ld   b,b    
07CA              ld   h,b    
07CB              ret  m      
07CC              ld   l,l    
07CD              ld   e,49h  	; 73, 'I'
07CF              add  hl,bc  
07D0              cpl         
07D1              ld   c,a    
07D2              sub  c      
07D3              ld   (hl),d 
07D4              ld   c,c    
07D5              dec  hl     
07D6              call nz,SUB07 	; 74B1h
07D9              ld   c,c    
07DA              ld   h,e    
07DB              ld   a,(de) 
07DC              ld   h,a    
07DD              ld   h,a    
07DE              ld   l,b    
07DF              ld   b,l    
07E0              ld   h,c    
07E1              ld   b,65h  	; 101, 'e'
07E3              rlca        
07E4              ld   e,66h  	; 102, 'f'
07E6              ld   a,(DATA3) 	; 1E14h
07E9              ccf         
07EA              ld   a,l    
07EB              ld   d,a    
07EC              add  hl,bc  
07ED              ld   b,e    
07EE              ld   c,e    
07EF              inc  b      
07F0              add  a,h    
07F1              ld   a,(DATA1) 	; 1000h
07F4              ld   h,d    
07F5              ld   h,a    
07F6              nop         
07F7              nop         
07F8              cpl         
07F9              ld   b,l    
07FA              nop         
07FB              nop         
07FC              ld   h,e    
07FD              inc  c      
07FE              rst  38h    
07FF              ret  p      
; ...
; ...
; ...
```

Also, [roms.list](../xtras/roms.list)


Note: I am not totally convinced that the disassembly makes total sense. I may have needed to specify an *offset*?
