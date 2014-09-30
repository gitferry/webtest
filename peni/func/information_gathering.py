
__author__ = 'ruluo1992-PC'

import os
from string import Template
import subprocess
import result


def nmap(ip, result):
    command_t = Template('nmap -T4 -A -v ${target}')
    command = command_t.substitute(lang = 'Python', target = ip)

    #command = 'nmap -T4 -A -v ' + ip
    #output = commands.getoutput(command)
    #output = os.popen(command).readlines()
    process = subprocess.Popen(command, shell = True, stdout=subprocess.PIPE)
    process.wait()
    output = process.stdout.readlines()
    start = False
    #stdoutput = process.communicate()
    for line in output:
        if(line[0] == '|'):
            continue
        elif(start == True):
            if(line[0] >= '0' and line[0] <= '9'):
                parts = line.split(' ')
                length = len(parts)
                detail = ''
                for i in range(1,length):
                    detail += parts[i] + '  '
                result.portservice[parts[0]] = detail
            else:
                start = False
        elif(line.startswith('PORT')):
            start = True
            continue
        elif(line.startswith('OS details')):
            parts = line.split(':')
            result.operatingsystem = parts[1]
    #print stdoutput

def whatweb(ip, result):
    command_t = Template('whatweb --no-error --colour=never ${target}')
    command = command_t.substitute(lang = 'Python', target = ip)
    process = subprocess.Popen(command, shell = True, stdout=subprocess.PIPE)
    process.wait()
    output = process.stdout.readlines()
    line = output[0]
    parts = line.split(', ')
    for part in parts:
        result.webinformation.append(part)
        #tparts = part.split(r'[')
        #tkey = tparts[0]
        #tvalue = part[len(tkey):]
        #print tkey


if __name__ == '__main__':
    print 'hello'
    t = result.result()
    #nmap("10.0.0.55", t)
    #print t.operatingsystem
    #for key in t.portservice.keys():
    #    print key + ':' + t.portservice[key]
    whatweb('http://211.155.81.16/', t)
    for info in t.webinformation:
        print info
