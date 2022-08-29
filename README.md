# radiuslivefilter
Simultaneously filtering freeradius debug log (freeradius -X) based on macaddress, username etc.


On Freeradius production environment which many logs flow, it's hard to find and analyse logs for a problematic user or MAC address or etc. 

The goal of this script is to print screen all authentication and accounting logs related to searched text (MAC address, username, network device IP address etc.) but not others.


--HOW IT'S WORK

Stop freeradius deamon

Start Freeradius deamon in debug mode (freeradius -X)

read logs and print the ones related to searched text.


--HOW to RUN

1) run command "python3 radiuslivefilter.py" in installation folder.
2) Copy or link script to bin folder, give permissons and use as a command any where in cli.

  In command mode if you don't type any option script will show you a menu and help you to filter.

--HELP:

NAME :
        radiuslivefilter        filter radius debug logs on console.

SYNOPSIS
        radiuslivefilter [-h] [-s text to be searched] [-t radius packet type]

OPTIONS :
        -h --help       prints help.
        -s --search     MAC address, username, IP address etc. to be filtered. Formats must be same as network device send.
        -t --type       Type of the radius packet to be filtered. Authentication [auth], Accounting [acct] or any. 
		
--DISCLAIMER :
	This scipt used in my environment, use at your own risk
