from concurrent.futures import ThreadPoolExecutor, Future
import threading
import datetime

class TaskExecutor():
    
    executor = None
    io_lock = threading.RLock()
    result = Future()
    concurrency = 10
    task = lambda _: None
    on_fail=lambda _: None
    iterator = iter([])
    
    def __init__(self, concurrency=10):
        self.concurrency = concurrency
        
    def submit(self):
        try:
            obj = next(self.iterator)
        except StopIteration:
            return
        if self.result.cancelled():
            return
        self.result.stats['delayed'] += 1
        self.future = self.executor.submit(self.task, obj)
        self.future.obj = obj
        self.future.add_done_callback(self.upload_done)

    def upload_done(self, future):
        with self.io_lock:
            self.submit()
            self.result.stats['delayed'] -= 1
            self.result.stats['done'] += 1
        if future.exception():
            self.on_fail(future.exception(), future.obj)
        if self.result.stats['delayed'] == 0:
            self.result.set_result(self.result.stats)

    def cleanup(self, _):
        with self.io_lock:
            self.executor.shutdown(wait=False)
            
    def run(self, task, iterator, on_fail=lambda _: None):
        self.iterator = iterator
        self.task = task
        self.on_fail = on_fail

        self.executor = ThreadPoolExecutor(self.concurrency)
        self.result = Future()
        self.result.stats = {'done': 0, 'delayed': 0}
        self.result.add_done_callback(self.cleanup)
        
        with self.io_lock:
            for _ in range(self.concurrency):
                self.submit()

        return self.result

class TestIterator():
    array = []
    counter = 0
    
    def __init__(self, array):
        self.array = array
        
    def __iter__(self):
        return self
    
    def next(self):
        if len(self.array) <= self.counter:
            raise StopIteration
        else:
            self.counter += 1
            return self.array[self.counter-1]
        
def test_task(obj):
    None#print "d", obj
    
def printX(_):
    print "e", _
    
def end(r):
    print r.result()
    finish_time = datetime.datetime.now()
    print (finish_time - start_time)
    print finish_time 
#task_queue(test_task, TestIterator([1,3,5,6,7,8,9,"s"]), 10, lambda x: printX(x))
#r = task_queue(test_task, TestIterator(xrange(200)), 10, lambda x: printX(x))
start_time = datetime.datetime.now()
print start_time
te = TaskExecutor(100)
r = te.run(test_task, TestIterator(xrange(20000)))
print r.result()
r = te.run(printX, TestIterator(xrange(200)))
print r.result()
