import os
import subprocess
import time

import psutil

proc = subprocess.Popen(f".\HSE_Bot.run.bat",
                        creationflags=subprocess.CREATE_NEW_CONSOLE)
time.sleep(10)

pobj = psutil.Process(proc.pid)

# list children & kill them
for c in pobj.children(recursive=True):
    c.kill()
pobj.kill()
