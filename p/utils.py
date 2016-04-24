import datetime
import os
import uuid
import random

class TimeCounter():
    """
    counts process timing
    """
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
    if not os.path.exists(d): return
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
