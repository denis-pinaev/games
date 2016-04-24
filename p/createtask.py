import os
import zipfile
import random
from utils import TimeCounter, get_random_int, get_random_string, get_unique_sting, rm_rf, read_file, save_file
from taskexecutor import run_tasks
from config import *
from router import Router


def generate_lines(times = 1):
    lines = ""
    sample_line = "<object name='%s'/>"
    for _ in xrange(times):
        lines += sample_line % get_random_string(create_count_max_lines_per_xml)
    return lines
        
def read_xml_template():
    global xml_template
    if not xml_template:
        xml_template = read_file("xml_sample.txt")
    Router.send(Router.State.read_xml_template_done)
    
def generate_xml_file():
    global xml_template
    params = {
        "unique_string" : get_unique_sting(),
        "random_int" : get_random_int(100),
        "random_lines" : generate_lines(random.randint(1,10))
    }
    xml_text = xml_template.format(**params) 
    return xml_text

def generate_save_files(direcory="./", count=10):
    if not os.path.exists(direcory):
        os.mkdir(direcory)
    for i in xrange(count):
        file_name = "%stest_xml_%03d.xml" % (direcory, i)
        save_file(generate_xml_file(), file_name)

def generate_zip_file(file_count=1):
    try:
        if not os.path.exists(input_zip_file_path):
            os.mkdir(input_zip_file_path)
        directory = "%stmp_%02d/" % (input_zip_file_path, file_count)
        generate_save_files(directory, create_count_xml_in_zip)
        file_name = "%szip_%02d.zip" % (input_zip_file_path, file_count)
        zip_file = zipfile.ZipFile(file_name, "w")
        for d, dirs, files in os.walk(directory):
            for f in files:
                path = os.path.join(d, f)
                zip_file.write(path,f)
        zip_file.close()
    except Exception as e:
        print type(e), e
        
def create_zip_files():
    global xml_template
    if not xml_template:
        xml_template = read_file(create_xml_sample_file)
    run_tasks(generate_zip_file, iter(xrange(create_count_zip_files)), create_zip_files_final_callback)
    
def create_zip_files_final_callback(r):
    Router.send(Router.State.create_zip_files_done)
    

xml_template = None