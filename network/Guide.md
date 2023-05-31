# Guide: Python auto-provisioning script

These instructions should help explain the contents of my script, what these files exactly are, and how to use it. Don't worry: actually using it is really not that difficult. I bet you could figure it out without this guide, but nonetheless, I don't want to make assumptions and it's always nice to have a handy reference.

## File reference
- __`provision_v2.py`__ &mdash; __This is the main file for configuring the access points.__ More instructions down below on how to use it.
- `devices.py` &mdash; This file contains functions for getting info on USB devices connected to your computer.
- `range_string.py` &mdash; This file contains a function for generating a readable string of number ranges from a list of numbers (such as a list of APs to be configured).
- `runconfig.py` &mdash; This file contains the logic for looping through each access point and sending configuration commands to its console.
- `site_config.py` &mdash; This file contains the structure for parsing through config files.

## Instructions

### Setting up Python environment
1. Install Python on your device. You can do this in a few ways.
    - Start a Powershell terminal and type `python`. If you don't have Python installed, it will automatically open up the download page for Python in the Windows Store. You can also just navigate to the Windows Store on your own and download it.
    - Go to the [Python Downloads Page](https://www.python.org/downloads/) and download it from there.
2. Install the necessary packages for running the script.
    - To download Python packages, you can use a command line tool called PIP. It comes with Python when you download it. For all the Python files to work, you will need to download `pexpect`, `blessed`, and `deepdiff`. Any other packages referenced within the files are builtin and don't need to be downloaded. You can download the files like this:
    ```powershell
    pip install pexpect blessed deepdiff
    ```
    Another option is using the `requirements.txt` file included in this folder. Use it like this:
    ```shell
    pip install -r requirements.txt
    ```
    Make sure you're in the folder where `requirements.txt` is. Otherwise, this command won't work.

### Using the provisioning script

To start provisioning access points, make sure you have a micro USB cord connected to your computer. Additionally, the config file for the site you're configuring APs for must be in the folder where you're running the script. Like this:
```
provision/
├── provision_v2.py
├── SITECONFIG.txt
└── (all the other files...)
```
From here, you have two choices on how to run the script
1. Using command-line arguments
2. Using direct input into the Python script

#### __Using command-line arguments__
To use command-line arguments, refer to the help message below:
```
usage: provision_v2.py [-h] [-p START] config_file usb_port

Configure APs consecutively from the command line.

positional arguments:
  config_file           Name of file containing all configs for the APs
  usb_port              Port connecting USB and AP;
                          used with PuTTY Link (Plink)

options:
  -h, --help            show this help message and exit
  -p START, --start START, --start_ap START
                        Starting point for configuring next APs (default: 1)
```
When using CLI arguments, you always have to specify the config file and the USB port the AP is connected to. You can choose to specify an AP to start from (by its number) if you'd like to start in the middle of the list of APs for a site.

#### __Using direct input into Python script__
Alternatively, you can directly input information into the Python script. If you run the script with no command-line arguments, it will instead prompt you for information. It should look like this:
```
> python provision_v2.py
Enter filename containing all configs for the APs:      hrg.txt
Enter name of port with USB connection to APs:          com4
Enter starting point for configuring next APs:          1
Access points to be configured: 1, 6-42, 44-104, 106-181, 201-203
Ready to configure APs...


Starting from AP 1
```
The benefit of using direct input is that the script will detect:
- if the filename you entered actually exists,
- if the USB port entered is active/exists, and
- if the starting AP # you entered is in the config file specified.

This allows you to identify individual errors 