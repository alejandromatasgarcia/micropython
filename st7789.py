from machine import Pin,SPI,PWM
import framebuf

# asignación de pines
BL = const(13)
DC = const(8)
RST = const(12)
MOSI = const(11)
SCK = const(10)
CS = const(9)

class LCD_1inch14(framebuf.FrameBuffer):
    # esta clase hereda de FrameBuffer
    def __init__(self,rotation=0,brightness=16384):
        # añadimos rotación
        if rotation in (0,90,180,270):
            self.rotation = rotation
        else:
            self.rotation = 0
        self.rot0180 = (self.rotation == 0 or self.rotation == 180)
        if self.rot0180:
            self.width = 240
            self.height = 135
        else:
            self.width = 135
            self.height = 240
        # las 2 rotaciones "que faltan" las haremos haciendo mirror de X e Y
        
        self.cs = Pin(CS,Pin.OUT)
        self.rst = Pin(RST,Pin.OUT)
        
        self.cs(1)
        self.spi = SPI(1)
        self.spi = SPI(1,1000_000)
        self.spi = SPI(1,10000_000,polarity=0, phase=0,sck=Pin(SCK),mosi=Pin(MOSI),miso=None)
        self.dc = Pin(DC,Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init_display()
        
        self.pwm = PWM(Pin(BL))
        self.pwm.freq(1000)
        self.brillo(brightness)
        
        # teclas.
        self.keyA = Pin(15,Pin.IN,Pin.PULL_UP) # A
        self.keyB = Pin(17,Pin.IN,Pin.PULL_UP) # B
        self.keyC = Pin(3,Pin.IN,Pin.PULL_UP) # centro
        # Las definimos según la rotación de la pantalla
        if self.rotation == 0:
            self.keyUP = Pin(2,Pin.IN,Pin.PULL_UP) # arriba
            self.keyLEFT = Pin(16,Pin.IN,Pin.PULL_UP) # izquierda
            self.keyDOWN = Pin(18,Pin.IN,Pin.PULL_UP) # abajo
            self.keyRIGHT = Pin(20,Pin.IN,Pin.PULL_UP) # derecha
        elif self.rotation == 90:
            self.keyUP = Pin(20,Pin.IN,Pin.PULL_UP) # arriba
            self.keyLEFT = Pin(2,Pin.IN,Pin.PULL_UP) # izquierda
            self.keyDOWN = Pin(16,Pin.IN,Pin.PULL_UP) # abajo
            self.keyRIGHT = Pin(18,Pin.IN,Pin.PULL_UP) # derecha
        elif self.rotation == 180:
            self.keyUP = Pin(18 ,Pin.IN,Pin.PULL_UP) # arriba
            self.keyLEFT = Pin(20 ,Pin.IN,Pin.PULL_UP) # izquierda
            self.keyDOWN = Pin(2 ,Pin.IN,Pin.PULL_UP) # abajo
            self.keyRIGHT = Pin(16 ,Pin.IN,Pin.PULL_UP) # derecha
        elif self.rotation == 270:
            self.keyUP = Pin(16,Pin.IN,Pin.PULL_UP) # arriba
            self.keyLEFT = Pin(18,Pin.IN,Pin.PULL_UP) # izquierda
            self.keyDOWN = Pin(20,Pin.IN,Pin.PULL_UP) # abajo
            self.keyRIGHT = Pin(2,Pin.IN,Pin.PULL_UP) # derecha
        
        # colores codificados como RGB565 (bytes invertidos)
        self.red   =   0x00F8
        self.green =   0xE007
        self.blue  =   0x1F00
        self.yellow =  0xE0FF
        self.magenta = 0x1FF8
        self.cyan =    0xFF07
        self.black =   0x0000
        self.white =   0xFFFF

    def brillo(self, brillo):
        """ brillo 0-65535 """
        self.pwm.duty_u16(brillo)
    
    def write_cmd(self, cmd):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)

    def init_display(self):
        """Initialize display"""  
        self.rst(1)
        self.rst(0)
        self.rst(1)
        
        self.write_cmd(0x36)
        if self.rotation == 0:
            # por defecto
            self.write_data(0x70)
        elif self.rotation == 90:
            # rotación 270 y mirror X-Y
            self.write_data(0xC0)
        elif self.rotation == 180:
            # rotación 0 y mirror X-Y
            self.write_data(0xB0)
        elif self.rotation == 270:
            self.write_data(0x00)

        self.write_cmd(0x3A) 
        self.write_data(0x05)

        self.write_cmd(0xB2)
        self.write_data(0x0C)
        self.write_data(0x0C)
        self.write_data(0x00)
        self.write_data(0x33)
        self.write_data(0x33)

        self.write_cmd(0xB7)
        self.write_data(0x35) 

        self.write_cmd(0xBB)
        self.write_data(0x19)

        self.write_cmd(0xC0)
        self.write_data(0x2C)

        self.write_cmd(0xC2)
        self.write_data(0x01)

        self.write_cmd(0xC3)
        self.write_data(0x12)   

        self.write_cmd(0xC4)
        self.write_data(0x20)

        self.write_cmd(0xC6)
        self.write_data(0x0F) 

        self.write_cmd(0xD0)
        self.write_data(0xA4)
        self.write_data(0xA1)

        self.write_cmd(0xE0)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0D)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2B)
        self.write_data(0x3F)
        self.write_data(0x54)
        self.write_data(0x4C)
        self.write_data(0x18)
        self.write_data(0x0D)
        self.write_data(0x0B)
        self.write_data(0x1F)
        self.write_data(0x23)

        self.write_cmd(0xE1)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0C)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2C)
        self.write_data(0x3F)
        self.write_data(0x44)
        self.write_data(0x51)
        self.write_data(0x2F)
        self.write_data(0x1F)
        self.write_data(0x1F)
        self.write_data(0x20)
        self.write_data(0x23)
        
        self.write_cmd(0x21)

        self.write_cmd(0x11)

        self.write_cmd(0x29)

    def show(self):
        if self.rotation == 0:
            # por defecto
            self.write_cmd(0x2A)
            self.write_data(0x00)
            self.write_data(0x28)
            self.write_data(0x01)
            self.write_data(0x17)
            self.write_cmd(0x2B)
            self.write_data(0x00)
            self.write_data(0x35)
            self.write_data(0x00)
            self.write_data(0xBB)
        elif self.rotation == 90:
            self.write_cmd(0x2A)
            self.write_data(0x00)
            self.write_data(0x35)
            self.write_data(0x00)
            self.write_data(0xBB)
            self.write_cmd(0x2B)
            self.write_data(0x00)
            self.write_data(0x28)
            self.write_data(0x01)
            self.write_data(0x17)
        if self.rotation == 180:
            self.write_cmd(0x2A)
            self.write_data(0x00)
            self.write_data(0x28)
            self.write_data(0x01)
            self.write_data(0x17)
            self.write_cmd(0x2B)
            self.write_data(0x00)
            self.write_data(0x34)
            self.write_data(0x00)
            self.write_data(0xBA)
        elif self.rotation == 270:
            self.write_cmd(0x2A)
            self.write_data(0x00)
            self.write_data(0x34)
            self.write_data(0x00)
            self.write_data(0xBA)
            self.write_cmd(0x2B)
            self.write_data(0x00)
            self.write_data(0x28)
            self.write_data(0x01)
            self.write_data(0x17)
            
        self.write_cmd(0x2C)
        
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)
        
    def off(self):
        """ DISPOFF """
        self.write_cmd(0x28)
    
    def on(self):
        """ DISPON """
        self.write_cmd(0x29)
        
    def rgb565(self,r: int,g: int,b: int) -> int:
        """ codifica RGB888 a RGB565 invirtiendo los bytes """
        return ((g & 0x1c) << 11) | (g >> 5) | ((b & 0xf8) << 5) | (r & 0xf8)