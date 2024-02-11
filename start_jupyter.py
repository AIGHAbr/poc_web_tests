import subprocess
import webbrowser
import time

def start_jupyter():
    command = ["jupyter-notebook", "--no-browser"]
    sp = subprocess.Popen(command)
    time.sleep(5)
    webbrowser.open("http://localhost:8888/notebooks/01.%20start_here.ipynb", new=2)
    return sp

sp = start_jupyter()
sp.wait()