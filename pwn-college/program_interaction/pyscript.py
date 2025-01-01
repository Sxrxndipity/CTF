import os
import subprocess

#os.environ['gsizpd'] = 'tmkvmfzsik'

#with open('/tmp/wmzcob','w') as file:
#    file.write("uiguelaj")

os.environ.clear()

process = subprocess.Popen(
        ['/challenge/run'],
        stdin = subprocess.PIPE,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        text = True
        )
stderr = process.communicate()
print(stderr)

