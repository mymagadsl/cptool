#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 作者: mymag (mymag_20@msn.com)
# 授權: 隨意授權,如有修改請分享原始碼給我,感謝!
# 小弟第一次寫 python 程式,如有修改,煩請分享給我
# ============================================
from tkinter import *
import os,sys
import time
import subprocess
import threading
import tkinter.font as tkFont
import tkinter.ttk as ttk
import tkinter.messagebox as tkMsg
# ============================================
# 應用程式設定
# ============================================
ToolVersion = "0.11"                #程式版本
win = Tk()                          #宣告視窗
win.title("➠ 高速耕地執行工具 ➠ Ver "+ToolVersion)
win.geometry("640x530")
win.resizable(False, False)
# 將工作目錄切換至執行檔案所在目錄
cwd = os.path.dirname(os.path.realpath(sys.argv[0]))
os.chdir(cwd)
# 宣告一個結構
startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
# ============================================
# 變數設定,請勿更動
# ============================================
CP_DEBUG = 0                        #除錯指令
counter = 0                         #目前執行次數,不須更動
sec = 0                             #目前階段執行時間,不須更動
cp_delay = 0                        #減少資源占用
cp_pid_cmd =""                      #指定CMD Shell 的 PID
cp_pid_chia_plot = ""               #指定Chia_plot 的 PID
cp_Interrupt = FALSE                #指定是否為中斷耕地過程
# ============================================
# 預設值變數設定,可手動輸入
# ============================================
fontsize = tkFont.Font(size=10)     #字型尺寸
fname = cwd+"\\chia_plot.exe"       #chia_plot 高速P圖程式的檔案名稱
ChiaVer = "1.1.7"                   #安裝的Chia版本(查詢公鑰,礦池公鑰,農民公鑰需要)
PoltNum = "1"                       #執行耕地數量(一次要生產的耕地數量)
CoreNum = "8"                       #耕地使用執行緒數量(依照自己的核心數調整)
BuketNum = "256"                    #耕地使用桶數(不建議更動)
TempDir1 = "D:\\CHIATEMP\\"         #耕地使用的暫存資料夾1
TempDir2 = "D:\\CHIATEMP\\"         #耕地使用的暫存資料夾2(作者建議使用RAM)
TargetDir = "E:\\CHIA\\"            #耕地完成檔案放置位置
PoolPublicKey = ""                  #礦池公鑰,請按顯示公鑰查詢
FarmerPublicKey = ""                #農民公鑰,請按顯示公鑰查詢
# ============================================
# TODO: 清除進度區資料
def UseTime():  
    etrxtext1.delete(0,"end")
    etrxtext2.delete(0,"end")
    etrxtext3.delete(0,"end")
    etrxtext4.delete(0,"end")
    etrxtext5.delete(0,"end")
    etrxtext1.config(bg="#404040",fg="white")
    etrxtext2.config(bg="#C0C0C0")
    etrxtext3.config(bg="#C0C0C0")
    etrxtext4.config(bg="#C0C0C0")
    etrxtext5.config(bg="#C0C0C0")
# ============================================
# TODO: 檢查是否忘了加上斜線
def CheckDir(temp1,temp2,target1):  
    if temp1[-1] != "\\":
        temp1 = temp1+"\\"
        etr4.delete(0,"end")
        etr4.insert(0,temp1)
    if temp2[-1] != "\\":
        temp2 = temp2+"\\"
        etr5.delete(0,"end")
        etr5.insert(0,temp2)
    if target1[-1] != "\\":
        target1 = target1+"\\"
        etr8.delete(0,"end")
        etr8.insert(0,target1)
    return temp1,temp2,target1
# ============================================
# TODO: 顯示並填入公鑰資訊
def ShowMeInfo():
    LocalStr = os.getenv("LOCALAPPDATA")
    if etrver1.get() != "":
        chiaver = etrver1.get()
    else:
        tkMsg.showwarning(title="Chia 版本未設定",message="Chia 版本必須設定才能輸出 Chia 公鑰資訊!\n 這裡將版本預設為1.1.7")
        chiaver = ChiaVer
        etrver1.insert(0,ChiaVer)
    text1.delete(1.0,"end")
    text1.insert(INSERT," ============================================================== \n")
    CmdStr = LocalStr+"\\chia-blockchain\\app-"+chiaver+"\\resources\\app.asar.unpacked\\daemon\\chia.exe"
    if os.path.exists(CmdStr):
        CmdStr ="\""+ CmdStr + "\" keys show"
        # 顯示指令
        text1.insert(INSERT," "+CmdStr+" \n")
        with subprocess.Popen(CmdStr,startupinfo=startupinfo,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE) as p:
            showkeys = p.stdout.read().decode("big5")
            showerr = p.stderr.read().decode("big5")
        text1.insert(INSERT," ============================================================== \n")
        text1.insert(INSERT,showkeys+" \n")
        text1.insert(INSERT,showerr+" \n")
        text1.insert(INSERT," ============================================================== \n")
        lblx.config(text="  ➠ 顯示並填入公鑰資訊...",bg="#404070")
        #指定每組公鑰的分割字串
        keys = showkeys.split("Fingerprint")
        #讀取總共有幾組公鑰字串
        keyscounter = showkeys.count("Fingerprint:")
        text1.insert(INSERT,"  ➠ 您有 "+str(keyscounter)+" 組公鑰...\n")
        text1.see("end")
        global counter
        counter = 1
        strppk=""
        strfpk=""
        # 開始擷取每個公鑰並且填入下拉選單
        while TRUE:
            fpk = keys[counter].partition("Farmer public key")
            ppk = keys[counter].partition("Pool public key")
            fpk = fpk[2].partition("):")
            ppk = ppk[2].partition("):")
            fpk = fpk[2].split()
            ppk = ppk[2].split()
            strppk = strppk + ppk[0]+" "
            strfpk = strfpk + fpk[0]+" "
            if counter == 1:
                ppkComboBox.delete(0,"end")
                fpkComboBox.delete(0,"end")
                ppkComboBox.insert(0,ppk[0])
                fpkComboBox.insert(0,fpk[0])
            #寫入下拉選單,並且指定下一筆資料
            if counter == keyscounter:               
                ppkComboBox["value"] = strppk.split(" ")
                fpkComboBox["value"] = strfpk.split(" ")
                break
            counter += 1
    else:
        text1.insert(INSERT,"  ➠ Chia主程式不存在...\n")
        lblx.config(text="  ➠ Chia主程式不存在...",bg="#404070")
        text1.see(END)
# ============================================
# TODO: 正式開始執行外部指令,P圖開始
def RunCmd(CmdStr):
    #重置變數
    global sec
    sec = 0 
    global cp_delay 
    cp_delay = 0
    global cp_pid_cmd
    global cp_pid_chia_plot
    cp_pid_cmd = ""
    cp_pid_chia_plot = ""
    global cp_Interrupt
    cp_Interrupt = FALSE
    #關閉按鈕
    btn1.config(state=DISABLED)
    btn2.config(state=DISABLED)
    btn3.config(state=DISABLED)
    btnX.config(state=DISABLED)
    Interrupt.config(state=NORMAL)
    etr1.config(state=DISABLED)
    etr2.config(state=DISABLED)
    etr3.config(state=DISABLED)
    etr4.config(state=DISABLED)
    etr5.config(state=DISABLED)
    etr8.config(state=DISABLED)
    ppkComboBox.config(state=DISABLED)
    fpkComboBox.config(state=DISABLED)

    lblx.config(text="   ➠ 耕地準備中,請稍後...... ",bg="#802020")
    text1.insert(INSERT,"   ➠ 耕地準備中,請稍後...... \n")
    text1.insert(INSERT," ============================================================== \n")
    # DEBUG 測試用
    if CP_DEBUG == 1:
        CmdStr = "ping -n 10 8.8.8.8"
    # 開始執行指令
    with subprocess.Popen(CmdStr,startupinfo=startupinfo,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE) as p:
        LineStr = p.stdout.readline().decode("big5")
        lblx.config(text=" ➠ 耕地中,請稍後... ",bg="#802020")
        while p.poll() == None and LineStr !="":
            # 輸出執行LOG
            text1.insert(INSERT,LineStr)
            LineStr = p.stdout.readline().decode("big5")
            if LineStr.find("Process ID:") != -1:    # 清除上一次耕地紀錄
                LStr = LineStr.split()
                UseTime()
                sec = "0"
                cp_pid_chia_plot = LStr[2]
                cp_pid_cmd = str(p.pid)
                text1.insert(INSERT,">> cp_pid_chia_plot = "+cp_pid_chia_plot+"\n")
                text1.insert(INSERT,">> cp_pid_cmd = "+cp_pid_cmd+"\n")
            if LineStr.find("Plot Name:") != -1:    # 顯示目前耕地檔案名稱
                LStr = LineStr.split()
                etrxtext1.insert(0,LStr[2]+".plot")
                etrxtext1.config(bg="#802020")
                cp_delay = 1 #進入P圖階段,開始減少資源占用
            if LineStr.find("[P1]") != -1:
                lblx.config(text=" ➠ 耕地中,第一階段... ",bg="#502020")
                etrxtext2.config(bg="#702020")
            if LineStr.find("Phase 1 took") != -1:
                LStr = LineStr.split()
                etrxtext2.insert(0,LStr[3])
                etrxtext2.config(bg="#206020")
            if LineStr.find("[P2]") != -1:
                lblx.config(text=" ➠ 耕地中,第二階段... ",bg="#602020")
                etrxtext3.config(bg="#702020")
            if LineStr.find("Phase 2 took") != -1:
                LStr = LineStr.split()
                etrxtext3.insert(0,LStr[3])
                etrxtext3.config(bg="#206020")
            if LineStr.find("[P3-") != -1:
                lblx.config(text=" ➠ 耕地中,第三階段... ",bg="#702525")
                etrxtext4.config(bg="#702020")
            if LineStr.find("Phase 3 took") != -1:
                LStr = LineStr.split()
                etrxtext4.insert(0,LStr[3])
                etrxtext4.config(bg="#206020")
            if LineStr.find("[P4]") != -1:
                lblx.config(text=" ➠ 耕地中,第四階段... ",bg="#803030")
                etrxtext5.config(bg="#702020")
            if LineStr.find("Phase 4 took") != -1:
                LStr = LineStr.split()
                etrxtext5.insert(0,LStr[3])
                etrxtext5.config(bg="#206020")
                cp_delay = 0    #P圖階段完成,開始回復即時檢測
            if LineStr.find("Total plot creation time was") != -1:
                stra =  LineStr.split()
                sec = str(round(float(stra[5])/60,1))
            if LineStr.find("Started copy to") != -1:
                lblx.config(text=" ➠ 複製耕地往目標資料夾中,耕地總計時間: "+str(sec)+" 分鐘",bg="#A03030")
                etrxtext1.config(bg="#406040")
                cp_delay = 0
            text1.see(END)
            # 減少資源占用
            if cp_delay == 1:
                time.sleep(0.2)
    text1.insert(INSERT,"\n ============================================================== \n")
    if cp_Interrupt:
        lblx.config(text="   ➽ 中斷耕地完成! 請記得按下右下角清除暫存按鈕! \n",bg="#C0C040")
        text1.insert(INSERT,"   ➽ 中斷耕地完成! 請記得按下右下角清除暫存按鈕! \n")
        text1.see(END)
        btn1.config(state=DISABLED)
        btn2.config(state=DISABLED)
        btnDeleteTemp.config(state=NORMAL)
    else:
        lblx.config(text="   ➠ 耕地完成!  最後耕地總計花費: "+str(sec)+" 分鐘",bg="#409040")
        text1.insert(INSERT,"   ➠ 耕地完成!  最後耕地總計花費: "+str(sec)+" 分鐘 \n")
        text1.see(END)
        btn1.config(state=NORMAL)
        btn2.config(state=NORMAL)
    btn3.config(state=NORMAL)
    btnX.config(state=NORMAL)
    Interrupt.config(state=DISABLED)
    etr1.config(state=NORMAL)
    etr2.config(state=NORMAL)
    etr3.config(state=NORMAL)
    etr4.config(state=NORMAL)
    etr5.config(state=NORMAL)
    etr8.config(state=NORMAL)
    ppkComboBox.config(state=NORMAL)
    fpkComboBox.config(state=NORMAL)
    return p
# ============================================
# TODO: 耕地之前檢查,除錯!
def RunChiaPlot():
    global counter
    global fname
    counter = 0
    err = 0
    #檢查路徑是否正常
    if not os.path.isdir(etr4.get()) or not os.path.isdir(etr5.get()) or not os.path.isdir(etr8.get()):
        err=1
    if not str.isdigit(etr2.get()) or not str.isdigit(etr3.get()):
        err=2
    if not str.isdigit(etr1.get()): #確定不是數字
        if not str("-1"):   # 確定不是 -1
            err=2
    #檢查是否少了斜線
    temp1,temp2,target1 = CheckDir(etr4.get(),etr5.get(),etr8.get())
    #組合外部指令
    if err == 0:
        cmdstr = "\"" + os.path.abspath(fname) + "\" -n "+etr1.get()+" -r "+etr2.get()+" -u "+etr3.get()+" -t "+temp1+" -2 "+temp2+" -d "+target1+" -p "+ppkComboBox.get()+" -f "+fpkComboBox.get()
    if os.path.exists(fname) or CP_DEBUG == 1:
        if etr1.get() == "" or etr2.get() == "" or etr3.get() == "" or etr4.get() == "" or etr5.get() == "" or ppkComboBox.get() == "" or fpkComboBox.get() == "" or etr8.get() == "":
            text1.delete(1.0,"end")
            text1.insert(INSERT," ============================================================== \n")
            text1.insert(INSERT,"   ➠ 設定框有遺漏輸入設定...... \n")
            lblx.config(text="  ➠ 設定框內必須有輸入文字....",bg="#604040")
        else:
            # 開一個執行緒
            if err == 1:
                text1.delete(1.0,"end")
                text1.insert(INSERT," ============================================================== \n")
                text1.insert(INSERT,"   ➠ 暫存1,暫存2,或目標目錄其中有目錄是不存在! \n")
                lblx.config(text="  ➠ 資料夾不存在所以停止耕地....",bg="#202080")
            elif err == 2:
                text1.delete(1.0,"end")
                text1.insert(INSERT," ============================================================== \n")
                text1.insert(INSERT,"   ➠ 耕地數,核心數,桶數量,有格子內輸入不是數字的文字! \n")
                lblx.config(text="  ➠ 有格子內輸入不是數字的文字所以停止耕地....",bg="#202080")
            else:
                counter += 1
                text1.delete(1.0,"end")
                text1.insert(INSERT," ============================================================== \n")
                text1.insert(INSERT,"      第 "+str(counter)+" 次耕地執行中,請稍後!!\n")
                text1.insert(INSERT," ============================================================== \n")
                text1.insert(INSERT,"  "+cmdstr+"\n")
                text1.insert(INSERT," ============================================================== \n")
                text1.insert(INSERT,"   ➠ 耕地開始,請稍後...... \n")
                lblx.config(text="  ➠ 耕地開始,請稍後....")
                t1 = threading.Thread(target=RunCmd,args=(cmdstr,))
                t1.start()
    else:
        text1.delete(1.0,"end")
        text1.insert(INSERT," ============================================================== \n")
        text1.insert(INSERT,"      程式發生一些狀況,請依照以下的說明處理!! \n")
        text1.insert(INSERT," ============================================================== \n")
        text1.insert(INSERT,"\n ➠ 耕地程式 \"" + os.path.abspath(fname) + "\" 檔案不存在!! \n")
        text1.insert(INSERT,"\n ➠ 請前往 https://github.com/stotiks/chia-plotter/releases 下載,放在此資料夾!\n")
        lblx.config(text="  ➠ 程式檢測到一些況狀,請排除...",bg="#604040")
        btn1.config(state=NORMAL)
# ============================================
# TODO: 預設值按鈕,將格子內資料全部改回預設值
def BackDefault():
    text1.delete(1.0,"end")
    lblx.config(text="  ➠ 清除程式執行結果區,並清空變回預設值....",bg="#404040")
    etr1.delete(0,"end")
    etr1.insert(0,PoltNum)
    etr2.delete(0,"end")
    etr2.insert(0,CoreNum)
    etr3.delete(0,"end")
    etr3.insert(0,BuketNum)
    etr4.delete(0,"end")
    etr4.insert(0,TempDir1)
    etr5.delete(0,"end")
    etr5.insert(0,TempDir2)
    ppkComboBox.delete(0,"end")
    ppkComboBox.insert(0,PoolPublicKey)
    fpkComboBox.delete(0,"end")
    fpkComboBox.insert(0,FarmerPublicKey)
    etr8.delete(0,"end")
    etr8.insert(0,TargetDir)
# ============================================
# TODO: 儲存設定,並且結束程式
def ExitApp():  
    SFile = open(cwd+"\\cptool.ini",mode="w")
    SFile.writelines(etr1.get()+"\n")
    SFile.writelines(etr2.get()+"\n")
    SFile.writelines(etr3.get()+"\n")
    SFile.writelines(etr4.get()+"\n")
    SFile.writelines(etr5.get()+"\n")
    SFile.writelines(ppkComboBox.get()+"\n")
    SFile.writelines(fpkComboBox.get()+"\n")
    SFile.writelines(etr8.get()+"\n")
    SFile.writelines(etrver1.get()+"\n")
    SFile.close
    win.destroy()
# ============================================
# TODO: 中斷目前耕地
def InterruptChiaPlot():
    if tkMsg.askyesno("中斷耕地","你確定要中斷耕地嗎?"):
        global cp_pid_cmd
        global cp_pid_chia_plot
        if not cp_pid_cmd == "" and not cp_pid_chia_plot == "":
            try:
                global cp_Interrupt
                text1.insert(INSERT,"\n\n  ➼➼➼ 中斷 PID:"+cp_pid_chia_plot+" 中,這需要一些時間,請稍候!\n")
                lblx.config(text=" ➼➼➼ 正在中斷目前耕地的過程中,請稍候...",bg="#C0C060",fg="#101010")
                with subprocess.Popen('taskkill.exe /F /pid:'+cp_pid_chia_plot,shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as p:
                    text1.insert(INSERT,"\n\n "+p.stdout.read().decode("big5")+"\n")
                time.sleep(0.2)
                UseTime()
                cp_Interrupt = TRUE
            except OSError as e:
                tkMsg.showerror("➼ 發生例外狀況",e)
        else:
            tkMsg.showerror("➼ PID不存在","➼ PID不存在,可能並沒有在耕地中,或是耕地失敗\n"+cp_pid_cmd+"\n"+cp_pid_chia_plot)
        Interrupt.config(state=DISABLED)
# ============================================
# TODO: 刪除暫存的耕地
def DeleteTemp1Temp2File():
    text1.insert(INSERT," ============================================================== \n")
    text1.insert(INSERT,"\n  ➼➼➼ 正在刪除暫存的檔案,這需要一些時間,請稍候!\n")
    lblx.config(text=" ➼➼➼ 正在刪除暫存的檔案,請稍候...",bg="#C0C060",fg="#101010")
    text1.see(END)
    with subprocess.Popen("del "+etr4.get()+"*.tmp /f /q",shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as p1:
        text1.insert(INSERT,p1.stdout.read().decode("big5")+"\n")
    with subprocess.Popen("del "+etr5.get()+"*.tmp /f /q",shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as p2:
        text1.insert(INSERT,"\n"+p2.stdout.read().decode("big5")+"\n")
    text1.insert(INSERT,"  ➼➼➼ 暫存1與暫存2刪除完畢! \n")
    lblx.config(text=" ➼➼➼ 暫存1與暫存2刪除完畢!...",bg="#404040",fg="white")
    text1.see(END)
    btnDeleteTemp.config(state=DISABLED)
    global cp_Interrupt
    if cp_Interrupt:
        cp_Interrupt = FALSE
        btn1.config(state=NORMAL)
        btn2.config(state=NORMAL)
# ============================================
# TODO: 檢查資料夾是否有暫存檔案
def CheckDirList():
    TempDir1List = etr4.get()
    try:
        if not os.path.exists(TempDir1List):
            return False
        else:
            Files=os.listdir(TempDir1List)
        for f in range(len(Files)):
            Files[f]=os.path.splitext(Files[f])[1]
        Str='.tmp'
        if Str in Files:
            return True
        else:
            return False
    except:
        return False
# ==============
#  TODO: 視窗主框架
# ==============
frm1 = Frame(win, width=640,height=480).pack()
# ==============
#  TODO: 視窗分區框架
# ==============
lbf2 = LabelFrame(frm1,text="[輸入區]",font=fontsize)
lbf1 = LabelFrame(frm1,text="[顯示區]",font=fontsize)
lbf3 = LabelFrame(frm1,text="[進度區]",font=fontsize)
lbf2.place(x=10,y=10,width=620,height=100)
lbf1.place(x=10,y=110,width=620,height=300)
lbf3.place(x=10,y=410,width=620,height=110)
# ==============
#  TODO: 顯示區框架
# ==============
lab2 = Label(lbf1,text="程式執行結果區",font=fontsize)
lab2.place(x=150,y=-3)
lbver1 = Label(lbf1,text="請輸入你的Chia版本:")
lbver1.place(x=419,y=-6)
etrver1 = Entry(lbf1,width=8,bg="#303030",fg="white",justify=CENTER)
etrver1.place(x=538,y=-4)
# ==============
#  TODO: 顯示區內文框
# ==============
scroll = Scrollbar(lbf1)
scroll.pack(side=RIGHT , fill=Y)
text1 = Text(lbf1,width=85,height=20,bg="#303030",fg="white", yscrollcommand=scroll.set)
text1.place(x=0,y=16)
scroll.config(command=text1.yview)
# ==============
#  TODO: 創建輸入區設定格
# ==============
lb1 = Label(lbf2,text="耕地數",font=fontsize)
lb1.place(x=4,y=5)
etr1 = Entry(lbf2,bg="#606060",fg="white",width=6,justify=CENTER)
etr1.place(x=55,y=6)
lb1 = Label(lbf2,text="核心數",font=fontsize)
lb1.place(x=108,y=5)
etr2 = Entry(lbf2,bg="#606060",fg="white",width=6,justify=CENTER)
etr2.place(x=155,y=6)
lb1 = Label(lbf2,text="桶數量",font=fontsize)
lb1.place(x=208,y=5)
etr3 = Entry(lbf2,bg="#606060",fg="white",width=6,justify=CENTER)
etr3.place(x=255,y=6)
lb4 = Label(lbf2,text="暫存１",font=fontsize)
lb4.place(x=308,y=5)
etr4 = Entry(lbf2,bg="#606060",fg="white",width=15,justify=LEFT)
etr4.place(x=350,y=6)
lb5 = Label(lbf2,text="暫存２",font=fontsize)
lb5.place(x=458,y=5)
etr5 = Entry(lbf2,bg="#606060",fg="white",width=15,justify=LEFT)
etr5.place(x=500,y=6)
lb8 = Label(lbf2,text="目標路徑",font=fontsize)
lb8.place(x=358,y=30)
etr8 = Entry(lbf2,bg="#606060",fg="white",width=27,justify=LEFT)
etr8.place(x=416,y=31)

lb6 = Label(lbf2,text="礦池公鑰",font=fontsize)
lb6.place(x=4,y=55)
ppkComboBox = ttk.Combobox(width=39,justify=LEFT)
ppkComboBox.place(x=74,y=80)

lb7 = Label(lbf2,text="農民公鑰",font=fontsize)
lb7.place(x=4,y=31)
fpkComboBox = ttk.Combobox(width=39,justify=LEFT)
fpkComboBox.place(x=74,y=55)
# ==============
#  TODO: 創建輸入區按鈕集合
# ==============
btn1 = Button(lbf2,text="執行耕地",font=fontsize,fg="#0000FF",command=RunChiaPlot)
btn1.place(x=480,y=52)
btn2 = Button(lbf2,text="結束程式",font=fontsize ,command=ExitApp)
btn2.place(x=545,y=52)
btn3 = Button(lbf2,text="預設值",font=fontsize ,command=BackDefault)
btn3.place(x=427,y=52)
btnX = Button(lbf2,text="顯示公鑰",font=fontsize ,command=ShowMeInfo)
btnX.place(x=360,y=52)
# ==============
#  TODO: 創建進度區顯示框
# ==============
lblx = Label(lbf3,text=" ➠ 歡迎使用耕地指令工具 Ver "+ToolVersion,bg="#404040",fg="white",width=65,height=2,font=tkFont.Font(size=11))
lblx.place(x=44,y=50)
Interrupt = Button(lbf3,text="中斷\n耕地",font=fontsize,fg="#FF0000",command=InterruptChiaPlot)
Interrupt.place(x=4,y=50)
Interrupt.config(state=DISABLED)
btnDeleteTemp = Button(lbf3,text="清除\n暫存",font=fontsize,fg="#FF0000",command=DeleteTemp1Temp2File)
btnDeleteTemp.place(x=573,y=50)
btnDeleteTemp.config(state=DISABLED)
lblxpn = Label(lbf3,text="目前耕地")
lblxpn.place(x=4,y=0)
etrxtext1 = Entry(lbf3,bg="#404040",fg="white",width=78,justify=LEFT)
etrxtext1.place(x=60,y=2)
lblxpn1 = Label(lbf3,text="第一階段耗時")
lblxpn1.place(x=4,y=25)
etrxtext2 = Entry(lbf3,bg="#C0C0C0",fg="white",width=9,justify=LEFT)
etrxtext2.place(x=85,y=27)
lblxpn2 = Label(lbf3,text="第二階段耗時")
lblxpn2.place(x=155,y=25)
etrxtext3 = Entry(lbf3,bg="#C0C0C0",fg="white",width=9,justify=LEFT)
etrxtext3.place(x=237,y=27)
lblxpn3 = Label(lbf3,text="第三階段耗時")
lblxpn3.place(x=308,y=25)
etrxtext4 = Entry(lbf3,bg="#C0C0C0",fg="white",width=9,justify=LEFT)
etrxtext4.place(x=390,y=27)
lblxpn4 = Label(lbf3,text="第四階段耗時")
lblxpn4.place(x=460,y=25)
etrxtext5 = Entry(lbf3,bg="#C0C0C0",fg="white",width=9,justify=LEFT)
etrxtext5.place(x=543,y=27)
# ==============
#  TODO: 啟動時讀取設定檔案
# ==============
SFileName = cwd+"\\cptool.ini"
if os.path.exists(SFileName):
    SFile = open(cwd+"\\cptool.ini",mode="r")
    list1 =  SFile.readlines()
    etr1.insert(0,list1[0].replace("\n",""))    #讀取時消除換行字元
    etr2.insert(0,list1[1].replace("\n",""))
    etr3.insert(0,list1[2].replace("\n",""))
    etr4.insert(0,list1[3].replace("\n",""))
    etr5.insert(0,list1[4].replace("\n",""))
    # 礦池公鑰|農民公鑰|清除換行字元
    ppkComboBox.insert(0,list1[5].replace("\n",""))
    fpkComboBox.insert(0,list1[6].replace("\n",""))
    # 目標路徑清除換行字元
    etr8.insert(0,list1[7].replace("\n",""))
    try:
        etrver1.insert(0,list1[8].replace("\n",""))
    except:
        etrver1.insert(0,ChiaVer)
    SFile.close
else:
    BackDefault()
# ============================================
# TODO: 啟動系統後第一次顯示的訊息
text1.delete(1.0,"end")
text1.insert(INSERT," ============================================================== \n")
text1.insert(INSERT,"   ➠ 作者: mymag (mymag_20@msn.com)\n")
text1.insert(INSERT,"   ➠ 網頁: http://fgc.tw\n")
text1.insert(INSERT,"   ➠ 版本: "+ToolVersion+" \n")
text1.insert(INSERT,"   ➠ 程式工作目錄: "+cwd+"\n")
text1.insert(INSERT,"   ➠ Telegram 遊戲社群: https://t.me/QiYiWorld\n")
text1.insert(INSERT,"   ➠ 捐贈(Chia XCH): xch1vk3tcw89xtk6uqzgxuyssuwm9s4dsklnaa00hyppevxlg9tpulys98erd4\n")
text1.insert(INSERT,"   ➠ 捐贈(BTC-Bitcoin): 33gxYWhbp5MsSfsrH5J5dr2dmmbhZdFApq\n")
text1.insert(INSERT," ============================================================== \n")
if not os.path.exists(fname):
    text1.insert(INSERT,"\n ----------------------------------------------------------------------------- \n")
    text1.insert(INSERT,"   ➠ 耕地程式 \"" + os.path.abspath(fname) + "\" 檔案不存在!! \n")
    text1.insert(INSERT,"   ➠ 請前往 https://github.com/stotiks/chia-plotter/releases 下載,放在此資料夾!\n")
    text1.insert(INSERT,"   ➠ 本軟體只是輔助工具,需要 chia-plotter 才能使用!\n")
    text1.insert(INSERT," ----------------------------------------------------------------------------- \n")
if CheckDirList():
    btnDeleteTemp.config(state=NORMAL)
    text1.insert(INSERT,"\n ----------------------------------------------------------------------------- \n")
    text1.insert(INSERT,"   ➠ 暫存資料夾內有檔案,建議清除後再執行耕地!\n")
    text1.insert(INSERT," ----------------------------------------------------------------------------- \n")
# ============================================
win.mainloop()