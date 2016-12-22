import subprocess
import netifaces as ni
import re

def get_eth0_ip():
    return get_ip('eth0')

def get_ip(type):
    return ni.ifaddresses(type)[2][0]['addr']

def execute_unix(inputcommand):
   p = subprocess.Popen(inputcommand, stdout=subprocess.PIPE, shell=True)
   (output, err) = p.communicate()
   return output

def shutdown():
    execute_unix("shutdown -h 0")

def ping(host_ip):
    try:
        ping = subprocess.Popen(["ping", host_ip, "-n", "1"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, error = ping.communicate()
        if out:
            try:
                minimum = int(re.findall(r"Minimum = (\d+)", out)[0])
                maximum = int(re.findall(r"Maximum = (\d+)", out)[0])
                average = int(re.findall(r"Average = (\d+)", out)[0])
                packet = int(re.findall(r"Lost = (\d+)", out)[0])
                if packet > 1:
                    packet = 5 / packet * 100
            except Exception as ex:
                return False
        else:
            return False

    except subprocess.CalledProcessError:
        return False
    return True

if __name__ == "__main__":
    for i in range(250):
        host = '172.20.10.%d'%i
        if  ping(host):
            print(host)