import asyncio
from main.modules.utils import format_text
import requests
import time
import os
from bs4 import BeautifulSoup
from datetime import datetime
from string import digits

ANIME_QUERY = """
query ($id: Int, $idMal:Int, $search: String) {
  Media (id: $id, idMal: $idMal, search: $search, type: ANIME) {
    id
    idMal
    title {
      romaji
      english
      native
    }
    format
    status
    episodes
    duration
    countryOfOrigin
    source (version: 2)
    trailer {
      id
      site
    }
    genres
    tags {
      name
    }
    studios {
    nodes {
        name
    }
    }
    averageScore
    relations {
      edges {
        node {
          title {
            romaji
            english
          }
          id
        }
        relationType
      }
    }
    nextAiringEpisode {
      timeUntilAiring
      episode
    }
    isAdult
    isFavourite
    mediaListEntry {
      status
      score
      id
    }
    siteUrl
  }
}
"""

ANIME_DB = {}

async def return_json_senpai(query: str, vars_: dict):
    url = "https://graphql.anilist.co"
    anime = vars_["search"]
    db = ANIME_DB.get(anime)

    if db:
      return db
    data = requests.post(url, json={"query": query, "variables": vars_}).json()
    ANIME_DB[anime] = data

    return data

temp = []

async def get_anime(vars_,less):
    if 1 == 1:
        result = await return_json_senpai(ANIME_QUERY, vars_)

        error = result.get("errors")
        if error:
            error_sts = error[0].get("message")
            print([f"[{error_sts}]"])
            print(vars_)
            data = temp[0]
            temp.pop(0) 
        else:
          data = result["data"]["Media"]   
          temp.append(data)
        idm = data.get("id")
        title = data.get("title")
        tit = title.get("english")
        if tit == None:
            tit = title.get("romaji")

        title_img = f"https://img.anili.st/media/{idm}"
        
        if less == True:
          return idm, title_img, tit

        return data

async def get_anime_img(query):
    vars_ = {"search": query}
    idm, title_img, title = await get_anime(vars_,less=True)

    #title = format_text(title)
    return idm, title_img, title
    
def get_anime_name(title):
    x = title.split(" - ")[-1]
    title = title.replace(x,"").strip()
    title = title[:-2].strip()

    x = title.split(" ")[-1].strip()
    if str(x[-1]) in digits and str(x[0]) == "S" and str(x[1]) in digits:
      if "S" in x:
        y = x.replace("S","S")
        title = title.replace(x,y)
    return title

atext = """
📺 **{}**
      **({})**
**━━━━━━━━━━━━━━━━━━━━━━**
▸ **Type**: {}
▸ **Source**: {}
▸ **Score**: 🌟{}
▸ **Episodes**: {}
▸ **Genre**: #{}
▸ **Status**: {}
▸ **Aired**: {}
▸ **Premiered**: {}
▸ **Licensors**: {}
▸ **Studio**: {}
▸ **Themes**: {}
▸ **Duration**: {} mins/Ep
▸ **Rating**: {}
▸ **Rank**: {} | **Popularity**: {}
"""

async def get_anilist_data(name):
    malurl = f"https://api.jikan.moe/v4/anime?q={name}"
    malresponse = requests.get(malurl)
    maldata = malresponse.json()
    vars_ = {"search": name}
    data = await get_anime(vars_,less=False)
    id_ = data.get("id")
    title = data.get("title")
    form = data.get("format")
    source = data.get("source")
    status = data.get("status")
    episodes = data.get("episodes")
    duration = data.get("duration")
    trailer = data.get("trailer")
    genres = data.get("genres")
    averageScore = data.get("averageScore")
    img = f"https://img.anili.st/media/{id_}"

    # title
    title1 = title.get("english")
    title2 = title.get("romaji")

    if title2 == None:
      title2 = title.get("native")

    if title1 == None:
      title1 = title2   

    # genre

    genre = ""

    for i in genres:
      genre += i + ", #"

    genre = genre[:-3]
    genre = genre.replace("#Slice of Life", "#Slice_of_Life")
    genre = genre.replace("#Mahou Shoujo", "#Mahou_Shoujo")    
    genre = genre.replace("#Sci-Fi", "#SciFi")
    studiox = data['studios']['nodes'][0]['name']
    tags = []
    for i in data['tags']:
        tags.append(i["name"])
    tagsx = "#" + f"{', #'.join(tags)}"
    tagsx = tagsx.replace("#Age Gap", "#Age_Gap")
    tagsx = tagsx.replace("#Anti-hero", "#Antihero")
    tagsx = tagsx.replace("#Artificial Intelligence", "#Artificial_Intelligence")
    tagsx = tagsx.replace("#Augmented Reality", "#Augmented_Reality")
    tagsx = tagsx.replace("#Battle Royale", "#Battle_Royale")
    tagsx = tagsx.replace("#Body Horror", "#Body_Horror")
    tagsx = tagsx.replace("#Boys' Love", "#Boys_Love")
    tagsx = tagsx.replace("#Card Battle", "#Card_Battle")
    tagsx = tagsx.replace("#Coming of Age", "#Coming_of_Age")
    tagsx = tagsx.replace("#Cosmic Horror", "#Cosmic_Horror")
    tagsx = tagsx.replace("#Cute Boys Doing Cute Things", "#Cute_Boys_Doing_Cute_Things")
    tagsx = tagsx.replace("#Cute Girls Doing Cute Things", "#Cute_Girls_Doing_Cute_Things")
    tagsx = tagsx.replace("#Ensemble Cast", "#Ensemble_Cast")
    tagsx = tagsx.replace("#Fairy Tale", "#Fairy_Tale")
    tagsx = tagsx.replace("#Family Life", "#Family_Life")
    tagsx = tagsx.replace("#Female Harem", "#Female_Harem")
    tagsx = tagsx.replace("#Female Protagonist", "#Female_Protagonist")
    tagsx = tagsx.replace("#Full CGI", "#Full_CGI")
    tagsx = tagsx.replace("#Full Color", "#Full_Color")
    tagsx = tagsx.replace("#Found Family", "#Found_Family")
    tagsx = tagsx.replace("#Gender Bending", "#Gender_Bending")
    tagsx = tagsx.replace("#Ice Skating", "#Ice_Skating")
    tagsx = tagsx.replace("#Language Barrier", "#Language_Barrier")
    tagsx = tagsx.replace("#Lost Civilization", "#LostCivilization")
    tagsx = tagsx.replace("#Love Triangle", "#Love_Triangle")
    tagsx = tagsx.replace("#Male Protagonist", "#Male_Protagonist")
    tagsx = tagsx.replace("#Martial Arts", "#Martial_Arts")
    tagsx = tagsx.replace("#Memory Manipulation", "#Memory_Manipulation")
    tagsx = tagsx.replace("#Monster Boy", "#Monster_Boy")
    tagsx = tagsx.replace("#Monster Girl", "#Monster_Girl")
    tagsx = tagsx.replace("#Non-fiction", "#Nonfiction")
    tagsx = tagsx.replace("#Office Lady", "#Office_Lady")
    tagsx = tagsx.replace("#Ojou-sama", "#Ojousama")
    tagsx = tagsx.replace("#Otaku Culture", "#Otaku_Culture")
    tagsx = tagsx.replace("#Post-Apocalyptic", "#Post_Apocalyptic")
    tagsx = tagsx.replace("#Primarily Adult Cast", "#Primarily_Adult_Cast")
    tagsx = tagsx.replace("#Primarily Child Cast", "#Primarily_Child_Cast")
    tagsx = tagsx.replace("#Primarily Female Cast", "#Primarily_Female_Cast")
    tagsx = tagsx.replace("#Primarily Male Cast", "#Primarily_Male_Cast")
    tagsx = tagsx.replace("#Primarily Teen Cast", "#Primarily_Teen_Cast")
    tagsx = tagsx.replace("#School Club", "#School_Club")
    tagsx = tagsx.replace("#Real Robot", "#Real_Robot")
    tagsx = tagsx.replace("#Ero Guro", "#Ero_Guro")
    tagsx = tagsx.replace("#Software Development", "#Software_Development")
    tagsx = tagsx.replace("#Time Manipulation", "#Time_Manipulation")
    tagsx = tagsx.replace("#Surreal Comedy", "#Surreal_Comedy")
    tagsx = tagsx.replace("#Teens' Love", "#Teens_Love")
    tagsx = tagsx.replace("#Urban Fantasy", "#Urban_Fantasy")
    tagsx = tagsx.replace("#Super Power", "#Super_Power")
    tagsx = tagsx.replace("#Super Robot", "#Super_Robot")
    tagsx = tagsx.replace("#Video Games", "#Video Games")
    tagsx = tagsx.replace("#Virtual World", "#Virtual_World")
    tagsx = tagsx.replace("#Shrine Maiden", "#Shrine_Maiden")
    tagsx = tagsx.replace("#Lost Civilization", "#Lost_Civilization")
    tagsx = tagsx.replace("#Dissociative Identities", "#Dissociative_Identities")
    tagsx = tagsx.replace("#Achronological Order", "#Achronological Order")
    tagsx = tagsx.replace("#Time Skip", "#Time_Skip")
    tagsx = tagsx.replace("#Age Regression", "#Age_Regression")
    tagsx = tagsx.replace("#Human Pet", "#Human_Pet")
    tagsx = tagsx.replace("#Achronoligical Order", "#Achronoligical_Order")
    tagsx = tagsx.replace("#Family Life", "#Family_Life")
    tagsx = tagsx.replace("#Body Swapping", "#Body_Swapping")
    tagsx = tagsx.replace("#Large Breasts", "Large_Breasts")
    tagsx = tagsx.replace("#Classic Literature", "#Classic_Literature")
    tagsx = tagsx.replace("#Tanned Skin", "#Tanned_Skin")
    tagsx = tagsx.replace("#Video Games", "#Video_Games")
    if data and "data" in maldata and len(maldata["data"]) > 0:
      mal = maldata["data"][0]
      producer = []
      for i in mal['producers']:
        producer.append(i["name"])
      producer = ", ".join(producer)
      licensor = []
      for i in mal['licensors']:
        licensor.append(i["name"])
      licensor = ", ".join(licensor)
      theme = []
      for i in mal['themes']:
        theme.append(i["name"])
      theme = ", ".join(theme)
      season = f"{mal['season']} {mal['year']}"
      rating = mal['rating']
      aired = mal['aired']['string']
      malink = mal['url']
      malrank = mal['rank']
      malpopularity = mal['popularity']
      
      caption = atext.format(
      title1,
      title2,
      form,
      source,   
      averageScore,
      episodes,
      genre,
      status,
      aired,
      season,
      licensor,
      studiox,
      theme,
      duration,
      rating,
      malrank,
      malpopularity
    )

    if trailer != None:
      ytid = trailer.get("id")
      site = trailer.get("site")
    else:
      site = None

    if site == "youtube":
      caption += f"\n**▸ Links: [Trailer](https://www.youtube.com/watch?v={ytid}) | [AniList](https://anilist.co/anime/{id_}) | [MAL]({malink})\n ━━━━━━━━━━━━━━━━━━━━━━\n@Latest_ongoing_airing_anime**"
    else:
      caption += f"\n**▸ Links: [AniList](https://anilist.co/anime/{id_}) | [MAL]({malink})\n━━━━━━━━━━━━━━━━━━━━━━\n@Latest_ongoing_airing_anime**"

    return img, caption
