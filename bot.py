from telethon import TelegramClient
import json
import datetime
import os

conf_template = {
    "api_id": "",
    "api_hash": "",
    "proxy": {
        "socks5": "",
        "socks4": "",
        "http": ""
    },
    "channels":
    {
    }
}

log_template = {
    "year": "",
    "month": "",
    "day": "",
    "updated": []
}

if not os.path.exists(f"./conf.json"):
    with open("./conf.json", "w+") as f:
        json.dump(conf_template, fp=f, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)
        
    with open("./log.json", "w+") as f:
        json.dump(log_template, fp=f, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)
    
    print("[+] 请填写基本信息后启动")
    exit()

with open(f"conf.json", 'rb') as f:
    conf = json.load(f)
api_id = int(conf["api_id"])
api_hash = conf["api_hash"]

client = None
for i in conf['proxy']:
    if conf['proxy'][i] != '':
        url = conf['proxy'][i].split(":")
        client = TelegramClient('anon', api_id, api_hash, proxy=(i, url[0], int(url[1])))
        break

if client == None:
    client = TelegramClient('anon', api_id, api_hash)



async def init(channel_id:int):
    
    tmp = {}

    async for message in client.iter_messages(channel_id, reverse=True):
        # print(message.id, message.text, message.date)
        msdate = message.date
        # print(msdate.year)
        if msdate.year not in tmp.keys():
            tmp[msdate.year] = {}
            
        if msdate.month not in tmp[msdate.year].keys():
            tmp[msdate.year][msdate.month] = {}
            
        if msdate.day not in tmp[msdate.year][msdate.month].keys():
            tmp[msdate.year][msdate.month][msdate.day] = []

        tmp[msdate.year][msdate.month][msdate.day].append(message.id)

    with open(f"./data/channel{channel_id}.json", 'w+') as f:
        json.dump(tmp, fp=f, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)

async def update_yesterday(channel_id:int):
    currdate = datetime.datetime.now()
    yestdate = currdate - datetime.timedelta(days=1)
    with open(f"./data/channel{channel_id}.json", 'r') as f:
        tmpconf  = json.load(f)

    yestlist = []
    currlist = []
    async for message in client.iter_messages(channel_id):
        if message.date.year >= yestdate.year:
            if message.date.month >= yestdate.month:
                if message.date.day > yestdate.day:
                    currlist.append(message.id)
                    continue
                if message.date.day == yestdate.day:
                    yestlist.append(message.id)
                    continue
                
        break
    
    currlist = sorted(currlist)
    yestlist = sorted(yestlist)

    tmpconf[str(currdate.year)][str(currdate.month)][str(currdate.day)] = currlist
    tmpconf[str(yestdate.year)][str(yestdate.month)][str(yestdate.day)] = yestlist
    with open(f"./data/channel{channel_id}.json", 'w+') as f:
        json.dump(tmpconf, fp=f, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)

async def forward(message, forward_user:list):
    
    if message.noforwards == False:
        for i in forward_user:
            await message.forward_to(int(i))

async def forward_channel(channel, currdate):
    now_year = str(currdate.year)
    now_month = str(currdate.month)
    now_day = str(currdate.day)

    with open(f"./data/channel{channel}.json", 'rb') as f:
        channel_log = json.load(f)
    
    for eachyear in channel_log.keys():
        eachyear_log = channel_log[eachyear]

        if now_year == eachyear: # Remove todays
            continue

        if now_month not in eachyear_log.keys(): # empty check
            continue

        if now_day not in eachyear_log[now_month].keys(): # empty check
            continue
        
        for i in conf['channels'][channel]: # 年份提醒
            await client.send_message(int(i), f"{eachyear} 年的 {now_month}/{now_day}")

        for msgid in eachyear_log[now_month][now_day]:
            async for message in client.iter_messages(int(channel), ids=msgid):
                await forward(message, conf['channels'][channel])

async def check():
    currdate = datetime.datetime.now()

    now_year = str(currdate.year)
    now_month = str(currdate.month)
    now_day = str(currdate.day)
    channels = conf['channels'].keys()

    with open("./log.json", "r") as f:
        log = json.load(f)
    
    rmlist = []
    if now_year == log['year']:
        if now_month == log['month']:
            if now_day == log['day']:
                rmlist = log['updated']
    
    updated = rmlist
    for channel in channels:
        if channel in rmlist:
            continue
        await forward_channel(channel, currdate)
        updated.append(channel)
    
    log['year'] = now_year
    log['month'] = now_month
    log['day'] = now_day
    log['updated'] = updated
    
    with open("./log.json", "w+") as f:
        log = json.dump(log, fp=f)

async def check_channels():
    channels = conf['channels'].keys()
    for i in channels:
        if os.path.exists(f"./data/channel{i}.json"):
           await update_yesterday(int(i))
           continue
        print(f"[+] 检测到新频道: {i}\n[+] 正在更新")
        await init(int(i))


async def main():
    print("[+] 更新频道 ID 中")
    with open("channels.log", 'w+', encoding='utf-8') as f:
        async for dialog in client.iter_dialogs():
            print(dialog.name, ': ', dialog.id, file=f)

    print("[+] 检查频道更新")
    await check_channels()
    
    print("[+] 发送频道更新")
    await check()


with client:
    client.loop.run_until_complete(main())
