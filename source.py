# autogal return false
from io import BytesIO
from lxml import html
import threading
from win10toast import ToastNotifier
import base64
from win32com.shell import shell
import requests
import execjs
import sys
import pythoncom
import getpass
import tkinter
from random import randint
from tkinter import ttk
from tkinter import messagebox
import os
import json
import traceback
from webbrowser import open_new_tab
from tkinter import scrolledtext
import win32con, win32clipboard, win32gui
from PIL.ImageGrab import grabclipboard, grab
from aip import AipOcr
from time import sleep
from pynput import mouse
from pynput.keyboard import Key, Listener, Controller
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.ocr.v20181119 import ocr_client, models
from pynput import keyboard
from time import time
from PIL import Image,ImageTk
# 百度，腾讯
Controll = Controller()
LanguageAll = {
    "中+英": "CHN_ENG",
    "英": "CHN_ENG",
    "日": "JAP",
    "韩": "KOR"
}
OcrAll = {
    "百度普通版(50k次/天)": "bd_normal",
    "百度高精度(500次/天)（仅中+英）": "bd_accurate",
    "腾讯快速版(1k次/月)（仅中+英）": "tx_quick",
    "腾讯普通版(1k次/月)": "tx_normal",
    "腾讯高精度(1k次/月)（仅中+英）": "tx_accurate"
}
TransAll = {
    "百度":"bd_trans",
    "有道":"yd_trans",
    "谷歌":"gg_trans",
    "爱词霸":"icb_trans"
}
GalAll = {
    "英":"Eng",
    "日":"JAP",
    "韩":"KOR"
}
BaiduTransParameter = {
    "CHN_ENG":"en",
    "JAP": "jp",
    "KOR": "kor"
}

# 获取设置保存,方便维护
AllSetting = ["OcrSetting","OCRLangSetting","GALLangSetting","TranslationSetting"]
OtherSetting = ["StartUp","ToClip","BanHotKey"]
AllTransSetting = ["百度", "有道", "谷歌", "爱词霸"]
OcrPri = ["bd_normal", "bd_accurate", "tx_quick", "tx_normal", "tx_accurate"]
HotKeyEvent = False
Version = 1.0

def GetLatestVersion():
    try:
        etree = html.etree
        response = requests.get("https://github.com/jizhihaoSAMA/OCR-GALGAME-SystemTray/tags").text
        return etree.HTML(response).xpath("/html/body/div[5]/div/main/div[3]/div/div[2]/div[2]/div/div/div[1]/h4/a")[0].text.replace(" ", "").replace("\n", "")
    except:
        pass

class MultiProcessGetResultWithoutArgs(threading.Thread):
    def __init__(self, func):
        threading.Thread.__init__(self)
        self.func = func
        self.result = None

    def getResult(self):
        try:
            return self.result
        except:
            return None

    def run(self):
        self.result = self.func()

def GetWxPay():
    return Image.open(BytesIO(requests.get('https://s2.ax1x.com/2020/02/07/12usP0.md.jpg').content)).resize((250,250))

def GetAliPay():
    return Image.open(BytesIO(requests.get('https://s2.ax1x.com/2020/02/08/1Wl4mT.md.jpg').content)).resize((250,250))

def GetTXKey():
    open_new_tab("https://console.cloud.tencent.com/cam/capi")
    messagebox.showinfo(u"提示","新建密钥后即可")

def GetBDKey():
    open_new_tab("https://console.bce.baidu.com/ai/#/ai/ocr/app/create")
    messagebox.showinfo(u"提示","创建应用后点击管理应用即可得到密钥")

def ProgressBarWait(Progress: ttk.Progressbar):
    Random = randint(3,25)
    Now = Progress["value"]
    if Now+Random <= 94:
        Progress["value"] += Random
        Progress.update()
    sleep(0.5)

def on_activate_OCR():
    global HotKeyEvent
    HotKeyEvent = True
    if not BanHotKey.get():
        onlyOCR()

def on_activate_GAL():
    global HotKeyEvent
    HotKeyEvent = True
    if not BanHotKey.get():
        galgameMode()

def showTip(Text):
    toaster = ToastNotifier()
    toaster.show_toast(u'提示', u"{}".format(Text),icon_path='2.ico',duration=5,threaded=False)

def showSuprise(SupriseText): # Wow
    SupriseText["text"] = "什么Σ(ﾟдﾟ)？\n你还真有许可证？NBNB"

def showAbout():
    AboutWin = tkinter.Toplevel()
    AboutWin.geometry('+{}+{}'.format(Win.winfo_geometry().split("+")[1],Win.winfo_geometry().split("+")[2]))
    AboutWin.resizable(0,0)
    AboutWin.title("关于")
    tkinter.Label(AboutWin,text="作者：").grid(row=0,column=0)
    tkinter.Label(AboutWin,text="机智豪SAMA").grid(row=0,column=1)
    tkinter.Label(AboutWin,text="Github：").grid(row=1,column=0)
    tkinter.Button(AboutWin,text="https://github.com/jizhihaoSAMA",command=lambda :open_new_tab("https://github.com/jizhihaoSAMA"),bd=0,cursor="hand2",font=('微软雅黑','10','normal','underline'),foreground="blue",relief="flat").grid(row=1,column=1,ipadx=0,ipady=0)
    tkinter.Label(AboutWin,text="介绍：").grid(row=2,column=0)
    tkinter.Label(AboutWin,text="突发奇想。一写，就是这么半年").grid(row=2,column=1)
    tkinter.Label(AboutWin,text="当前版本：").grid(row=3,column=0)
    tkinter.Label(AboutWin,text="{}（平民版）".format(str(Version))).grid(row=3,column=1)
    tkinter.Label(AboutWin,text="License（软件激活码）：").grid(row=4,column=0,columnspan=2,sticky="W",padx=10)
    SupriseText = tkinter.Label(AboutWin)
    SupriseText.grid(row=6,column=1,sticky="W")
    Suprise = tkinter.Text(AboutWin,width=40,height=7,relief="solid",font=("微软雅黑",10))
    Suprise.grid(row=5,column=0,columnspan=2,pady=(3,10),padx=20)
    ttk.Button(AboutWin,text="检查激活码",command=lambda :messagebox.showinfo(u"恶意提示",u"检你个锤子，妮可别让我逮住了。不然可有你好果子吃的_(¦3」∠)_")).grid(row=6,column=1,sticky="E",pady=5,padx=20,ipadx=20,ipady=5)
    Suprise.bind("<Key>",lambda event:showSuprise(SupriseText))
    AboutWin.mainloop()

def checkUpdate():
    ProgressFrame = tkinter.Frame(Win)
    ProgressFrame.grid(row=1,column=0,columnspan=2,sticky="E",padx=5,pady=3)
    tkinter.Label(ProgressFrame,text="操作进度：",background="SystemButtonFace").grid(row=0,column=0)
    Progress = ttk.Progressbar(ProgressFrame,length=150,mode="determinate",value=0,maximum=100)
    Progress.grid(row=0,column=1)
    Win.update()
    CheckThread = MultiProcessGetResultWithoutArgs(GetLatestVersion)
    CheckThread.start()
    StartTime = time()
    while True:
        if CheckThread.getResult():
            Progress["value"] = 100
            Progress.update()
            LastestVersion = CheckThread.getResult()[0:3] #截取 前3位
            if float(LastestVersion) > Version:
                Choice = messagebox.askyesno(u"检查更新",u"检测到新版本 {} 咯\n你的当前版本是 {} ，去康康吧？".format(str(LastestVersion),str(Version)))
                if Choice:
                    open_new_tab("https://github.com/jizhihaoSAMA/OCR-GALGAME-SystemTray/tags") # 须修改
            else:
                messagebox.showinfo(u"提示",u"宁当前已经是最新版本辣，")
            ProgressFrame.grid_forget()
            Win.update()
            break
        if time()-StartTime > 10: #更新时间大于10秒
            Choice = messagebox.askyesno(u"检查更新",u"检查更新失败，自己去Github首页康康吧？")
            if Choice:
                open_new_tab("https://github.com/jizhihaoSAMA/OCR-GALGAME-SystemTray/tags") # too
            ProgressFrame.grid_forget()
            Win.update()
            break
        ProgressBarWait(Progress)

def browserTxAPI():
    open_new_tab("https://console.cloud.tencent.com/ocr/general")

def browserBdAPI():
    open_new_tab("https://console.bce.baidu.com/ai/#/ai/ocr/overview/index")

def bd_trans(Text): #Cookie已爆炸 # 1.31号恢复正常使用
    FromParameter = BaiduTransParameter[LanguageAll[GALLangSetting.get()]] #获取当前选择的语言所对应的百度参数
    with open("./important/setting.json") as f:
        Cookie = json.load(f)["cookie"]
    url = 'https://fanyi.baidu.com/v2transapi'
    data = {
        'query': Text.replace("\n",""),
        'token': 'f61270e14644b9cf3c0a675ab86a5f2b',
        'sign': "",
        'from': FromParameter,  # kor jp en
        'to': "zh",
    }
    headers = {
        'cookie': Cookie
    }
    with open("important/baidutrans.js", 'r') as f:
        ctx = execjs.compile(f.read())
    sign = ctx.call("e", Text.replace("\n",""))
    data["sign"] = sign
    response = requests.post(url, headers=headers, data=data)
    return (response.json()['trans_result']['data'][0]['dst']) if response.json().get("trans_result") else ""

def icb_trans(Text):
    trans = Text.replace("\n","")
    url = "http://fy.iciba.com/ajax.php?a=fy"
    data = {
        'f': "auto",
        "t": "auto",
        "w": trans
    }
    response = requests.post(url, data=data)
    return response.json()['content']['out']

def yd_trans(Text):
    trans = Text.replace("\n","")
    url = 'http://fanyi.youdao.com/translate?&doctype=json&type=AUTO&i=%s' % trans
    response = requests.post(url)
    return response.json()['translateResult'][0][0]['tgt']

def gg_trans(Text):
    trans = Text.replace("\n","")
    url = "http://translate.google.cn/translate_a/single?client=gtx&dt=t&dj=1&ie=UTF-8&sl=auto&tl=zh_CN&q=%s" % trans
    response = requests.get(url)
    return response.json()['sentences'][0]["trans"]

def clearClipboard():
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.CloseClipboard()

def oneShot():
    with Controll.pressed(Key.cmd_l):
        with Controll.pressed(Key.shift):
            Controll.press('s')
            Controll.release('s')

def GetPointer():
    def on_click(x, y, button, pressed):
        global Click_x, Click_y, Release_x, Release_y, STOP
        if pressed:
            Click_x = x
            Click_y = y
        else:
            Keyboardlistener.stop()
            Release_x = x
            Release_y = y
            STOP = False
            return False

    def on_release(key):
        global STOP
        if key == Key.esc: #Esc结束截图并停止线程,打开主页面
            Mouselistener.stop()
            STOP = True
            return False

    with mouse.Listener(on_click=on_click) as Mouselistener, Listener(on_release=on_release) as Keyboardlistener:
        Mouselistener.join()
        Keyboardlistener.join()

with open("./important/setting.json","r+") as f:
    setting = json.load(f)
TimeInterval = int(setting["AutoGALTimeInterval"])

def getNowOCR():
    nowOCR = setting['defaultOCR']
    return OcrPri.index(nowOCR)

def getNowLang():
    LangPri = ['CHN_ENG',"JAP","KOR"]
    GalPri = ['Eng','JAP']
    nowOCRLang = setting['defaultOCRLanguage']
    nowGALLang = setting['defaultGALLanguage']
    OCRLangSetting.current(LangPri.index(nowOCRLang))
    GALLangSetting.current(GalPri.index(nowGALLang))

def getNowTrans():
    TransPri = ["bd_trans", "yd_trans", "gg_trans", "icb_trans"]
    nowTrans = setting["trans"]
    return TransPri.index(nowTrans)

def getOtherSetting():
    Othersetting = setting['otherSetting']
    for i in OtherSetting:
        onesetting = Othersetting[i]
        eval(i+".set("+str(onesetting)+")")

def saveSetting(*args):
    #判断电脑启动
    with open("./important/setting.json", "r+") as f:
        setting = json.load(f)
    SettingList = []
    OtherSettingList = []
    count=0
    for j in AllSetting: #遍历所有下拉框设置内容
        SettingList.append({**OcrAll, **LanguageAll, **GalAll,**TransAll}[eval(j + ".get()")])  # 获取选项内容转换Json内容
    for j in OtherSetting:
        OtherSettingList.append(str(eval(j+".get()")))
    for i in setting:#Maybe it is not a good idea
        if count < len(SettingList):
            setting[i] = SettingList[count]
            count += 1
        else:
            break
    count = 0
    for i in setting['otherSetting']:
        setting['otherSetting'][i] = OtherSettingList[count]
        count += 1

    with open("./important/setting.json", "w+") as f:
        json.dump(setting,f,indent=2)

    user_name = getpass.getuser()
    if setting['otherSetting']['StartUp'] == "True":  # 确定开机启动
        if not os.path.exists('C:/Users/' + user_name + '/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/' + os.path.basename(sys.argv[0]) + '.lnk'):  # 不存在路径
            filename = sys.argv[0]
            lnkname = r"C:/Users/" + user_name + "/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup" + r"/" + os.path.basename(sys.argv[0]) + ".lnk"  # 将要在此路径创建快捷方式

            shortcut = pythoncom.CoCreateInstance(shell.CLSID_ShellLink, None,pythoncom.CLSCTX_INPROC_SERVER, shell.IID_IShellLink)
            shortcut.SetPath(filename)
            shortcut.SetWorkingDirectory(os.path.dirname(os.path.realpath(sys.argv[0])))
            if os.path.splitext(lnkname)[-1] != '.lnk':
                lnkname += ".lnk"
            shortcut.QueryInterface(pythoncom.IID_IPersistFile).Save(lnkname, 0)
    else:  # 取消关机启动
        if os.path.exists('C:/Users/' + user_name + '/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/' + os.path.basename(sys.argv[0]) + '.lnk'):  # 存在路径
            os.remove('C:/Users/' + user_name + '/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/' + os.path.basename(sys.argv[0]) + '.lnk')

def changeOCR(*args):
    if OcrAll[OcrSetting.get()] =="bd_accurate":
        OCRLangSetting['value'] = ['中+英']
        OCRLangSetting.current(0)
    else:
        OCRLangSetting['value'] = ['中+英', '日', '韩']
        OCRLangSetting.current(0)

def openSettingFile(*args):
    os.system("start /b notepad ./important/setting.json")

def returnToPrimary():
    getNowOCR()
    getNowLang()
    getNowTrans()
    getOtherSetting()

def feedBack():
    open_new_tab("https://github.com/jizhihaoSAMA/OCR-Translation-SystemTray/issues")
    messagebox.showinfo(u"提示",u"提交issue就可以辣。（¯﹃¯）")

def checkWhetherGet(win,thread,position):
    result = thread.getResult()
    if result:
        result.resize((20,20))
        TempImageObj = ImageTk.PhotoImage(result)
        Pic = tkinter.Label(win,image=TempImageObj)
        Pic.image = TempImageObj
        Pic.grid(row=1,column=position)
        win.update()
        win.after_cancel(position+1)
    else:
        win.after(300,lambda :checkWhetherGet(win,thread,position))

def donateMoney():
    DonateWin = tkinter.Toplevel()
    DonateWin.geometry('+{}+{}'.format(Win.winfo_geometry().split("+")[1],Win.winfo_geometry().split("+")[2]))
    DonateWin.resizable(0,0)
    tkinter.Label(DonateWin,text="如果觉得还⑧错，给个快乐水的钱不辣？").grid(row=0,column=0,columnspan=2,pady=10)
    tkinter.Label(DonateWin,text="加载中......").grid(row=1,column=0,padx=100,pady=100)
    tkinter.Label(DonateWin,text="加载中......").grid(row=1,column=1,padx=100,pady=100)
    tkinter.Label(DonateWin,text="谢谢支持").grid(row=2,column=0,columnspan=2)
    Wxthread = MultiProcessGetResultWithoutArgs(GetWxPay)
    Wxthread.start()
    Alithread = MultiProcessGetResultWithoutArgs(GetAliPay)
    Alithread.start()
    DonateWin.after(0,lambda :checkWhetherGet(DonateWin,Wxthread,0))
    DonateWin.after(0,lambda :checkWhetherGet(DonateWin,Alithread,1))
    DonateWin.mainloop()

def howToUse():
    pass

def textToClip():
    global OCRText,OCRWin
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(OCRText)
    win32clipboard.CloseClipboard()
    showTip("OCR识别结果已复制到剪贴板！(*ˉ﹃ˉ)")

def OCR_Core(Image,**kwargs):
    #: PIL.Image
    with open("./important/setting.json", 'r+') as f:
        setting = json.load(f)
    global GALMode, ResultJson  # 为了文字处理使用
    global LastImageValue, OCRText, OCRResultSetting
    if kwargs.get("EXTRA"):
        SelectOCR = OcrAll[OCRResultSetting.get()]
    else:
        SelectOCR = OcrAll[OcrSetting.get()]
        #写入内存，太慢，更换保存本地方式
        Image.save('important/LastImage.jpg')
        with open('important/LastImage.jpg', 'rb+') as f:
            LastImageValue = f.read()
    OCRText = ""
    if SelectOCR == "bd_normal" or SelectOCR =="bd_accurate":
        AppID = setting["userInfo"]["bd_info"]["AppID"]
        APIKey = setting["userInfo"]["bd_info"]["APIKey"]
        SecretKey = setting["userInfo"]["bd_info"]["SecretKey"]
        BDOcr = AipOcr(AppID,APIKey,SecretKey)
        if not GALMode: #在gal模式下获取下拉框内容
            if SelectOCR == "bd_normal":
                OCRLanguage = setting["defaultOCRLanguage"]
                ResultJson = BDOcr.basicGeneral(LastImageValue, {"language_type":OCRLanguage}) #格式错误
            else:
                ResultJson = BDOcr.basicAccurate(LastImageValue)
        else:
            GALLanguage = setting["defaultGALLanguage"]
            ResultJson = BDOcr.basicGeneral(LastImageValue, {"language_type": GALLanguage})  # 格式错误
        if not (ResultJson["words_result_num"]):# 没有结果
            if GALMode:
                return ""
            else:
                messagebox.showinfo(u"识别错误",u"未识别到文字")
        if ResultJson.get("words_result"): #能获取结果
            # 文本处理
            for i in ResultJson["words_result"]:
                OCRText += i['words']+"\n"
            return OCRText
        elif ResultJson.get('error_code') ==14: #证书失效,检查用户信息
            messagebox.showerror(title="Error", message=u"检查APPID,APIKEY,以及SECRET_KEY,程序退出")
            sys.exit()
        elif ResultJson.get('error_code') ==17: #今天超额
            messagebox.showerror(title="Error", message=u"今日次数超额")
            sys.exit()
        else:
            messagebox.showerror(title="Error", message=u"错误代码:"+str(ResultJson))
            sys.exit()
    else:#腾讯OCR
        TX_INFO = setting["userInfo"]["tx_info"]
        SecretId = TX_INFO["SecretId"]
        SecretKey = TX_INFO["SecretKey"]
        try:
            cred = credential.Credential(SecretId, SecretKey)
            httpProfile = HttpProfile()
            httpProfile.endpoint = "ocr.tencentcloudapi.com"

            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            # zh\auto\jap\kor
            client = ocr_client.OcrClient(cred, "ap-guangzhou", clientProfile)
            params = '{"ImageBase64":"' + str(bytes.decode(base64.b64encode(LastImageValue), encoding='utf-8')) + '","LanguageType":"auto"}' #生成传输参数
            # 可修改
            # GeneralFasterOCR == 通用印刷体识别高速版，没有语言选项，有方位
            # GeneralBasicOCR == 通用印刷体识别，有语言选项，有方位
            # GeneralAccurateOCR == 通用印刷体高精度版，没有语言选项，有方位
            if SelectOCR == "tx_normal":
                req = models.GeneralBasicOCRRequest()
                req.from_json_string(params)
                resp = client.GeneralBasicOCR(req)
            elif SelectOCR == "tx_quick":
                req = models.GeneralFastOCRRequest()
                req.from_json_string(params)
                resp = client.GeneralFastOCR(req)
            else:
                req = models.GeneralAccurateOCRRequest()
                req.from_json_string(params)
                resp = client.GeneralAccurateOCR(req)
            ResultJson = json.loads(resp.to_json_string()) # 获取结果json
            OCRText = "" # 纯文本
            for i in ResultJson["TextDetections"]:
                OCRText += i["DetectedText"]+"\n"
            return OCRText

        except TencentCloudSDKException as err:
            if err.get_code() == "FailedOperation.ImageNoText":
                if not GALMode:
                    messagebox.showinfo("识别失败","没有识别到文字")
                return False

def Text2Novel():
    global ResultJson,OCRResultText,ComeBackButton,Text2NovelButton
    NovelText = ""
    if ResultJson.get("words_result"):  # 能获取结果，则是百度翻译
        # 文本处理不带文本
        ResultList = []
        for i in ResultJson['words_result']:
            ResultList.append(i["words"])
        MaxLength = MaxLength = len(max(ResultList, key=len))
        ResultListLength = len(ResultList)
        TextEndFlag = True
        for i in range(ResultListLength):
            if len(ResultList[i]) < MaxLength and i != ResultListLength - 1:
                # 判断一行字数是否小于最大长度,要进行处理.yes->有3种情况,
                # 1:开头,用i!=0排除
                # 2:一段的开头,则上一次的长度小于等于MaxLength,最好用一段结尾判断,需要在加这行之前加入\t
                # 3:一段的结尾,则下一行小于MaxLength,结尾需要加入\n
                # 4:文章最结尾,用i!=len-1排除
                if TextEndFlag:  # 上一行是结尾,这一行一定是开头,这一行开头需要加\t
                    NovelText += '\t'
                    TextEndFlag = False
                NovelText += ResultList[i]
                if len(ResultList[i + 1]) < MaxLength and len(ResultList[i]) <= MaxLength:  # 下一行小于最长长度且这一行也小,则下一行是结尾,这一行
                    NovelText += '\n'
                    TextEndFlag = True
            else:  # 满长度直接加，不需要换行
                NovelText += ResultList[i]

    else: #为腾讯的OCR，通过坐标处理
        NovelText = "\t"
        TextDetections = ResultJson["TextDetections"]
        FirstParag = 1
        for i in TextDetections:
            if json.loads(i["AdvancedInfo"])["Parag"]["ParagNo"] != FirstParag:
                NovelText += "\n\t"
                FirstParag += 1
            NovelText += i["DetectedText"]

    OCRResultText.delete(1.0,"end")
    OCRResultText.insert("end",NovelText)
    Text2NovelButton.grid_forget()
    ComeBackButton.grid(row=0,column=2,ipady=5,ipadx=10,pady=3)

def ComeToPrimaryFormat():
    global OCRText,OCRResultText,Text2NovelButton,ComeBackButton
    ComeBackButton.grid_forget()
    Text2NovelButton.grid(row=0,column=2,ipady=5,ipadx=10,pady=3)
    OCRResultText.delete(1.0,"end")
    OCRResultText.insert("end",OCRText)

def OCR():
    global Click_x, Click_y, Release_x, Release_y
    global STOP
    clearClipboard()
    oneShot()
    GetPointer()
    # sleep(1) #必须sleep（下次尝试用try抓取异常->对于剪贴板本来就有图片会导致图片识别的上一张，现在改为判断上一次的图片和现在的图片是否相等->判定很奇怪，改成先清空剪贴板再利用异常捕获），grabclipboard函数要立即截取，而存入剪贴板需要时间，所以需要等待
    while True:
        try: #如果与上次不相等
            if STOP or (Click_x == Release_x and Click_y == Release_y):
                return False
            return OCR_Core(grabclipboard())
        except AttributeError:
            pass
        except:
            messagebox.showinfo(u"出现错误辣", "错误信息：\n" + traceback.print_exc())

def changeOCRAndOCR(*args):
    global OCRText
    OCRText = OCR_Core(None,EXTRA=True) #可优化
    OCRResultText.delete(1.0, "end")
    OCRResultText.insert("end", OCRText)

def continueOCR():
    OCRWin.withdraw()
    oneShot()
    GetPointer()
    while True:
        try: #如果与上次不相等
            if STOP or (Click_x == Release_x and Click_y == Release_y):
                return False
            OCRText = OCR_Core(grabclipboard())
        except:
            messagebox.showinfo(u"出现错误辣", "错误信息：\n" + traceback.print_exc())
        else:
            OCRResultText.delete(1.0, "end")
            OCRResultText.insert("end", OCRText)
            OCRWin.deiconify()
            if ToClip.get():
                textToClip()
            break

def onlyOCR():
    global OCRResultText, OCRResultSetting, OCRWin, TrayExists, GALMode
    # pass
    try:
        GALMode = False
        Win.deiconify()
        ExdStyle = win32gui.GetWindowLong(Win_hwnd, win32con.GWL_EXSTYLE)
        win32gui.SetWindowLong(Win_hwnd, win32con.GWL_EXSTYLE, ExdStyle | win32con.WS_EX_LAYERED)
        win32gui.SetLayeredWindowAttributes(Win_hwnd, 255, 0, win32con.LWA_ALPHA)
        # Win.after_cancel(1) # 取消获取窗口句柄函数绑定
        sleep(0.5) # 防止Win窗口没有及时隐藏
        OCRText = OCR()
        win32gui.SetLayeredWindowAttributes(Win_hwnd, 255, 255, win32con.LWA_ALPHA)
        if not OCRText:
            try:
                win32gui.SetForegroundWindow(Win_hwnd)
            except BaseException as e:
                if e.args[0]:
                    messagebox.showinfo(u"出现错误辣","错误信息：\n"+traceback.print_exc())
            except Exception:
                messagebox.showinfo(u"出现错误辣", "错误信息：\n" + traceback.print_exc())
            return False
        else:
            pass
        Win.withdraw()
        OCRWin = tkinter.Toplevel()
        OCRWin.title("OCR结果")
        OCRWin.wm_attributes("-topmost",1)
        OCRWin.geometry('+500+250')
        OCRWin.resizable(0,0)
        OCRWin.protocol("WM_DELETE_WINDOW",lambda :Win.deiconify()+OCRWin.withdraw() if TrayExists==False else OCRWin.withdraw())
        global ComeBackButton,Text2NovelButton
        tkinter.Label(OCRWin,text="识别结果如下：",font=("微软雅黑",10)).grid(row=0,column=0)
        Text2NovelButton = ttk.Button(OCRWin,text="结果转文章形式",command=Text2Novel)
        Text2NovelButton.grid(row=0,column=2,ipady=5,ipadx=10,pady=3)
        ComeBackButton = ttk.Button(OCRWin,text="还原为原格式",command=ComeToPrimaryFormat)
        OCRResultText = scrolledtext.ScrolledText(OCRWin,width=50,height=8,font=("微软雅黑",12),tabs=32,relief="solid")
        OCRResultText.grid(row=1,column=0,padx=10,pady=(10,0),columnspan=3)
        # ResultText.insert("end",'aaa')
        tkinter.Label(OCRWin,text="更改OCR引擎:",font=("微软雅黑",9)).grid(row=2,column=0,padx=(20, 0))
        OCRResultSetting = ttk.Combobox(OCRWin,width=28,state="readonly")
        OCRResultSetting['value'] = ['百度普通版(50k次/天)', '百度高精度(500次/天)（仅中+英）', '腾讯快速版(1k次/月)（仅中+英）', '腾讯普通版(1k次/月)', '腾讯高精度(1k次/月)（仅中+英）']
        Index = getNowOCR()
        OCRResultSetting.current(Index)
        OCRResultSetting.bind("<<ComboboxSelected>>", changeOCRAndOCR)  # 修改OCR选项立即查看OCR 结果
        OCRResultSetting.grid(row=2, column=1 ,pady=10)
        ttk.Button(OCRWin,text="继续OCR",command=continueOCR).grid(row=2, column=2,padx=(30,5),ipadx=10,ipady=5,pady=10)
        OCRResultText.delete(1.0, "end")
        OCRResultText.insert("end", OCRText)
        if ToClip.get():
            textToClip()
        if not HotKeyEvent:
            OCRWin.mainloop()
    except Exception as e:
        messagebox.showinfo(u"崩溃了", u"错误信息为：{}\n程序退出".format(str(e.args)))
        sys.exit(0)

def autoGAL():
    if Auto.get() == 1:
        global Click_x, Click_y, Release_x, Release_y, LastImageValue, GALResultText, TranslationSetting
        # NowImage = grab((Click_x, Click_y, Release_x, Release_y))
        NowImage = grab((Click_x, Click_y, Release_x+1, Release_y+1)) #一个像素差
        NowImage.save('important/NowImage.jpg')
        with open('important/NowImage.jpg','rb+') as f:
            NowImageValue = f.read()
        if NowImageValue != LastImageValue:  # 区域不一样，继续OCR
            OCRText = OCR_Core(NowImage)
            if not OCRText:
                return False
            GALResultText.delete(1.0, "end")
            GALResultText.insert("end", eval(TransAll[GALTranslationSetting.get()] + """('''""" + OCRText + """''')"""))
        GALResultText.after(TimeInterval,autoGAL)
    else:
        GALResultText.after_cancel(1)

def changeGAL(*args):
    global GALTranslationSetting,OCRText
    GALResultText.delete(1.0, "end")
    GALResultText.insert("end", eval(TransAll[GALTranslationSetting.get()] + """('''""" + OCRText + """''')"""))

def continueGAL(*args):
    oneShot()
    GetPointer()
    while True:
        try:  # 如果与上次不相等
            if STOP or (Click_x == Release_x and Click_y == Release_y):
                return False
            OCRText = OCR_Core(grabclipboard())
        except:
            messagebox.showinfo(u"出现错误辣", "错误信息：\n" + traceback.print_exc())
        else:
            GALResultText.delete(1.0, "end")
            GALResultText.insert("end", eval(TransAll[GALTranslationSetting.get()] + """('''""" + OCRText + """''')"""))
            break

def galgameMode():#galgame游戏吞按键
    try:
        global Win_hwnd, OCRText, GALResultText, GALMode, GALTranslationSetting
        GALMode = True
        Win.deiconify()
        ExdStyle = win32gui.GetWindowLong(Win_hwnd, win32con.GWL_EXSTYLE)
        win32gui.SetWindowLong(Win_hwnd, win32con.GWL_EXSTYLE, ExdStyle | win32con.WS_EX_LAYERED)
        win32gui.SetLayeredWindowAttributes(Win_hwnd, 255, 0, win32con.LWA_ALPHA)
        OCRText = OCR()
        sleep(0.5)  # 防止Win窗口没有及时隐藏
        win32gui.SetLayeredWindowAttributes(Win_hwnd, 255, 255, win32con.LWA_ALPHA)
        if not OCRText or (Click_x == Release_x and Click_y == Release_y): # ESC取消后
            win32gui.SetForegroundWindow(Win_hwnd)
            return False
        else:
            OCRText = OCRText
        Win.withdraw()
        GALWin = tkinter.Toplevel()
        GALWin.wm_attributes("-topmost", 1)
        GALWin.geometry('+500+250')
        GALWin.resizable(0,0)
        GALWin.protocol("WM_DELETE_WINDOW",lambda :Win.deiconify()+GALWin.withdraw() if TrayExists==False else GALWin.withdraw())
        tkinter.Label(GALWin,text="翻译结果如下：",font=("微软雅黑",10)).grid(row=0,column=0)
        GALResultText = scrolledtext.ScrolledText(GALWin, width=50, height=8, font=("微软雅黑", 12),relief="solid",borderwidth=1,tabs=33)
        GALResultText.grid(row=1,column=0,padx=10,pady=(10,0),columnspan=4)
        tkinter.Label(GALWin,text="更改翻译引擎:",font=("微软雅黑",9)).grid(row=2,column=0,ipadx=0)
        GALTranslationSetting = ttk.Combobox(GALWin, width=10, state="readonly")  # textvariable
        GALTranslationSetting["value"] = AllTransSetting
        GALTranslationSetting.bind_all('<<ComboboxSelected>>',changeGAL)
        Index = getNowTrans()
        GALTranslationSetting.current(Index)
        GALTranslationSetting.grid(row=2,column=1,sticky="W")
        Auto_CKButton = ttk.Checkbutton(GALWin, text="自动扫描", variable=Auto, command=autoGAL)
        Auto_CKButton.grid(row=2, column=2)
        ttk.Button(GALWin,text="更改区域",command=continueGAL).grid(row=2,column=3,pady=10,ipady=5)
        GALResultText.delete(1.0, "end")
        GALResultText.insert("end", eval(TransAll[TranslationSetting.get()] + """('''""" + OCRText + """''')"""))
        if not HotKeyEvent:
            GALWin.mainloop()
    except Exception as e:
        messagebox.showinfo(u"崩溃了",u"错误信息为：{}\n程序退出".format(str(e.args)))
        sys.exit(0)

def on_closing():
    global TrayExists,ToClip,StartUp,BanHotKey
    Win.after_cancel(1) # 取消获取窗口句柄绑定
    if not TrayExists:  # 没有托盘的情况下
        Choice = messagebox.askyesnocancel("提示", "需要最小化窗口吗？(｡í _ ì｡)\n是：保存到系统托盘\n否：直接退出 ")
        if Choice:
            Win.withdraw()
            def menu_func(event, x, y):
                global WinExists, ToClip_Tray
                # print(ToClip_Tray.get())
                if event == 'WM_RBUTTONDOWN':  # 监听右击事件
                    menu.tk_popup(x, y)  # 弹出菜单
                if event == 'WM_LBUTTONDOWN':  # 左 事件  还有其他的如 WM_LBUTTONDBLCLK 左双击
                    Win.deiconify()  # 显示主页面

            Win.tk.call('package', 'require', 'Winico')
            icon = Win.tk.call('winico', 'createfrom', '2.ico')
            Win.tk.call('winico', 'taskbar', 'add', icon,
                        '-callback', (Win.register(menu_func), '%m', '%x', '%y'),
                        '-pos', 0,
                        '-text', u'jizhihaoSAMA’s Tool')
            menu = tkinter.Menu(Win, tearoff=0, font=('微软雅黑', 9))
            menu.add_command(label=u'显示主页面', command=lambda: Win.deiconify())
            menu.add_command(label=u'OCR        ', command=onlyOCR)
            menu.add_command(label=u'GALGAME    ', command=galgameMode)
            OtherSettingMenu = tkinter.Menu(menu, tearoff=0)
            OtherSettingMenu.add_checkbutton(label=u'开机启动', variable=StartUp)
            OtherSettingMenu.add_checkbutton(label=u'禁用快捷键', variable=BanHotKey)
            OtherSettingMenu.add_checkbutton(label=u'OCR结果复制到剪贴板', variable=ToClip)
            menu.add_cascade(label=u"其他设置", menu=OtherSettingMenu)
            menu.add_separator()
            menu.add_command(label=u'退出', command=sys.exit)
            last = OtherSettingMenu.index('end')

            for i in range(last):  # 绑定保存设置函数
                OtherSettingMenu.entryconfigure(i, command=saveSetting)
            TrayExists = True
        elif Choice == False:
            Win.destroy()
            sys.exit(0)
        else:
            pass
    else:# 直接最小化
        Win.withdraw()

def GetWinHWND():
    global Win_hwnd
    Win_hwnd = win32gui.GetActiveWindow()

def SetKey():
    messagebox.showinfo(u"提示",u"请打开配置文件并将密钥直接复制到对应的地方(TX_INFO AND BD_INFO)")

try:
    Win = tkinter.Tk()
    OCRandGALHotKey = keyboard.GlobalHotKeys({setting["galHotKey"]: on_activate_GAL,setting["ocrHotKey"]: on_activate_OCR})
    OCRandGALHotKey.start()
    TrayExists = False
    Win.geometry("505x325+500+250")
    Win.resizable(0,0)
    Win.option_add("*background","white")
    # Win.option_add("*font","('微软雅黑','1')") # 字体很丑
    Win.protocol("WM_DELETE_WINDOW", on_closing)
    Win.title("OCR-Translation-SystemTray")

    StartUp = tkinter.BooleanVar()
    ToClip = tkinter.BooleanVar()
    BanHotKey = tkinter.BooleanVar()
    Auto = tkinter.BooleanVar()
    MenuBar = tkinter.Menu(Win)
    OCREntry = tkinter.StringVar()
    GALEntry = tkinter.StringVar()
    OCREntry.set(setting['ocrHotKey'].replace("<","").replace(">","").title())
    GALEntry.set(setting['galHotKey'].replace("<","").replace(">","").title())
    Style = ttk.Style()
    Style.configure("TCheckbutton",background="white")
    # Style.configure(,background="DimGray",borderwidth=10,foreground="FloralWhite",anchor="CENTER",bordercolor="black",relief="raised")

    Start = tkinter.Menu(MenuBar, tearoff=False)
    Start.add_command(label="OCR",  command=onlyOCR)
    Start.add_command(label="Galgame",  command=galgameMode)
    Start.add_separator()
    Start.add_command(label="设置密钥", command=SetKey)
    Start.add_command(label="打开配置文件     Ctrl+O",  command=openSettingFile)
    MenuBar.add_cascade(label=" 开始(S) ", menu=Start, underline=4)
    HelpMenu = tkinter.Menu(MenuBar,tearoff=False)
    ConcatUsMenu = tkinter.Menu(MenuBar,tearoff=False)
    ConcatUsMenu.add_command(label="反馈BUG", command=feedBack)
    ConcatUsMenu.add_command(label="捐助", command=donateMoney)
    HelpMenu.add_cascade(label="反馈&&支持",menu=ConcatUsMenu)
    APIBrowser = tkinter.Menu(HelpMenu,tearoff=False)
    APIBrowser.add_command(label="腾讯OCR", command=browserTxAPI)
    APIBrowser.add_command(label="百度OCR", command=browserBdAPI)
    HelpMenu.add_cascade(label="查看接口调用情况",menu=APIBrowser)
    KeyBrowser = tkinter.Menu(HelpMenu,tearoff=False)
    KeyBrowser.add_command(label="获取腾讯密钥",command=GetTXKey)
    KeyBrowser.add_command(label="获取百度密钥",command=GetBDKey)
    HelpMenu.add_cascade(label="获取接口密钥",menu=KeyBrowser)
    HelpMenu.add_separator()
    HelpMenu.add_command(label="关于...",command=showAbout)
    HelpMenu.add_command(label="检查更新", command=checkUpdate)
    HelpMenu.add_command(label="如何使用", command=howToUse)
    MenuBar.add_cascade(label=" 帮助(H) ",menu=HelpMenu,underline=4)
    Win.config(menu=MenuBar)
    Win.bind_all("<Control-o>",lambda event: os.system("start /b notepad ./important/setting.json"))
    TabControl = ttk.Notebook(Win)
    Page1 = tkinter.Frame(TabControl)
    Page2 = tkinter.Frame(TabControl)
    TabControl.add(Page1,text="   常规设置   ",padding="0.1i")
    TabControl.add(Page2,text="   其他设置   ",padding="0.1i")
    TabControl.grid(row=0,column=0,pady=(2,0),padx=(2,0),columnspan=2)
    #OCR框架
    OcrFrame = tkinter.LabelFrame(Page1,text="设置默认OCR",foreground="black",font=("微软雅黑",12),bd=2)
    tkinter.Label(OcrFrame,text="选择引擎：",font=("微软雅黑",10)).grid(row=0,column=0,padx=(20,0),pady=10)
    OcrSetting = ttk.Combobox(OcrFrame,width=28,state="readonly") #textvariable
    OcrSetting['value']=['百度普通版(50k次/天)','百度高精度(500次/天)（仅中+英）','腾讯快速版(1k次/月)（仅中+英）','腾讯普通版(1k次/月)','腾讯高精度(1k次/月)（仅中+英）']
    index = getNowOCR()
    OcrSetting.current(index)
    OcrSetting.bind("<<ComboboxSelected>>",changeOCR) #textvariable
    OcrSetting.grid(row=0,column=1,padx=(0,20))
    tkinter.Label(OcrFrame,text="*超过次数会产生费用").grid(row=1,column=0,columnspan=2)
    OcrFrame.grid(row=0,column=0,padx=20,columnspan=2)
    #语言选择框架
    LangFrame = tkinter.LabelFrame(Page1,text="默认语言设置",foreground="black",font=("微软雅黑",12),bd=2)
    tkinter.Label(LangFrame,text="选择OCR语言：",font=("微软雅黑",10)).grid(row=0,column=0,pady=10,padx=(20,0))
    OCRLangSetting = ttk.Combobox(LangFrame,width=10,state="readonly") #textvariable
    if OcrAll[OcrSetting.get()] == "bd_normal" or OcrAll[OcrSetting.get()] == "tx_normal":
        OCRLangSetting['value'] = ['中+英', '日', '韩']
    else:
        OCRLangSetting['value'] = ['中+英']
    OCRLangSetting.grid(row=0,column=1,padx=(0,20))
    tkinter.Label(LangFrame, text="选择GAL语言：", font=("微软雅黑", 10)).grid(row=1, column=0, pady=10, padx=(20, 0))
    GALLangSetting = ttk.Combobox(LangFrame, width=10, state="readonly")
    GALLangSetting['value'] = ['英', '日', '韩']
    GALLangSetting.grid(row=1,column=1,padx=(0,20))
    getNowLang()
    LangFrame.grid(row=1,column=0,pady=20,padx=(20,0),sticky="W")
    # 翻译选择框架
    TranslationFrame = tkinter.LabelFrame(Page1,text="设置默认翻译",font=("微软雅黑",12))
    tkinter.Label(TranslationFrame,text="选择平台：").grid(row=0,column=0,padx=(20,0),pady=10)
    TranslationSetting = ttk.Combobox(TranslationFrame,width=10,state="readonly") #textvariable
    TranslationSetting["value"] = AllTransSetting
    index = getNowTrans()
    TranslationSetting.current(index)
    TranslationSetting.grid(row=0,column=1,padx=(0,20))
    TranslationFrame.grid(row=1,column=1,pady=20,padx=(20,0))
    #tip
    # 其他选项栏
    BootStart_CKButton = ttk.Checkbutton(Page2,text="开机启动",variable=StartUp)
    BootStart_CKButton.grid(row=0,column=0,sticky="W",pady=2)
    ToClip_CKButton = ttk.Checkbutton(Page2,text="OCR结果复制到剪贴板",variable=ToClip)
    ToClip_CKButton.grid(row=1,column=0,sticky="W",pady=2)
    # HideWin_CKButton = tkinter.Checkbutton(Page2,text="截图时隐藏窗口",variable=HideWin)
    # HideWin_CKButton.grid(row=2,column=0,sticky="W",pady=2)
    BanHotKey_CKButton = ttk.Checkbutton(Page2,text="禁用快捷热键",variable=BanHotKey)
    BanHotKey_CKButton.grid(row=3,column=0,sticky="W",pady=2)
    # HideWin.set(True) == HideWin.set(1)
    getOtherSetting()
    Win.bind_all("<<ComboboxSelected>>",saveSetting)
    for i in Page2.winfo_children():
        i.config(command=saveSetting)
    Win.after(1000,GetWinHWND)
    tkinter.Label(Page2,text="目前的OCR快捷键为：").grid(row=4,column=0,sticky="W",pady=5)
    tkinter.Label(Page2,text="目前的Galgame快捷键为：").grid(row=5,column=0,sticky="W")
    ttk.Entry(Page2, state="readonly",textvariable=OCREntry).grid(row=4, column=1,sticky="W")
    ttk.Entry(Page2, state="readonly",textvariable=GALEntry).grid(row=5, column=1,sticky="W")
    tkinter.Label(Page2,text="*请到Setting.json配置文件中(Ctrl+O)修改快捷键").grid(row=6,columnspan=3,pady=10,sticky="W")
    tkinter.Label(Page2,text="*若发现按下快捷键后没有出现截图的情况则是快捷键冲突的情况，请更改快捷键").grid(row=7,columnspan=3,sticky="W")
    Win.mainloop()

except SystemExit as e: #不捕获系统退出异常
    pass

except:
    messagebox.showerror("啊噢，出现异常了(´･_･`)","执行错误，错误信息为：\n"+traceback.format_exc())