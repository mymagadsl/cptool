#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 作者: mymag (mymag_20@msn.com)
# 授權: 隨意授權,如有修改請分享原始碼給我,感謝!
# 小弟第一次寫 python 程式,如有修改,煩請分享給我
from sys import stdout
from tkinter import *
import os,sys
import subprocess
import threading
import tkinter.font as tkFont
# ============================================
# 應用程式設定
# ============================================
ToolVersion = "0.04"
win = Tk() 
win.title("== 高速耕地執行工具 == Ver "+ToolVersion)
win.geometry("640x530")
win.resizable(False, False)
# 將工作目錄切換至執行檔案所在目錄
cwd = os.path.dirname(os.path.realpath(sys.argv[0]))
os.chdir(cwd)
# ============================================
# 預設值變數設定,可手動輸入
# ============================================
startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
DEBUG = 0                           #除錯指令
fontsize = tkFont.Font(size=11)     #字型尺寸
counter = 0                         #目前執行次數,不須更動
fname = cwd+"\\chia_plot.exe"       #chia_plot 高速P圖程式的檔案名稱
ChiaVer = "1.1.7"                   #安裝的Chia版本(查詢公鑰,礦池公鑰,農民公鑰需要)
PoltNum = "1"                       #執行耕地數量(一次要生產的耕地數量)
CoreNum = "8"                       #耕地使用執行緒數量(依照自己的核心數調整)
BuketNum = "128"                    #耕地使用桶數(不建議更動)
TempDir1 = "D:\\CHIATEMP\\"         #耕地使用的暫存資料夾1
TempDir2 = "D:\\CHIATEMP\\"         #耕地使用的暫存資料夾2(作者建議使用RAM)
TargetDir = "E:\\CHIA\\"            #耕地完成檔案放置位置
PoolPublicKey = ""                  #礦池公鑰,請按顯示公鑰查詢
FarmerPublicKey = ""                #農民公鑰,請按顯示公鑰查詢
# ============================================

def UseTime():
    etrxtext1.delete(0,"end")
    etrxtext2.delete(0,"end")
    etrxtext3.delete(0,"end")
    etrxtext4.delete(0,"end")
    etrxtext5.delete(0,"end")
    etrxtext1.config(bg="#404040")
    etrxtext2.config(bg="#C0C0C0")
    etrxtext3.config(bg="#C0C0C0")
    etrxtext4.config(bg="#C0C0C0")
    etrxtext5.config(bg="#C0C0C0")

def ShowMeInfo():
    LocalStr = os.getenv("LOCALAPPDATA")
    chiaver = etrver1.get()
    text1.delete(1.0,"end")
    text1.insert(INSERT," ============================================================== \n")
    CmdStr = LocalStr+"\\chia-blockchain\\app-"+chiaver+"\\resources\\app.asar.unpacked\\daemon\\chia.exe"
    if os.path.exists(CmdStr):
        CmdStr = CmdStr + " keys show"
        # 顯示指令
        text1.insert(INSERT," "+CmdStr+" \n")
        with subprocess.Popen(CmdStr,startupinfo=startupinfo,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE) as p:
            showkeys = p.stdout.read().decode("big5")
            showerr = p.stderr.read().decode("big5")
        text1.insert(INSERT," ============================================================== \n")
        text1.insert(INSERT,showkeys+" \n")
        text1.insert(INSERT,showerr+" \n")
        lblx.config(text="  ➠ 顯示並填入公鑰資訊...",bg="#404070")
        fpk = showkeys.partition("Farmer public key")
        ppk = showkeys.partition("Pool public key")
        fpk = fpk[2].partition("):")
        ppk = ppk[2].partition("):")
        fpk = fpk[2].split()
        ppk = ppk[2].split()
        etr6.delete(0,"end")
        etr7.delete(0,"end")
        etr6.insert(0,ppk[0])
        etr7.insert(0,fpk[0])
    else:
        text1.insert(INSERT,"  ➠ Chia主程式不存在...\n")
        lblx.config(text="  ➠ Chia主程式不存在...",bg="#404070")
        text1.see(END)

def RunCmd(CmdStr):
    global counter
    counter = 1
    btn1.config(state=DISABLED)
    btn2.config(state=DISABLED)
    btn3.config(state=DISABLED)
    btnX.config(state=DISABLED)
    lblx.config(text="   ➠ 耕地中,請稍後...... ",bg="#802020")
    text1.insert(INSERT,"   ➠ 耕地中,請稍後...... \n")
    text1.insert(INSERT," ============================================================== \n")
    # DEBUG 測試用
    if DEBUG == 1:
        CmdStr = "ping -n 10 8.8.8.8"
    # 開始執行指令
    with subprocess.Popen(CmdStr,startupinfo=startupinfo,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE) as p:
        LineStr = p.stdout.readline().decode("big5")
        lblx.config(text=" ➠ 耕地中,請稍後... ",bg="#802020")
        sec = "0"
        # 清除使用時間的顏色與資料
        UseTime()
        while p.poll() == None and LineStr !="":
            text1.insert(INSERT,LineStr)
            LineStr = p.stdout.readline().decode("big5")
            if LineStr.find("Plot Name:") != -1:    # 顯示目前耕地檔案名稱
                LStr = LineStr.split()
                etrxtext1.insert(0,LStr[2])
                etrxtext1.config(bg="#602020")
            if LineStr.find("[P1]") != -1:
                lblx.config(text=" ➠ 耕地中,第一階段... ",bg="#702020")
            if LineStr.find("Phase 1 took") != -1:
                LStr = LineStr.split()
                etrxtext2.insert(0,LStr[3])
                etrxtext2.config(bg="#702020")
            if LineStr.find("[P2]") != -1:
                lblx.config(text=" ➠ 耕地中,第二階段... ",bg="#752020")
            if LineStr.find("Phase 2 took") != -1:
                LStr = LineStr.split()
                etrxtext3.insert(0,LStr[3])
                etrxtext3.config(bg="#702020")
            if LineStr.find("[P3-") != -1:
                lblx.config(text=" ➠ 耕地中,第三階段... ",bg="#802525")
            if LineStr.find("Phase 3 took") != -1:
                LStr = LineStr.split()
                etrxtext4.insert(0,LStr[3])
                etrxtext4.config(bg="#702020")
            if LineStr.find("[P4]") != -1:
                lblx.config(text=" ➠ 耕地中,第四階段... ",bg="#803030")
            if LineStr.find("Phase 4 took") != -1:
                LStr = LineStr.split()
                etrxtext5.insert(0,LStr[3])
                etrxtext5.config(bg="#702020")
            if LineStr.find("Total plot creation time was") != -1:
                stra =  LineStr.split()
                sec = str(round(float(stra[5])/60,1))
            if LineStr.find("Started copy to") != -1:
                lblx.config(text=" ➠ 複製耕地往目標資料夾中...耕地總計時間: "+sec+" 分鐘",bg="#A03030")
                etrxtext1.config(bg="#408040")
            text1.see(END)
    text1.insert(INSERT," ============================================================== \n")
    lblx.config(text="   ➠ 耕地完成!耕地總計花費: "+sec+" 分鐘",bg="#408040")
    text1.insert(INSERT,"   ➠ 耕地完成!耕地總計花費: "+sec+" 分鐘 \n")
    text1.see(END)
    btn1.config(state=NORMAL)
    btn2.config(state=NORMAL)
    btn3.config(state=NORMAL)
    btnX.config(state=NORMAL)
    return p

def runme():
    global counter
    global fname
    counter = 1
    cmdstr = os.path.abspath(fname) + " -n "+etr1.get()+" -r "+etr2.get()+" -u "+etr3.get()+" -t "+etr4.get()+" -2 "+etr5.get()+" -d "+etr8.get()+" -p "+etr6.get()+" -f "+etr7.get()
    if os.path.exists(fname) or DEBUG == 1:
        if etr1.get() == "" or etr2.get() == "" or etr3.get() == "" or etr4.get() == "" or etr5.get() == "" or etr6.get() == "" or etr7.get() == "" or etr8.get() == "":
            text1.delete(1.0,"end")
            text1.insert(INSERT,"   ➠ 設定框有遺漏輸入設定...... \n")
            lblx.config(text="  ➠ 設定框內必須有輸入文字....",bg="#604040")
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
            # 開一個執行緒
            t1 = threading.Thread(target=RunCmd,args=(cmdstr,))
            t1.start()
    else:
        text1.delete(1.0,"end")
        text1.insert(INSERT," ============================================================== \n")
        text1.insert(INSERT,"      程式發生一些狀況,請依照以下的說明處理!! \n")
        text1.insert(INSERT," ============================================================== \n")
        text1.insert(INSERT,"\n 耕地程式 "+ os.path.abspath(fname) +" 檔案不存在!! \n\n 請前往 https://github.com/stotiks/chia-plotter/releases 下載,放在此資料夾!\n")
        text1.insert(INSERT,"\n 請查看指令的程式所在位置: \n "+cmdstr+" \n")
        lblx.config(text="  ➠ 程式檢測到一些況狀,請排除...",bg="#604040")
        btn1.config(state=NORMAL)

def checkCP():
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
    etr6.delete(0,"end")
    etr6.insert(0,PoolPublicKey)
    etr7.delete(0,"end")
    etr7.insert(0,FarmerPublicKey)
    etr8.delete(0,"end")
    etr8.insert(0,TargetDir)

def ExitApp():
    SFile = open(cwd+"\\cptool.ini",mode="w")
    SFile.writelines(etr1.get()+"\n")
    SFile.writelines(etr2.get()+"\n")
    SFile.writelines(etr3.get()+"\n")
    SFile.writelines(etr4.get()+"\n")
    SFile.writelines(etr5.get()+"\n")
    SFile.writelines(etr6.get()+"\n")
    SFile.writelines(etr7.get()+"\n")
    SFile.writelines(etr8.get()+"\n")
    SFile.close
    win.destroy()

# ==============
#  視窗主框架
# ==============
frm1 = Frame(win, width=640,height=480).pack()
# ==============
#  視窗分區框架
# ==============
lbf2 = LabelFrame(frm1,text="[輸入區]",font=fontsize)
lbf1 = LabelFrame(frm1,text="[顯示區]",font=fontsize)
lbf3 = LabelFrame(frm1,text="[進度區]",font=fontsize)
lbf2.place(x=10,y=10,width=620,height=100)
lbf1.place(x=10,y=110,width=620,height=300)
lbf3.place(x=10,y=410,width=620,height=110)

# ==============
#  顯示區框架
# ==============
lab2 = Label(lbf1,text="程式執行結果區:",font=fontsize)
lab2.place(x=0,y=-3)

lbver1 = Label(lbf1,text="請輸入你的Chia版本:")
lbver1.place(x=419,y=-6)
etrver1 = Entry(lbf1,width=8,justify=CENTER)
etrver1.insert(0,ChiaVer)
etrver1.place(x=538,y=-4)
# ==============
#  顯示區內文框
# ==============
scroll = Scrollbar(lbf1)
scroll.pack(side=RIGHT , fill=Y)
text1 = Text(lbf1,width=85,height=20,bg="#303030",fg="white", yscrollcommand=scroll.set)
text1.place(x=0,y=16)
scroll.config(command=text1.yview)

# ==============
#  輸入區設定格
# ==============
lb1 = Label(lbf2,text="耕地數:",font=fontsize)
lb1.place(x=10,y=5)
etr1 = Entry(lbf2,bg="#606060",fg="white",width=6,justify=CENTER)
etr1.place(x=55,y=6)
lb1 = Label(lbf2,text="核心數",font=fontsize)
lb1.place(x=110,y=5)
etr2 = Entry(lbf2,bg="#606060",fg="white",width=6,justify=CENTER)
etr2.place(x=155,y=6)
lb1 = Label(lbf2,text="桶數量",font=fontsize)
lb1.place(x=210,y=5)
etr3 = Entry(lbf2,bg="#606060",fg="white",width=6,justify=CENTER)
etr3.place(x=255,y=6)
lb4 = Label(lbf2,text="暫存１",font=fontsize)
lb4.place(x=310,y=5)
etr4 = Entry(lbf2,bg="#606060",fg="white",width=15,justify=LEFT)
etr4.place(x=350,y=6)
lb5 = Label(lbf2,text="暫存２",font=fontsize)
lb5.place(x=460,y=5)
etr5 = Entry(lbf2,bg="#606060",fg="white",width=15,justify=LEFT)
etr5.place(x=500,y=6)
lb6 = Label(lbf2,text="礦池公鑰",font=fontsize)
lb6.place(x=10,y=30)
etr6 = Entry(lbf2,bg="#606060",fg="white",width=40,justify=LEFT)
etr6.place(x=73,y=31)
lb7 = Label(lbf2,text="農民公鑰",font=fontsize)
lb7.place(x=10,y=55)
etr7 = Entry(lbf2,bg="#606060",fg="white",width=40,justify=LEFT)
etr7.place(x=73,y=56)
lb8 = Label(lbf2,text="目標路徑",font=fontsize)
lb8.place(x=360,y=30)
etr8 = Entry(lbf2,bg="#606060",fg="white",width=27,justify=LEFT)
etr8.place(x=416,y=31)
# ==============
#  輸入區按鈕集合
# ==============
btn1 = Button(lbf2,text="執行耕地",command=runme)
btn1.place(x=480,y=52)
btn2 = Button(lbf2,text="結束程式" ,command=ExitApp)
btn2.place(x=550,y=52)
btn3 = Button(lbf2,text="預設值" ,command=checkCP)
btn3.place(x=425,y=52)
btnX = Button(lbf2,text="顯示公鑰" ,command=ShowMeInfo)
btnX.place(x=360,y=52)

# ==============
#  進度區顯示框
# ==============
lblx = Label(lbf3,text=" ➠ 歡迎使用耕地指令工具...",bg="#404040",fg="white",width=75,height=2,font=fontsize)
lblx.place(x=4,y=50)
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
#  讀取設定檔案
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
    etr6.insert(0,list1[5].replace("\n",""))
    etr7.insert(0,list1[6].replace("\n",""))
    etr8.insert(0,list1[7].replace("\n",""))
    SFile.close
else:
    checkCP()
text1.delete(1.0,"end")
text1.insert(INSERT," ============================================================== \n")
text1.insert(INSERT,"   ➠ 作者: mymag (mymag_20@msn.com) \n")
text1.insert(INSERT,"   ➠ 網頁: http://fgc.tw \n")
text1.insert(INSERT,"   ➠ 版本: "+ToolVersion+" \n")
text1.insert(INSERT,"   ➠ 程式工作目錄: "+cwd+"\n")
text1.insert(INSERT,"   ➠ 捐贈(chia): xch1vk3tcw89xtk6uqzgxuyssuwm9s4dsklnaa00hyppevxlg9tpulys98erd4 \n")
text1.insert(INSERT,"   ➠ 捐贈(btc): xch1vk3tcw89xtk6uqzgxuyssuwm9s4dsklnaa00hyppevxlg9tpulys98erd4 \n")
text1.insert(INSERT," ============================================================== \n")

win.mainloop()