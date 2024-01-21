Code for the Waveshare Pico LCD 1.14" V2 with chipset ST7789VW and a resolution of 240x135 pixels.

Created from the original code available at https://www.waveshare.com/wiki/Pico-LCD-1.14#Download_Demo_codes

Modifies the original class LCD_1inch14 to add rotation (0,90,180 & 270 degrees) and brightness control (0-65535)
Also changes the definition of the key pins so when you rotate the screen, the up, down, left & right keys also rotate

Added 4 methods: on() & off(), to turn the display on and off; brillo()*, to change brightness; and rgb565(r,g,b) to create a RGB565 color word (with its bytes inverted) from R, G & B values (0-255) to use with the framebuffer methods

*: some comments are in Spanish, they'll be translated into English with the next version.
