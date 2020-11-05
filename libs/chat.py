import json, requests
from threading import Thread
from tkinter import *
from time import sleep

def GetUserGroupByID(groupID : int, conf : dict) -> str:
    userDict = json.loads(requests.get("http://" + conf["address"] + ":25108/user/get", auth=(conf["Username"], conf["Password"])).text)
    return userDict["chats"][groupID]

class CmdWindow(Tk):
    def __init__(self, groupID : int, conf : dict):
        super().__init__()
        self.geometry("500x100")
        self.title("Msg-Window")
        self.resizable(0, 0)
        self.groupID = GetUserGroupByID(groupID, conf)
        self.conf = conf
        self.CreateWidgets()
        self.mainloop()

    def CreateWidgets(self):
        self.frame = Frame(self, width=500, height=100, bg="gray")
        self.frame.place(x=0, y=0)
        self.text = Text(self, width=500, height=100, bg="white")
        self.text.place(x=0, y=0)
        self.sendButton = Button(self, width=100, height=100, bg="white", text="send", command=self.SendButtonPress)
        self.sendButton.place(x=400, y=0)

    def SendButtonPress(self):
        sendData = { "chatID" : self.groupID, "message" : self.text.get("1.0", "end") }
        if sendData["message"] == "\n":
            print("Error, write text idiot")
        else:
            print("System>>", json.loads(requests.post("http://10.147.17.24:25108/chat/add/message", auth=(self.conf["Username"], self.conf["Password"]), json=sendData).text)["text"])
            self.text.replace("1.0", "end", "")
        

def StartWindow(groupID : int, conf : dict):
    cmd = CmdWindow(groupID, conf)
    
class Chat():
    @staticmethod
    def start(args : list, conf : dict, chatID : int):
        startThread = Thread(target=StartWindow, args=(chatID, conf))
        startThread.start()

        while True:
            sleep(0.25)
            request = requests.post( "http://" + conf["address"] + ":25108/chat/get/unread", auth=(conf["Username"], conf["Password"]), 
                json={ "chatID" : GetUserGroupByID(chatID, conf) } )
            jsonDict = json.loads(request.text)
            if len(jsonDict["text"]) > 0:
                for msg in jsonDict["text"]:
                    message = msg["sender"] + "\nTime: " + msg["time"] + "\n" + msg["content"]
                    print(message)
