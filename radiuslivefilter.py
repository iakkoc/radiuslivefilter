#!/usr/bin/python3
# -*- coding: utf-8 -*-

import subprocess
import os
import getopt
import sys

class bcolors:
    YELLOW = '\033[33m'    
    WHITE = '\033[37m' 
    RED = '\033[31m' 
    NAVY = '\033[34m' 
    GREEN = '\033[32m' 
    ENDC = '\033[0m'

class notifications:
    invalidinput = 'Invalid input value...'
    radiusstarting = 'Starting Radius Server in debug mode...'
    radiusstarted = 'Radius Server Started in debug mode...'
    radiusstopping = 'Stopping Radius Server...'
    radiusstopped = 'Radius Server Stopped...'
    radiuswaiting = 'Waiting request for'
    paramerror = 'invalid option for '
    mayuseoptions = 'You can use command options too. Try <radiuslivefilter -h> for detailed information.'

class ptcheckvalue:
    AUTH = 'Received Access-Request'
    ACCT = 'Received Accounting-Request'

def printhelp():
        print (
                '''
NAME :
        radiuslivefilter        filter radius debug logs on console.

SYNOPSIS
        radiuslivefilter [-h] [-s text to be searched] [-t radius packet type]

OPTIONS :
        -h --help       prints help.
        -s --search     MAC address, username, IP address etc. to be filtered. Formats must be same as network device send.
        -t --type       Type of the radius packet to be filtered. Authentication [auth], Accounting [acct] or any.

'''
        )

def startradius ():
    global popen
    print (notifications.radiusstarting)
    popen = subprocess.Popen(['freeradius','-X'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    print (notifications.radiusstarted)
    return

def stopradius ():
    s = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    output, error = s.communicate()
    target_process = "freeradius"
    print (notifications.radiusstopping)
    for line in output.splitlines():
        if target_process in str(line):
            pid = int(line.split(None, 1)[0])
            os.kill(pid, 9)
    print (notifications.radiusstopped)
    return

def findcolor (satir):
    if 'Login OK:' in satir:
        return bcolors.GREEN
    elif 'Login incorrect'  in satir:
        return bcolors.RED
    elif 'ERROR' in satir:
        return bcolors.RED
    elif 'WARNING' in satir:
        return bcolors.YELLOW

def printscreen (pline):
    pcolor = findcolor (pline)
    if pcolor:
        print (f"{pcolor}" + pline + f"{bcolors.ENDC}")
    else:
        print (pline)

def findcontrolvalue (value):
    if value == 'auth':
        return ptcheckvalue.AUTH
    elif value == 'acct':
        return ptcheckvalue.ACCT

def collectparam():
    cpsrc = ''
    cpupackettype = 'any'
    try:
        options, remainder = getopt.getopt(sys.argv[1:],'hs:t:',['help','search=','type=',])
        if not options:
            cpsrc,cpupackettype = collectparammenu()
            return (cpsrc,cpupackettype)
    except getopt.GetoptError as err:
        print('ERROR:', err)
        sys.exit(2)
    for opt, arg in options:
            if opt in ('-h','--help'):
                    printhelp()
                    exit()
            elif opt in ('-t','--type'):
                    if arg != 'any' and arg != 'auth' and arg != 'acct':
                            print (notifications.paramerror, opt, ',valid options are [auth,acct,any]')
                            exit()
                    cpupackettype = arg
            elif opt in ('-s','--search'):
                    cpsrc = arg
    return (cpsrc,cpupackettype)

def collectparammenu():
    print (notifications.mayuseoptions)
    cpmsrc=input(f"{bcolors.YELLOW}Type The Username or MAC Address (must be same format with the switch send) or other Parameter to Filter:{bcolors.ENDC}")
    cpmupackettype = input(f"{bcolors.YELLOW}Select Packet Type [auth, acct, any (Default)]:{bcolors.ENDC}")
    if not cpmupackettype:
            cpmupackettype = 'any'
    while (cpmupackettype != 'any' and cpmupackettype != 'auth' and cpmupackettype != 'acct' ):
            print (notifications.invalidinput)
            cpmupackettype = input(f"{bcolors.YELLOW}Select Packet Type [auth, acct, any (Default)]:{bcolors.ENDC}")
    return (cpmsrc,cpmupackettype)


templinenumber = ''
found = 0
fid = ''
linelist = []
foundlinelist = []
upackettype = 'any'
rpackettype = ''
checkvalue = ''

src,upackettype = collectparam ()
ptcontrolvalue = findcontrolvalue (upackettype)

stopradius()
startradius()
print (notifications.radiuswaiting,'\'',src,'\'','packettype','\'',upackettype,'\'')

for line in popen.stdout:
    linenumber = line.split()[0] #(0)
    linex = list(linenumber)

    if linex[0] == '(':

        if templinenumber == linenumber:
            linelist.append(line)

            if found:
                printscreen (line.strip())
                
            else:

                for fid in linelist:

                    if pttrue and src in fid:
                        found = True
                        foundlinelist.append(linenumber) # previously founded line numbers

                        for a in linelist:
                            printscreen(a.strip())

        else:

            if linenumber in foundlinelist:
               printscreen(line.strip())

            templinenumber = linenumber
            linelist.clear()
            linelist.append(line)
            found = False
            if upackettype == 'any' or (ptcontrolvalue in line):
                pttrue = True
            else:
                pttrue = False

    elif (found):
        printscreen(line.strip())