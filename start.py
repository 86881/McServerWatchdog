#-*- coding:utf-8 -*-
#WatchDog made by 86881 at 20230429
#------------------Default setting---------------------
hostname='127.0.0.1'#伺服器位址
port='25505'#埠口
detectTime=30 #週期(s)
folderName='server'#伺服器資料夾
serverName='start.bat'#執行檔
#------------------setting end------------------------
import os
import time
import subprocess
import time
import threading
from time import gmtime, strftime
try:
    import tkinter as tk
except ImportError:
    os.system('pip install tkinter')
    import tkinter as tk
state='waitPing'
running=True
def main():
    while running:
        pingHost()
        if state=='Offline':
            offline()
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
    hostname=entry0.get()
    port=entry1.get()
    detectTime=int(entry2.get())
    folderName=entry3.get()
    serverName=entry4.get()
    setting=[['伺服器位址','埠口','週期(s)','伺服器資料夾','執行檔'],[hostname,port,detectTime,folderName,serverName]]
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
    print("Start ping!")
    runMain.start()
def Quit():
    global running
    print("Quit!")
    running=False
    window.quit()
window = tk.Tk()
window.title('Minecraft Server Watchdog')
window.geometry("500x250+250+150")
setting=[['伺服器位址','埠口','週期(s)','伺服器資料夾','執行檔'],[hostname,port,detectTime,folderName,serverName]]
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
        if len(response)==6:#True
            f.write('Online')
            print('Online')
            state='Online'
        elif len(response)==9:#False
            f.write('Offline')
            print('Offline')
            state='Offline'
        else:
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


def offline():
    headers = {
        "Authorization": "Bearer " + "你的權杖(token)",
        "Content-Type": "application/x-www-form-urlencoded"
    }
 
    params = {"message": "伺服器已離線"}
 
    r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=params)
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
    
   