# Questo codice e' stato realizzato per l'asd GUARDIANI DEL PO 
# non si tratta di un vero ordigno ma bensi' si un giocattolo 
# atto a ricreare funzionalita' di un vero ordingno a tempo con 
# possibilita' di essere disinnescato tagliando dei fili in 
# ordine specifico.  Davide Gentilucci non si assume responsabilia' 
# alcuna per l'uso improprio di questo script


from threading import Thread,Semaphore

import time,os
import lcddriver
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

global lcd 
lcd = lcddriver.lcd()

global PID_FILE
PID_FILE='/home/pi/TIMER_RUNNING'

global screenlock 
screenlock = Semaphore(value=1)

global version
version = '0.3'

global wires,arr
#wires_arr=OrderedDict[4,17,27,22,23,24,25,5]
wires_arr=[]

#prova ordinamento taglio fili
global w_a,w_b,w_c,w_d,w_e,w_f,w_g,w_h
w_a=w_b=w_c=w_d=w_e=w_f=w_g=w_h=False


for pin in wires_arr:
    GPIO.setup(pin, GPIO.IN)

    
    
def printOnLcD(str,row):
    screenlock.acquire()
    lcd.lcd_display_string(str.center(20),row) 
    screenlock.release()    

def getWiresOrder():
    file = open("/var/www/html/wires.txt", "r")
    arr = file.read().split(" ")
    wires=''    
    for w in arr:
        wires='%s %s' %(wires,w)
    return wires.strip()
        
wires_arr=getWiresOrder()        
  
class CountdownProgram:  
    def __init__(self):
        self._running = True
        
        printOnLcD("GDP narcos bomb %s" % version,1) 
      

    def terminate(self):  
        self._running = False  

    def getTimeFromString(self):
        file = open("/var/www/html/time.txt", "r")
        arr = file.read() .split(" ")
        time=(int(arr[0])*3600)+(int(arr[1])*60)+(int(arr[2]))
        return time 
    
    def run(self):
        touch(PID_FILE)
        
        while self._running:
            timer_rem=self.getTimeFromString()
           
           
            while timer_rem >0:
                timer_rem=timer_rem-1
                m, s = divmod(timer_rem, 60)
                h, m = divmod(m, 60)
                time_str="%02d:%02d:%02d" % (h, m, s)
                
                printOnLcD(time_str,2)    
                
                time.sleep(1)
            
            self.terminate()
            
                
                 

class WiresCheck:  
    def __init__(self):
        self._running = True

    def terminate(self):  
        self._running = False  
        
    

    def run(self):
        
        while Stopwatch._running:
            # screenlock.acquire()
            # lcd.lcd_display_string(self.getWiresOrder().center(20),4)   
            # screenlock.release()
        
            if w_a or w_b or w_c or w_d or w_e or w_f or w_g or w_h:
                str="Defusing"
               
                printOnLcD(str,3)  
            else:
                str="Defuse it!"
               
                printOnLcD(str,3)   
                
                
            
            
            if GPIO.input(wires_arr[0]) == GPIO.LOW:
                print("Wire #1 cutted")
                if not w_a and not w_b and not w_c and not w_d and not w_e and not w_f and not w_g and not w_h:
                    print("ORDER GOOD")
                    w_a=True
                
            if GPIO.input(wires_arr[1]) == GPIO.LOW:
                print("Wire #2 cutted")
                if w_a and not w_b and not w_c and not w_d and not w_e and not w_f and not w_g and not w_h:
                    print("ORDER GOOD")
                    w_b=True
                else:
                    print("ORDER NOT GOOD")
                    
            if GPIO.input(wires_arr[2]) == GPIO.LOW:
                print("Wire #3 cutted")
                if w_a and w_b and not w_c and not w_d and not w_e and not w_f and not w_g and not w_h:
                    print("ORDER GOOD")
                    w_c=True
                else:
                    print("ORDER NOT GOOD")
                    
            if GPIO.input(wires_arr[3]) == GPIO.LOW:
                print("Wire #4 cutted")
                if w_a and w_b and w_c and not w_d and not w_e and not w_f and not w_g and not w_h:
                    print("ORDER GOOD")
                    w_d=True
                else:
                    print("ORDER NOT GOOD")
                    
            if GPIO.input(wires_arr[4]) == GPIO.LOW:
                print("Wire #5 cutted")
                if w_a and w_b and w_c and w_d and not w_e and not w_f and not w_g and not w_h:
                    print("ORDER GOOD")
                    w_e=True
                else:
                    print("ORDER NOT GOOD")
                    
            if GPIO.input(wires_arr[5]) == GPIO.LOW:
                print("Wire #6 cutted")
                if w_a and w_b and w_c and w_d and  w_e and not w_f and not w_g and not w_h:
                    print("ORDER GOOD")
                    w_f=True
                else:
                    print("ORDER NOT GOOD")
                    
                    
            if GPIO.input(wires_arr[6]) == GPIO.LOW:
                print("Wire #7 cutted")
                if w_a and w_b and w_c and  w_d and  w_e and w_f and not w_g and not w_h:
                    print("ORDER GOOD")
                    w_g=True
                else:
                    print("ORDER NOT GOOD")
                    
                    
            if GPIO.input(wires_arr[7]) == GPIO.LOW:
                print("Wire #8 cutted")
                if w_a and w_b and w_c and  w_d and  w_e and  w_f and  w_g and not w_h:
                    print("ORDER GOOD")
                    w_h=True
                else:
                    print("ORDER NOT GOOD")
                
                
            time.sleep(1)
            
       
        printOnLcD("BOOOOOOM!!",3)
        
        os.remove(PID_FILE)
    
        self.terminate()
        

def touch(path):
    with open(path, 'a'):
        os.utime(path, None)

        

     
if __name__ == '__main__':

    try:
    
        #GPIO.wait_for_edge(24, GPIO.FALLING)
    
    
    
        #Create Class
        Stopwatch = CountdownProgram()
        #Create Thread
        StopwatchThread = Thread(target=Stopwatch.run) 
        #Start Thread 
        StopwatchThread.start()

        
        
        
        
        #Create Class
        DefuseBomb = WiresCheck()
        #Create Thread
        DefuseBombThread = Thread(target=DefuseBomb.run) 
        #Start Thread 
        DefuseBombThread.start()
        
        
    
        
        
    except KeyboardInterrupt:
        pass        

        



