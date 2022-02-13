Control a 8x32 led Matrix with an Arduino Uno, on the Serial port.

Currently done : 
  - A Python script sends data to update the matrix to the Serial port
  - The connected Arduino Uno is reading this data and updating the matrix accordingly


Material required : 
  - A compatible Arduino (Uno...)
  - Jumpwire cables
  - A 8x32 LEDs matrix (code will be change in the future to include different shapes) that is able to be piloted with the MAX72xx Arduino library.
  - A computer with Arduino and Python 3 installed
  - A USB cable to connect both

Steps to obtain the same working status :
  - Connect the 8x32 LEDs matrix to the Arduino with the following pinout
    - CLK <> 13
    - DATA <> 11
    - CS <> 10
    - GND <> GND
    - VCC <> 5V
  - Open the Arduino script and load it on the Arduino
  - Open the Python script and load it (maybe change the port variable)
  - The LEDS should now light up and scroll in a controlled way
