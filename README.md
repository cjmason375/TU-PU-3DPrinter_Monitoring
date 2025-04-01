# TU-PU-3DPrinter_Monitoring
This repository documents the necessary background, procedures, and code to conduct an experiment alike the one detailed in the paper "**Online and Real-Time 3D Printer Monitoring using MTConnect Data Integration Towards Printing Part Error Diagnostics**". 





### *INTRODUCTION*

  With [Industry 4.0](https://www.ibm.com/topics/industry-4-0) promising to revolutionize the future of smarter factories, it has become increasingly important to ensure machines are able to intelligently communicate with one another utilizing the [Internet of Things (IoT)](https://www.ibm.com/think/topics/internet-of-things) and make decisions based on real-time data analysis and [Articial Intelligence (AI)](https://www.ibm.com/think/topics/artificial-intelligence). As [Additive Manufacturing (AM)](https://mitsloan.mit.edu/ideas-made-to-matter/additive-manufacturing-explained) technologies continue to develop, these processes have become more commonplace in producing final parts rather than prototyping models. However, 3D printing, especially Fused Deposition Modeling (FDM), are susceptible to small defects that can result in large errors in a final part or set of parts. In this project, a MTConnect Framework was implemented to collect three sets of data from a hobbyist Ultimaker S5 3D Printer; sound data, current data, and machine data. The team then analyzed each set for indications of failures within the data, which will then developed into a real-time anomaly and part failure detection model. The adoption of FDM processes into industry can be accelerated utilizing intelligent systems that can automatically detect and correct failures based on real-time continuous data analysis.



### *1) SENSOR INSTALLATION*

  First, sensors must be set up to collect data from the machine. For the study, **machine data** (such as bed temperature, fan speed, camera snapshots, and other sub-component information) could be collected from the Ultimaker API, so external sensors were not necessary for this data. To monitor machine sound, a microphone was installed within the printer's enclosure, and a current transformer was installed onto the printer's main power line to monitor current consumption. The external sensors were then hooked to a Raspberry Pi computer, which would be used as the study's edge computer for collecting data.



### *2) STATIC IP ADDRESSES*

  With the sensors connected, it is then necessary to set up a static IP address on the Raspberry Pi. By default, most devices utilize a Dynamic IP address standard, which constantly changes the device's IP address each time it updates to the network. However, it is necessary to assign a Static IP address to the Raspberry Pi to make it easier to access the Pi in code. Then, the same process must be done to establish a Static IP address on the Ultimaker Printer. Once the Static IP addresses are assigned, note them down for later use in code.



### *3) SETTING UP MTCONNECT*

  [MTConnect](https://www.mtconnect.org) offers a robust and versatile system that can be adopted by modern and legacy machines alike. As the industry standard for manufacturing data integration across multiple machines, utilizing MTConnect for aggregating multiple datasets enabled the team to contextualize collected data while avoiding proprietary formatting. Implementing the free, open-source MTConnect software is not only cost-effective, but also encourages interoperability within factories. Utilizing MTConnect allows further scaling of this project and enables real-time remote monitoring of collected data.

  MTConnect operates based off of two major components: [the ***Adapter*** and the ***Agent***](https://www.mmsonline.com/articles/understanding-mtconnect-agents-and-adapters). The ***Adapter*** collects the data from the machine and/or sensors, converts it into a text dictionary, and passes that dictionary along to the Agent. In other words, it allows the machines to speak in the MTConnect language. In the case study, the machine and current data were combined onto the same adapter, each data group had its own adapter; a 3D printer adapter that utilized the Swagger API to convert status variables into a MTConnect-compliant format, a current transformer adapter for collecting current data, and a sound stream adapter for collecting sound data. The ***Agent*** takes the dictionary from the Adapter, formats it into a XML stream, and makes that data available on the cloud. In our case study, the Agent uses a HTTP-based REST communication standard. Then, the operator can utilize ***applications*** to fully utilize the MTConnect framework, such as accessing monitoring systems or analytics platforms for conducting further processing and visualization. In this study, the "Device.xml" information model served as the application.

![Case Study Setup](https://github.com/user-attachments/assets/addae1b6-0bc5-44c5-9912-1c6d3c1237c5)


#### *3.1) Developing "Device_xml" Data Information Model*

  A Data Information Model takes the information from the Agent and conceptually represents the data's relationships. For the 3D printer's case, the "Device.xml" data information model was created to centralize elements of an operation's process at the same timestamp into a single file. Primarily, electrical, thermal, and mechanical state variables from the machine data adapter and the current adapter were utilized in this information model.
 
 The collected data was combined and put into the XML file format. This file defined the types of data each measuring device collects, along with the frequency and units of that collection. Because files like "Device.xml" are uncommon for 3D printing, categorization and filtering was done to determine a) which variables can be collected by the printer or additional IoT devices, and b) which variables would prove valuable for analysis. After determining these prevalent datapoints from the printer API and the additional sensor of the current transducer, they were fed into the xml file as an element tree. Through this formatting, additional components can be interconnected, expanding the analytic capabilities; a cognizance is required in understanding the format of the data to be included and the required formatting for it.

 To access the "Device.xml" file on your edge computer, upload and run the [Device.xml](https://github.com/cjmason375/TU-PU-3DPrinter_Monitoring/blob/main/Device.xml) file on your edge computer and parse the code to made the necessary edits for your system. Then, you can use the command *"[RPi IP Address]:[RPi port]"* to access the "Device.xml" file for your setup - this can be done on the Raspberry Pi or a seperate computer, but you must ensure both devices are on the same network. A screenshot of the result is shown below:

![Device xml Screenshot](https://github.com/user-attachments/assets/6a83e903-6d15-488a-89aa-3380e736ac3d)

 
  Currently, MTConnect does not support a method to incorporate JPG images into the model, so those had to be collected individually from the API. To access the images at a specific moment, you can use the command *"[PRINTER IP Address]:[PRINTER port]/?action=snapshot"*. 
  
  Continuous sound collection alongside the other ongoing processes has the potential to overload the collection stream and cause errors in collecting other variables. Therefore, the collected audio stream had an independent adapter designated to a seperate device port of the same Raspberry Pi IP address. For the study, the MTConnect Adapter was housed on port 5000 and the Sound Adapter was housed on port 5001. 

  For each stream of data (Visual, Audio, etc.), clients may be required for the proper formatting of the resulting data. These clients are responsible for the collection, formatting, and/or analysis of data from these devices. For each form of data, a specific set of middleware is required, depending on the final state of data analysis desired.  


#### *3.2) Running Agent*

  The Agent needs to be run first on the Raspberry Pi device to allow for the Adapters to work properly. To do this, SSH or VNC into the Raspberry Pi (or manually connect the Pi to a monitor). Then, upload the following code into a file on the Raspberry Pi: [Agent_Code](insertcodehere). To run the Agent, open the command line and first use the "cd" command to go into the directory where the "agent" file is stored. Then, use the command *"sudo ./agent"* to run the Agent.
  

#### *3.3) Running Adapters*

  After the Agent is started, the Adapters can be turned on. To do so, upload the following code into a file on your Raspberry Pi: [API and Current Adapter Script](https://github.com/cjmason375/TU-PU-3DPrinter_Monitoring/blob/main/MTConnect_Adapter.py) and [Ultimaker Machine Data Adapter Script](https://github.com/cjmason375/TU-PU-3DPrinter_Monitoring/blob/main/Ultimaker_Adapter.py) . To run the Adapters, use the following commands in the Command Line/Terminal: *"python3 [current_adapter_filename].py"* for the current adapter, and *"python3 [ultimaker_adapter_filename].py"* for the machine adapter.



#### 4) *COLLECTING DATA*

  Finally, it is time to collect data from the machine. To do so, you need to designate a computer to serve as a "collection computer". For our purposes, we used a desktop computer in the research lab to serve as the collection computer. This process could techically be accomplished on the Raspberry Pi itself, but the team decided it was better to use an independent computer to reduce the bandwith and strain on the Raspberry Pi. The adapter and camera commands will continously collect data at specified intervals, from manually starting the program to stopping the program - however, the team is working on ways to automate this process. The sound command needs the user to estimate the approximate print time so sound data can be recorded over a pre-determined interval, but again, the team is working on ways to automate this process as well.

  ADAPTER DATA: To collect machine and current data through Device.xml, upload the following code onto your collection computer: [Machine_Data_Collection Script](https://github.com/cjmason375/TU-PU-3DPrinter_Monitoring/blob/main/API_Current_Collection_Script.py). In the code, update the IP address location to the proper coordinates. Also, designate a file location for a CSV file where data can be collected into. Then, you can collect data by running the code in an integrated development environment (IDE) or by using the command line.

  CAMERA DATA: To collect camera data, upload the following code onto your collection computer and repeat the same steps as above: [Camera Collection Script](https://github.com/cjmason375/TU-PU-3DPrinter_Monitoring/blob/main/Camera_Collection_Script.py).

  SOUND DATA: To collect sound data, upload the following code onto your collection computer and repeat the same steps as above: [Sound Collection Script](https://github.com/cjmason375/TU-PU-3DPrinter_Monitoring/blob/main/Sound_Collection_Script.py). You can run this command to collect data through the command line using the command "python3 [sound_data_file_name.py] [RPi IP_address:port] [device name] [timezone] [length of each time recording] [total amount of seconds to record]". An example of collecting sound data for a print under 40 minutes in this case study would be "python3 Sound_Collector2.py [IP_address]:5001 UTC 2400 2400".



### FUTURE DEVELOPMENT/USAGE

  As this work progresses, we hope to see uses for this technology in real-time monitoring usage and predictive maintenance models. By integrating FDM 3D printers into the industrial world, this work has great room for expansion and can innovate the future of factories.
