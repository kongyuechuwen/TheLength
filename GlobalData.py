
FILE_PATH = "C:\\"
SCAN_FLAG = True

def set_path():
    global FILE_PATH
    f = open("length.config", "r")

    try:
         FILE_PATH = f.read( )
    finally:
         f.close()

