import numpy as np
import os
import sys
import time
import math
import datetime
import requests
from xml.etree import ElementTree as ET
import scipy.io.wavfile
from multiprocessing import Process

## == CONST ==
SAMPLE = "sample"  # sample string
CURRENT = "current"  # current string
SAMP_RATE = 48000
CHUNK = 2 ** 11
## ==


def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)


class TimeFormat(object):
    def __init__(self, time):
        self.timeUTC = datetime.datetime.strptime(time[:-1], "%Y-%m-%dT%H:%M:%S.%f")
        self.timeLOCAL = self.timeUTC.replace(tzinfo=datetime.timezone.utc).astimezone(tz=None)

    def utc(self):
        return datetime.datetime.strftime(self.timeUTC, '%Y%m%d_%H%M%S.%fZ')

    def local(self):
        return datetime.datetime.strftime(self.timeLOCAL, '%Y%m%d_%H%M%S.%f')


def recording(times, agent, sensor, startSeq, lengthSeq, MTCONNECT_STR, name, timezone, save_folder):
    for j in range(times):
        print("\n========== {}th collection from {} has started. ==========".format(j + 1, sensor))
        url_updated = agent + "?from=" + str(startSeq) + "&path=//DataItem[@id=%27" + str(sensor) + "%27]"
        response = requests.get(url_updated)
        root = ET.fromstring(response.content)
        header = root.find("./" + MTCONNECT_STR + "Header")
        header_attribs = header.attrib
        nextSeq = int(header_attribs["nextSequence"])  # get next sequence

        i = 0  # ith sequence index
        array = []  # initialize array

        while lengthSeq > i - 1:
            try:
                response = requests.get(url_updated)
                root = ET.fromstring(response.content)
                header = root.find("./" + MTCONNECT_STR + "Header")
                header_attribs = header.attrib
                nextSeq = int(header_attribs["nextSequence"])  # get next sequence

                for sample in root.iter(MTCONNECT_STR + "DisplacementTimeSeries"):
                    i += 1
                    if i == 1:
                        timestamp = sample.get('timestamp')
                        if timezone == "local":
                            timestr = TimeFormat(timestamp).local()
                        else:
                            timestr = TimeFormat(timestamp).utc()
                        filename = "_".join([timestr, name, sensor])
                        wav_output_filename = os.path.join(save_folder, f"{filename}.wav")  # Save in the provided folder
                        chunk = np.fromstring(sample.text, dtype=np.int16, sep=' ')
                        array.append(chunk)
                    else:
                        if lengthSeq == i - 1:
                            sequence = sample.get('sequence')
                        elif lengthSeq < i - 1:
                            pass
                        else:
                            try:
                                chunk = np.fromstring(sample.text, dtype=np.int16, sep=' ')
                                array.append(chunk)
                            except Exception as e:
                                print(e)
                                i -= 1
                                continue
                time.sleep(1)
                url_updated = agent + "?from=" + str(nextSeq) + "&path=//DataItem[@id=%27" + sensor + "%27]"

            except KeyboardInterrupt:
                print("Stopping collecting...")
                break

        data = np.concatenate(array, axis=0)
        print("{}: {}th collection is done ({:.2f} seconds, {})".format(sensor, j + 1, len(data) / SAMP_RATE, wav_output_filename))

        scipy.io.wavfile.write(wav_output_filename, SAMP_RATE, data.astype(np.int16))
        startSeq = int(sequence)


if __name__ == "__main__":
    args = sys.argv[1:]

    if len(args) != 5:
        print("<Usage error!>")
        print("< direction > $ python3 program.py IP:Port name timezone record_time(sec) total_time(sec)")
        print("<description> arguments: IP:Port:str, name:str, timezon:str (local or UTC), record_time:Int (second), total_time:Int (second)")
        print("<  example  > $ python3 sound_collector.py 127.0.0.1:5001 VM20i local 3600 36000")
        print("<description> For 10 hours (total time), 10 wav files will be generated of 1-hour long from the localhost with specified timezone (local or UTC).")
        print("title example: yyyyMMdd_HHmmss.fZ_VM20i_sensor0.wav")
        sys.exit()
    else:
        IP_Port = args[0]
        name = args[1]
        timezone = args[2]
        recordtime = int(args[3])
        totaltime = int(args[4])

    times = math.ceil(totaltime / recordtime)

    print("Sound Collection Info.:\n",
          "Machine (name):", name, "\n",
          "Timezone (title):", timezone, "\n",
          "Each file length:", recordtime, "[sec]\n",
          "Total length:", totaltime, "[sec]\n",
          "Number of files:", times)
    print("========== collection started ==========\n")

    # Specify the folder where the files will be saved
    save_folder = r"C:/Users/TUPUProject/Desktop/Printer Recording/Sound Files"  # You can modify this path to your desired folder
    createFolder(save_folder)  # Ensure the folder exists

    agent = "http://" + IP_Port + "/"  # MTConnect agent server .. args
    response = requests.get(agent + CURRENT)  # get XML response
    root = ET.fromstring(response.content)  # XML Parsing

    MTCONNECT_STR = root.tag.split("}")[0] + "}"
    header = root.find("./" + MTCONNECT_STR + "Header")  # Find Header root to find
    header_attribs = header.attrib  # attribute of header

    nextSeq = int(header_attribs["nextSequence"])  # get next sequence
    firstSeq = int(header_attribs["firstSequence"])  # get first sequence
    lastSeq = int(header_attribs["lastSequence"])  # get last sequence

    devices = []  # devices list
    sensors = []  # sensors list
    for device in root.iter(MTCONNECT_STR + "DeviceStream"):
        deviceName = device.get('name')  # get Device name
        devices.append(deviceName)
        print('Device name:', devices)
        for sample in device.iter(MTCONNECT_STR + "DisplacementTimeSeries"):  # get Sensor name
            sensorName = sample.get('name')
            sensors.append(sensorName)
            print("Sensor name:", sensorName)

    startSeq = lastSeq  # start sequence is the last sequence (latest sequence)

    lengthSeq = int(recordtime / (CHUNK / SAMP_RATE))  # total length of the sequence

    procs = []  # multi-process list

    for i in range(len(sensors)):  # setting up starting multi-processes
        proc = Process(target=recording, args=(times, agent + SAMPLE, sensors[i], startSeq, lengthSeq, MTCONNECT_STR, name, timezone, save_folder))
        procs.append(proc)
        proc.start()

    for proc in procs:  # merging all multi-processes
        proc.join()

    print("Collection Done!")
