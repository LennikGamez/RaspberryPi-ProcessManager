import os
import subprocess, psutil
import time
import sys

class Process:
    def __init__(self, name, command, onstartup=False, endpoint=None):
        self.name = name
        self.command = command
        self.process = None
        self.is_running = False
        self.start_on_startup = onstartup
        self.endpoint = endpoint

        if self.start_on_startup:
            self.run()
    def run(self):
        if not self.is_running:
            self.process = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, shell=False)
            self.is_running = True

        return self
    
    def log(self):
        with open(f'{get_static_folder()}/log.txt', 'a+') as logfile:
            for line in self.process.stdout.readlines():
                logfile.write(time.localtime().tm_hour.__str__() + ':' + time.localtime().tm_min.__str__() + ':' + time.localtime().tm_sec.__str__() + ' - ' + self.name + ' - ' + line + '\n')
                
    def stop(self):
        if self.is_running:
            children = psutil.Process(self.process.pid).children()
            for child in children:
                child.kill()
                
            self.process.kill()
            self.process.terminate()
            self.is_running = False
        return self
    
    def running(self):
        if not self.process:
            return False
        # print(self.process.poll())
        running = self.process.poll() is None

        if not running:
            self.log()

        return running



def get_static_folder():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    return os.path.join(SITE_ROOT, 'static')