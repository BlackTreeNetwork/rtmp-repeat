import os, sys
import utility
import subprocess
import shutil
from os import listdir
from os.path import isfile, join
from time import gmtime, strftime, sleep
from threading import Thread

internal000 = ["114.31.51.68","114.31.50.122","114.31.50.123","114.31.50.124","180.182.60.247","180.182.60.248"]
internal001 = ["180.182.60.194","180.182.60.196","180.182.60.210","180.182.60.211"]

sustain_process = []
find = False

class Hook:
    def __init__(self):
        self.kill = False

    def hook(self, path, url):
        while self.kill is False:
            if get_size(path) > 0:
                print("We found the url : %s" % url)
                print("Please don't terminate this program. It working record the live-stream video.")
                onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
                for f in onlyfiles:
                    if os.path.getsize(path + "/" + f) == 0:
                        os.remove(path + "/" + f)
                break
            else:
                pass

def doWorkstation(streamer, date, internal, start, end, output_file=None, p_code=1):
    command_header = "rtmpdump -v -r"
    url = "rtmp://{ip}:1935/pop_cast/_definst_/"
    pcode = "P-000{:02d}".format(p_code)
    target = "{name}_" + pcode + "_{date}"
    global find
    output_flag = "-o"
    unspecified = False
    if output_file is None:
        unspecified = True

    for address in internal[start:end]:    
        output_file = target.format(name=streamer, date=address.replace('.', '') + "_" + date)
        url_format = url.format(ip=address)
        for second in range(0, 60):
            if find:
                break
            target_url = target.format(name=streamer, date=date + "{:02d}".format(second))
            command = "{a} {b}{c} {d} {e}".format(a=command_header, b=url_format, c=target_url, d=output_flag, e=streamer + "/" + output_file + ".flv")
            with open(os.devnull, "w") as f:
                hookObject = Hook()
                hookThread = Thread(target=hookObject.hook, args=(streamer, url_format + target_url))
                hookThread.start()
                a = subprocess.call(command.split(' '), stdout=f, stderr=subprocess.DEVNULL)
                hookObject.kill = True
                isHookedStream(streamer + "/" + output_file)

def get_size(start_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

def isHookedStream(path, flag=None):
    global find
    if os.path.exists(path + ".flv"):
        if int(os.stat(path + ".flv").st_size) > 0:
            print("Recorded video streaming")
            print("the streamer's live ended.")
            find = True
        else:
            pass

if __name__ == "__main__":
    argv, output_file =  utility.disting_args(sys.argv[1:])
    streamer = utility.define_argument_value(argv, "-streamer", None, flag='-s')
    pcode = utility.define_argument_value(argv, "-pcode", 1, flag='-p')
    date = utility.define_argument_value(argv, "-time", None, flag="-t")

    if len(output_file) == 0:
        output_file = None
    else:
        output_file = output_file[0]

    if streamer is None:
        raise ValueError()
    
    if date is None:
        raise ValueError()

    print("Scarching the stream server for channel ...")

    if not os.path.exists(streamer):
        os.mkdir(streamer)

    for i in range(0, len(internal000)):
        sustain_process.append(Thread(target=doWorkstation, args=(streamer, date, internal000, i, i+1, output_file)))
    
    for p in sustain_process:
        p.start()
    for p in sustain_process:
        p.join()
    
    sustain_process = [t for t in sustain_process if t.is_alive()]
    if find:
        print("download done.")
        exit(0)

    print("Scarching the stream server for channel 2 ...")
    for i in range(0, len(internal001)):
        sustain_process.append(Thread(target=doWorkstation, args=(streamer, date, internal001, i, i+1, output_file)))
    for p in sustain_process:
        p.start()
    for p in sustain_process:
        p.join()
    if find:
        print("download done.")
        exit(0)
    else:
        print('Sorry. Not found the stream')
        shutil.rmtree(streamer)