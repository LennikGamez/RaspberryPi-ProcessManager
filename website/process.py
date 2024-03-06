import subprocess

class Process:
    def __init__(self, name, command, onstartup=False):
        self.name = name
        self.command = command
        self.process = None
        self.is_running = False
        self.start_on_startup = onstartup

        if self.start_on_startup:
            self.run()
    def run(self):
        if not self.is_running:
            self.process = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=False)
            self.is_running = True
        return self
    def stop(self):
        if self.is_running:
            self.process.kill()
            self.process.terminate()
            self.is_running = False
        return self
    
    def running(self):
        if not self.process:
            return False
        return self.process.poll() == None