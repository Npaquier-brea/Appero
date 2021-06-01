import numpy as np
import threading
import time

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print("Starting ", self.name)
        threadLock.acquire()
        print_time(self.name, self.counter, 3)
        threadLock.release()
        
def print_time(threadName, delay, counter):
    while counter:
        time.sleep(delay)
        print ("%s: %s" % (threadName, time.ctime(time.time())))
        counter -= 1


fileName = "nbrThreads.txt"
file = open(fileName, "r")

nbThreads = None
for elt in file:
    nbThreads = int(elt) 



threadLock = threading.Lock()
threads = []

for i in range(nbThreads):
    thread1 = myThread(1, "Thread-" + str(i), i)
    thread1.start()
    threads.append(thread1)

for t in threads:
   t.join()
print ("Exiting Main Thread")