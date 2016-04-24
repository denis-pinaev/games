"""Includes functions for second task
"""

import threading
import os
import zipfile
import csv
import xml.etree.ElementTree as ET
from taskexecutor import run_tasks
from config import *
from router import Router
from utils import TimeCounter, rm_rf

def error_zip_extracted(error, future):
    print "ERROR [error_zip_extracted]:", error, "IN", future.obj
    
def extract_zip_files():
    zip_file_names = []
    for d, dirs, files in os.walk(input_zip_file_path):
        for f in files:
            if f[-3:] == "zip":
                zip_file_names.append(os.path.join(d, f))
    run_tasks(extract_zip_file, iter(zip_file_names), final_zip_extracted_callback, error_zip_extracted)
    
def final_zip_extracted_callback(r):
    Router.send(Router.State.extract_zip_files_done)
    
def final_get_xml_data_callback(r):
    Router.send(Router.State.collect_xml_data_done)
    
def get_xml_data(file_name):
    global xml_data
    try:
        tree = ET.parse(file_name)
        root = tree.getroot()
        gen_data={}
        for var in root.iter("var"):
            attrib = var.attrib
            if attrib.has_key("name") and attrib.get("name") == "id" and attrib.has_key("value"):
                id = attrib.get("value")
                gen_data["id"] = id
            if attrib.has_key("name") and attrib.get("name") == "level" and attrib.has_key("value"):
                level = attrib.get("value")
                gen_data["level"] = level
        if gen_data.has_key("id"):
            gen_data["objects"] = []
            for var in root.iter("objects"):
                for var2 in var.iter("object"):
                    attrib = var2.attrib
                    if attrib.has_key("name"):
                        name = attrib.get("name")
                        gen_data["objects"].append(name)
        with threading.RLock():
            xml_data[file_name] = gen_data
    except Exception as e:
        print type(e), e

def generate_csv():
    if os.path.exists(output_csv_file_path):
        timer = TimeCounter()
        rm_rf(output_csv_file_path)
        print timer.stop(), 'clear old output csv files'
    timer = TimeCounter()
    os.mkdir(output_csv_file_path)
    xml_file_names = []
    for d, dirs, files in os.walk(output_zip_file_path):
        for f in files:
            if f[-3:] == "xml":
                xml_file_names.append(os.path.join(d, f))
    timer = TimeCounter()
    run_tasks(get_xml_data, iter(xml_file_names), final_get_xml_data_callback)
    
    
def extract_zip_file(file_name):
    try:
        if not os.path.exists(output_zip_file_path):
            os.mkdir(output_zip_file_path)
        output_directory = os.path.join(output_zip_file_path, file_name[len(input_zip_file_path):-4])
        if not os.path.exists(output_directory):
            os.mkdir(output_directory)
        zip_file = zipfile.ZipFile(file_name, "r")
        for file_name_in_zip in zip_file.namelist():
            zip_file.extract(file_name_in_zip, output_directory)
        zip_file.close()
    except Exception as e:
        print type(e), e
        
def write_data_to_csv():
    with open('%sid_level.csv' % output_csv_file_path, 'w') as csvfile:
        fieldnames = ['id', 'level']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for file_name in xml_data:
            item = xml_data[file_name]
            writer.writerow({'id': item["id"], 'level': item["level"]})
    with open('%sid_objects.csv' % output_csv_file_path, 'w') as csvfile:
        fieldnames = ['id', 'object']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for file_name in xml_data:
            item = xml_data[file_name]
            for object in item["objects"]:
                writer.writerow({'id': item["id"], 'object': object})
    Router.send(Router.State.save_csv_data_done)
    
xml_data = {}
#clear_tests()
#create_zip_files()
#clear_tests()