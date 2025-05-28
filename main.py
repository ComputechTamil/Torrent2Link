from seedr import SeedrAPI
from json import load
from time import sleep
from sys import argv
import os
from dotenv import load_dotenv
load_dotenv(".env")
"""Logged in """
##with open("login.json") as f:
##    credential=load(f)
email=os.environ["SEEDR_EMAIL"]
passwd=os.environ["SEEDR_PASSWORD"]
Seedr=SeedrAPI(email=email,password=passwd)



def get_link()->str:
    #see info about the drive,folders and i,get the folder id of what we want
    folder_id=Seedr.get_drive()["folders"][0]["id"]
    #print(folder_id)
    ##see info about the folder contain files info id,etc,we want id to use get_file method 
    file_info=Seedr.get_folder(folder_id)
    #print(file_info)
    file_id=file_info.get("files")[0]["folder_file_id"]
    #print(file_id)
    #it gives the all file info including file id using file id to use return url for normal downloading using get_file method["This method return dict of name,size,url"]
    return Seedr.get_file(file_id)["url"]
def torrent2link(magnet_link,smart_mode=False):
    """smart_mode=True delete the existing video then add a new torrent
       if not enough storage
       Default Off[smart_mode=False]"""
    if smart_mode:
        print("Smart Mode is on...")
        folder_info=Seedr.get_drive()["folders"]
        if len(folder_info)<1:
            pass
        else:
            print("Deleting Existing ")
            print(Seedr.delete_folder(str(folder_info[0]["id"])))
    else:
        print("Smart Mode is not turned on...")
    add_result=Seedr.add_torrent(magnet_link)
    if add_result["result"]==True:
        print(f"Succesfully added the following Torrent\n{add_result['title']}")
        print("Download the Video using the following link!")
        sleep(10)
        #print(get_link())
        return get_link()
    else:
        #print(add_result["result"])
        return add_result["result"]
if __name__=="__main__":
    magnet_link=input("Paste the magnet link:")
    torrent2link(magnet_link,1)
