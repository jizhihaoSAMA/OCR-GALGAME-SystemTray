# OCR-translation-systemIcon

一个用来OCR，翻译galgame的工具
A tool which is used to OCR, translate galgame to Chinese.

所用技术（python）：
tkinter+tk拓展winico+百度api接口OCR+requests爬虫百度翻译

#### 识别图片中的文字？
#### Do you want to recognize the words in the picture?

#### 想啃生肉？懒得配置VNR？
#### Do you want to play galgame without translation when you don't study Japanese?Don't want to configure VNR?(~~Are you pig?~~) ?

这个工具用的百度接口OCR，识别率对比国内其他OCR还是挺高的，每天免费使用3w次，够用了（本来准备用tesserocr识别的，但不是每个人都有这玩意而且训练也很麻烦））
翻译直接爬的百度翻译，对比过google翻译，必应翻译，有道翻译，百度翻译略微比其他三个准确。

**高准度模式仅仅支持中+英，日常galgame使用普通模式足以**

**本来不想设置GALGAME的默认语言的，百度翻译必须要带参数了**

## 优点：

·支持系统托盘

·支持开机启动

·支持快捷键，快捷键Ctrl+F1直接OCR，Ctrl+F2 直接galgame模式

·galgame模式会记录鼠标记录，保持持续翻译该窗口

·局部持续翻译（专为翻译galgame制作的）<br>


## 已知缺陷：

1. ~~不支持修改快捷键~~ 目前重写代码尝试支持快捷键
2. ~~目前仅支持百度翻译(tkinter学习不到位，有道翻译本来可以加入进去的)~~ 目前支持大部分平台的翻译
3. ~~galgame是翻译模式，但托盘中和快捷键模式只支持日译中~~ 目前设置了默认模式
4. 暂不支持图片自定义。？
5. ~~偶尔的开机暴死~~
6. 偶尔的识别失误(这个是OCR自己的问题了，不管关我的事)
7. 使用快捷键进行OCR如果取消导致无法再次使用快捷键
8. 继续捕捉窗口不在顶层
9. ~~tab键顺序就尼玛离谱~~ 重写代码解决
10. 剪贴板还原问题
11. 除主屏幕外，其他屏幕无法截屏，问题：grab的C代码出了问题
12. ~~百度翻译爬虫措施修改  ~~ ~~1.27日使用一次性cookie导致无法重复使用~~   1.31日恢复正常可正常使用百度翻译
13. 二次回到主页面无法修改配置文件
14. 后续考虑加入OCR统计次数

欢迎讨论以及共同修改，Q574106827
