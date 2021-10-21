import pickle
#import json
#import pandas as pd

objects = []
with (open("Anytown_Jan06_fullweek_dict.pkl","rb")) as openfile:
    while True:
        try:
            objects.append(pickle.load(openfile))
        except EOFError:
            break

x = input("Please say 'p' for print or 'f' for file: ")
file = ("pickle2text.txt")

if x == 'p':
    print(objects[0])
elif x == 'f':
    textfile = open(file,"w")
    for i in objects:
        textfile.write(str(i) + "\n")
    textfile.close()