import os

def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):

       print(type(files)) #当前路径下所有非目录子文件

       for i in range(len(files)):
           print(type(files[i]))

file_name("c:/bianban2")