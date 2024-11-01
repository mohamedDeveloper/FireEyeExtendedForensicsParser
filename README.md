Hello Everyone

Many organizations use FireEye as one of the systems for threat detection and response. However, one feature that not everyone may know about or use is a module called FireEye Extended Forensics. This unit allows you to pull samples from selected devices or even conduct a complete scan of a specific item in the entire environment. For example, you can run YARA on all devices that have the FireEye agent installed, or you can extract the Amcache from all devices at once for examination. There are many useful features in this unit for threat hunting, enabling proactive threat detecion without waiting for alerts from security systems.

The issue with this unit is that it doesn’t come with the system and requires you to install it yourself from the FireEye store. Here are the installation instructions:

[FireEye Installation Instructions](https://fireeye.market/assets/apps/QCrdQkNZ//b4c0bd66/EF_0_1_0_UG-en.pdf)

There’s also another issue: the results from the module, once the file download is complete, will be saved in many files with random names inside a compressed folder named results.zip. 

To address this issue, I created a simple executable file that organizes and sorts all the results into an Excel file, so you don't have to struggle with the analysis. Plus, it won't take much effort; all you need to do is place the executable program in the same command line as the compressed file and run them:

![image](https://github.com/user-attachments/assets/efe4f96f-75fd-4edb-b43e-a5bda209a1fc)

Then The magic appear:

![image](https://github.com/user-attachments/assets/f35c874f-7c44-4c2a-ab62-a57e8c8eb2bc)
