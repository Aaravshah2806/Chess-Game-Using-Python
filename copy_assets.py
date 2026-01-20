import shutil
import os

source = 'images'
destination = 'simple_frontend/images'

if not os.path.exists(destination):
    os.makedirs(destination)

for filename in os.listdir(source):
    s = os.path.join(source, filename)
    d = os.path.join(destination, filename)
    if os.path.isfile(s):
        shutil.copy2(s, d)
        print(f"Copied {filename}")
