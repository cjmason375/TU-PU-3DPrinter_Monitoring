# TU-PU-3DPrinter_Monitoring
This repository documents the necessary background, procedures, and code to conduct an experiment alike the one detailed in the paper "**Online and Real-Time 3D Printer Monitoring using MTConnect Data Integration: Printing Part Error Diagnostics Case Study**". 




### *INTRODUCTION*

  With [Industry 4.0](https://www.ibm.com/topics/industry-4-0) promising to revolutionize the future of smarter factories, it has become increasingly important to ensure machines are able to intelligently communicate with one another utilizing the [Internet of Things (IoT)](...) and make decisions based on real-time data analysis and [Articial Intelligence (AI)](...). As [Additive Manufacturing (AM)](https://mitsloan.mit.edu/ideas-made-to-matter/additive-manufacturing-explained) technologies continue to develop, these processes have become more commonplace in producing final parts rather than prototyping models. However, 3D printing, especially Fused Deposition Modeling (FDM) processes, are susceptible to small defects that can result in large errors in a final part or set of parts. In this project, a MTConnect Framework was implemented to collect three data sources from a hobbyist Ultimaker S5 3D Printer; sound data, current data, and machine data. The team then analyzed each set for indications of failures within the data, which will then developed into a real-time anomaly and part failure detection model. The adoption of FDM processes into industry can be accelerated utilizing intelligent systems that can automatically detect and correct failures based on real-time continuous data analysis.

  [MTConnect](https://www.mtconnect.org) offers a robust and versatile system that can be adopted by modern and legacy systems alike. As the industry standard for manufacturing data integration across multiple machines, utilizing MTConnect for aggregating multiple datasets enabled the team to contextualize data while avoiding proprietary formatting. Implementing the free, open-source MTConnect software is not only cost-effective, but also encourages interoperability within factories. Utilizing MTConnect allows further scaling of this project and enables real-time remote monitoring of collected data.





### *SENSOR SETUP*

  To conduct the case study, the project required data collection. Listed below are the three methods for collecting data for this project:

1) **Machine data** - To collect machine data, the Ultimaker API was utilized to access real-time machine statistics provided by the Ultimkaer S5
2) **Current data** - To collect current consumption data, a current transformer was installed on the main power cable of the Ultimaker S5 along with an analog-digital converter to read real-time current consumption data
3) **Sound data** - To collect sound data, a microphone was installed inside of the Ultimaker S5's enclosure to capture operation and idle sounds

  A Raspberry Pi (served as an edge computer?) for this case study and was necessary to connect the sensors and also to deploy the MTConnect framework on.

### *SETTING UP MTCONNECT*

  MTConnect operates based off of two major components: the ***Adapter*** and the ***Agent***. The ***Adapter*** collects the data from the machine and/or sensors, converts it into a text dictionary, and passes that dictionary along to the Agent. In the case study, each data group had its own adapter; a 3D printer adapter that utilized the Swagger API to convert status variables into a MTConnect-compliant format, a current transformer adapter for collecting current data, and a sound stream adapter for collecting sound data. The ***Agent*** takes the dictionary from the Adapter, formats it into a XML stream, and makes that data available on the cloud. In our case study, the Agent uses a HTTP-based REST communication standard. Then, the operator can utilize ***applications*** to fully utilize the MTConnect framework, such as accessing monitoring systems or analytics platforms for conducting further processing and visualization.

  *(In the paper, it was mentioned that "details of the MTConnect Information Model (Device.XML) and its development are listed in the Repository, so Eunseob should add onto this with whatever information he feels necessary")*

  A custom MTConnect information model was developed to collect and structure the data and extend MTConnect usage to 3D printers and external sensors. Listed are links to the code for each Adapter, as well as the Agent.



[link the code here!]


### *COLLECTING DATA*

(meet w/ Nathon & Diara about how they collected data, align with paper details but give more speficifc and case-by-case example of what to do to pull specific data-item)

Commmands:
(push, 

### *REAL-TIME MONITORING*

(have Eunseob put in details and link to Grafana web dashboard and explain how it works)


### FUTURE DEVELOPMENT/USAGE

(talk about implementing this technology for creating ML predicitve maintenance model & real-time monitoring and failure detection/classification usage)

