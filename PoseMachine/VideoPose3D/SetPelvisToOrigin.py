import pandas as pd
import os
import getopt,sys


argumentList = sys.argv[1:]

options = "p:n:"
long_options = ["filepath", "filename"]


try:
    arguments, values = getopt.getopt(argumentList, options, long_options)
    for currentArgument, currentValue in arguments:
        if currentArgument in ("-p", "--filepath"):
            path = currentValue
            print ("File Path: ", currentValue)
             
        elif currentArgument in ("-n", "--filename"):
            fileName = currentValue
            print ("Displaying filename:", currentValue)
             
except getopt.error as err:
    # output error, and return with an error code
    print (str(err))


df = pd.read_csv('data.csv', index_col=0)

#timeFrame = 3
#df = df[df["Time"] < timeFrame]
list = df.values.tolist()
time = list[-1][0]

firstPelvis = 16
nextFrame = 21
count = 0


for k in range(4,7):
    for i in range(0, time+1):
        tmpPelvis = list[(i*nextFrame) + firstPelvis][k]
     
        for j in range (nextFrame*i, nextFrame*i+nextFrame):
            list[j][k] -= tmpPelvis
            


column_names = ["Time", "Parts", "Joint","Label", "X", "Y", "Z"]
df = pd.DataFrame(list, columns=column_names)

df.to_csv(path+fileName+".csv")


"""
for i,data in df.iterrows():

    if (i>20 and i%21==0):
        firstPelvis += nextPelvis
"""