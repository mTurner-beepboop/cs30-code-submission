import dns
import pymongo

def connect(user, password):
    try:
        client = pymongo.MongoClient("mongodb+srv://"+user+":"+password+"@cluster0.rpq32.mongodb.net/flatfile?retryWrites=true&w=majority")
        client.server_info()#Check connection to the server
        db = client['flatfile']
        return db
    except:
        return -1 #Return an error code if username and password is invalid