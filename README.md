# network-tools
***A tiny suite of tools for the PHS Network Team***

## Requirements:
A valid Python installation (options: Microsoft Store, [Python website](https://www.python.org/downloads/))

## Getting started

### Checking Python installation
To begin using network-tools, make sure you install Python and have it working on your system. To test that Python is working, open a Terminal window and run the `python` command:
```
PS C:\Users\...> python
```
The output should look something like this:
```
Python 3.11.3 (tags/v3.11.3:f3909b8, Apr  4 2023, 23:49:59) [MSC v.1934 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>>
```
If you get an error and you know Python was installed on your machine, try restarting it.

### Installing `network-tools`
To install the network-tools package, follow these steps:
1. Navigate to the network-tools repository :white_check_mark:
2. Open the dropdown from the ![Green button labeled Code with angle brackets and a dropdown arrow](./pics/codebtn.png) button.
3. In the dropdown menu, click "**Download ZIP**"<br>![Dropdown menu with multiple options](./pics/codedd.png)
4. Extract the new ZIP file to a location. Remember it.

### Installing required packages
There are specific Python packages that are required in order for network-tools to run correctly. You can easily install all the required packages at once.

Simply open a terminal inside the network-tools folder that you just downloaded. Then, run this command:
```
pip install -r requirements.txt
```
All the necessary packages for network-tools should be installed on your machine.

## About this module

The network-tools module consists of a main program called "**main.py**" and other helper modules, stored in the `network` folder. Here's what your downloaded folder structure should look like:
```
network-tools-main/
├── README.md
├── main.py
├── requirements.txt
└── network/
    ├── __init__.py
    ├── __utils__.py
    ├── devices.py
    ├── provision.py
    ├── range_string.py
    ├── runconfig.py
    └── site_config.py
```

### Using network tools

Currently, here are all the functions available with ***network-tools***:
- [x] Provisioning access points
- [x] Checking for gaps in config files
- [x] Experimenting with a Python object holding a config file
- [ ] Generating AP SN/MAC spreadsheet