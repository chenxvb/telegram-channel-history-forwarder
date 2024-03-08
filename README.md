## telegram-channel-history-forwarder

### Introduction

该项目是基于 [Telethon](https://github.com/LonamiWebs/Telethon) 的 TG 机器人，通过爬取频道历史信息来得到每日推送，类似于 私人频道版 历史上的今天

本项目支持私人/公共频道的推送，但需要使用账号作为 user bot 

或者，你也可以联系作者使用做好的成品 bot

### Requirement

Just  `pip install -r requirement` 

### Getting Start

1. 运行 `git clone https://github.com/chenxvb/telegram-channel-history-forwarder.git`
2. 运行 `python3 bot.py` 以生成必要文件
3. 在生成的 `conf.json` 里填入自己用户的 api_id 和 api_hash，此处可以参考 [sign in](https://docs.telethon.dev/en/stable/basic/signing-in.html) 或着也可以参考以下步骤
   1. 访问 my.telegram.org
   2. 点击 *API Development tools*
   3. 点击 *Create new application*，并只需填入 *App title* 和 *Short name* 
      1. 注意！访问网站的 IP 地址需要和手机号码地址一致
   4. 得到 api_id 和 api_hash
4. （可选）需要代理的可以在 proxy 一栏里在相对于协议的地方写上你的代理地址 “your.proxy.ip.address:port”，若不需要请留空
5. 运行  `python3 bot.py` ，按照命令行提示填入手机号和后面接收到的验证码。收到后等频道 ID 更新完后 ctrl-c 关闭
6. 在 channels.log 确定你需要操作的频道 id 和转发接收者的 id
7. 在生成的 `conf.json` 里 “channels” 一栏按照 “操作频道 id” : ["接收者1 id", "接收者 2 id"] 的格式填入
   1. 例子：假设爬取转发的频道 id 为 “12345”，接收者 id 为 “67890”，那么填写方式为：“12345”: [“67890”]
8. 最后运行 `python3 bot.py` ，脚本会在运行时启动一次，后面一直等到次日 7：30 才会运行

