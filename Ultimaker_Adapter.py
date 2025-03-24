import time
import datetime
import requests
import json
from data_item import Event, Sample
from mtconnect_adapter import Adapter


def get_data(url:str,req:str):
    try:
        response = requests.get(url+req)
        response.raise_for_status()
        
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
    except KeyError as e:
        print(f"Missing key in response data: {e}")

# MTconnect adapter class
class MTConnectAdapter(object):
    
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.adapter = Adapter((host, port))
        
        # for samples
        self.ambient_temp = Sample('ambient_temp')
        self.adapter.add_data_item(self.ambient_temp)
        
        self.bed_current_temp = Sample('bed_current_temp')
        self.adapter.add_data_item(self.bed_current_temp)
        
        self.bed_target_temp = Sample('bed_target_temp')
        self.adapter.add_data_item(self.bed_target_temp)
        
        self.ext0_current_temp = Sample('ext0_current_temp')
        self.adapter.add_data_item(self.ext0_current_temp)
        
        self.ext0_target_temp = Sample('ext0_target_temp')
        self.adapter.add_data_item(self.ext0_target_temp)
        
        self.ext1_current_temp = Sample('ext1_current_temp')
        self.adapter.add_data_item(self.ext1_current_temp)
        
        self.ext1_target_temp = Sample('ext1_target_temp')
        self.adapter.add_data_item(self.ext1_target_temp)
        
        self.fan_load = Sample('fan_load')
        self.adapter.add_data_item(self.fan_load)
        
        self.xpos = Sample('xpos')
        self.adapter.add_data_item(self.xpos)
        
        self.ypos = Sample('ypos')
        self.adapter.add_data_item(self.ypos)
        
        self.zpos = Sample('zpos')
        self.adapter.add_data_item(self.zpos)        
        
        self.led_brightness = Sample('led_brightness')
        self.adapter.add_data_item(self.led_brightness)
        
        self.up_time = Sample('up_time')
        self.adapter.add_data_item(self.up_time)
        
        self.est_time = Sample('est_time')
        self.adapter.add_data_item(self.est_time)
        
        self.elap_time = Sample('elap_time')
        self.adapter.add_data_item(self.elap_time)
        
        self.total_time = Sample('total_time')
        self.adapter.add_data_item(self.total_time)
        
        self.progress = Sample('progress')
        self.adapter.add_data_item(self.progress)
        
        
        # for events
        self.avail = Event('avail')
        self.adapter.add_data_item(self.avail)
        
        self.printerSerial = Event('printerSerial')
        self.adapter.add_data_item(self.printerSerial)
        
        self.bed_type = Event('bed_type')
        self.adapter.add_data_item(self.bed_type)
        
        self.bed_preheat_state = Event('bed_preheat_state')
        self.adapter.add_data_item(self.bed_preheat_state)
        
        self.ext0_material = Event('ext0_material')
        self.adapter.add_data_item(self.ext0_material)
        
        self.ext1_material = Event('ext1_material')
        self.adapter.add_data_item(self.ext1_material)
        
        self.status = Event('status')
        self.adapter.add_data_item(self.status)
        
        self.program = Event('program')
        self.adapter.add_data_item(self.program)
        
        self.print_state = Event('print_state')
        self.adapter.add_data_item(self.print_state)
        
        self.print_result = Event('print_result')
        self.adapter.add_data_item(self.print_result)
        
        self.datetime_started = Event('datetime_started')
        self.adapter.add_data_item(self.datetime_started)
        
        self.datetime_finished = Event('datetime_finished')
        self.adapter.add_data_item(self.datetime_finished)
                
               
        # start MTConnect
        self.adapter.start()
        self.adapter.begin_gather()
        self.avail.set_value("AVAILABLE")
        self.adapter.complete_gather()
        self.adapter_stream()
        
    def adapter_stream(self):
        try:
            while True:
                printer = get_data(url_api,"printer") # printer req.
                bed_type = printer["bed"]["type"]
                bed_preheat_state = printer["bed"]["pre_heat"]["active"]
                bed_current_temp = printer["bed"]["temperature"]["current"]
                bed_target_temp = printer["bed"]["temperature"]["target"]
                ext0_current_temp = printer["heads"][0]["extruders"][0]["hotend"]["temperature"]["current"]
                ext0_target_temp = printer["heads"][0]["extruders"][0]["hotend"]["temperature"]["target"]
                ext0_material = printer["heads"][0]["extruders"][0]["active_material"]["GUID"]
                ext1_current_temp = printer["heads"][0]["extruders"][1]["hotend"]["temperature"]["current"]
                ext1_target_temp = printer["heads"][0]["extruders"][1]["hotend"]["temperature"]["target"]
                ext1_material = printer["heads"][0]["extruders"][1]["active_material"]["GUID"]
                fan_load = printer["heads"][0]["fan"]
                xpos = printer["heads"][0]["position"]["x"]
                ypos = printer["heads"][0]["position"]["y"]
                zpos = printer["heads"][0]["position"]["z"]
                led_brightness = printer["led"]["brightness"]
                status = printer["status"]
                              
                
                ambient = get_data(url_api,"ambient_temperature") # ambient temperature req.
                ambient_temp = ambient["current"]
                
                
                system = get_data(url_api,"system") # system req.
                printerSerial = system["guid"]
                up_time = system["uptime"]
                
                self.adapter.begin_gather()
                self.bed_type.set_value(str(bed_type))
                self.bed_preheat_state.set_value(str(bed_preheat_state))
                self.bed_current_temp.set_value(str(bed_current_temp))
                self.bed_target_temp.set_value(str(bed_target_temp))
                self.ext0_current_temp.set_value(str(ext0_current_temp))
                self.ext0_target_temp.set_value(str(ext0_target_temp))
                self.ext0_material.set_value(str(ext0_material))
                self.ext1_current_temp.set_value(str(ext1_current_temp))
                self.ext1_target_temp.set_value(str(ext1_target_temp))
                self.ext1_material.set_value(str(ext1_material))
                self.fan_load.set_value(str(fan_load))
                self.xpos.set_value(str(xpos))
                self.ypos.set_value(str(ypos))
                self.zpos.set_value(str(zpos))
                self.led_brightness.set_value(str(led_brightness))
                self.status.set_value(str(status))
                self.ambient_temp.set_value(str(ambient_temp))
                self.printerSerial.set_value(str(printerSerial))
                self.up_time.set_value(str(up_time))
                self.adapter.complete_gather()
                
                if status == "printing": # when printer status is printing...
                    print_job = get_data(url_api,"print_job") # only available when printing... status
                    print_state = print_job["state"]
                    print_result = print_job["result"]
                    program = print_job["name"]
                    datetime_started = print_job["datetime_started"]
                    datetime_finished = print_job["datetime_finished"]
                    est_time = print_job["time_estimated"]
                    elap_time = print_job["time_elapsed"]
                    total_time = print_job["time_total"]
                    progress = print_job["progress"]*100
                    self.adapter.begin_gather()
                    self.print_state.set_value(str(print_state))
                    self.print_result.set_value(str(print_result))
                    self.datetime_started.set_value(str(datetime_started))
                    self.datetime_finished.set_value(str(datetime_finished))
                    self.est_time.set_value(str(est_time))
                    self.elap_time.set_value(str(elap_time))
                    self.total_time.set_value(str(total_time))
                    self.progress.set_value(str(progress))
                    self.program.set_value(str(program))
                    self.adapter.complete_gather()
                    
                else:
                    self.adapter.begin_gather()
                    self.print_state.set_value("UNAVAILABLE")
                    self.print_result.set_value("UNAVAILABLE")
                    self.datetime_started.set_value("UNAVAILABLE")
                    self.datetime_finished.set_value("UNAVAILABLE")
                    self.est_time.set_value("UNAVAILABLE")
                    self.elap_time.set_value("UNAVAILABLE")
                    self.total_time.set_value("UNAVAILABLE")
                    self.progress.set_value("UNAVAILABLE")
                    self.adapter.complete_gather()                    
                
                time.sleep(1)
                          

        except KeyboardInterrupt:
            self.adapter.stop()
            print("Process interruped by user... closing MTConnect adapter...")
        except Exception as e:
            print(f"Cricial error: {e}")
            

if __name__ == "__main__":
    IP = "10.114.4.104" # you should update this if changed.
    url_api = "http://"+IP+"/api/v1/"
    
    print(f"{datetime.datetime.now()} - MTConnect adapter for Ultimaker S5 started...")
    MTConnectAdapter('127.0.0.1', 7878)