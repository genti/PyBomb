# Questo codice e' stato realizzato per l'asd GUARDIANI DEL PO 
# non si tratta di un vero ordigno ma bensi' si un giocattolo 
# atto a ricreare funzionalita' di un vero ordingno a tempo con 
# possibilita' di essere disinnescato tagliando dei fili in 
# ordine specifico. Davide Gentilucci, l'asd NARCOS e l'asd I GUARDIANI DEL PO non si assume responsabilia' 
# alcuna per l'uso improprio di questo script
from threading import Thread,Semaphore
import pyximport; 
pyximport.install()

import time,os
import lcddriver
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

global lcd,enabled
log_enabled = False
lcd = lcddriver.lcd()

global PID_FILE
PID_FILE='/home/pi/TIMER_RUNNING'

global screenlock 
screenlock = Semaphore(value=1)

global version
version = '0.5'

global arr
wires_arr=[]

def printLog(str):
    if log_enabled:
        print str
        
def printOnLcD(str,row):
    screenlock.acquire()
    lcd.display_string(str.center(20),row) 
    screenlock.release()    
   

def getWiresOrder():
    file = open("/home/pi/scripts/PyBomb/html/wires.txt", "r")
    arr = file.read().split(" ")
    arr=filter(None,map(int, arr))
    return arr

def touch(path):
    with open(path, 'a'):
        os.utime(path, None)   
        
class CountdownProgram:  
    def __init__(self):
        self._running = True
    def terminate(self):  
        self._running = False  
    def getTimeFromString(self):
        file = open("/home/pi/scripts/PyBomb/html/time.txt", "r")
        arr = file.read() .split(" ")
        time=(int(arr[0])*3600)+(int(arr[1])*60)+(int(arr[2]))
        return time    
    def run(self): 
        i=0
        inc=True
        
        DefuseBomb = WiresCheck()
        DefuseBombThread = Thread(target=DefuseBomb.run) 
        DefuseBombThread.start()
        while self._running:
            timer_rem=self.getTimeFromString()
            while timer_rem >0 and self._running:
                timer_rem=timer_rem-1
                m, s = divmod(timer_rem, 60)
                h, m = divmod(m, 60)
                time_str="%02d:%02d:%02d" % (h, m, s)
                printOnLcD(time_str,2)    
                time.sleep(1)
            self.terminate()
##classe gestione disinnesco                   
class WiresCheck:  
    def __init__(self):
        self._running = True
        self.w_a = self.w_b = self.w_c = self.w_d = self.w_e = self.w_f = self.w_g = self.w_h = False
        self.wires_arr=getWiresOrder()
        GPIO.setup(self.wires_arr, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
    def terminate(self):  
        self._running = False 
        
    def run(self):
        defuseError=False;
        defuseCorrect=0;
        defused=False;
        
        while Stopwatch._running:
            if defuseCorrect == 1:
                str="Defusing"
                printOnLcD(str,3)
                              
            if defuseCorrect == 0:
                str="Defuse it!"
                printOnLcD(str,3)  
            
            printOnLcD("%s wires remains" % (4-defuseCorrect),4)
            
            #############################################
            if len(self.wires_arr) > 0:
                if GPIO.input(self.wires_arr[0]) == GPIO.HIGH and not self.w_a:
                    printLog("Wire #1 cutted")
                    if not self.w_a and not self.w_b and not self.w_c and not self.w_d and not self.w_e and not self.w_f and not self.w_g and not self.w_h:
                        printLog("ORDER GOOD")
                        defuseCorrect+=1
                        self.w_a=True
                    else:
                        defuseError=True;
            #############################################
            if len(self.wires_arr) > 1 and not defuseError:    
                if GPIO.input(self.wires_arr[1]) == GPIO.HIGH and not self.w_b:
                    printLog("Wire #2 cutted")
                    if self.w_a and not self.w_b and not self.w_c and not self.w_d and not self.w_e and not self.w_f and not self.w_g and not self.w_h:
                        printLog("ORDER GOOD")
                        defuseCorrect+=1
                        self.w_b=True
                    else:
                        defuseError=True;
            #############################################
            if len(self.wires_arr) > 2 and not defuseError:             
                if GPIO.input(self.wires_arr[2]) == GPIO.HIGH and not self.w_c:
                    printLog("Wire #3 cutted")
                    if self.w_a and self.w_b and not self.w_c and not self.w_d and not self.w_e and not self.w_f and not self.w_g and not self.w_h:
                        printLog("ORDER GOOD")
                        defuseCorrect+=1
                        self.w_c=True
                    else:
                        defuseError=True;
            #############################################
            if len(self.wires_arr) > 3 and not defuseError:         
                if GPIO.input(self.wires_arr[3]) == GPIO.HIGH and not self.w_d:
                    printLog("Wire #4 cutted")
                    if self.w_a and self.w_b and self.w_c and not self.w_d and not self.w_e and not self.w_f and not self.w_g and not self.w_h:
                        printLog("ORDER GOOD")
                        defuseCorrect+=1
                        self.w_d=True
                    else:
                        defuseError=True;
                        
                        
                        
        
            if defuseError:
                Stopwatch.terminate()
            if len(self.wires_arr) == defuseCorrect:
                Stopwatch.terminate()
                defused=True
            printLog ("wire loop      ")
            time.sleep(0.5)
        if not defused:
            printOnLcD("BOOOOOOM!!",3)
            printOnLcD("YOU LOOSE",4)
        else:
            printOnLcD("BOMB",3)
            printOnLcD("DEFUSED",4)
        os.remove(PID_FILE)
        self.terminate()
        GPIO.cleanup() 
     
if __name__ == '__main__':
    try:
        started = False
        b=False
        GPIO.cleanup() 
        GPIO.setup(21, GPIO.IN)
        
        touch(PID_FILE)
        printLog ("__init__")
        while not started:
            
            printLog ("loop started")
            
            #printLog ("MODE: %s, 4:%s, 27: %s,22: %s,25: %s, sw: %s" % (GPIO.getmode(),GPIO.input(4),GPIO.input(27),GPIO.input(22),GPIO.input(25),GPIO.input(21)));
            if not started and GPIO.input(21) == GPIO.HIGH:   
                Stopwatch = CountdownProgram()
                StopwatchThread = Thread(target=Stopwatch.run) 
                StopwatchThread.start()
            
                started = True
            if not b:
                printOnLcD("GDP PyBomb v %s" % version,1) 
                printOnLcD("Gira la chiave per",3)
                printOnLcD("innescare la bomba",4)
                b=True
            time.sleep(.5)
    except KeyboardInterrupt:
        pass        