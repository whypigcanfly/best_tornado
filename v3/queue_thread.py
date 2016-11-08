import Queue
import threading
from  threading import Thread

class _Worker(Thread):
    '''
    worker thread which get task from queu to execute
    '''

    def __init__(self, threadname, workQueue, parent):
        threading.Thread.__init__(self, name=threadname)
        self.__parent = parent
        self.__workQueue = workQueue
        self.stop = False

    def run(self):
        while not self.stop:
            try:
                callback = self.__workQueue.get()
                if not callback:
                    continue
                     
                try:
                    callback()
                except Exception as processEx:
		    print 'error'
            except IOError:
                pass
            except Exception as getEx:
           	print 'error' 

class _WorkerManager(object):
    
    @classmethod
    def instance(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
        return cls._instance
        
    def initialize(self, workerCount=5):
        self.__workQueue = Queue.Queue(maxsize=10)
        self.__workerCount = workerCount
        self.__workers = []   
        for i in range(self.__workerCount):
            worker = _Worker("_Worker-" + str(i + 1), self.__workQueue, self)
            worker.start()
            self.__workers.append(worker)
            
    def add_task(self, callback):
        self.__workQueue.put(callback)


ThreadPool = _WorkerManager.instance()


