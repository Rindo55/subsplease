import asyncio
from main.modules.schedule import update_schedule
from main.modules.usschedule import update_schedulex
from main.modules.utils import status_text
from main import status
from main.modules.db import get_animesdb, get_uploads, save_animedb
import feedparser
from main import queue
from main.inline import button1

def trim_title(title: str):
    title = title.rsplit(' ', 1)[0]
    title = title.replace("[SubsPlease] ", "")
    title = title.replace("Dr. Stone - New World", "Dr Stone New World")
    title = title.replace("Opus.COLORs", "Opus COLORs")
    title = title.replace("Ousama Ranking - Yuuki no Takarabako", "Ousama Ranking Yuuki no Takarabako")
    ext = ".mkv"
    title = title + ext
    return title

def parse():
    a = feedparser.parse("https://nyaa.si/?page=rss&u=subsplease&q=1080p")
    b = a["entries"]
    b = b[0:2]
    data = []    

    for i in b:
        item = {}
        item['title'] = trim_title(i['title'])        
        item['size'] = i['nyaa_size']   
        item['link'] = "magnet:?xt=urn:btih:" + i['nyaa_infohash']
        data.append(item)
    data.reverse()
    return data

async def auto_parser():
    while True:
        try:
            await status.edit(await status_text("Parsing Rss, Fetching Magnet Links..."),reply_markup=button1)
        except:
            pass

        rss = parse()
        data = await get_animesdb()
        uploaded = await get_uploads()

        saved_anime = []
        for i in data:
            saved_anime.append(i["name"])

        uanimes = []
        for i in uploaded:
            uanimes.append(i["name"])
        
        for i in rss:
            if i["title"] not in uanimes and i["title"] not in saved_anime:
                if ".mkv" in i["title"] or ".mp4" in i["title"]:
                    title = i["title"]
                    await save_animedb(title,i)

        data = await get_animesdb()
        for i in data:
            if i["data"] not in queue:
                queue.append(i["data"])    
                print("Saved ", i["name"])   

        try:
            await status.edit(await status_text("Idle..."),reply_markup=button1)
            await update_schedule()
            await asyncio.sleep(6)
            await update_schedulex()
        except:
            pass

        await asyncio.sleep(30)
