import pandas as pd #Dependencies must include pandas and xlrd, pip install pandas, pip install xlrd
import numpy as np #np is downloaded with pip pandas
import sys
from tkinter import filedialog

#Set up a file explorer interface to make retrieving the file much easier, opens  tkinter window for some reason too
#The file itself will probable be selected somewhere else anyway, and this file will end up being a function in the api, this is just for my ease of use
def browseFiles():
    filename=filedialog.askopenfilename(initialdir="/",title="Select the flatfile",filetypes=(("Excel Files","*.xlsx"),("All Files","*.*")))
    return filename

filename = browseFiles()
if (filename==""): #Check a file was selected, if not, stop
    raise Exception("No file was selected, suspending operation")

try: #Try to read the file, will throw error if not right one
    excel_frame = pd.read_excel(filename,nrows=1,header=1,engine='xlrd',
              usecols=["Scope","Level_1","Level_2","Level_3","Level_4","Level_5","Emission_factor","last update"],
              dtype={'Emission_factor':np.float64, 'Level_5':str})
except:
    print("Error reading the flatfile, are you sure you selected the right file?")

#Put the frame into json format so it's ready to be uploaded to the cloud
list = list()
column_names = excel_frame.columns

for row in excel_frame.iterrows():
    dict = {}
    iter = 0
    for item in row[1]: #Extract the items from the series returned
        dict[column_names[iter]] = item
        iter += 1 #Keeps track of the column
    list.append(dict)

#Once the data is read, this is where it will be sent to the cloud

#To save on some time/bandwidth, will check the unique ids, where there is a duplicate on the cloud, check
#the last update timestamp and keep the one with the lataer stamp.
print(list)