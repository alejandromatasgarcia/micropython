Code for the **Waveshare Pico LCD 1.14" V2** with chipset **ST7789VW** and a resolution of 240x135 pixels.

Created from the original code available at https://www.waveshare.com/wiki/Pico-LCD-1.14#Download_Demo_codes

Modifies the supplied class ```LCD_1inch14``` to add rotation (0,90,180 & 270 degrees) and brightness control.
Also changes the definition of the key pins so when you rotate the screen, the up, down, left & right keys also rotate.

Added new methods:
* ```on()```: turn the display on.
* ```off()```: turn the display off.
* ```set_brightness(brightness)```: change LCD backlight brightness (0-65535)
* ```rgb565(r,g,b)```: creates a RGB565 color word (with its bytes swapped) from R, G & B values (0-255) to use with the framebuffer methods
* ```gray565(gray)```: creates a RGB565 color word (with its bytes swapped) from a grayscale value (0-255) to use with the framebuffer methods
