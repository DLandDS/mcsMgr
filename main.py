import yaml
import sys
import os
from subprocess import run

config_file = open("config.yml")
config = yaml.load(config_file, Loader=yaml.FullLoader)
servers = config["Servers"]
screenPrefix = config["ScreenPrefixId"]
screenStart = "screen -d -m -S " + str(screenPrefix)
screenResume = "screen -d -r " + str(screenPrefix)
screenList = ["screen", "-ls"]
screenStop = "screen -S " + str(screenPrefix)
screenStopFlags = " -X -p 0 stuff "
screenKill = "screen -XS " + str(screenPrefix)
screenKillSignal = " quit"
prejar = "java"
postjar = "-jar"

def exec(command):
    #print(command)
    os.system(command)

def start(server):
    try:
        pwd = os.getcwd()
        os.chdir(server)
        command = ""
        jarfile = config["Servers"][server]["jarfile"]
        maxMem = config["Servers"][server]["maxMem"]
        initMem = config["Servers"][server]["initMem"]
        print("Starting", server, "server", end ="... ")
        if(isServerUp(server)):
            print("Skipped (Already Started)", end ="\n")
        else:
            command += str(screenStart) + str(server) + str(" ")
            command += str(prejar) + str(" ")
            command += str("-Xms") + str(initMem.lower()) + str(" ")
            command += str("-Xmx") + str(maxMem.lower()) + str(" ")
            command += str(postjar) + str(" ") + str(jarfile) + str(" ") + str("nogui")
            exec(command)
            print("")
        os.chdir(pwd)
    except:
        print("Server not found")

def startall():
    for server, info in servers.items():
        start(server)

def listServer():
    i = 1;
    for server, info in servers.items():
        print( i, ". ",server, sep='')
        i+=1

def isServerUp(server):
    up = False
    target = str(screenPrefix) + str(server)
    sessionData = run(screenList, capture_output=True).stdout.decode("utf-8").split("\n")
    for i in sessionData:
        if i.find(target)>0:
            up = True
    return up

def status():
    i = 1
    count = 0
    for server, info in servers.items():
        statusData = isServerUp(server)
        count = count + (0,1)[statusData]
        print(i, ". ", server, " (", ("inactive", "active")[statusData], ")", sep='')
        i += 1
    print(count, "server(s) is active")
def resume(server):
    command = ""
    command += str(screenResume) + str(server)
    exec(command)

def inturrupt(server, signal):
    command = ""
    command += str(screenStop) + str(server) + str(screenStopFlags) + signal
    exec(command)

def stop(server):
    inturrupt(server, "stop^M")


def stopall():
    for server, info in servers.items():
        stop(server)

def restartall():
    for server, info in servers.items():
        restart(server)

def restart(server):
    inturrupt(server, "restart^M")
    start(server)

def kill(server):
    command = ""
    command += str(screenKill) + str(server) + str(screenKillSignal)
    exec(command)

def killall():
    for server, info in servers.items():
        kill(server)

def help():
    print(
        "mcsMgr is Server Manager Minecraft. It allow you to control your Minecraft screen",
        "Author  : Dlands/FTAGame",
        "usages  : mcsmgr [command] [argument]",
        "          mcsmgr [server] : to resume sesion",
        "command :",
        "   start   : Start all server or specific server in argument", #
        "   list    : List all your server in config.yml", #
        "   stop    : Send inturrupt signal to screan session server or specific with argument", #
        "   status  : Show all your server status or specific with argument", #
        "   restart : Send restart signal all to your server or specific with argument", #
        "   kill    : force kill all screen session server or specific with argument", #
        sep='\n'
    )

def main(argv):
    #print(config)
    if argv[1] in servers:
        resume(argv[1])
    else :
        if(len(argv)>1):
            if (argv[1] == "start"):
                if ((len(argv)) > 2):
                    start(argv[2])
                else:
                    startall()
            elif (argv[1] == "list"):
                listServer()
            elif (argv[1] == "stop"):
                if((len(argv))>2):
                    stop(argv[2])
                else:
                    stopall()
            elif (argv[1] == "status"):
                status()
            elif (argv[1] == "restart"):
                if ((len(argv)) > 2):
                    restart(argv[2])
                else:
                    restartall()
            elif (argv[1] == "kill"):
                if((len(argv))>2):
                    kill(argv[2])
                else:
                    killall()
            else:
                print("The", argv[1], "command is unkown")
                help()
        else:
            help()
if __name__ == '__main__':
    main(sys.argv)
