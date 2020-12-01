import pandas as pd #Dependencies must include pandas and xlrd, pip install pandas, pip install xlrd
import numpy as np #np is downloaded with pip pandas
import sys
import pymongo
from connect2 import connect
from tkinter import filedialog

'''
Still to be added:

For time being, the writing will overwrite all entries in the db, even if they are identical, this can be made more efficient
Adapt this file to be a function for easy integration to api
Remove file search as this will be passed by the dbms to the api
Change user authentication to be passed in and used in the connect call
Remove nrows in read excel to read entire flatfile
'''

#Set up a file explorer interface to make retrieving the file much easier, opens  tkinter window for some reason too
#The file itself will probable be selected somewhere else anyway, and this file will end up being a function in the api, this is just for my ease of use
def browseFiles():
    filename=filedialog.askopenfilename(initialdir="/",title="Select the flatfile",filetypes=(("Excel Files","*.xlsx"),("All Files","*.*")))
    return filename

filename = browseFiles()
if (filename==""): #Check a file was selected, if not, stop
    raise Exception("No file was selected, suspending operation")

try: #Try to read the file, will throw error if not right one ----- in final implementation, remove nrows parameter -----
    excel_frame = pd.read_excel(filename,nrows=1,header=1,engine='xlrd',
              usecols=["Unique_identifier","Scope","Level_1","Level_2","Level_3","Level_4","Level_5","Emission_factor","Calculation Unit","Source","Preference","last update"],
              dtype={'Emission_factor':np.float64})
except:
    raise Exception("Error reading the flatfile, are you sure you selected the right file?")

#Put the frame into json format so it's ready to be uploaded to the cloud
list = list()
column_names = excel_frame.columns

for row in excel_frame.iterrows():
    dict = {}
    nav_dict = {}
    calc_dict = {}
    other_dict = {}
    iter = 0
    for item in row[1]: #Extract the items from the series returned
        if column_names[iter] in ["Scope","Level_1","Level_2","Level_3","Level_4","Level_5"]:
            nav_dict[column_names[iter]] = item
        elif column_names[iter] in ["Emission_factor","Calculation Unit"]:
            if column_names[iter] == "Calculation Unit":
                calc_dict["Calculation_Unit"] = item
            else:
                calc_dict[column_names[iter]] = item
        elif column_names[iter] in ["last update","Preference","Source"]:
            if column_names[iter] == "last update":
                other_dict["Last_Update"] = item
            else:
                other_dict[column_names[iter]] = item
        else:
            dict["Reference_Number"] = item

        iter += 1 #Keeps track of the column
    dict["Navigation_info"] = nav_dict
    dict["Calculation_info"] = calc_dict
    dict["Other_info"] = other_dict
    list.append(dict)

#Once the data is read, this is where it will be sent to the cloud

#To save on some time/bandwidth, will check the unique ids, where there is a duplicate on the cloud, check
#the last update timestamp and keep the one with the later stamp. This will need to be done as mongodb is 
#happy to have multiple duplicates of an object in a collection

db = connect("Mark_2386300", "2386300") #For the time being, this is hardcoded to use my admin account, this will be changed once user authentication is added to the dbms

#Check if the user exists in the db/information was given correctly
if db == -1:
    raise Exception("Authentication to the server failed, password or username was incorrect")

collection = db['Carbon_info']
for data in list:
    id = collection.update_one({"Reference_Number":data["Reference_Number"]},{"$set":data}, upsert=True)#Push the list to the db cloud server overwriting the any duplicates already in the db

print(id) #Mainly here for the moment to ensure the function has worked correctly