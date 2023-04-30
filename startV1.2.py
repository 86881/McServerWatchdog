#-*- coding:utf-8 -*-
#WatchDog made by 86881 at 20230429
#------------------Default setting---------------------
hostname='127.0.0.1'#伺服器位址
port='25565'#埠口
detectTime=30 #週期(s)
folderName='server'#伺服器資料夾
serverName='start.bat'#執行檔
token=''#line notify token
#------------------setting end------------------------
from http.client import responses
import os
import time
import subprocess
import time
import threading
from time import gmtime, strftime
from xmlrpc.client import ResponseError
try:
    import tkinter as tk
except ImportError:
    os.system('pip install tkinter')
    import tkinter as tk
    
try:
    import requests
except ImportError:
    os.system('pip install requests')
    import requests
state='waitPing'
running=True
reOnline=False
def main():
    while running:
        pingHost()
        if state=='Offline':
            offline()
        elif state=='Online':
            online()
        showlog()
        time.sleep(detectTime)
        
runMain=threading.Thread(target=main)
runMain.daemon=True

def onSet():
    global hostname
    global port
    global detectTime
    global folderName
    global serverName
    global token
    hostname=entry0.get()
    port=entry1.get()
    detectTime=int(entry2.get())
    folderName=entry3.get()
    serverName=entry4.get()
    token=entry5.get()
    setting=[['伺服器位址','埠口','週期(s)','伺服器資料夾','執行檔','token'],[hostname,port,detectTime,folderName,serverName,token]]
    for i in range(len(setting[0])):
        print(setting[0][i],":",setting[1][i])
    if os.path.isfile('watchdog.log')==False:
        with open('watchdog.log', 'w') as f:
            f.write('Hostname: '+hostname)
            f.write(' Port: '+port+'\n')
    else:
        with open('watchdog.log', 'a') as f:
            f.write('Hostname: '+hostname)
            f.write(' Port: '+port+'\n')
    startButton.destroy()
    url = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': 'Bearer ' + token}
    data = {'message':'Minecraft Server Watchdog Start！'}
    data = requests.post(url, headers=headers, data=data)
    print("Start ping!")
    runMain.start()
def Quit():
    global running
    url = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': 'Bearer ' + token}
    data = {'message':'Minecraft Server Watchdog Stop！'}
    data = requests.post(url, headers=headers, data=data)
    print("Quit!")
    running=False
    window.quit()
window = tk.Tk()
window.title('Minecraft Server Watchdog')
window.geometry("500x250+250+150")
setting=[['伺服器位址','埠口','週期(s)','伺服器資料夾','執行檔','token'],[hostname,port,detectTime,folderName,serverName,token]]
'''
for i in range(len(setting[0])):
    tempString='label'+str(i)
    tempString = tk.Label(window, text = setting[0][i])
    tempString.grid(column=0, row=i)
    entry_text = tk.StringVar()
    tempString='entry'+str(i)
    tempString = tk.Entry(window, width = 20, textvariable=entry_text)
    entry_text.set(setting[1][i])
    tempString.grid(column=1, row=i)
    '''
label0 = tk.Label(window, text = setting[0][0])
label0.grid(column=0, row=0)
entry_text = tk.StringVar()
entry0 = tk.Entry(window, width = 20, textvariable=entry_text)
entry_text.set(setting[1][0])
entry0.grid(column=1, row=0)
label1 = tk.Label(window, text = setting[0][1])
label1.grid(column=0, row=1)
entry_text = tk.StringVar()
entry1 = tk.Entry(window, width = 20, textvariable=entry_text)
entry_text.set(setting[1][1])
entry1.grid(column=1, row=1)
label2 = tk.Label(window, text = setting[0][2])
label2.grid(column=0, row=2)
entry_text = tk.StringVar()
entry2 = tk.Entry(window, width = 20, textvariable=entry_text)
entry_text.set(setting[1][2])
entry2.grid(column=1, row=2)
label3 = tk.Label(window, text = setting[0][3])
label3.grid(column=0, row=3)
entry_text = tk.StringVar()
entry3 = tk.Entry(window, width = 20, textvariable=entry_text)
entry_text.set(setting[1][3])
entry3.grid(column=1, row=3)
label4 = tk.Label(window, text = setting[0][4])
label4.grid(column=0, row=4)
entry_text = tk.StringVar()
entry4 = tk.Entry(window, width = 20, textvariable=entry_text)
entry_text.set(setting[1][4])
entry4.grid(column=1, row=4)
label5 = tk.Label(window, text = setting[0][5])
label5.grid(column=0, row=5)
entry_text = tk.StringVar()
entry5 = tk.Entry(window, width = 20, textvariable=entry_text)
entry_text.set(setting[1][5])
entry5.grid(column=1, row=5)
startButton = tk.Button(window, text = "Start", command = onSet)
quitButton = tk.Button(window, text = "Quit", command = Quit)
startButton.grid(column=0, row=len(setting[0]))
quitButton.grid(column=1, row=len(setting[0]))
print('Default setting\nHostname: '+hostname+' Port: '+port)

def pingHost():
    global hostname 
    global port
    global state
    print("Pinging...")
    response=subprocess.check_output(["powershell","Test-NetConnection",hostname,"-port",port],shell=True, text=True)
    response=list( filter( None, response.split('\n') ) )
    with open('watchdog.log', 'a') as f:
        f.write('['+strftime("%d %b %Y %H:%M:%S", time.localtime())+'] ')
        print('['+strftime("%d %b %Y %H:%M:%S", time.localtime())+'] ',end='')
        #print(response[-1].split(":")[-1])
        if response[-1].split(":")[-1]=='True':#True
            f.write('Online')
            print('Online')
            state='Online'
        else:#False
            f.write('Offline')
            print('Offline')
            state='Offline'

            if len(response)!=9:
                f.write('Error\n')
                f.write('Output: \n    ')
                for i in response:
                    f.write(i+'\n    ')
                print('Error Output was writed in log')
        f.write('\n')

def process_exists(process_name):
    progs = str(subprocess.check_output('tasklist'))
    if process_name in progs:
        return True
    else:
        return False

def showlog():
    with open('watchdog.log', 'r') as f:
        log = tk.Label(window, text ='Logs')
        log.grid(column=4, row=0)
        rowCount=1
        for line in f.readlines()[-10:]:
            log = tk.Label(window, text ='                              ')
            log.grid(column=4, row=rowCount)
            log = tk.Label(window, text ='  '+line.replace('\n','')+'  ')
            log.grid(column=4, row=rowCount)
            rowCount+=1
def online():
    global reOnline
    global token
    if reOnline==True:
        url = 'https://notify-api.line.me/api/notify'
        headers = {'Authorization': 'Bearer ' + token}
        data = {'message':'伺服器恢復連線！'}
        data = requests.post(url, headers=headers, data=data)
        reOnline=False

def offline():
    global reOnline
    global token
    if reOnline==False:
        url = 'https://notify-api.line.me/api/notify'
        headers = {'Authorization': 'Bearer ' + token}
        data = {'message':'伺服器離線！'}
        data = requests.post(url, headers=headers, data=data)
        reOnline=True
    if( process_exists("java.exe") =="True"):#Jave執行中
        response=subprocess.check_output(["powershell","Test-NetConnection www.google.com"],shell=True, text=True)
        response=list( filter( None, response.split('\n') ) )
        print(response)
        if( len(response)==6 ):
           print("The computer can connect to the network but not the server.")
           with open('watchdog.log', 'a') as f:
                f.write("The computer can connect to the network but not the server\n")
        elif( len(response)==9 ):
           print("The computer can't connect to the network, and neither can the server.")
           with open('watchdog.log', 'a') as f:
                f.write("The computer can't connect to the network, and neither can the server.\n")
        else:
            print(response)
            with open('watchdog.log', 'a') as f:
                f.write("something wrong...")
                f.write('    Output: \n        ')
                for i in response:
                    f.write(i+'\n        ')
    else:#Java未執行
        print("Try restarting the server")
        with open('watchdog.log', 'a') as f:
            f.write("Try restarting the server.\n")
        os.chdir(folderName)
        os.system("start "+serverName)
        os.chdir('../')
        
window.mainloop()
    
   
