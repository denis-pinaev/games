"""Router provides workflow for all test process
"""


from utils import TimeCounter, rm_rf
from config import input_zip_file_path, output_zip_file_path

class Router():
    """
    provides workflow for all test process
    """
    
    timer = None
    total_timer = None
    debud_message = True
    
    class State():
        initial_clean_old_files = "initial_clean_old_files"
        initial_clean_old_files_done = "initial_clean_old_files_done"
        read_xml_template = "read_xml_template"
        read_xml_template_done = "read_xml_template_done"
        create_zip_files = "create_zip_files"
        create_zip_files_done = "create_zip_files_done"
        extract_zip_files = "extract_zip_files"
        extract_zip_files_done = "extract_zip_files_done"
        collect_xml_data = "collect_xml_data"
        collect_xml_data_done = "collect_xml_data_done"
        generate_csv_data = "collect_xml_data"
        generate_csv_data_done = "collect_xml_data_done"
        save_csv_data = "save_csv_data"
        save_csv_data_done = "save_csv_data_done"
        final_clean_old_files = "final_clean_old_files"
        final_clean_old_files_done = "final_clean_old_files_done"
    
    @staticmethod
    def send(message):
        Router.print_message(message)
        if message == Router.State.initial_clean_old_files:
            Router.start_timer()
            rm_rf(input_zip_file_path)
            rm_rf(output_zip_file_path)
            Router.send(Router.State.initial_clean_old_files_done)
        elif message == Router.State.initial_clean_old_files_done:
            Router.stop_timer("ROUTER: initial input & output temp data removed")
            Router.send(Router.State.read_xml_template)
        elif message == Router.State.read_xml_template:
            Router.start_total_timer_if_not_launched()
            Router.start_timer()
            createtask.read_xml_template()
        elif message == Router.State.read_xml_template_done:
            Router.start_total_timer_if_not_launched()
            Router.stop_timer("ROUTER: xml template read")
            Router.send(Router.State.create_zip_files)
        elif message == Router.State.create_zip_files:
            Router.start_total_timer_if_not_launched()
            Router.start_timer()
            createtask.create_zip_files()
        elif message == Router.State.create_zip_files_done:
            Router.start_total_timer_if_not_launched()
            Router.stop_timer("ROUTER: zip files created")
            Router.send(Router.State.extract_zip_files)
        elif message in Router.State.extract_zip_files:
            Router.start_total_timer_if_not_launched()
            Router.timer = TimeCounter()
            analyzertask.extract_zip_files()
        elif message == Router.State.extract_zip_files_done:
            Router.start_total_timer_if_not_launched()
            Router.stop_timer("ROUTER: zip files extracted")
            Router.send(Router.State.generate_csv_data)
        elif message in Router.State.generate_csv_data:
            Router.start_total_timer_if_not_launched()
            Router.timer = TimeCounter()
            analyzertask.generate_csv()
        elif message == Router.State.generate_csv_data_done:
            Router.start_total_timer_if_not_launched()
            Router.stop_timer("ROUTER: csv files data collected")
            Router.send(Router.State.save_csv_data)
        elif message == Router.State.save_csv_data:
            Router.start_total_timer_if_not_launched()
            Router.print_message("ROUTER: write data to csv")
            Router.timer = TimeCounter()
            analyzertask.write_data_to_csv()
        elif message == Router.State.save_csv_data_done:
            Router.start_total_timer_if_not_launched()
            Router.stop_timer("ROUTER: csv data saved")
            Router.stop_total_timer("ROUTER: TEST COMPLETED")
            Router.send(Router.State.final_clean_old_files)
        elif message == Router.State.final_clean_old_files:
            Router.start_total_timer_if_not_launched()
            rm_rf(input_zip_file_path)
            rm_rf(output_zip_file_path)
            Router.send(Router.State.final_clean_old_files_done)
        elif message == Router.State.final_clean_old_files_done:
            Router.stop_timer("ROUTER: final input & output temp data removed")
        else:
            Router.start_total_timer_if_not_launched()
            Router.print_message("ERROR: unknown message: %s" % message)
            Router.stop_total_timer("ROUTER: stopped on error")

    @staticmethod
    def start_timer():
        Router.timer = TimeCounter()

    @staticmethod
    def stop_timer(message = None):
        if Router.timer and message:
            print Router.timer.stop(), message
            
    @staticmethod
    def start_total_timer_if_not_launched():
        if not Router.total_timer:
            Router.total_timer = TimeCounter()
            
    @staticmethod
    def stop_total_timer(message = None):
        if Router.total_timer and message:
            print Router.total_timer.stop(), message
            
    @staticmethod
    def print_message(message, debug=True):
        if Router.debud_message or not debug:
            print "ROUTER:", message
        
    def __unicode__(self):
        return "ROUTER"

import createtask, analyzertask
