

## P I P 

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup,InlineKeyboardButton,InlineQuery,InlineQueryResultArticle,InputTextMessageContent

from yt_dlp import YoutubeDL
from youtube_search import YoutubeSearch

import os, wget

## A P P 

api_id = int(os.environ.get("APP_ID"))
api_hash = os.environ.get("API_HASH")
token = os.environ.get("TOKEN")


app = Client("YouTube-Robot", bot_token = token, api_id = api_id, api_hash = api_hash)
programmer_id = '5495221292'

## T E X T S

texts = {
    "start": "**➖➖➖➖➖➖➖➖➖➖➖➖\n\n👋 مرحبا {} ! \n\nℹ️ أنا {} \n\n❇️ يمكنني التنزيل من الـ YouTube بصيغ متعددة و طرق سريعـة \n\n🛄 إضغـط علي "الأوامر" و اتبع الخطـوات \n\n✅ لكي تكون قادرًا على استخدامي ، يجب أن تكون مشتركًا في قناة التحديثات \n\n➖➖➖➖➖➖➖➖➖➖➖➖➖**",
    "first_loading": "⚡",
    "last_loading": "**💡 يرجى الانتظار ، جاري معالجة طلبك ... **",
    "uploading": "** 🚀 جار الرفع علي خوادم التيليجرام ... **",
    "done": "=*", 
}

## S T A R T

@app.on_message(filters.command("start"))
async def start(client, message):
   await message.reply_text(
      texts["start"].format(message.from_user.mention),
      reply_markup = InlineKeyboardMarkup(
         [
            [
               InlineKeyboardButton(" قناة التحديثات 🛠 ", url = f"https://t.me/XT_T1"),
               InlineKeyboardButton(" المـطـور 🥷 ", url = f"https://t.me/A7medNegm"),
            ],
            [
               InlineKeyboardButton("  استخدام الـ Inline 👾 ", switch_inline_query = f""),
            ]
         ]
      )
   )


## V I D E O   O R   A U D I O 


@app.on_message(filters.regex(r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$"))
async def ytdl(client, message):
   await message.reply_text(
      f"🎬  : {message.text}",disable_web_page_preview = True,
      reply_markup = InlineKeyboardMarkup(
         [
            [
               InlineKeyboardButton("🎧 مقطع صوتي .", callback_data="audio"),
               InlineKeyboardButton("🎬 مقطع فيديو .", callback_data="video"),
            ]
         ]
      )
   )


## V I D E O 


@app.on_callback_query(filters.regex("video"))
async def VideoDownLoad(client, callback_query):
   await callback_query.edit_message_text(texts["first_loading"])
   try:
      url = callback_query.message.text.split(' : ',1)[1]
      with YoutubeDL(video) as ytdl:
         await callback_query.edit_message_text(texts["last_loading"])
         ytdl_data = ytdl.extract_info(url, download = True)
         video_file = ytdl.prepare_filename(ytdl_data)
   except Exception as e:
      await client.send_message(chat_id = programmer_id,text = e)
      return await callback_query.edit_message_text(e)
   await callback_query.edit_message_text(texts["uploading"])
   await client.send_video(
            callback_query.message.chat.id,
            video = video_file,
            duration = int(ytdl_data["duration"]),
            file_name = str(ytdl_data["title"]),
            supports_streaming = True,
            caption = f"[{ytdl_data['title']}]({url})"
        )
   await callback_query.edit_message_text(texts["done"])
   os.remove(video_file)


## A U D I O 


@app.on_callback_query(filters.regex("audio"))
async def AudioDownLoad(client, callback_query):
   await callback_query.edit_message_text(texts["first_loading"])
   try:
      url = callback_query.message.text.split(' : ',1)[1]
      with YoutubeDL(audio) as ytdl:
         await callback_query.edit_message_text(texts["last_loading"])
         ytdl_data = ytdl.extract_info(url, download = True)
         audio_file = ytdl.prepare_filename(ytdl_data)
         thumb = wget.download(f"https://img.youtube.com/vi/{ytdl_data['id']}/hqdefault.jpg")
   except Exception as e:
      await client.send_message(chat_id = programmer_id,text = e)
      return await callback_query.edit_message_text(e)
   await callback_query.edit_message_text(texts["uploading"])
   await client.send_audio(
      callback_query.message.chat.id,
      audio = audio_file,
      duration = int(ytdl_data["duration"]),
      title = str(ytdl_data["title"]),
      performer = str(ytdl_data["uploader"]),
      file_name = str(ytdl_data["title"]),
      thumb = thumb,
      caption = f"[{ytdl_data['title']}]({url})"
   )
   await callback_query.edit_message_text(texts["done"])
   os.remove(audio_file)
   os.remove(thumb)


## S E A R C H 


@app.on_message(filters.command("بحث",None))
async def search(client, message):
    try:
        query = message.text.split(None, 1)[1]
        if not query:
            await message.reply_text("** استخدم الامر هكذا ( بحث + الكلمه ) **")
            return

        m = await message.reply_text("** يتم البحث انتضر قليلا ... **")
        results = YoutubeSearch(query, max_results = 5).to_dict()
        i = 0
        text = ""
        while i < 5:
            text += f"**👤 العنوان :** `{results[i]['title']}`\n"
            text += f"**🕑 المده‍ :** `{results[i]['duration']}`\n"
            text += f"**👁 عدد المشاهدات :** `{results[i]['views']}`\n"
            text += f"**🌐 المصدر : {results[i]['channel']}**\n"
            text += f"**🔗 الرابط :** `https://www.youtube.com{results[i]['url_suffix']}`\n\n"
            text += f"          ➖➖➖➖➖➖ 🆕 ➖➖➖➖➖➖\n\n"
            i += 1
        await m.edit(text, reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Ahmed Negm ⁞ Bots Service", url="https://t.me/XT_T1")]]), disable_web_page_preview = True)
    except Exception as e:
        await m.edit(str(e))


## I N L I N E 


@app.on_inline_query()
async def inline(client, query: InlineQuery):
    answers = []
    search_query = query.query.lower().strip().rstrip()

    if search_query == "":
        await client.answer_inline_query(
            query.id,
            results = answers,
            switch_pm_text="💡 اكتب اسم الفيديو المطلوب للبحث عنه ",
            switch_pm_parameter="help",
            cache_time = 0,
        )
    else:
        results = YoutubeSearch(search_query).to_dict()
        for result in results:
         answers.append(
               InlineQueryResultArticle(
                  title = result["title"],
                  description="{}, {} مشاهدة".format(
                     result["duration"], result["views"]
                  ),
                  input_message_content = InputTextMessageContent(
                     "🔗 https://www.youtube.com/watch?v={}".format(result["id"])
                  ),
                  thumb_url = result["thumbnails"][0],
               )
         )
        
        try:
            await query.answer(results = answers, cache_time = 0)
        except errors.QueryIdInvalid:
            await query.answer(
                results = answers,
                cache_time = 0,
                switch_pm_text="حدث خطأ !",
                switch_pm_parameter="",
            )
            
video = {"format": "best","keepvideo": True,"prefer_ffmpeg": False,"geo_bypass": True,"outtmpl": "%(title)s.%(ext)s","quite": True}
audio = {"format": "bestaudio","keepvideo": False,"prefer_ffmpeg": False,"geo_bypass": True,"outtmpl": "%(title)s.mp3","quite": True}


@app.on_message(filters.private)
async def developer(client, message):
   if str(message.from_user.id) == str(programmer_id):
      pass
   else :
      await client.forward_messages(
         chat_id = programmer_id,
         from_chat_id = message.chat.id,
         message_ids = message.id
      )

print("The Bot Was Already Started")
app.run()
