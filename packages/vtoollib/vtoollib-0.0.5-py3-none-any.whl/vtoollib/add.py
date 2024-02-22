# from dll.logger import *
# from dll.image import *
# from dll.imPlug import *
import os
file_path = os.path.abspath(__file__)
dir_path = os.path.dirname(file_path)
print(file_path)
print(dir_path)
print(__file__)
# os.chdir(dir_path)
def add(a,b):
    return a+b
def get_data():
    # config = os.path.join(dir_path,"data.txt")
    with open("./data/data.txt") as f:
        data = f.readlines()
        return data

