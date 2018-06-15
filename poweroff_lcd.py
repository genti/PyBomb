#!/usr/bin/python
#--------------------------------------
#--------------------------------------
#--------------------------------------
#-------- NARCOS pyBomb v0.4 ----------
#--------------------------------------
#--------------------------------------
#--------------------------------------
import socket,commands
from threading import Thread,Semaphore
import lcddriver
global screenlock 
screenlock = Semaphore(value=1)

global lcd

lcd = lcddriver.lcd()

def main():
    screenlock.acquire()
    lcd.backlight_off() 
    lcd.display_string("GDP narcos bomb".center(20),2) 
    lcd.display_string("See you".center(20),3) 
    screenlock.release()
    
if __name__ == '__main__':

  try:
    main()
  except KeyboardInterrupt: 
    pass
  # finally:
    # lcd_byte(0x01, LCD_CMD)

