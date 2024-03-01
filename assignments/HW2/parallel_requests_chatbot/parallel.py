import logging
import threading
import time
import requests
import random
import os

figlet_url = os.system("systemctl status faasd | grep Resolver | grep gateway | grep -E -o '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'")
chatbot_url = 'http://127.0.0.1:8080/async-function/andy-boto-9'
num_thread = 500
def thread_function(name):
    response = requests.post(chatbot_url, data='figlet CSEN241 is my number ' +  str(random.random() * 2))
    logging.info("Thread %s: starting", name)
    print(response.text)
    logging.info("Thread %s: finishing", name)

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    threads = list()
    for index in range(num_thread):
        logging.info("Main    : create and start thread %d.", index)
        x = threading.Thread(target=thread_function, args=(index,))
        threads.append(x)
        x.start()

    for index, thread in enumerate(threads):
        logging.info("Main    : before joining thread %d.", index)
        thread.join()
        logging.info("Main    : thread %d done", index)
        
    print(figlet_url)
