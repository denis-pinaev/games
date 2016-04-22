from concurrent.futures import ThreadPoolExecutor, Future
import threading
import datetime
import os
import uuid
import random
import zipfile

class TimeCounter():
    start_time = datetime.datetime.now()
    finish_time = datetime.datetime.now()
    
    def __init__(self):
        self.start_time = datetime.datetime.now()
        
    def start(self):
        self.start_time = datetime.datetime.now()
        
    def uptime(self):
        return self.finish_time - self.start_time
    
    def stop(self):
        self.finish_time = datetime.datetime.now()
        return self.uptime()
    
    def __unicode__(self):
        return str(self.uptime())

class TaskExecutor():
    
    executor = None
    io_lock = threading.RLock()
    result = Future()
    concurrency = 10
    task = lambda _: None
    on_fail = lambda _: None
    iterator = iter([])
    available = False
    
    def __init__(self, concurrency=10):
        self.concurrency = concurrency
        self.executor = ThreadPoolExecutor(concurrency)
        self.available = True

    def submit(self):
        try:
            obj = next(self.iterator)
        except StopIteration:
            return
        if self.result.cancelled():
            return
        self.result.stats['delayed'] += 1
        future = self.executor.submit(self.task, obj)
        future.obj = obj
        future.add_done_callback(self.upload_done)

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
        self.available = False
        with self.io_lock:
            self.executor.shutdown(wait=False)
            
    def run(self, task, iterator, on_fail=lambda _: None):
        if not self.available: raise Exception("Executor is not available")
        
        self.iterator = iterator
        self.task = task
        self.on_fail = on_fail

        self.result = Future()
        self.result.stats = {'done': 0, 'delayed': 0}
        self.result.add_done_callback(self.cleanup)
        
        with self.io_lock:
            for _ in range(self.concurrency):
                self.submit()

        return self.result


def read_file(file_name):
    f = open(file_name, "r")
    data = f.read()
    f.close()
    return data

def save_file(data, file_name):
    f = open(file_name, "w")
    f.write(data)
    f.close()

def rm_rf(d):
    for path in (os.path.join(d, f) for f in os.listdir(d)):
        if os.path.isdir(path):
            rm_rf(path)
        else:
            os.unlink(path)
    os.rmdir(d)

def get_unique_sting():
    return uuid.uuid4().hex

def get_random_int(base=100):
    return random.randint(0,base)

def get_random_string(length=10):
    number = '0123456789'
    alpha = 'abcdefghijklmnopqrstuvwxyz'
    id = ''
    for _ in range(0, length, 2):
        id += random.choice(number)
        id += random.choice(alpha)
    return id

def generate_lines(times = 1):
    lines = ""
    sample_line = "<object name='%s'/>"
    for _ in xrange(times):
        lines += sample_line % get_random_string(10)
    return lines
        
def generate_xml_file():
    xml_text = read_file("xml_sample.txt")
    params = {
        "unique_string" : get_unique_sting(),
        "random_int" : get_random_int(100),
        "random_lines" : generate_lines(random.randint(1,10))
    }
    xml_text = xml_text.format(**params) 
    return xml_text

def generate_save_files(direcory="./", count=10):
    if not os.path.exists(direcory):
        os.mkdir(direcory)
    for i in xrange(count):
        file_name = "%stest_xml_%03d.xml" % (direcory, i)
        save_file(generate_xml_file(), file_name)

def generate_zip_file(file_count=1):
    try:
        if not os.path.exists(tmp_file_path):
            os.mkdir(tmp_file_path)
        directory = "%stmp_%02d/" % (tmp_file_path, file_count)
        generate_save_files(directory, 10)
        file_name = "%szip_%02d.zip" % (tmp_file_path, file_count)
        zip_file = zipfile.ZipFile(file_name, "w")
        for d, dirs, files in os.walk(directory):
            for f in files:
                path = os.path.join(d, f)
                zip_file.write(path,f)
        zip_file.close()
    except Exception as e:
        print type(e), e
        
def create_zip_files():
    global timer
    if os.path.exists(tmp_file_path):
        timer = TimeCounter()
        rm_rf(tmp_file_path)
        print timer.stop(), '- clear old files'
    timer = TimeCounter()
    run_tasks(generate_zip_file, iter(xrange(100)), create_zip_files_final_callback)
    
def create_zip_files_final_callback(r):
    global timer
    print timer.stop(), r.stats["done"], "zip files created"

def run_tasks(task, iterator, final_callback=lambda _:None):
    r = TaskExecutor(10).run(task, iterator)
    while True:
        try:
            r.result()
        except: None
        if r.stats["delayed"] == 0:
            final_callback(r)
            break
    
tmp_file_path = "./tmp2/"
create_zip_files()
#rm_rf(tmp_file_path)