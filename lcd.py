import lcddriver
import time

lcd = lcddriver.lcd()






def getTimeFromString():
    file = open("/var/www/html/time.txt", "r")
    arr = file.read() .split(" ")
    time=(int(arr[0])*3600)+(int(arr[1])*60)+(int(arr[2]))
    return time 
    
    
def countdown():
    timer_rem=getTimeFromString()
   
   
    while timer_rem >0:
        timer_rem=timer_rem-1
        m, s = divmod(timer_rem, 60)
        h, m = divmod(m, 60)
        lcd.lcd_display_string("%d:%02d:%02d" % (h, m, s),1)    
        time.sleep(1)











countdown();








# lcd.lcd_clear();
#lcd.lcd_display_string("LoremLoremLoremLoremLoremLoremLoremLoremLoremLorem", 1)
