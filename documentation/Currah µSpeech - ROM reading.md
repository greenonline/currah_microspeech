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

    delayMicroseconds(delayTime);  // not relly needed

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

