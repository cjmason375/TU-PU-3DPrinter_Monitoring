# TU-PU-3DPrinter_Monitoring
This repository documents the necessary background, procedures, and code to conduct an experiment alike the one detailed in the paper "**Online and Real-Time 3D Printer Monitoring using MTConnect Data Integration: Printing Part Error Diagnostics Case Study**". 





### *INTRODUCTION*

  With [Industry 4.0](https://www.ibm.com/topics/industry-4-0) promising to revolutionize the future of smarter factories, it has become increasingly important to ensure machines are able to intelligently communicate with one another utilizing the [Internet of Things (IoT)](https://www.ibm.com/think/topics/internet-of-things) and make decisions based on real-time data analysis and [Articial Intelligence (AI)](https://www.ibm.com/think/topics/artificial-intelligence). As [Additive Manufacturing (AM)](https://mitsloan.mit.edu/ideas-made-to-matter/additive-manufacturing-explained) technologies continue to develop, these processes have become more commonplace in producing final parts rather than prototyping models. However, 3D printing, especially Fused Deposition Modeling (FDM) processes, are susceptible to small defects that can result in large errors in a final part or set of parts. In this project, a MTConnect Framework was implemented to collect three sets of data from a hobbyist Ultimaker S5 3D Printer; sound data, current data, and machine data. The team then analyzed each set for indications of failures within the data, which will then developed into a real-time anomaly and part failure detection model. The adoption of FDM processes into industry can be accelerated utilizing intelligent systems that can automatically detect and correct failures based on real-time continuous data analysis.



### *1) SENSOR INSTALLATION*

  First, sensors must be set up to collect data from the machine. For the study, machine data such as bed temperature, fan speed, camera snapshots, and other sub-component information could be collected from the Ultimaker API, so external sensors were not necessary. To monitor machine sound, a microphone was installed within the printer's enclosure, and a current transformer was installed onto the printer's main power line to monitor current consumption. The external sensors were then hooked to a Raspberry Pi computer, which would be used as the study's edge computer for collecting data.



### *2) STATIC IP ADDRESSES*

  With the sensors connected to the Raspberry Pi, it is then necessary to set up a static IP address on the Raspberry Pi. By default, most devices utilize a Dynamic IP address standard, which constantly changes the device's IP address each time it updates to the network. However, it is necessary to assign a Static IP address to the Raspberry Pi to make it easier to access the Pi in code. Then, the same process must be done to establish a Static IP address on the Ultimaker Printer. Once the Static IP addresses are assigned, note them down for later use in code.

### *3) SETTING UP MTCONNECT*

  [MTConnect](https://www.mtconnect.org) offers a robust and versatile system that can be adopted by modern and legacy systems alike. As the industry standard for manufacturing data integration across multiple machines, utilizing MTConnect for aggregating multiple datasets enabled the team to contextualize collected data while avoiding proprietary formatting. Implementing the free, open-source MTConnect software is not only cost-effective, but also encourages interoperability within factories. Utilizing MTConnect allows further scaling of this project and enables real-time remote monitoring of collected data.

  MTConnect operates based off of two major components: [the ***Adapter*** and the ***Agent***](https://www.mmsonline.com/articles/understanding-mtconnect-agents-and-adapters). {{{The ***Adapter*** collects the data from the machine and/or sensors, converts it into a text dictionary, and passes that dictionary along to the Agent. In other words, it allows the machines to speak in the MTConnect language. In the case study, each data group had its own adapter; a 3D printer adapter that utilized the Swagger API to convert status variables into a MTConnect-compliant format, a current transformer adapter for collecting current data, and a sound stream adapter for collecting sound data. The ***Agent*** takes the dictionary from the Adapter, formats it into a XML stream, and makes that data available on the cloud. In our case study, the Agent uses a HTTP-based REST communication standard. Then, the operator can utilize ***applications*** to fully utilize the MTConnect framework, such as accessing monitoring systems or analytics platforms for conducting further processing and visualization.}}}

#### *3.1) Developing "Device_xml" Data Information Model*

  A Data Information Model takes the information from the Agent and conceptually represents the data's relationships. For the 3D printer's case, the "Device_xml" data information model was created to  elements of an operation's process at the same timestamp into a single file. Primarily, electrical, thermal, and mechanical state variables were utilized in this information model.

  
  
  Currently, MTConnect does not support a method to incorporate JPG images into the model, so those had to be collected individually. As well, the collected sound data had an independent adapter as continous sound collection alongside the other ongoing processes has the potential to overload the Raspberry Pi.




#### 4) *COLLECTING DATA*

(mention how to collect camera and sound data)

  
  






### SETTING UP MTCONNECT*

  [MTConnect](https://www.mtconnect.org) offers a robust and versatile system that can be adopted by modern and legacy systems alike. As the industry standard for manufacturing data integration across multiple machines, utilizing MTConnect for aggregating multiple datasets enabled the team to contextualize data while avoiding proprietary formatting. Implementing the free, open-source MTConnect software is not only cost-effective, but also encourages interoperability within factories. Utilizing MTConnect allows further scaling of this project and enables real-time remote monitoring of collected data.

  MTConnect operates based off of two major components: the ***Adapter*** and the ***Agent***. The ***Adapter*** collects the data from the machine and/or sensors, converts it into a text dictionary, and passes that dictionary along to the Agent. In the case study, each data group had its own adapter; a 3D printer adapter that utilized the Swagger API to convert status variables into a MTConnect-compliant format, a current transformer adapter for collecting current data, and a sound stream adapter for collecting sound data. The ***Agent*** takes the dictionary from the Adapter, formats it into a XML stream, and makes that data available on the cloud. In our case study, the Agent uses a HTTP-based REST communication standard. Then, the operator can utilize ***applications*** to fully utilize the MTConnect framework, such as accessing monitoring systems or analytics platforms for conducting further processing and visualization.

  *(In the paper, it was mentioned that "details of the MTConnect Information Model (Device.XML) and its development are listed in the Repository, so Eunseob should add onto this with whatever information he feels necessary")*

  

  A custom MTConnect information model was developed to collect and structure data and extend MTConnect usage to 3D printers and external sensors. To set up MTConnect on your system, you must run three Python scripts on the collection computer (in the study's case, this was a Windows desktop computer) to set up XML documents. A Purdue researcher on our team personally developed these data device models.
  
  
  
  the following Python scripts are to be run on the Raspberry Pi to collect data. Utilizing a platform that allows VNC or SSH interfacing with the Raspberry Pi reduces the need for an external monitor for the Pi and allows you to control the Pi's interface from another computer. For this study, we used "VNC Viewer", set a static IP address for the Raspberry Pi, and set up the platform using that IP address. 

  (put RPi scripts here once they are uploaded to the GitHub)

  
  
  
  
  Listed are links to the code for each Adapter, as well as the Agent - these code snippets should be run on the Raspberry Pi. (verify?)

1)  [3D Printer Machine Data Script](https://github.com/cjmason375/TU-PU-3DPrinter_Monitoring/blob/main/API_Data_Collection_Script) <br>
2)  [Camera Collection Script](https://github.com/cjmason375/TU-PU-3DPrinter_Monitoring/blob/main/Camera_Script) <br>
3)  [Sound Collection Script](https://github.com/cjmason375/TU-PU-3DPrinter_Monitoring/blob/main/Sound_Collect_Script) <br>




### *SENSOR SETUP*

  To conduct the case study, the project required data collection. Listed below are the three methods for collecting data for this project:

1) **Machine data** - To collect machine data, the Ultimaker API was utilized to access real-time machine statistics provided by the Ultimkaer S5
2) **Current data** - To collect current consumption data, a current transformer was installed on the main power cable of the Ultimaker S5 along with an analog-digital converter to read real-time current consumption data
3) **Sound data** - To collect sound data, a microphone was installed inside of the Ultimaker S5's enclosure to capture operation and idle sounds

  A Raspberry Pi (served as an edge computer?) for this case study and was necessary to connect the sensors and also to deploy the MTConnect framework on.




  






### *COLLECTING DATA*

(meet w/ Nathon & Diara about how they collected data, align with paper details but give more speficifc and case-by-case example of what to do to pull specific data-item)

Commmands:
(push, 

### *REAL-TIME MONITORING*

(have Eunseob put in details and link to Grafana web dashboard and explain how it works)


### FUTURE DEVELOPMENT/USAGE

(talk about implementing this technology for creating ML predicitve maintenance model & real-time monitoring and failure detection/classification usage)

