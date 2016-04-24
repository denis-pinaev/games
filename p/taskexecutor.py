"""Package for concurrent operations
"""

from concurrent.futures import ThreadPoolExecutor, Future
import threading

class TaskExecutor():
    """
    Runs concurrent tasks
    
    - initial parameter is number of concurrent threads
    
    - run method applies task, iterator, fail_function
    """
    
    _executor = None
    _io_lock = threading.RLock()
    _concurrency = 10
    _task = lambda _: None
    _on_fail = lambda _: None
    _iterator = iter([])
    _available = False
    result = Future()
    
    def __init__(self, concurrency=10):
        self._concurrency = concurrency
        self._executor = ThreadPoolExecutor(concurrency)
        self._available = True

    def _submit(self):
        try:
            obj = next(self._iterator)
        except StopIteration:
            return
        if self.result.cancelled():
            return
        self.result.stats['delayed'] += 1
        future = self._executor.submit(self._task, obj)
        future.obj = obj
        future.add_done_callback(self._upload_done)

    def _upload_done(self, future):
        with self._io_lock:
            self._submit()
            self.result.stats['delayed'] -= 1
            self.result.stats['done'] += 1
        if future.exception():
            self._on_fail(future.exception(), future.obj)
        if self.result.stats['delayed'] == 0:
            self.result.set_result(self.result.stats)

    def _cleanup(self, _):
        self._available = False
        with self._io_lock:
            self._executor.shutdown(wait=False)
            
    def run(self, task, iterator, on_fail=lambda _: None):
        if not self._available: raise Exception("Executor is not _available")
        
        self._iterator = iterator
        self._task = task
        self._on_fail = on_fail

        self.result = Future()
        self.result.stats = {'done': 0, 'delayed': 0}
        self.result.add_done_callback(self._cleanup)
        
        with self._io_lock:
            for _ in range(self._concurrency):
                self._submit()

        return self.result

def run_tasks(task, iterator, final_callback=lambda _:None, on_error=lambda _e,_o:None):
    """
    runs task for each element in iterator, if failed with raised error returned on_error
    when completed future returned to final_callback 
    """
    r = TaskExecutor(10).run(task, iterator, on_error)
    while True:
        try:
            r.result()
        except:
            None
        if r.stats["delayed"] == 0:
            final_callback(r)
            break
    
