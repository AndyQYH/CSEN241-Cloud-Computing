import multiprocessing
import requests
from multiprocessing import Process
import logging
import subprocess

chatbot_url = 'http://127.0.0.1:8080/async-function/andy-boto-9'
num_threads = 100
print("cpu: ", multiprocessing.cpu_count())

output = subprocess.check_output('systemctl status faasd | grep Resolver | grep gateway | grep -E -o "[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}"', shell=True)
print(output.decode('utf-8'))
