import pandas as pd #Dependencies must include pandas and xlrd, pip install pandas, pip install xlrd
import numpy as np #np is downloaded with pip pandas
import requests

'''
Still to be added:

For time being, the writing will overwrite all entries in the db, even if they are identical, this can be made more efficient
Remove nrows in read excel to read entire flatfile
'''

def readFlatFile(filename):

    try: #Try to read the file, will throw error if not right one ----- in final implementation, remove nrows parameter -----
        excel_frame = pd.read_excel(filename,nrows=10,header=1,engine='xlrd',
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

    #Iterate through the list sending post requests to the API to add new data where no data with the same ref num exists, and updating where one does exist
    for data in list:
        entry = requests.get('http://localhost:8000/api/carbon/' + data["Reference_Number"]).json()
        #Case entry exists
        try:
            requests.put('http://localhost:8000/api/carbon/' + data["Reference_Number"], data=data)
        #Case entry does not exist
        except:
            requests.post('http://localhost:8000/api/carbon/', data=data)

