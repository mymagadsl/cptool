#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 作者: mymag (mymag_20@msn.com)
# 授權: 隨意授權,如有修改請分享原始碼給我,感謝!
# 小弟第一次寫 python 程式,如有修改,煩請分享給我
from sys import stdout
from tkinter import *
import os
import subprocess
import threading
import tkinter.font as tkFont

ToolVersion = "0.02"
win = Tk() 
win.title("== 高速耕地執行工具 == Ver "+ToolVersion)
win.geometry("640x480")
# ============================================
# 預設值變數設定,可手動輸入
# ============================================
fontsize = tkFont.Font(size=11)     #字型尺寸
DEBUG = 0                           #除錯指令
counter = 0                         #目前執行次數,不須更動
fname = "chia_plot.exe"             #chia_plot 高速P圖程式的檔案名稱
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

def ShowMeInfo():
    LocalStr = os.getenv("LOCALAPPDATA")
    chiaver = etrver1.get()
    text1.delete(1.0,"end")
    text1.insert(INSERT," ============================================================== \n")
    text1.insert(INSERT,"   ➠ 作者: mymag (mymag_20@msn.com) \n")
    text1.insert(INSERT,"   ➠ 網頁: http://fgc.tw \n")
    text1.insert(INSERT,"   ➠ 版本: Version "+ToolVersion+" \n")
    text1.insert(INSERT,"   ➠ 捐贈: xch1vk3tcw89xtk6uqzgxuyssuwm9s4dsklnaa00hyppevxlg9tpulys98erd4 \n")
    text1.insert(INSERT," ============================================================== \n")
    CmdStr = LocalStr+"\\chia-blockchain\\app-"+chiaver+"\\resources\\app.asar.unpacked\\daemon\\chia.exe"
    if os.path.exists(CmdStr):
        CmdStr = CmdStr + " keys show"
        text1.insert(INSERT,CmdStr+" \n")
        with subprocess.Popen(CmdStr,shell=False,stdout=subprocess.PIPE) as p:
            showkeys = p.stdout.read().decode("big5")
        text1.insert(INSERT," ============================================================== \n")
        text1.insert(INSERT,showkeys+" \n")
        lblx.config(text="  ➠ 顯示公鑰資訊...",bg="#404070")
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
        CmdStr = "ping -n 22 8.8.8.8"
    # 開始執行指令
    with subprocess.Popen(CmdStr,shell=True,stdout=subprocess.PIPE) as p:
        LineStr = p.stdout.readline()
        LineProcess = "➠"
        while p.poll() == None and LineStr !="":
            text1.insert(INSERT,LineStr.decode("big5"))
            LineStr = p.stdout.readline()
            LineProcess = LineProcess + "➠"
            counter += 1
            if counter == 21:
                counter = 1
                LineProcess = "➠"
            lblx.config(text=" ➠ 耕地中,請稍後... "+LineProcess,bg="#802020")
            text1.see(END)
    
    text1.insert(INSERT," ============================================================== \n")
    lblx.config(text="   ➠ 耕地完成....... ",bg="#408040")
    text1.insert(INSERT,"   ➠ 耕地完成...... \n")
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
    etr1.insert(0,"1")
    etr2.delete(0,"end")
    etr2.insert(0,"8")
    etr3.delete(0,"end")
    etr3.insert(0,"128")
    etr4.delete(0,"end")
    etr4.insert(0,"D:\\")
    etr5.delete(0,"end")
    etr5.insert(0,"D:\\")
    etr6.delete(0,"end")
    etr6.insert(0,"")
    etr7.delete(0,"end")
    etr7.insert(0,"")
    etr8.delete(0,"end")
    etr8.insert(0,"E:\\")


frm1 = Frame(win, width=640,height=480).pack()

lbf1 = LabelFrame(frm1,text="[顯示區]",font=fontsize)
lbf2 = LabelFrame(frm1,text="[輸入區]",font=fontsize)
lbf3 = LabelFrame(frm1,text="[進度區]",font=fontsize)

lbf2.place(x=10,y=10,width=620,height=100)
lbf1.place(x=10,y=110,width=620,height=300)
lbf3.place(x=10,y=410,width=620,height=60)

lab2 = Label(lbf1,text="........程式執行結果區.......",font=fontsize)
lab2.pack()

scroll = Scrollbar(lbf1)
scroll.pack(side=RIGHT , fill=Y)
text1 = Text(lbf1,width=85,height=20,bg="#303030",fg="white", yscrollcommand=scroll.set)
text1.pack()
scroll.config(command=text1.yview)


lb1 = Label(lbf2,text="圖數量")
lb1.place(x=10,y=5)
etr1 = Entry(lbf2,bg="#606060",fg="white",width=6,justify=CENTER)
etr1.insert(0,PoltNum)
etr1.place(x=55,y=6)
lb1 = Label(lbf2,text="核心數")
lb1.place(x=110,y=5)
etr2 = Entry(lbf2,bg="#606060",fg="white",width=6,justify=CENTER)
etr2.insert(0,CoreNum)
etr2.place(x=155,y=6)
lb1 = Label(lbf2,text="桶數量")
lb1.place(x=210,y=5)
etr3 = Entry(lbf2,bg="#606060",fg="white",width=6,justify=CENTER)
etr3.insert(0,BuketNum)
etr3.place(x=255,y=6)

lb4 = Label(lbf2,text="暫存１")
lb4.place(x=310,y=5)
etr4 = Entry(lbf2,bg="#606060",fg="white",width=15,justify=LEFT)
etr4.insert(0,TempDir1)
etr4.place(x=350,y=6)

lb5 = Label(lbf2,text="暫存２")
lb5.place(x=460,y=5)
etr5 = Entry(lbf2,bg="#606060",fg="white",width=15,justify=LEFT)
etr5.insert(0,TempDir2)
etr5.place(x=500,y=6)

lb6 = Label(lbf2,text="礦池公鑰")
lb6.place(x=10,y=30)
etr6 = Entry(lbf2,bg="#606060",fg="white",width=40,justify=LEFT)
etr6.insert(0,PoolPublicKey)
etr6.place(x=73,y=31)

lb7 = Label(lbf2,text="農民公鑰")
lb7.place(x=10,y=55)
etr7 = Entry(lbf2,bg="#606060",fg="white",width=40,justify=LEFT)
etr7.insert(0,FarmerPublicKey)
etr7.place(x=73,y=56)

lb8 = Label(lbf2,text="目標路徑")
lb8.place(x=360,y=30)
etr8 = Entry(lbf2,bg="#606060",fg="white",width=27,justify=LEFT)
etr8.insert(0,TargetDir)
etr8.place(x=416,y=31)

lbver1 = Label(lbf1,text="請輸入你的Chia版本:")
lbver1.place(x=419,y=0)
etrver1 = Entry(lbf1,width=8,justify=CENTER)
etrver1.insert(0,ChiaVer)
etrver1.place(x=538,y=1)

btn1 = Button(lbf2,text="執行耕地",command=runme)
btn1.place(x=480,y=52)
btn2 = Button(lbf2,text="結束程式" ,command = win.destroy)
btn2.place(x=550,y=52)
btn3 = Button(lbf2,text="預設值" ,command=checkCP)
btn3.place(x=425,y=52)

btnX = Button(lbf2,text="顯示公鑰" ,command=ShowMeInfo)
btnX.place(x=360,y=52)


lblx = Label(lbf3,text=" ➠ 歡迎使用耕地指令工具...",bg="#404040",fg="white",width=75,height=2,font=fontsize)
lblx.place(x=4,y=1)

win.mainloop()