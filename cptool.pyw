#!/usr/bin/python
# -*- coding: UTF-8 -*-
# ============================================
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
import psutil
from idlelib.tooltip import Hovertip
# ============================================
# 應用程式設定
# ============================================
ToolVersion = "0.43"                #程式版本
win = Tk()                          #宣告視窗
win.title("➠ 高速耕地執行工具 ➠ Ver "+ToolVersion)
win.geometry("740x580")
win.resizable(False, False)
# 將工作目錄切換至執行檔案所在目錄
cwd = os.path.dirname(os.path.realpath(sys.argv[0]))
os.chdir(cwd)
# ============================================
# 變數設定,請勿更動
# ============================================
CP_DEBUG = FALSE                    #除錯指令
counter = 0                         #目前執行次數,不須更動
sec = 0                             #目前階段執行時間,不須更動
cp_delay = 0                        #減少資源占用
cp_pid_chia_plot = ""               #指定 Chia_plot 的 PID
cp_Interrupt = FALSE                #指定是否為中斷耕地過程
cp_Num = 0                          #目前耕地數量
# 宣告一個結構
startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
# ============================================
# 預設值變數設定
# ============================================
fontsize = tkFont.Font(size="10")     #字型尺寸
hddsizefont = tkFont.Font(family="微軟正黑體",size="10",weight="bold")
fname = cwd+"\\chia_plot.exe"       #chia_plot 高速P圖程式的檔案名稱
ChiaVer = "1.2.2"                   #安裝的Chia版本(查詢公鑰,礦池公鑰,農民公鑰需要)
PoltNum = "1"                       #執行耕地數量(一次要生產的耕地數量)
CoreNum = "8"                       #耕地使用執行緒數量(依照自己的核心數調整)
BuketNum = "256"                    #耕地使用桶數(不建議更動)
TempDir1 = "D:\\CHIATEMP\\"         #耕地使用的暫存資料夾1
TempDir2 = "D:\\CHIATEMP\\"         #耕地使用的暫存資料夾2(作者建議使用RAM)
TargetDir = "E:\\CHIA\\"            #耕地完成檔案放置位置
HDDusage = psutil.disk_usage("C:\\")#目標硬碟預設值為 C:\
LanDisk = FALSE                     #預設是否使用網路硬碟
PoolPublicKey = ""                  #礦池公鑰,請按顯示公鑰查詢
FarmerPublicKey = ""                #農民公鑰,請按顯示公鑰查詢
chkValue = BooleanVar()
chkValue.set(False)                 #-G 核取方塊,預設值 FALSE
chkValueW = BooleanVar()
chkValueW.set(False)                 #-G 核取方塊,預設值 FALSE
radioValue = IntVar()               #-c 或是 -p 選擇
radioValue.set(1)                   # 預設值 1 = 農會耕地
GoldKey = [["0","0","0"]]
# ============================================
# TODO: 清除進度區資料
def UseTime():  
    etrxtext1.delete(0,END)
    etrxtext2.delete(0,END)
    etrxtext3.delete(0,END)
    etrxtext4.delete(0,END)
    etrxtext5.delete(0,END)
    etrxtext1.config(bg="#202020",fg="white")
    etrxtext2.config(bg="#C0C0C0")
    etrxtext3.config(bg="#C0C0C0")
    etrxtext4.config(bg="#C0C0C0")
    etrxtext5.config(bg="#C0C0C0")
# ============================================
# TODO: 檢查是否忘了加上斜線
def CheckDir(temp1,temp2,target1):  
    if temp1[-1] != "\\":
        temp1 = temp1+"\\"
        etr4.delete(0,END)
        etr4.insert(0,temp1)
    if temp2[-1] != "\\":
        temp2 = temp2+"\\"
        etr5.delete(0,END)
        etr5.insert(0,temp2)
    if target1[-1] != "\\":
        target1 = target1+"\\"
        etr8.delete(0,END)
        etr8.insert(0,target1)
    return temp1,temp2,target1
# ============================================
# TODO: 顯示並填入公鑰資訊
def ShowMeInfo():
    LocalStr = os.getenv("LOCALAPPDATA")
    if etrver1.get() != "":
        chiaver = etrver1.get()
    else:
        tkMsg.showwarning(title="Chia 版本未設定",message="Chia 版本必須設定才能輸出 Chia 公鑰資訊!\n 這裡將版本預設為1.2.0")
        chiaver = ChiaVer
        etrver1.insert(0,ChiaVer)
    text1.delete(1.0,END)
    text1.insert(END," ============================================================== \n")
    CmdStr = LocalStr+"\\chia-blockchain\\app-"+chiaver+"\\resources\\app.asar.unpacked\\daemon\\chia.exe"
    if os.path.exists(CmdStr):
        CmdStr ="\""+ CmdStr + "\" keys show"
        # 顯示指令
        text1.insert(END," "+CmdStr+" \n")
        with subprocess.Popen(CmdStr,startupinfo=startupinfo,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE) as p:
            showkeys = p.stdout.read().decode("big5")
            showerr = p.stderr.read().decode("big5")
        #指定每組公鑰的分割字串
        keys = showkeys.split("Fingerprint")
        #讀取總共有幾組公鑰字串
        keyscounter = showkeys.count("Fingerprint:")
        text1.insert(END," ============================================================== \n")
        text1.insert(END,showkeys+" \n")
        text1.insert(END,showerr+" \n")
        text1.insert(END," ============================================================== \n")
        lblx.config(text="  ➠ 您共有 "+str(keyscounter)+" 組公鑰",bg="#404070")
        text1.insert(END,"  ➠ 您共有 "+str(keyscounter)+" 組公鑰...\n")
        text1.see(END)
        global counter
        counter = 1
        strppk=""
        strfpk=""
        strpca=""
        global GoldKey
        # 開始擷取每個公鑰並且填入下拉選單
        while TRUE:
            fpk = keys[counter].partition("Farmer public key")
            ppk = keys[counter].partition("Pool public key")
            pca = keys[counter].partition(":")
            fpk = fpk[2].partition("):")
            ppk = ppk[2].partition("):")
            pca = pca[2].partition(" ")
            fpk = fpk[2].split()
            ppk = ppk[2].split()
            pca = pca[2].split()
            strppk = strppk + ppk[0]+" "
            strfpk = strfpk + fpk[0]+" "
            strpca = strpca + pca[0]+" "
            GoldKey.insert(counter,[pca[0],ppk[0],fpk[0]])
            if counter == 1:
                ppkComboBox.delete(0,END)
                fpkComboBox.delete(0,END)
                pcaComboBox.delete(0,END)
                ppkComboBox.insert(0,ppk[0])
                fpkComboBox.insert(0,fpk[0])
                pcaComboBox.insert(0,pca[0])
            #寫入下拉選單,並且指定下一筆資料
            if counter == keyscounter:               
                ppkComboBox["value"] = strppk.split(" ")
                fpkComboBox["value"] = strfpk.split(" ")
                pcaComboBox["value"] = strpca.split(" ")
                break
            counter += 1
    else:
        text1.insert(END," ============================================================== \n")
        text1.insert(END,"  ➠ Chia主程式不存在,或是版本輸入不正確...\n")
        lblx.config(text="  ➠ Chia主程式不存在,或是版本輸入不正確...",bg="#404070")
        text1.see(END)
# ============================================
# TODO: 正式開始!! 執行外部指令,P圖開始
def RunCmd(CmdStr):
    #重置變數
    global sec
    global cp_delay 
    global cp_pid_chia_plot
    global cp_Interrupt
    sec = 0                     # 耕地時間
    cp_delay = 0                # 減少占用
    cp_pid_chia_plot = ""       # chia_plot.exe PID
    cp_Interrupt = FALSE        # 是否中斷耕地
    cp_Num = 0                  # 清除數量
    cp_NumEnd = etr1.get()      # 總計數量
    text2.delete(1.0,END)       # 清除記錄區
    #關閉按鈕
    btn1.config(state=DISABLED)
    btn2.config(state=DISABLED)
    btn3.config(state=DISABLED)
    btnX.config(state=DISABLED)
    Interrupt.config(state=NORMAL)
    etr1.config(state=DISABLED)
    etr2.config(state=DISABLED)
    etr3.config(state=DISABLED)
    etr34.config(state=DISABLED)
    etr4.config(state=DISABLED)
    etr5.config(state=DISABLED)
    etr8.config(state=DISABLED)
    ppkComboBox.config(state=DISABLED)
    etrPool.config(state=DISABLED)
    fpkComboBox.config(state=DISABLED)
    pcaComboBox.config(state=DISABLED)
    rdioNew.config(state=DISABLED)
    rdioOld.config(state=DISABLED)
    cbW.config(state=DISABLED)
    cbG.config(state=DISABLED)
    etrver1.config(state=DISABLED)
    text1.insert(END," ============================================================== \n")
    text1.insert(END,"   ➠ 耕地準備中,請稍後...... \n")
    text1.insert(END," ============================================================== \n")
    lblx.config(text="   ➠ 耕地準備中,請稍後...... ",bg="#702020")
    text2.tag_config("tag1",foreground="#84C1FF")
    text2.tag_config("tag2",foreground="#FFDC35")
    text2.tag_config("tag3",foreground="#FF2020")
    # 開始執行指令
    with subprocess.Popen(CmdStr,startupinfo=startupinfo,shell=False,stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE) as p:
        lblx.config(text=" ➠ 開始耕地中,請稍後... ",bg="#903030")
        while p.poll() == None:
            # 輸出執行LOG
            LineStr = p.stdout.readline().decode("big5")
            text1.insert(END,LineStr)
            # 判斷過程執行功能
            if "Process ID:" in LineStr:    # 清除上一次耕地紀錄
                LStr = LineStr.split()
                UseTime()
                sec = "0"
                cp_pid_chia_plot = LStr[2]
            if "Plot Name:" in LineStr:     # 顯示目前耕地檔案名稱
                LStr = LineStr.split()
                etrxtext1.insert(0,LStr[2]+".plot")
                etrxtext1.config(bg="#6C3365")
                cp_delay = 1                #進入P圖階段,開始減少資源占用
            if "[P1]" in LineStr:
                lblx.config(text=" ➠ 耕地中,第一階段... ",bg="#502020")
                etrxtext2.config(bg="#7E3D76")
            if "Phase 1 took" in LineStr:
                LStr = LineStr.split()
                etrxtext2.insert(0,LStr[3])
                etrxtext2.config(bg="#003E3E")
            if "[P2]" in LineStr:
                lblx.config(text=" ➠ 耕地中,第二階段... ",bg="#502020")
                etrxtext3.config(bg="#7E3D76")
            if "Phase 2 took" in LineStr:
                LStr = LineStr.split()
                etrxtext3.insert(0,LStr[3])
                etrxtext3.config(bg="#003E3E")
            if "[P3-" in LineStr:
                lblx.config(text=" ➠ 耕地中,第三階段... ",bg="#502020")
                etrxtext4.config(bg="#7E3D76")
            if "Phase 3 took" in LineStr:
                LStr = LineStr.split()
                etrxtext4.insert(0,LStr[3])
                etrxtext4.config(bg="#003E3E")
            if "[P4]" in LineStr:
                lblx.config(text=" ➠ 耕地中,第四階段... ",bg="#502020")
                etrxtext5.config(bg="#7E3D76")
            if "Phase 4 took" in LineStr:
                LStr = LineStr.split()
                etrxtext5.insert(0,LStr[3])
                etrxtext5.config(bg="#003E3E")
                cp_delay = 0                  #P圖階段完成,開始回復即時檢測
            if "Total plot creation time was" in LineStr:
                stra =  LineStr.split()
                sec = str(round(float(stra[5])/60,1))
                cp_Num += 1
            if "Started copy to" in LineStr:
                lblx.config(text=" ➠ 複製耕地往目標資料夾中,耕地總計時間: "+str(sec)+" 分鐘",bg="#BF0060")
                etrxtext1.config(bg="#003E3E")
                text2.insert(END,str(cp_Num)+"/"+cp_NumEnd,"tag1")
                text2.insert(END,":")
                text2.insert(END,str(sec)+"\n","tag2")
                if CheckHddFreeSize(None) <= 318 and not LanDisk:
                    text2.insert(END,"硬碟快用完\n","tag3")
                cp_delay = 0
                text2.see(END)
            # 減少資源占用
            if cp_delay == 1:
                time.sleep(0.2)
            text1.see(END)
    text1.insert(END,"\n ============================================================== \n")
    if cp_Interrupt:
        lblx.config(text="   ➽ 中斷耕地完成! 請記得按下右下角清除暫存按鈕! \n",bg="#C0C040")
        text1.insert(END,"   ➽ 中斷耕地完成! 請記得按下右下角清除暫存按鈕! \n")
        text1.see(END)
        btn1.config(state=DISABLED)
        btn2.config(state=DISABLED)
        btnDeleteTemp.config(state=NORMAL)
    else:
        lblx.config(text="   ➠ 耕地完成!  最後耕地總計花費: "+str(sec)+" 分鐘",bg="#206020")
        text1.insert(END,"   ➠ 耕地完成!  最後耕地總計花費: "+str(sec)+" 分鐘 \n")
        text1.see(END)
        btn1.config(state=NORMAL)
        btn2.config(state=NORMAL)
    btn3.config(state=NORMAL)
    btnX.config(state=NORMAL)
    Interrupt.config(state=DISABLED)
    etr1.config(state=NORMAL)
    etr2.config(state=NORMAL)
    etr3.config(state=NORMAL)
    etr34.config(state=NORMAL)
    etr4.config(state=NORMAL)
    etr5.config(state=NORMAL)
    etr8.config(state=NORMAL)
    fpkComboBox.config(state=NORMAL)
    pcaComboBox.config(state=NORMAL)
    rdioNew.config(state=NORMAL)
    rdioOld.config(state=NORMAL)
    cbW.config(state=NORMAL)
    cbG.config(state=NORMAL)
    etrver1.config(state=NORMAL)
    ChangPlot()
    return p
# ============================================
# TODO: 耕地之前檢查,首先除錯,防呆!!!
def RunChiaPlot():
    global counter
    global fname
    counter = 0
    err = 0
    global chkValue
    # err 的錯誤代碼表
    # 1=路徑不存在 2=前三格不是數字 3=路徑有空格 5=全部輸入格其中有沒輸入的
    # 99=檢查是否DEBUG或是chia_plot是否不存在
    temp1,temp2,target1 = CheckDir(etr4.get(),etr5.get(),etr8.get())
    # 檢查前兩格是否為數字
    if not str.isdigit(etr2.get()) or not str.isdigit(etr3.get()) or not str.isdigit(etr34.get()):
        err = 2
    # 檢查耕地數是否為數字
    if not str.isdigit(etr1.get()):
        if not str("-1"):   # 確定不是 -1
            err = 2
    if len(etr1.get()) == 0 or len(etr2.get()) == 0 or len(etr3.get())==0 or len(etr34.get())==0 or len(temp1) == 0 or len(temp2) == 0 or len(fpkComboBox.get()) == 0 or len(target1) == 0:
        err = 5
    #檢查路徑是否存在
    if not os.path.isdir(temp1) or not os.path.isdir(temp2) or not os.path.isdir(etr8.get()):
        err = 1
    #檢查路徑是否有空格
    if " " in temp1 or " " in temp2 or " " in target1:
        err = 3
    #檢查 madMAx43v3r/chia-plotter的 chia_plot.exe 是否存在或是使用除錯指令
    if not os.path.exists(fname):
        err = 99
    if CP_DEBUG:
        err = 0
    # 組合外部指令
    cmdstr = "\"" + os.path.abspath(fname) + "\" -n "+etr1.get()+" -r "+etr2.get()+" -u "+etr3.get()
    if etr3.get() != etr34.get():
        cmdstr =cmdstr +" -v "+etr34.get()
    if chkValue.get():
        cmdstr =cmdstr +" -G"
    if chkValueW.get():
        cmdstr =cmdstr +" -w"
    cmdstr = cmdstr + " -t " + temp1 + " -2 " + temp2 + " -d " + target1
    if radioValue.get() == 1:
        if not etrPool.get()[0:3] == "xch" and radioValue.get() == 1:
            err = 6
        else:
            cmdstr = cmdstr + " -c " + etrPool.get()
    else:
        if len(ppkComboBox.get()) == 0 and radioValue.get() == 2:
            err = 6
        else:
            cmdstr = cmdstr + " -p " + ppkComboBox.get()
    cmdstr = cmdstr + " -f " + fpkComboBox.get()
    #開始時先更新硬碟容量
    if CheckHddFreeSize(None) < 106 and not LanDisk:
        err = 7
    #開始檢測後執行
    text1.delete(1.0,END)
    text1.insert(END,"   ➠ 錯誤代碼 ERR = "+str(err)+"\n")
    text1.insert(END," ============================================================== \n")
    if err == 0:
        counter += 1
        text1.insert(END,"      第 "+str(counter)+" 次耕地執行中,請稍後!!\n")
        text1.insert(END," ============================================================== \n")
        text1.insert(END,"   ➠ 目前工作目錄: "+os.getcwd()+"\n")
        text1.insert(END," ============================================================== \n")
        text1.insert(END,"  "+cmdstr+"\n")
        text1.insert(END," ============================================================== \n")
        text1.insert(END,"   ➠ 耕地開始,請稍後...... \n")
        lblx.config(text="  ➠ 耕地開始,請稍後....")
        if not CP_DEBUG:
            t1 = threading.Thread(target=RunCmd,args=(cmdstr,))
            t1.start()
    elif err == 7:
        text1.insert(END,"   ➠ 目標路徑硬碟空間不足,或是路徑錯誤...... \n")
        lblx.config(text="  ➠ 目標路徑硬碟空間不足,或是路徑錯誤....",bg="#F02080")    
    elif err == 6:
        text1.insert(END,"   ➠ 礦池公鑰或是礦池合約與該選項沒有填入...... \n")
        lblx.config(text="  ➠ 礦池公鑰或是礦池合約與該選項沒有填入....",bg="#F02080")
    elif err == 5:
        text1.insert(END,"   ➠ 設定框有遺漏輸入設定...... \n")
        lblx.config(text="  ➠ 設定框內必須有輸入文字....",bg="#F02080")
    elif err == 1:
        text1.insert(END,"   ➠ 暫存1,暫存2,或目標目錄其中有目錄是不存在! \n")
        lblx.config(text="  ➠ 資料夾不存在所以停止耕地....",bg="#F02080")
    elif err == 2:
        text1.insert(END,"   ➠ 耕地數,核心數,桶數量,3-4桶,有格子內輸入不是數字的文字! \n")
        lblx.config(text="  ➠ 有格子內輸入不是數字的文字所以停止耕地....",bg="#F02080")
    elif err == 3:
        text1.insert(END,"   ➠ 暫存1,暫存2,或目標目錄中有空格! \n   ➠ madMAx43v3r/chia-plotter 不支援有空格的資料夾,請修正!\n")
        lblx.config(text="  ➠ madMAx43v3r/chia-plotter 不支援有空格的資料夾...",bg="#F02080")
    elif err == 99:
        text1.insert(END,"      程式發生一些狀況,請依照以下的說明處理!! \n")
        text1.insert(END," ============================================================== \n")
        text1.insert(END,"\n ➠ 耕地程式 \"" + os.path.abspath(fname) + "\" 檔案不存在!! \n")
        text1.insert(END,"\n ➠ 請前往 https://github.com/stotiks/chia-plotter/releases 下載,放在此資料夾!\n")
        lblx.config(text="  ➠ 程式檢測到一些況狀,請排除...",bg="#604040")
        btn1.config(state=NORMAL)
    else:
        text1.insert(END,"      程式發生一些未知狀況,請回報狀況感謝\n")
        lblx.config(text="  ➠ 程式檢測到一些況狀,請回報狀況...",bg="#604040")
        btn1.config(state=NORMAL)
    text1.insert(END," ============================================================== \n")
# ============================================
# TODO: 預設值按鈕,將格子內資料全部改回預設值
def BackDefault():
    text1.delete(1.0,END)
    lblx.config(text="  ➠ 清除程式執行結果區,並清空變回預設值....",bg="#404040")
    etr1.delete(0,END)
    etr1.insert(0,PoltNum)
    etr2.delete(0,END)
    etr2.insert(0,CoreNum)
    etr3.delete(0,END)
    etr3.insert(0,BuketNum)
    etr34.delete(0,END)
    etr34.insert(0,BuketNum)
    etr4.delete(0,END)
    etr4.insert(0,TempDir1)
    etr5.delete(0,END)
    etr5.insert(0,TempDir2)
    ppkComboBox.delete(0,END)
    ppkComboBox.insert(0,PoolPublicKey)
    fpkComboBox.delete(0,END)
    fpkComboBox.insert(0,FarmerPublicKey)
    etr8.delete(0,END)
    etr8.insert(0,TargetDir)
    text2.delete(1.0,END)
# ============================================
# TODO: 儲存設定,並且結束程式
def ExitApp():  
    SFile = open(cwd+"\\cptool.ini",mode="w")
    SFile.writelines(etr1.get()+"\n")           #耕地數
    SFile.writelines(etr2.get()+"\n")           #執行緒
    SFile.writelines(etr3.get()+"\n")           #桶數量
    SFile.writelines(etr4.get()+"\n")           #暫存1
    SFile.writelines(etr5.get()+"\n")           #暫存2
    SFile.writelines(ppkComboBox.get()+"\n")    #礦池公鑰
    SFile.writelines(fpkComboBox.get()+"\n")    #農民公鑰
    SFile.writelines(etr8.get()+"\n")           #最終路徑
    SFile.writelines(etrver1.get()+"\n")        #Chia 版本
    SFile.writelines(etrPool.get()+"\n")        #農會合約地址
    SFile.writelines(str(radioValue.get())+"\n")#預設使用耕地
    SFile.writelines(str(chkValueW.get())+"\n") #預設是否有複製時啟動下個耕地
    SFile.writelines(str(pcaComboBox.get())+"\n") #儲存錢包指紋
    SFile.close
    win.destroy()
# ============================================
# TODO: 中斷目前耕地
def InterruptChiaPlot():
    if tkMsg.askyesno("中斷耕地","你確定要中斷耕地嗎?"):
        global cp_pid_chia_plot
        if  not cp_pid_chia_plot == "":
            try:
                global cp_Interrupt
                global cp_delay
                global cp_Num
                text1.insert(END,"\n\n  ➼➼➼ 中斷 PID:"+cp_pid_chia_plot+" 中,這需要一些時間,請稍候!\n")
                lblx.config(text=" ➼➼➼ 正在中斷目前耕地的過程中,請稍候...",bg="#C0C060",fg="#101010")
                with subprocess.Popen('taskkill.exe /F /pid:'+cp_pid_chia_plot,shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as p:
                    text1.insert(END,"\n\n "+p.stdout.read().decode("big5")+"\n")
                time.sleep(0.2)
                UseTime()
                cp_Interrupt = TRUE
                cp_pid_chia_plot = ""
                cp_delay = 0
                cp_Num = 0
            except OSError as e:
                tkMsg.showerror("➼ 發生例外狀況",e)
        else:
            tkMsg.showerror("➼ PID不存在","➼ PID不存在,可能並沒有在耕地中,或是耕地失敗\n"+cp_pid_chia_plot)
        Interrupt.config(state=DISABLED)
# ============================================
# TODO: 刪除暫存的耕地
def DeleteTemp1Temp2File():
    text1.insert(END," ============================================================== \n")
    text1.insert(END,"\n  ➼➼➼ 正在刪除暫存的檔案,這需要一些時間,請稍候!\n")
    lblx.config(text=" ➼➼➼ 正在刪除暫存的檔案,請稍候...",bg="#C0C060",fg="#101010")
    text1.see(END)
    with subprocess.Popen("del "+etr4.get()+"*.tmp /f /q",shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as p1:
        text1.insert(END,p1.stdout.read().decode("big5")+"\n")
    with subprocess.Popen("del "+etr5.get()+"*.tmp /f /q",shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as p2:
        text1.insert(END,"\n"+p2.stdout.read().decode("big5")+"\n")
    text1.insert(END,"  ➼➼➼ 暫存1與暫存2刪除完畢! \n")
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
def ChangPlot():
    if radioValue.get() == 1:
        ppkComboBox.config(state=DISABLED)
        etrPool.config(state=NORMAL)
        text1.insert(END,"\n  ➠ 切換至農會耕地!")
    else:
        etrPool.config(state=DISABLED)
        ppkComboBox.config(state=NORMAL)
        text1.insert(END,"\n  ➠ 切換至原始耕地!")
def ViewKey(vkeys):
    global GoldKey
    global counter
    counter = 0
    maxcounter = len(GoldKey)
    while counter < maxcounter:
        if GoldKey[counter][0] == vkeys:
            return GoldKey[counter][2]
        counter += 1
def ViewPpkKey(vkeys):
    global GoldKey
    global counter
    counter = 0
    maxcounter = len(GoldKey)
    while counter < maxcounter:
        if GoldKey[counter][0] == vkeys:
            return GoldKey[counter][1]
        counter += 1
def PcaList(self):
    LocalStr = os.getenv("LOCALAPPDATA")
    if etrver1.get() != "":
        chiaver = etrver1.get()
    else:
        tkMsg.showwarning(title="Chia 版本未設定",message="Chia 版本必須設定才能輸出 Chia 資訊!\n 這裡將版本預設為1.2.0")
        chiaver = ChiaVer
        etrver1.insert(0,ChiaVer)
    text1.delete(1.0,END)
    text1.insert(END," ============================================================== \n")
    CmdStr = LocalStr+"\\chia-blockchain\\app-"+chiaver+"\\resources\\app.asar.unpacked\\daemon\\chia.exe"
    if os.path.exists(CmdStr) and len(GoldKey)> 1:
        CmdStr ="\""+ CmdStr + "\" plotnft show -f " + pcaComboBox.get()
        # 顯示指令
        text1.insert(END," "+CmdStr+" \n")
        if radioValue.get() == 1:
            fpkComboBox.delete(0,END)
            fpkComboBox.insert(0,ViewKey(pcaComboBox.get()))
        else:
            fpkComboBox.delete(0,END)
            fpkComboBox.insert(0,ViewKey(pcaComboBox.get()))
            ppkComboBox.delete(0,END)
            ppkComboBox.insert(0,ViewPpkKey(pcaComboBox.get()))
        with subprocess.Popen(CmdStr,startupinfo=startupinfo,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE) as p:
            pcaskeys = p.stdout.read().decode("big5")
            pcaserr = p.stderr.read().decode("big5")
        #指定每組公鑰的分割字串
        pcas = pcaskeys.split("Wallet id")
        #讀取總共有幾組公鑰字串
        pcascounter = pcaskeys.count("Wallet id")
        text1.insert(END," ============================================================== \n")
        text1.insert(END,pcaskeys+" \n")
        text1.insert(END,pcaserr+" \n")
        text1.insert(END," ============================================================== \n")
        lblx.config(text="  ➠ 您共有 "+str(pcascounter)+" 組農會合約地址",bg="#404070")
        text1.insert(END,"  ➠ 您共有 "+str(pcascounter)+" 組農會合約地址...\n")
        text1.see(END)
        global counter
        counter = 1
        strpca=""
        # 開始擷取每個農會合約地址並且填入下拉選單
        text1.insert(END," ============================================================== \n")
        while TRUE:
            pca = pcas[counter].partition("P2 singleton address (pool contract address for plotting): ")
            text1.insert(END,pca[2][0:62]+"\n")
            strpca = strpca + pca[2][0:62] + " "
            if counter == 1:
                etrPool.delete(0,END)
                etrPool.insert(0,strpca)
            #寫入下拉選單,並且指定下一筆資料
            if counter == pcascounter:               
                etrPool["value"] = strpca.split(" ")
                text1.insert(END," ============================================================== \n")
                break
            counter += 1
    else:
        text1.insert(END," ============================================================== \n")
        text1.insert(END,"  ➠ 未先按下讀取公鑰,無法產生農會合約地址下拉選項...\n")
        lblx.config(text="  ➠ 未先按下讀取公鑰,無法產生農會合約地址下拉選項...",bg="#404070")
        text1.see(END)
def CheckHddFreeSize(self):
    TargetDir = etr8.get()
    global LanDisk
    if TargetDir[:2] == "\\\\" or TargetDir[:3] == "ftp":
        LanDisk = TRUE
        lbdisksize.config(text="網路硬碟",fg="#303090")
        return 0
    try:
        if len(TargetDir) >=2:
            HDDusage = psutil.disk_usage(TargetDir[:2])
            HddFreeSize = round(((HDDusage.free/1024)/1024)/1024)
            if HddFreeSize >= 106:
                lbdisksize.config(text=str(HddFreeSize)+" GiB",fg="#208020")
            else:
                lbdisksize.config(text=str(HddFreeSize)+" GiB",fg="#802020")
            LanDisk = FALSE
            return HddFreeSize
    except:
        LanDisk = FALSE
        lbdisksize.config(text="硬碟不存在",fg="#903030")
        text1.insert(END,"  ➠ 請檢查最終路徑是否正確!\n")
        return 0
# ============================================
# TODO: 視窗主框架
# ============================================
frm1 = Frame(win, width=745,height=530).pack()
# ============================================
# TODO: 視窗分區框架
# ============================================
lbf2 = LabelFrame(frm1,text="[輸入區]",font=fontsize)
lbf1 = LabelFrame(frm1,text="[顯示區]",font=fontsize)
lbf3 = LabelFrame(frm1,text="[進度區]",font=fontsize)
lbf4 = LabelFrame(frm1,text="[紀錄區]",font=fontsize)
lbf2.place(x=10,y=10,width=725,height=145)
lbf1.place(x=10,y=160,width=620,height=300)
lbf3.place(x=10,y=460,width=620,height=110)
lbf4.place(x=635,y=160,width=100,height=410)
# ============================================
# TODO: 顯示區框架
# ============================================
lab2 = Label(lbf1,text="程式執行結果區",font=fontsize)
lab2.place(x=150,y=-3)
lbver1 = Label(lbf1,text="請輸入你的Chia版本:")
lbver1.place(x=419,y=-6)
etrver1 = Entry(lbf1,width=8,bg="#303030",fg="white",justify=CENTER)
etrver1.place(x=538,y=-4)
# ============================================
# TODO: 顯示區內文框
# ============================================
scroll = Scrollbar(lbf1)
scroll.pack(side=RIGHT , fill=Y)
text1 = Text(lbf1,width=85,height=20,bg="#303030",fg="white", yscrollcommand=scroll.set)
text1.place(x=0,y=16)
scroll.config(command=text1.yview)
# ============================================
# TODO: 創建輸入區設定格
# ============================================
lb1 = Label(lbf2,text="耕地數",font=fontsize)
lb1.place(x=4,y=5)
etr1 = Entry(lbf2,bg="#606060",fg="white",width=4,justify=CENTER)
etr1.place(x=48,y=6)
lb1 = Label(lbf2,text="執行緒",font=fontsize)
lb1.place(x=82,y=5)
etr2 = Entry(lbf2,bg="#606060",fg="white",width=4,justify=CENTER)
etr2.place(x=128,y=6)
lb1 = Label(lbf2,text="桶數量",font=fontsize)
lb1.place(x=161,y=5)
etr3 = Entry(lbf2,bg="#606060",fg="white",width=5,justify=CENTER)
etr3.place(x=205,y=6)
lb4 = Label(lbf2,text="暫存１",font=fontsize)
lb4.place(x=325,y=5)
etr4 = Entry(lbf2,bg="#606060",fg="white",width=20,justify=LEFT)
etr4.place(x=372,y=6)
lb5 = Label(lbf2,text="暫存２",font=fontsize)
lb5.place(x=521,y=5)
etr5 = Entry(lbf2,bg="#606060",fg="white",width=20,justify=LEFT)
etr5.place(x=568,y=6)
lb8 = Label(lbf2,text="最終路徑",font=fontsize)
lb8.place(x=359,y=30)
etr8 = Entry(lbf2,bg="#606060",fg="white",width=30,justify=LEFT)
etr8.place(x=419,y=31)
etr8.bind("<Key>",CheckHddFreeSize)
HddFreeSize = round(((HDDusage.free/1024)/1024)/1024)
if HddFreeSize >= 106:
    lbdisksize = Label(lbf2,text=str(HddFreeSize)+" GiB",fg="#107010",font=hddsizefont,width=10)
else:
    lbdisksize = Label(lbf2,text=str(HddFreeSize)+" GiB",fg="#701010",font=hddsizefont,width=10)
lbdisksize.place(x=634,y=30)

cbW = Checkbutton(lbf2, text="等待複製完成再續耕", variable=chkValueW)
cbW.place(x=505,y=55)
cbWTip = Hovertip(cbW,'進階功能: 耕地完成後等待複製完成才繼續下一個耕地,若沒打勾複製時會繼續下個耕地')

cbG = Checkbutton(lbf2, text="暫存切換", variable=chkValue)
cbG.place(x=640,y=55)
cbGTip = Hovertip(cbG,'進階功能: 非必要,確定要使用才打勾!')

lb34 = Label(lbf2,text="3-4桶",font=fontsize)
lb34.place(x=245,y=5)
etr34 = Entry(lbf2,bg="#606060",fg="#A0A0A0",width=5,justify=CENTER)
etr34.place(x=280,y=6)
etr34Tip = Hovertip(etr34,'進階功能: 非必要,這是設定第三與第四階段的桶數,預設值與桶數量相同')

lb6 = Label(lbf2,text="礦池公鑰",font=fontsize)
lb6.place(x=4,y=57)
ppkComboBox = ttk.Combobox(width=39,justify=LEFT)
ppkComboBox.place(x=74,y=82)
ppkPoolTip = Hovertip(ppkComboBox,'注意: 如在礦池合約地址輸入合約地址會自動停用礦池公鑰.')

lb7 = Label(lbf2,text="農民公鑰",font=fontsize)
lb7.place(x=4,y=31)
fpkComboBox = ttk.Combobox(width=39,justify=LEFT)
fpkComboBox.place(x=74,y=55)

# 單選按鈕
rdioNew = Radiobutton(lbf2,text='農會耕地',fg="#106010",variable=radioValue, value=1, command=ChangPlot)
rdioNew.place(x=360,y=55)
rdioOld = Radiobutton(lbf2,text='原始耕地',fg="#707070",variable=radioValue, value=2, command=ChangPlot)
rdioOld.place(x=430,y=55)

# 錢包指紋
lbGoldKey = Label(lbf2,text="選擇錢包:",font=fontsize,fg="#6060FF")
lbGoldKey.place(x=280,y=81)
lbGoldKeyTip = Hovertip(lbGoldKey,'選擇錢包之前先選擇耕地再讀取公鑰,按Enter讀取農會,或是下拉選擇')
pcaComboBox = ttk.Combobox(width=10,justify=LEFT)
pcaComboBox.place(x=354,y=106)
pcaComboBox.bind("<<ComboboxSelected>>", PcaList)
pcaComboBox.bind("<Return>", PcaList)
pcaComboBoxTip = Hovertip(pcaComboBox,'選擇錢包之前先選擇耕地再讀取公鑰,按Enter讀取農會,或是下拉選擇')
lbPool = Label(lbf2,text="農會合約地址:(加入農會)",font=fontsize,fg="#FF6060")
lbPool.place(x=4,y=81)
etrPool = ttk.Combobox(width=58,justify=LEFT)
etrPool.place(x=18,y=128)
etrPoolTip = Hovertip(etrPool,'進階功能: 前三碼非xch字元會省略此參數並使用礦池公鑰,若使用此參數礦池公鑰會自動無效')
# ============================================
# TODO: 創建輸入區按鈕集合
# ============================================
btn1 = Button(lbf2,text="執行耕地",font=fontsize,fg="#0000FF",width=9,height=2,command=RunChiaPlot)
btn1.place(x=574,y=85)
btn2 = Button(lbf2,text="結束程式",font=fontsize,fg="#743A3A",width=7,height=2,command=ExitApp)
btn2.place(x=652,y=85)
btn3 = Button(lbf2,text="預設值",font=fontsize ,height=2,command=BackDefault)
btn3.place(x=519,y=85)
btnX = Button(lbf2,text="讀取公鑰",font=fontsize,fg="#4B0091",height=2,command=ShowMeInfo)
btnX.place(x=450,y=85)
# ============================================
# TODO: 創建進度區顯示框
# ============================================
lblx = Label(lbf3,text=" ➠ 歡迎使用耕地指令工具 Ver "+ToolVersion,bg="#202020",fg="white",width=65,height=2,font=tkFont.Font(size=11))
lblx.place(x=44,y=50)
Interrupt = Button(lbf3,text="中斷\n耕地",font=fontsize,fg="#FF0000",command=InterruptChiaPlot)
Interrupt.place(x=4,y=50)
Interrupt.config(state=DISABLED)
btnDeleteTemp = Button(lbf3,text="清除\n暫存",font=fontsize,fg="#FF0000",command=DeleteTemp1Temp2File)
btnDeleteTemp.place(x=573,y=50)
btnDeleteTemp.config(state=DISABLED)
lblxpn = Label(lbf3,text="目前耕地")
lblxpn.place(x=4,y=0)
etrxtext1 = Entry(lbf3,bg="#202020",fg="white",width=78,justify=LEFT)
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
# ============================================
# TODO: 創建紀錄區顯示框
# ============================================
scroll2 = Scrollbar(lbf4)
scroll2.pack(side=RIGHT , fill=Y)
text2 = Text(lbf4,width=11,height=29,bg="#303030",fg="white",yscrollcommand=scroll2.set)
text2.place(x=1,y=10)
scroll2.config(command=text2.yview)
# ============================================
# TODO: 啟動時讀取設定檔案
# ============================================
SFileName = cwd+"\\cptool.ini"
if os.path.exists(SFileName):
    SFile = open(cwd+"\\cptool.ini",mode="r")
    list1 =  SFile.readlines()
    etr1.insert(0,list1[0].replace("\n",""))    #讀取時消除換行字元
    etr2.insert(0,list1[1].replace("\n",""))
    etr3.insert(0,list1[2].replace("\n",""))
    etr34.insert(0,list1[2].replace("\n",""))   #將34桶的開機值與桶相同
    etr4.insert(0,list1[3].replace("\n",""))
    etr5.insert(0,list1[4].replace("\n",""))
    # 礦池公鑰|農民公鑰|清除換行字元
    ppkComboBox.insert(0,list1[5].replace("\n",""))
    fpkComboBox.insert(0,list1[6].replace("\n",""))
    # 目標路徑清除換行字元
    etr8.insert(0,list1[7].replace("\n",""))
    HddFree = CheckHddFreeSize(None)
    try:    # 讀取 Chia 版本
        etrver1.insert(0,list1[8].replace("\n",""))
    except:
        etrver1.insert(0,ChiaVer)
    try:    # 讀取農會合約地址
        etrPool.insert(0,list1[9].replace("\n",""))
    except:
        etrPool.insert(0,"")
    try:    # 讀取是否為農會耕地
        NewOldPlot = int(list1[10].replace("\n",""))
        radioValue.set(NewOldPlot)
        if NewOldPlot == 1:
            ppkComboBox.config(state=DISABLED)
            etrPool.config(state=NORMAL)
        else:
            ppkComboBox.config(state=NORMAL)
            etrPool.config(state=DISABLED)
    except:
        radioValue.set(1)
        ppkComboBox.config(state=DISABLED)
        etrPool.config(state=NORMAL)
    try:    # 讀取是否預設複製時執行下個耕地
        if list1[11].replace("\n","") == "True":
            chkValw = TRUE
        else:
            chkValw = FALSE
        chkValueW.set(chkValw)
    except:
        chkValueW.set(TRUE) 
    try:    # 讀取錢包指紋
        if len(list1[12].replace("\n","")) > 0:
            pcaComboBox.insert(END,list1[12].replace("\n",""))
    except:
        pcaComboBox.insert(END,"")
    SFile.close
else:
    BackDefault()
# ============================================
# TODO: 啟動系統後第一次顯示的訊息
# ============================================
#text1.delete(1.0,END)
text1.insert(END," ============================================================== \n")
text1.insert(END,"   ➠ 作者: mymag (mymag_20@msn.com)\n")
text1.insert(END,"   ➠ 網頁: http://fgc.tw\n")
text1.insert(END,"   ➠ 版本: "+ToolVersion+" \n")
text1.insert(END,"   ➠ 程式工作目錄: "+cwd+"\n")
text1.insert(END,"   ➠ Telegram 遊戲社群: https://t.me/QiYiWorld\n")
text1.insert(END,"   ➠ 捐贈(Chia XCH): xch1vk3tcw89xtk6uqzgxuyssuwm9s4dsklnaa00hyppevxlg9tpulys98erd4\n")
text1.insert(END,"   ➠ 捐贈(BTC-Bitcoin): 33gxYWhbp5MsSfsrH5J5dr2dmmbhZdFApq\n")
text1.insert(END," ============================================================== \n")
text1.insert(END,"   ➠ madMAx43v3r/chia-plotter 最新版下載位置 \n   ➠ https://github.com/stotiks/chia-plotter/releases\n")
text1.insert(END," ============================================================== \n")
text1.insert(END,"   ➲ 請問有沒有支援K32以外的耕地呢? \n")
text1.insert(END,"   ➲ 因為是 madMAx43v3r/chia-plotter 只支援K32,並不是CTPool不支援\n")
text1.insert(END," ============================================================== \n")
text1.insert(END,"   ➲ 感謝每一位捐贈者,不管多少,請受小的一拜! 感謝! \n")

if not os.path.exists(fname):
    text1.insert(END,"\n ----------------------------------------------------------------------------- \n")
    text1.insert(END,"   ➠ 耕地程式 \"" + os.path.abspath(fname) + "\" 檔案不存在!! \n")
    text1.insert(END,"   ➠ 請前往 https://github.com/stotiks/chia-plotter/releases 下載,放在此資料夾!\n")
    text1.insert(END,"   ➠ 本軟體只是輔助工具,需要 chia-plotter 才能使用!\n")
    text1.insert(END," ----------------------------------------------------------------------------- \n")
if CheckDirList():
    btnDeleteTemp.config(state=NORMAL)
    text1.insert(END,"\n ----------------------------------------------------------------------------- \n")
    text1.insert(END,"   ➠ 暫存資料夾內有檔案,建議清除後再執行耕地!\n")
    text1.insert(END," ----------------------------------------------------------------------------- \n")
# ============================================
win.mainloop()