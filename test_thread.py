# Questo codice e' stato realizzato per l'asd GUARDIANI DEL PO 
# non si tratta di un vero ordigno ma bensi' si un giocattolo 
# atto a ricreare funzionalita' di un vero ordingno a tempo con 
# possibilita' di essere disinnescato tagliando dei fili in 
# ordine specifico. Davide Gentilucci, l'asd NARCOS e l'asd I GUARDIANI DEL PO non si assume responsabilia' 
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
version = '0.4'

global arr
wires_arr=[]


    
def printOnLcD(str,row):
    screenlock.acquire()
    lcd.lcd_display_string(str.center(20),row) 
    screenlock.release()    

def getWiresOrder():
    file = open("/home/pi/scripts/PyBomb/html/wires.txt", "r")
    arr = file.read().split(" ")
    arr=filter(None,map(int, arr))
    return arr

def touch(path):
    with open(path, 'a'):
        os.utime(path, None)   
        

##classe gestione cronometro   
  
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
        
        
        touch(PID_FILE)
        
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
        
        # interruttore a chiave
        
        
        for pin in self.wires_arr:
            GPIO.setup(pin, GPIO.IN)  

    def terminate(self):  
        self._running = False  
        
    

    def run(self):
    
        defuseError=False;
        defuseCorrect=0;
        defused=False;
        
        while Stopwatch._running:
            
            if (self.w_a or self.w_b or self.w_c or self.w_d or self.w_e or self.w_f or self.w_g or self.w_h):
                str="Defusing"
                printOnLcD(str,3)  
            else:
                str="Defuse it!"
                printOnLcD(str,3)   
                
            
                
                
            #############################################
            if len(self.wires_arr) > 0:
                if GPIO.input(self.wires_arr[0]) == GPIO.HIGH and not self.w_a:
                    print("Wire #1 cutted")
                    if not self.w_a and not self.w_b and not self.w_c and not self.w_d and not self.w_e and not self.w_f and not self.w_g and not self.w_h:
                        print("ORDER GOOD")
                        defuseCorrect+=1
                        self.w_a=True
                    else:
                        defuseError=True;
            #############################################
            #############################################
            if len(self.wires_arr) > 1 and not defuseError:    
                if GPIO.input(self.wires_arr[1]) == GPIO.HIGH and not self.w_b:
                    print("Wire #2 cutted")
                    if self.w_a and not self.w_b and not self.w_c and not self.w_d and not self.w_e and not self.w_f and not self.w_g and not self.w_h:
                        print("ORDER GOOD")
                        defuseCorrect+=1
                        self.w_b=True
                    else:
                        defuseError=True;
            #############################################
            #############################################
            if len(self.wires_arr) > 2 and not defuseError:             
                if GPIO.input(self.wires_arr[2]) == GPIO.HIGH and not self.w_c:
                    print("Wire #3 cutted")
                    if self.w_a and self.w_b and not self.w_c and not self.w_d and not self.w_e and not self.w_f and not self.w_g and not self.w_h:
                        print("ORDER GOOD")
                        defuseCorrect+=1
                        self.w_c=True
                    else:
                        defuseError=True;
            #############################################
            #############################################
            if len(self.wires_arr) > 3 and not defuseError:         
                if GPIO.input(self.wires_arr[3]) == GPIO.HIGH and not self.w_d:
                    print("Wire #4 cutted")
                    if self.w_a and self.w_b and self.w_c and not self.w_d and not self.w_e and not self.w_f and not self.w_g and not self.w_h:
                        print("ORDER GOOD")
                        defuseCorrect+=1
                        self.w_d=True
                    else:
                        defuseError=True;
            #############################################
            #############################################       
            if len(self.wires_arr) > 4 and not defuseError:        
                if GPIO.input(self.wires_arr[4]) == GPIO.HIGH and not self.w_e:
                    print("Wire #5 cutted")
                    if self.w_a and self.w_b and self.w_c and self.w_d and not self.w_e and not self.w_f and not self.w_g and not self.w_h:
                        print("ORDER GOOD")
                        defuseCorrect+=1
                        self.w_e=True
                    else:
                        defuseError=True;
            #############################################
            #############################################
            if len(self.wires_arr) > 5 and not defuseError:         
                if GPIO.input(self.wires_arr[5]) == GPIO.HIGH and not self.w_f:
                    print("Wire #6 cutted")
                    if self.w_a and self.w_b and self.w_c and self.w_d and  self.w_e and not self.w_f and not self.w_g and not self.w_h:
                        print("ORDER GOOD")
                        defuseCorrect+=1
                        self.w_f=True
                    else:
                        defuseError=True;
            #############################################
            #############################################       
            if len(self.wires_arr) > 6 and not defuseError:        
                if GPIO.input(self.wires_arr[6]) == GPIO.HIGH and not self.w_g:
                    print("Wire #7 cutted")
                    if self.w_a and self.w_b and self.w_c and  self.w_d and  self.w_e and self.w_f and not self.w_g and not self.w_h:
                        print("ORDER GOOD")
                        defuseCorrect+=1
                        self.w_g=True
                    else:
                        defuseError=True;
            #############################################
            #############################################        
            if len(self.wires_arr) > 7 and not defuseError:         
                if GPIO.input(self.wires_arr[7]) == GPIO.HIGH and not self.w_h:
                    print("Wire #8 cutted")
                    if self.w_a and self.w_b and self.w_c and  self.w_d and  self.w_e and  self.w_f and  self.w_g and not self.w_h:
                        print("ORDER GOOD")
                        defuseCorrect+=1
                        self.w_h=True
                    else:
                        defuseError=True;
             #############################################
            #############################################   
                
            if defuseError:
                
                Stopwatch.terminate()
            
            if len(self.wires_arr) == defuseCorrect:
                Stopwatch.terminate()
                defused=True
                
            time.sleep(0.5)
            
        if not defused:
            printOnLcD("BOOOOOOM!!",3)
            printOnLcD("YOU LOOSE",4)
        else:
            printOnLcD("BOMB",3)
            printOnLcD("DEFUSED",4)
        
        
        
        os.remove(PID_FILE)
    
        self.terminate()
        



        

     
if __name__ == '__main__':

 

    try:
        
        started = False
        GPIO.setup(21, GPIO.IN) 
       
        while not started:
            if not started and GPIO.input(21) == GPIO.HIGH:

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
                
                started = True
            
            
    
            if not started and GPIO.input(21) == GPIO.LOW:
                printOnLcD("GDP PyBomb v" % version,1) 
                printOnLcD("Girare la chiave",2) 
            
            
            time.sleep(0.5)
            
        
    except KeyboardInterrupt:
        pass        

        



