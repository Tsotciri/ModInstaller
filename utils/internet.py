from urllib.request import urlopen
import os
from rich.progress import wrap_file
from rich.progress import Progress

def large_download(url,dir):
    count = 0
    response = urlopen(url)
    size = int(response.headers["Content-Length"])
    name =  os.path.basename(url)
    name = name[0:-5]
    CHUNK = 16 * 1024
    with wrap_file(response, size, description=name) as file:
        with open(dir + name, "wb") as f:
            while True:
                chunk = file.read(CHUNK)
                if not chunk:
                    break
                f.write(chunk)
            count += 1
