import json, requests, libs.chat

settings = {
    "Username" : "",
    "Password" : "",
    "address" : "10.147.17.24"
}

def CheckLogin():
    return (settings["Username"] != "") and (settings["Password"] != "")

def GetUserGroupByID(groupID : int, conf : dict):
    userDict = json.loads(requests.get("http://" + conf["address"] + ":25108/user/get", auth=(conf["Username"], conf["Password"])).text)
    return userDict["chats"][groupID]

class Commands():
    @staticmethod
    def login(args : list, conf : dict):
        print(" -- SET LOGIN DATA -- ")
        conf["Username"] = input("Username:// ")
        conf["Password"] = input("PASSWORD:// ")
        check = requests.get("http://" + conf["address"] + ":25108/dev/testuser", auth=(conf["Username"], conf["Password"]))
        if check.status_code == 200:
            print(check.text)
            print(" -- LOGIN SUCCESSFUL -- ")
        else:
            print(" -- ERROR: WRONG LOGIN DATA -- ")

    @staticmethod
    def register(args : list, conf : dict):
        print(" -- REGISTER NEW USER -- ")
        email = input("G-Mail:// ")
        emailPass = input("G-Mail-Password:// ")
        username = input("Username:// ")
        userPass = input("UserPassword:// ")
        request = requests.post( "http://" + conf["address"] + ":25108/user/new", auth=(email, emailPass), 
            json={ "username" : username, "password" : userPass } )
        if request.status_code == 401: 
            print(" -- ERROR - G-MAIL LDATA WRONG --")
            return 0
        print(json.loads(request.text)["text"])

    @staticmethod
    def getchats(args : list, conf : dict):
        if CheckLogin():
            print(" -- YOUR CHATS -- ")
            print(" ID | NAME ")
            request = json.loads(requests.get("http://" + conf["address"] + ":25108/user/get", auth=(conf["Username"], conf["Password"])).text)
            for i in range(len(request["chats"])):
                print("", i, "  ", request["chats"][i])
        else:
            print(" -- ERROR: LOGIN FIRST -- ")

    @staticmethod
    def enterchat(args : list, conf : dict):
        while True:
            chatArgs = input("[chat-"+ args[1] + "] cmd:// ").split(" ")
            try:
                getattr(libs.chat.Chat, chatArgs[0])(chatArgs, conf, int(args[1]))
            except AttributeError:
                print("Cmd not found")
            except IndexError:
                print("More arguments are needed")
            except ConnectionError:
                print("Server offline or not found")

while True:
    args = input("cmd:// ").split(" ")
    try:
        getattr(Commands, args[0])(args, settings)
    except AttributeError:
        print("Cmd not found")
    except IndexError:
        print("More arguments are needed")
    except ConnectionError:
        print("Server offline or not found")
