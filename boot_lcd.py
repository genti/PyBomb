#!/usr/bin/python
#--------------------------------------
#--------------------------------------
#--------------------------------------
#-------- NARCOS pyBomb v0.6 ----------
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
    IP=commands.getoutput('hostname -I')
    # Send some test
    screenlock.acquire()
    lcd.display_string("GDP narcos bomb".center(20),2) 
    lcd.display_string("%s" % IP.center(20),3) 
    screenlock.release()
    
if __name__ == '__main__':

  try:
    main()
  except KeyboardInterrupt:
    pass
  # finally:
    # lcd_byte(0x01, LCD_CMD)

