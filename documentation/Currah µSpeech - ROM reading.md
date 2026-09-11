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
     - Pin 18 LOW
     - Pin 20 ???
     - Pin 21 HIGH
   - Cycle through the ROM addresses (0000h - 0800h), outputing on the Arduino data lines connected to the address lines of the ROM
   - Wait 1-2 µS, even though the access time for the 9316C is only 450 nS (max.)
   - Read the ROM data, reading the Arduino data lines connected to the data lines of the ROM

The sme process can be applied to the ULA.

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
// Sketch to read 9316C ROM

// Use bit-shift method for bit detection
#define __USE_BITSHIFT__
// Use bitRead() method for bit detection (causes warning)
//#define __USE_BITREAD__

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
    romA0 = 20;
    romA1 = 22;
    romA2 = 24;
    romA3 = 26;
    romA4 = 28;
    romA5 = 30;
    romA6 = 32;
    romA7 = 34;
    romA8 = 36;
    romA9 = 38;
    romA10 = 40;

    // Chip select lines
    romCS1 = 44;
    romCS2 = 46;
    romCS3 = 48;

    // Data lines
    romD0 = 21;
    romD1 = 23;
    romD2 = 25;
    romD3 = 27;
    romD4 = 29;
    romD5 = 31;
    romD6 = 33;
    romD7 = 35;
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

  // Chip select lines
  pinMode(romCS1, OUTPUT);    // CS1
  pinMode(romCS2, OUTPUT);    // CS2
  pinMode(romCS3, OUTPUT);    // CS3

  // Data lines
  pinMode(romD0, INPUT);     // D0
  pinMode(romD1, INPUT);     // D1
  pinMode(romD2, INPUT);     // D2
  pinMode(romD3, INPUT);     // D3
  pinMode(romD4, INPUT);     // D4
  pinMode(romD5, INPUT);     // D5
  pinMode(romD6, INPUT);     // D6
  pinMode(romD7, INPUT);     // D7

  // Set ROM chip select lines
  digitalWrite(romCS1, LOW);    // Currah unknown
  digitalWrite(romCS1, HIGH);   // Currah unknown
  digitalWrite(romCS2, LOW);    // Currah tied to GND
  digitalWrite(romCS3, HIGH);   // Currah tied to VCC

  Serial.begin(9600);
}

void loop()
{
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
    if (outByte > 1023){
      outA10 = 1;
      outByte = outByte - 1024;
    }
    if (outByte > 511){
      outA9 = 1;
      outByte = outByte - 512;
    }
    if (outByte > 255){
      outA8 = 1;
      outByte = outByte - 256;
    }
    if (outByte > 127){
      outA7 = 1;
      outByte = outByte - 128;
    }
    if (outByte > 63){
      outA6 = 1;
      outByte = outByte - 64;
    }
    if (outByte > 31){
      outA5 = 1;
      outByte = outByte - 32;
    }
    if (outByte > 15){
      outA4 = 1;
      outByte = outByte - 16;
    }
    if (outByte > 7){
      outA3 = 1;
      outByte = outByte - 8;
    }
    if (outByte > 3){
      outA2 = 1;
      outByte = outByte - 4;
    }
    if (outByte > 1){
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

    delay(50);  // not needed

    inD0 = digitalRead(romD0);
    inD1 = digitalRead(romD1);
    inD2 = digitalRead(romD2);
    inD3 = digitalRead(romD3);
    inD4 = digitalRead(romD4);
    inD5 = digitalRead(romD5);
    inD6 = digitalRead(romD6);
    inD7 = digitalRead(romD7);

    inByte = (128 * inD7) + (64 * inD6) + (32 * inD5) + (16 * inD4) + (8 * inD3) + (4 * inD2) + (2 * inD1) + inD0;

    Serial.print (outByte);
    Serial.print (" : ");
    Serial.println (inByte);
  }
}
```



