from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup,InlineKeyboardButton,InlineQuery,InlineQueryResultArticle,InputTextMessageContent

from yt_dlp import YoutubeDL
from youtube_search import YoutubeSearch

import os, wget


app = Client("YouTube-Robot", bot_token = "5534809845:AAGh4hxEiCW5PPhWLLHW9blWiGXWnWcpHdA", api_id = 21871538, api_hash = "da886aa415f35a1c679744d3b24ac79e")
programmer_id = '5719372657'

start_message = """
👋🏻 مرحبـاً {}

🌐 أنا بـوت تحميـل من اليوتيـوب بأعلـى دقـة

⚡️** لتحميـل فيديــو / صـوت **
 ┤ أرسـل رابـط الفيديـو
 ╯ أختـر صيغـة التحميـل " صـوت / فيديـو "

🔎** للبحـث عـن فيديـو وجلـب نتائـج محدوده **
 ┤ اكتـب "`بحث + النـص`"
 ╯ انسـخ الرابـط و ارسلـه هنـا لتحميلـه أو في اي محادثـة البوت مشرفـاً فيهـا

🔎** للبحـث عـن فيديـو وجلـب نتائـج متعددة **
 ┤ اكتـب "@YTXIBOT + النـص "
 ╯ إضغـط فـوق النتيجـه التـي تريدهـا

--🗒 البـوت يعمـل في المجموعـات بـدون مشاكـل ، يجـب أن يكـون البـوت مشرفاً و يمكـن لأي عضـو استخدامـه--
"""

first_loading_message = "⚡"
last_loading_message = "** ⚡️ جـار تنفيـذ طلبـك ، انتظـر قليـلاً... **"
uploading_video_message = "** ⏳ جـار التحضيـر لإرسـال الفيديـو ، انتظـر قليـلاً... **"
uploading_audio_message = "** ⏳ جـار التحضيـر لإرسـال الصـوت ، انتظـر قليـلاً... **"
done_message = """
**👤 المستخـدم : **{}**

🔗 الرابـط : **`{}`
"""


@app.on_message(filters.command("start"))
async def start(client, message):
  await message.reply_text(
    start_message.format(message.from_user.mention),
    reply_markup = InlineKeyboardMarkup(
      [
        [
          InlineKeyboardButton(" ➕ أضـف البـوت إلـي مجموعتـك ➕ ", url = f"https://t.me/YTXIBOT?startgroup=true"),
        ],
        [
          InlineKeyboardButton(" قناة التحديثات 🛠 ", url = f"https://t.me/TD_T1"),
          InlineKeyboardButton(" المطـور 👨‍💻 ", url = f"https://t.me/a7mednegm"),
        ],
        [
          InlineKeyboardButton(" استخدام الـ Inline 👾 ", switch_inline_query_current_chat = f""),
        ]
      ]
    )
  )


@app.on_message(filters.regex(r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$"))
async def ytdl(client, message):
  await message.reply_text(
    f"🎬  : {message.text}",
    disable_web_page_preview = True,
    reply_markup = InlineKeyboardMarkup(
      [
        [
          InlineKeyboardButton("🎧 مقطع صوتي .", callback_data="audio"),
          InlineKeyboardButton("🎬 مقطع فيديو .", callback_data="video"),
        ]
      ]
    )
  )

@app.on_callback_query(filters.regex("video"))
async def VideoDownLoad(client, callback_query):
  await callback_query.edit_message_text(first_loading_message)
  try:
    url = callback_query.message.text.split(' : ',1)[1]
    with YoutubeDL(video) as ytdl:
      await callback_query.edit_message_text(last_loading_message)
      ytdl_data = ytdl.extract_info(url, download = True)
      video_file = ytdl.prepare_filename(ytdl_data)
  except Exception as e:
    await client.send_message(chat_id = programmer_id,text = e)
    return await callback_query.edit_message_text(e)
  await callback_query.edit_message_text(uploading_video_message)
  await client.send_video(
    callback_query.message.chat.id,
    video = video_file,
    duration = int(ytdl_data["duration"]),
    file_name = str(ytdl_data["title"]),
    supports_streaming = True,
    caption = f"[{ytdl_data['title']}]({url})"
  )
  await callback_query.edit_message_text(done_message.format(callback_query.from_user.mention, url))
  os.remove(video_file) 


@app.on_callback_query(filters.regex("audio"))
async def AudioDownLoad(client, callback_query):
  await callback_query.edit_message_text(first_loading_message)
  try:
    url = callback_query.message.text.split(' : ',1)[1]
    with YoutubeDL(audio) as ytdl:
      await callback_query.edit_message_text(last_loading_message)
      ytdl_data = ytdl.extract_info(url, download = True)
      audio_file = ytdl.prepare_filename(ytdl_data)
      thumb = wget.download(f"https://img.youtube.com/vi/{ytdl_data['id']}/hqdefault.jpg")
  except Exception as e:
    await client.send_message(chat_id = programmer_id,text = e)
    return await callback_query.edit_message_text(e)
  await callback_query.edit_message_text(uploading_audio_message)
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
  await callback_query.edit_message_text(done_message.format(callback_query.from_user.mention, url))
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
      await m.edit(text, reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("قناة التحديثات 🛠", url="https://t.me/TD_T1")]]), disable_web_page_preview = True)
  except Exception as e:
    await m.edit(str(e)) 


@app.on_inline_query()
async def inline(client, query: InlineQuery):
  answers = []
  search_query = query.query.lower().strip().rstrip()

  if search_query == "":
    await client.answer_inline_query(
      query.id,
      results = answers,
      switch_pm_text="✅ اكتـب عنـوان فيديـو اليوتيـوب",
      switch_pm_parameter="start",
      cache_time = 0,
    )
  else:
    results = YoutubeSearch(search_query).to_dict()
    for result in results:
      answers.append(
        InlineQueryResultArticle(
          title = result["title"],
          description = "المـده : {} • المشاهـدات {}".format(
          result["duration"], result["views"]
        ),
        input_message_content = InputTextMessageContent(
          "https://www.youtube.com/watch?v={}".format(result["id"])
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
