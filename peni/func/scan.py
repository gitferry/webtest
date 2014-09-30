
import result
from string import Template
import subprocess
import re
__author__ = 'ruluo1992-PC'

def wapiti(ip, result, basedir):
    command_t = Template('wapiti ${target}')
    command = command_t.substitute(lang = 'Python', target = ip)
    process = subprocess.Popen(command, shell = True, stdout=subprocess.PIPE, cwd = basedir)
    process.wait()
    result.webreport = basedir + 'generated_report/index.html'

def openvas_create_target(ip):
     #create target
     create_command_t = Template('omp --username admin --password nimda --xml=\'<create_target><name>${target}</name><hosts>${target}</hosts></create_target>\'')
     create_command = create_command_t.substitute(lang = 'Python', target = ip)
     create_process = subprocess.Popen(create_command, shell=True, stdout=subprocess.PIPE)
     create_process.wait()
     output = create_process.stdout.readlines()
     line = output[0]
     #line= r'<create_target_response id="9e6f27cd-4c30-44fd-b8f1-fde2359c0e46" status_text="OK, resource created" status="201"></create_target_response>'
     m = re.search(r'id=\"(.+?)\"', line)
     if m:
         return m.group(1)
     else:
         return 'nothing'

def openvas_alreadyhastarget(ip):
    command_t = Template('omp --username admin --password nimda --get-targets')
    command = command_t.substitute(lang = 'Python', target = ip)
    process = subprocess.Popen(command, shell = True, stdout=subprocess.PIPE)
    process.wait()
    output = process.stdout.readlines()
    for line in output:
        parts = line.split()
        tline = parts[1]
        if(cmp(ip, parts[1]) == 0):
            return parts[0]
    return 'nothing'

def openvas_alreadyhastask(ip):
    command_t = Template('omp --username admin --password nimda --get-tasks')
    command = command_t.substitute(lang = 'Python', target = ip)
    process = subprocess.Popen(command, shell = True, stdout=subprocess.PIPE)
    process.wait()
    output = process.stdout.readlines()
    for line in output:
        parts = line.split()
        tline = parts[2]
        if(tline == ip):
            return parts[0]
    return 'nothing'

def openvas_createtask(ip, targetid):
    command_t = Template('omp --create-task --target=${targetid} --name=${target} --config=daba56c8-73ec-11df-a475-002264764cea --username=admin --password=nimda')
    command = command_t.substitute(lang = 'Python', target = ip, targetid = targetid)
    process = subprocess.Popen(command, shell = True, stdout=subprocess.PIPE)
    process.wait()
    output = process.stdout.readlines()
    output[0] = output[0].replace('\n', '')
    return output[0]

def openvas(ip, result):
    targetid = openvas_alreadyhastarget(ip)
    if(targetid == 'nothing'):
        targetid = openvas_create_target(ip)
    taskid = openvas_alreadyhastask(ip)
    if(taskid == 'nothing'):
        taskid = openvas_createtask(ip, targetid)
    #print taskid
    command_t = Template('omp --xml=\'<start_task task_id="${task_id}"/>\' --username=admin --password=nimda')
    command = command_t.substitute(lang = 'Python', task_id = taskid)
    while(True):
        process = subprocess.Popen(command, shell = True, stdout=subprocess.PIPE)
        process.wait()
        output = process.stdout.readlines()
        line = output[0]
        m = re.search(r'status=\"(.+?)\"', line)
        r = m.group(1)
        #print r
        if(r == '202'):
            break;
    url_t = Template('http://10.1.10.117:9392/omp?cmd=get_task&task_id=${taskid}&token=b0539f04-33fc-4baf-83cc-444fcc8cb7ee')
    url = url_t.substitute(lang = 'Python', taskid = taskid)
    result.openvas_report = url

def wpscan(ip, result):
    command_t = Template('wpscan --url ${target} --no-color')
    command = command_t.substitute(lang = 'Python', target = ip)
    process = subprocess.Popen(command, shell = True, stdout=subprocess.PIPE)
    process.wait()
    output = process.stdout.readlines()
    result.wpscan_output = output

if __name__ == '__main__':
    r = result.result()
    #wapiti('10.0.0.55', r, '/home/')
    #print r.webreport
    #openvas('10.1.153.33', r)
    #print r.openvas_report
    wpscan('98.126.79.170', r)
    for line in r.wpscan_output:
        print line


