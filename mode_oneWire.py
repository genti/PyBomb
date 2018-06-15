# Questo codice e' stato realizzato per l'asd GUARDIANI DEL PO 
# non si tratta di un vero ordigno ma bensi' si un giocattolo 
# atto a ricreare funzionalita' di un vero ordingno a tempo. 
# Davide Gentilucci, l'asd NARCOS e l'asd I GUARDIANI DEL PO non si assumono responsabilia' 
# alcuna per l'uso improprio di questo script
from threading import Thread,Semaphore
import pyximport; 
pyximport.install()

import time,os
import lcddriver
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

global lcd,enabled
log_enabled = True
lcd = lcddriver.lcd()

global PID_FILE
PID_FILE='/home/pi/TIMER_RUNNING'

global screenlock
screenlock = Semaphore(value=1)

global version,defuseError,errors
version = '0.7'

#max errori ammessi
errors=1;

global arr,wires_arr,cutted_wires
wires_arr=[]
cutted_wires=[]

def printLog(str):
    if log_enabled:
        print str
        
def printOnLcD(str,row):
    screenlock.acquire()
    lcd.display_string(str.center(20),row) 
    screenlock.release()    
 
def suonaBuzzer(sec):
    printLog("SUONA")
    GPIO.output(5,GPIO.LOW)
    time.sleep(sec)
    GPIO.output(5,GPIO.HIGH)
    printLog("SUONA STOP")
    time.sleep(.05)
    GPIO.cleanup() 
    
def getWiresOrder():
    #genero l'array per il controllo dinnesco, il primo disinnesca 
    file = open("/home/pi/scripts/PyBomb/html/game_config.txt", "r")
    arr = file.read().split("|")
    arr = arr[1].split(" ")
    arr=filter(None,map(int, arr))
    #arr=[4,3,1,2] 
    return arr
    
def getTimeFromString():   
    file = open("/home/pi/scripts/PyBomb/html/game_config.txt", "r")
    arr = file.read().split("|")
    arr = arr[2].split(" ") 
    time=(int(arr[0])*3600)+(int(arr[1])*60)+(int(arr[2]))
    return time        
    
def touch(path):
    with open(path, 'a'):
        os.utime(path, None)   
        
def wireCuttedCheck(channel):
    global defuseError,defused,cutted_wires,wires_arr
    
    printLog (channel)
    printLog (cutted_wires)
    if ((channel == wires_arr[0]) and not(channel in cutted_wires)) : #il primo filo dell'array fili disinnesca la bomba
        #bomba disinnescata
        defused=True   
        defuseError=False
    else: #gli altri dano errore
        #errore disinnesco
        printLog (wires_arr[0])
        
        defused=False   
        defuseError=True
    cutted_wires.append(channel) 
    GPIO.remove_event_detect(channel) 
              
class CountdownProgram:  
    def __init__(self):
        self._running = True
        global timer_rem
        timer_rem = getTimeFromString()
    def terminate(self):  
        self._running = False  
    
    def run(self): 
        i=0
        inc=True
        global timer_rem
        DefuseBomb = WiresCheck()
        DefuseBombThread = Thread(target=DefuseBomb.run) 
        DefuseBombThread.start()
        while self._running:
            
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
        global wires_arr
        self._running = True
        
        wires_arr=getWiresOrder()
        GPIO.setup(wires_arr, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        for wire in wires_arr: 
            GPIO.add_event_detect(wire, GPIO.RISING, callback=wireCuttedCheck, bouncetime=2000)
                
                
    def terminate(self):  
        self._running = False 
        
    def run(self):
        global timer_rem,defused,defuseError
        
        defuseError=False;
        defuseError_counter=0;
        defused=False;
   
        while Stopwatch._running:
   
            if defuseError:
                printLog ("defuse error")
                defuseError_counter=defuseError_counter+1;
                timer_rem = timer_rem/2;
                defuseError=False
                if errors > 1:
                    printOnLcD("",3)
                    printOnLcD("!!! WARNING !!!",4)
            if defuseError_counter == errors:
                Stopwatch.terminate()

            if defused:
                Stopwatch.terminate()
      
            time.sleep(0.5)
            
        if not defused:
            printOnLcD("BOOOOOOM!!",3)
            printOnLcD("YOU LOOSE",4)
            #suonaBuzzer(3)
        else:
            Stopwatch.terminate()
            printOnLcD("BOMB",3)
            printOnLcD("DEFUSED",4)
        os.remove(PID_FILE)
        self.terminate()

        
if __name__ == '__main__':
    try:
        started = False
        b=False
        GPIO.cleanup() 
        GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        touch(PID_FILE)
        printLog ("__init__")
        
        #buzzer
        GPIO.setup(5,GPIO.OUT)
        GPIO.output(5,GPIO.HIGH)
               
        while not started:
            
            printLog ("loop started")    
            if not b:
                printOnLcD("GDP PyBomb v %s" % version,1) 
                printOnLcD("Innesca con chiave",3)               
                b=True
                time.sleep(.5)
            if not started and GPIO.input(21) == GPIO.HIGH:   
                printOnLcD("",3) 
                Stopwatch = CountdownProgram()
                StopwatchThread = Thread(target=Stopwatch.run) 
                StopwatchThread.start()
                
            
                started = True
            
                
            time.sleep(.5)
    except KeyboardInterrupt:
        GPIO.cleanup() 
        pass        