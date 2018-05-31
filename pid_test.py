import os

PID_FILE='/home/pi/TIMER_RUNNING'

def touch(path):
    with open(path, 'a'):
        os.utime(path, None)
        
        

if os.path.exists(PID_FILE):
    print "file exist";
    os.remove(PID_FILE)
    print "file deleted";
else:
    touch(PID_FILE)