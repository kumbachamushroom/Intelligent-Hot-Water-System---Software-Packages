import time
import serial
import os
import threading
from subprocess import call
from tkinter import *
import tkinter.font

##Initialize textfile to send currrent temp to website
save_path = '/var/www/html'
completeName = os.path.join(save_path,"load.php")
completeName2 = os.path.join(save_path,"temp.txt")
completeName3 = os.path.join(save_path,"databackup.csv")
completeName4 = os.path.join(save_path,"data.php")

CurrentTemp_File = open(completeName4, "w").close()
CurrentRms_File = open(completeName, "w").close()
Database_File = open(completeName3, "w")
Database_File.write("Date"+","+"Time"+","+"Current A(Rms)"+","+"Temperature °C"+","+"\n")
Database_File.close()



#toFile = raw_input(" ")// CurrentTemp_File.write(toFile) CurrentTemp_File.write(toFile)
##Initialize serial communication to Arduino
ser = serial.Serial('/dev/ttyACM0',115200)
ser.flush()
time.sleep(5)

#ser.flushInput()
##GUI DEFINITIONS
win = Tk()
win.title("Intelligent Hot Water System - Local Interface")
win.geometry("620x150")
myFont = tkinter.font.Font(family = 'Helvetica', size = 12, weight = "bold")

VisualInterface_Frame = Frame(win)
VisualInterface_Frame.pack(side = LEFT)
ControlInterface_Frame = Frame(win)
ControlInterface_Frame.pack(side = LEFT)

AutomaticControl_Frame = Frame(win)
SelfTest_Frame = Frame(win)


##Variable Defenitions for Widgets

##visual interface
Power_Status = StringVar()
Cloud_Status = StringVar()
Cloud_Transmission = StringVar()
Automatic_Mode = StringVar()

##Control Interface
Set_Temp = IntVar()
Actual_Temp = IntVar()
Current_RMS = IntVar()
DataString = 0
CurrentString = 0
TemperatureString = 0
DatabaseString = 0
Temp_Value = []
Actual_Temp = 0
ShutOff = 0
Set_Temp = 50
Update = 0
Time = 0
Date = 0
TempComparison1 = 0
TempComparison2 = 0
RemoteShutOff = 0
Remote_Previous = 1



##Event Functions
def Temp_Plus_Pressed(): #Temperature button pressed
    global Set_Temp
    global ShutOff
    global RemoteShutOff
    RemoteShutOff = 0
    ShutOff = 0
    lblAutomatic_Control['text'] = "Automatic Control: ON"
    Set_Temp = Set_Temp + 1
    if Set_Temp > 100:
        Set_Temp = 100
    #temp = open(completeName2,"w")
    #temp.write(str(Set_Temp)+",on")
    #temp.close()
    lblUserTemp['text'] = "Set Temperature: "+str(Set_Temp)+"°C"
    #SendTemp_Pressed
    #send_TempValue
    
    
    

def send_TempValue():
    global Set_Temp
    ser.flush()
    ser.flushInput()
    ShutOff = 1
    if Set_Temp < 10:
        ser.write(str.encode('Mode:2Temp:'+'00'+str(Set_Temp)+" "))
    elif Set_Temp < 100 and Set_Temp >9:
        ser.write(str.encode('Mode:2Temp:'+'0'+str(Set_Temp)+" "))
        print(str.encode('Mode:2Temp:'+'0'+str(Set_Temp)+" "))
    else:
        ser.write(str.encode('Mode:2Temp:100 '))
    ShutOff = 0
    #win.after(100,send_TempValue)

def Temp_Minus_Pressed(): #Temperature minus button pressed
    global Set_Temp
    global ShutOff
    global RemoteShutOff
    ShutOff = 0
    RemoteShutOff = 0
    lblAutomatic_Control['text'] = "Automatic Control: ON"
    Set_Temp = Set_Temp - 1
    if Set_Temp < 1:
        Set_Temp = 0
    #temp = open(completeName2,"w")
    #temp.write(str(Set_Temp)+",on")
    #temp.close()
    lblUserTemp['text'] = "Set Temperature: "+str(Set_Temp)+"°C"
    #SendTemp_Pressed
    #send_TempValue
    
    
    
def Emergency_OFF_Pressed():
    global ShutOff
    global RemoteShutOff
    global Remote_Previous
    if ShutOff == 0 and RemoteShutOff == 0:
        RemoteShutOff = 1
        ShutOff = 1
        Remote_Previous = 1
        lblAutomatic_Control['text'] = "Automatic Control: OFF"
        lblUserTemp['text'] = "System Shutdown in Effect"
        lblCurrentTemp['text'] = "Measurement Inactive"
        lblCurrent_Rms['text'] = "Measurement Inactive"
        ser.flush()
        ser.flushInput()
        ser.write(str.encode('Mode:3Temp:100 '))
        

    
def close():
    win.destroy() #Close GUI
    
def MenuManage(dummy): #Manage what options are available
        #Hide all buttons
    sel = Lb_ControlInterface.curselection()
    AutomaticControl_Frame.pack_forget()
    SelfTest_Frame.pack_forget()
    win.geometry("655x150")
    #Show relevant buttons depending on list selection
    if sel[0] == 0:
        AutomaticControl_Frame.pack(side = RIGHT)
    elif sel[0] ==1:
        SelfTest_Frame.pack(side = RIGHT)
        ser.write(str.encode('Mode:1Temp:100 '))
        time.sleep(2)
        testcomplete = 1
        ser.flush()
        while testcomplete:
            if ser.inWaiting() > 0:
                testresults = str(ser.readline(8))
                if testresults.find('T') > -1 and testresults.find('H') > -1:
                    print(testresults)
                    if testresults[testresults.find('T')+2:testresults.find('H')]== "1" and testresults[testresults.find('H')+2:testresults.find('H')+3] == "1":
                        print("passed")
                        
                    testcomplete = 0
                    
                
                
        
def run_selfTest():
    print(ser.readline(30))


def cloud_backup():
    backupdirectory = "/home/pi/Dropbox-Uploader/dropbox_uploader.sh upload /var/www/html/databackup.csv /Database"
    call([backupdirectory],shell=True)
    win.after(60000,cloud_backup)

def update_database():
    global ShutOff
    global DataString
    global DataString2
    #se vir lodewyk van die D vooraan!
    if ShutOff == 0:
       DataString = str(DataString)
       if DataString.find('A') > -1:
           if DataString.find('T') > -1:
               CurrentString = DataString[DataString.find('A')+1:DataString.find('T')]
               TemperatureString = DataString[DataString.find('T')+1:DataString.find('r')-1]
           if DataString.find('D') > -1:
               Date = DataString[DataString.find('D')+1:DataString.find('-')]
               DataString2 = DataString[DataString.find('-')+1:]
               Time = DataString2[:DataString2.find('-')]
               Database_File = open(completeName3, "a")
               Database_File.write(Date+","+Time+","+CurrentString+","+TemperatureString+"\n")
               
               Database_File.close()
    win.after(10,update_database)
    
def SendTemp_Pressed():
    global Set_Temp
    ser.flush()
    ser.flushInput()
    ShutOff = 1
    if Set_Temp < 10:
        ser.write(str.encode('Mode:2Temp:'+'0'+'0'+str(Set_Temp)+" "))
    if Set_Temp < 100:
        ser.write(str.encode('Mode:2Temp:'+'0'+str(Set_Temp)+" "))
        print(str.encode('Mode:2Temp:'+'0'+str(Set_Temp)+" "))
    else:
        ser.write(str.encode('Mode:2Temp:100 '))
    ShutOff = 0
        

def update():
    global Actual_Temp
    global Current_RMS
    global Update
    global Set_Temp
    global Temp_Value
    global DataString
    global CurrentString
    global TemperatureString
    global Time
    global Date
    global TempComparison1
    global TempComparison2
    global ShutOff
    global RemoteShutOff
    global Remote_Previous
    #Temp.txt
    with open(completeName2,"r") as temp:
        for line in temp:
            Temp_Value.append(line)
            #print(Temp_Value[1])
            TempComparison1 = Temp_Value[0]
            TempComparison2 = Temp_Value[1]
            if TempComparison2.find('on') > -1 and ShutOff == 0:
                RemoteShutOff = 0
                Remote_Previous = 0
                lblAutomatic_Control['text'] = "Automatic Control: ON"
                if TempComparison1[:TempComparison1.find(',')] != TempComparison2[:TempComparison2.find(',')]:
                    Set_Temp = int(TempComparison2[:TempComparison2.find(',')])
                    lblUserTemp['text'] = "Set Temperature: " + str(Set_Temp) + "°C"
                    ShutOff = 1
                    if Set_Temp < 100:
                        ser.write(str.encode('Mode:2Temp:'+'0'+str(Set_Temp)+" "))
                    else:
                        ser.write(str.encode('Mode:2Temp:100 '))
                    ShutOff = 0
            else:
                if Remote_Previous == 0:
                   Emergency_OFF_Pressed()
                   ShutOff = 0
            Temp_Value = []
            Temp_Value.append(line)
    #if RemoteShutOff == 0:
        #ShutOff = 0
   
    if ShutOff == 0 and RemoteShutOff == 0:
        if ser.inWaiting() > 0:
            print(ser.readline(31))
            DataString = str(ser.readline(31))
            Pos = DataString.find('A');
            if Pos > -1:
                    Pos = DataString.find('T');
                    if Pos > -1:
                        CurrentString = DataString[DataString.find('A')+1:DataString.find('T')]
                        TemperatureString = DataString[DataString.find('T')+1:DataString.find('r')-1]
                        ser.flush()
                        CurrentTemp_File = open(completeName4, "w")
                        CurrentTemp_File.write(str(TemperatureString))
                        CurrentTemp_File.close()
                        CurrentRms_File = open(completeName, "w")
                        CurrentRms_File.write(str(CurrentString))
                        CurrentRms_File.close()
                        lblCurrentTemp['text'] = "Current Temperature: "+str(TemperatureString)+"°C"
                        lblCurrent_Rms['text'] = "Current: " + str(CurrentString) + " A(RMS)"

   
    win.after(10,update)

###Widgets
##Visual Interface
#lblPowerSupply = Label(VisualInterface_Frame,text = "Power Supply: Connected",font = myFont)    
#lblPowerSupply.pack()
lblCloud_Status = Label(VisualInterface_Frame,text = "Cloud Status: Connected",font = myFont)
lblCloud_Status.pack()
lblCloud_Transmission = Label(VisualInterface_Frame,text = "Cloud Transmission: Transmitting",font = myFont)
lblCloud_Transmission.pack()
lblAutomatic_Control = Label(VisualInterface_Frame,text = "Automatic Control: ON", font = myFont)
lblAutomatic_Control.pack()
##Control Interface
Lb_ControlInterface = Listbox(ControlInterface_Frame,width = 25,height = 2)
Lb_ControlInterface.insert(1,"Automatic Temperature Control")
Lb_ControlInterface.insert(2,"Self Test")
Lb_ControlInterface.bind("<Double-Button-1>",MenuManage)
Lb_ControlInterface.pack()
#Automatic temperature control buttons

lblCurrent_Rms = Label(AutomaticControl_Frame, text = "Current: A(rms)",font = myFont)
lblCurrent_Rms.pack(side = TOP)

lblCurrentTemp = Label(AutomaticControl_Frame, text = "Current Temp: 50°C",font = myFont)
lblCurrentTemp.pack(side = TOP)

lblUserTemp = Label(AutomaticControl_Frame,text = "Set Temperature: ",font = myFont)
lblUserTemp.pack(side = TOP)

btnTemp_Plus = Button(AutomaticControl_Frame,text ='+',font=myFont,command=Temp_Plus_Pressed,bg='bisque2',height=1)
btnTemp_Plus.pack(side = LEFT)
btnTemp_Plus = Button(AutomaticControl_Frame,text ='-',font=myFont,command=Temp_Minus_Pressed,bg='bisque2',height=1)
btnTemp_Plus.pack(side = LEFT)
btnSend_Temp = Button(AutomaticControl_Frame,text = 'Set Temperature',font = myFont,command=SendTemp_Pressed,bg='bisque2',height =1)
btnSend_Temp.pack(side = BOTTOM)


#btnSetTemp = B

btnEmergency_OFF = Button(AutomaticControl_Frame,text = 'Deactivate Automatic Control',command=Emergency_OFF_Pressed,bg = 'red',height = 1)
btnEmergency_OFF.pack(side = BOTTOM)



with open (completeName2,"r") as temp:
        Temp_Value = []
        for line in temp:
            Temp_Value.append(line)


update()
#send_TempValue()
update_database()
cloud_backup()
win.mainloop() #Loops Forever




