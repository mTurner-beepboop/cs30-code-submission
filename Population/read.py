import pandas as pd #Dependencies must include pandas and openpyxl, pip install pandas, pip install openpyxl
import numpy as np #np is downloaded with pip pandas
import sys
import requests, json
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
    excel_frame = pd.read_excel(filename,nrows=2,header=1,engine='openpyxl',
              usecols=["Unique_identifier","Scope","Level_1","Level_2","Level_3","Level_4","Level_5","Emission_factor","Calculation Unit","Source","Preference","last update"],
              dtype={'Emission_factor':np.float64})
except:
    raise Exception("Error reading the flatfile, are you sure you selected the right file?")

#Put the frame into json format so it's ready to be uploaded to the cloud
list = list()
column_names = excel_frame.columns

for row in excel_frame.iterrows():
    dict = {'ref_num':"", 'navigation_info':"", 'calculation_info':"", 'other_info':""}
    nav_dict = {'scope':"",'level1':"",'level2':'','level3':'','level4':'','level5':''}
    calc_dict = {'ef':'','cu':''}
    other_dict = {'last_update':'','preference':'','source':''}
    iter=0
    for item in row[1]: #Extract the items from the series returned 
        if column_names[iter] == "Scope":
            nav_dict["scope"] = item
        elif column_names[iter] == "Level_1":
            if type(item) == float:
                nav_dict["level1"] = None
            else:
                nav_dict["level1"] = item
        elif column_names[iter] == "Level_2":
            if type(item) == float:
                nav_dict["level2"] = None
            else:
                nav_dict["level2"] = item
        elif column_names[iter] == "Level_3":
            if type(item) == float:
                nav_dict["level3"] = None
            else:
                nav_dict["level3"] = item
        elif column_names[iter] == "Level_4":
            if type(item) == float:
                nav_dict["level4"] = None
            else:
                nav_dict["level4"] = item
        elif column_names[iter] == "Level_5":
            if type(item) == float:
                nav_dict["level5"] = None
            else:
                nav_dict["level5"] = item
        elif column_names[iter] == "Emission_factor":
            calc_dict["ef"] = item
        elif column_names[iter] == "Calculation Unit":
            calc_dict["cu"] = item
        elif column_names[iter] == "last update":
            other_dict["last_update"] = str(item)
        elif column_names[iter] == "Source":
            other_dict["source"] = item
        elif column_names[iter] == "Preference":
            other_dict["preference"] = item
        else:
            dict["ref_num"] = item
        iter+=1

    dict["navigation_info"] = nav_dict
    dict["calculation_info"] = calc_dict
    dict["other_info"] = other_dict
    list.append(dict)

#Once the data is read, this is where it will be sent to the cloud

#Currently, it will send update requests regardless of if the current entry is the same as the new one

for data in list:
    json_payload = json.dumps(data)
    entry = requests.get('http://localhost:8000/api/carbon/' + str(data["ref_num"])).json()
    try:
        num = entry['ref_num']
    except:
        num = 0
        
    #Case entry exists
    if num == data['ref_num']:
        if entry.values() != data.values():
            requests.put('http://localhost:8000/api/carbon/' + str(data["ref_num"]), data={'payload':json_payload})
    #Case entry does not exist
    else:
        requests.post('http://localhost:8000/api/carbon', data={'payload':json_payload})
