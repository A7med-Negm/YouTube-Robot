from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup,InlineKeyboardButton,InlineQuery,InlineQueryResultArticle,InputTextMessageContent

from yt_dlp import YoutubeDL
from youtube_search import YoutubeSearch

import os, wget


app = Client("YouTube-Robot", bot_token = "5534809845:AAFDpUHI4lLHvGV84phAWbhYe6f0VynPC1M", api_id = 21871538, api_hash = "da886aa415f35a1c679744d3b24ac79e")
programmer_id = '5719372657'

start_message = """
๐๐ป ูุฑุญุจูุงู {}

๐ ุฃูุง ุจููุช ุชุญูููู ูู ุงูููุชูููุจ ุจุฃุนููู ุฏููุฉ

โก๏ธ** ูุชุญูููู ููุฏูููู / ุตููุช **
 โค ุฃุฑุณูู ุฑุงุจูุท ุงูููุฏููู
 โฏ ุฃุฎุชูุฑ ุตูุบูุฉ ุงูุชุญูููู " ุตููุช / ููุฏููู "

๐** ููุจุญูุซ ุนูู ููุฏููู ูุฌููุจ ูุชุงุฆูุฌ ูุญุฏูุฏู **
 โค ุงูุชูุจ "`ุจุญุซ + ุงูููุต`"
 โฏ ุงูุณูุฎ ุงูุฑุงุจูุท ู ุงุฑุณููู ูููุง ูุชุญููููู ุฃู ูู ุงู ูุญุงุฏุซูุฉ ุงูุจูุช ูุดุฑููุงู ููููุง

๐** ููุจุญูุซ ุนูู ููุฏููู ูุฌููุจ ูุชุงุฆูุฌ ูุชุนุฏุฏุฉ **
 โค ุงูุชูุจ "@YTXIBOT + ุงูููุตย "
 โฏ ุฅุถุบูุท ูููู ุงููุชูุฌูู ุงูุชูู ุชุฑูุฏููุง

--๐ ุงูุจููุช ูุนููู ูู ุงููุฌููุนูุงุช ุจูุฏูู ูุดุงููู ุ ูุฌูุจ ุฃู ููููู ุงูุจููุช ูุดุฑูุงู ู ููููู ูุฃู ุนุถูู ุงุณุชุฎุฏุงููู--
"""

first_loading_message = "โก"
last_loading_message = "** โก๏ธ ุฌูุงุฑ ุชููููุฐ ุทูุจูู ุ ุงูุชุธูุฑ ูููููุงู... **"
uploading_video_message = "** โณ ุฌูุงุฑ ุงูุชุญุถููุฑ ูุฅุฑุณูุงู ุงูููุฏููู ุ ุงูุชุธูุฑ ูููููุงู... **"
uploading_audio_message = "** โณ ุฌูุงุฑ ุงูุชุญุถููุฑ ูุฅุฑุณูุงู ุงูุตููุช ุ ุงูุชุธูุฑ ูููููุงู... **"
done_message = """
**๐ค ุงููุณุชุฎูุฏู : **{}**

๐ ุงูุฑุงุจูุท : **`{}`
"""


@app.on_message(filters.command("start"))
async def start(client, message):
  await message.reply_text(
    start_message.format(message.from_user.mention),
    reply_markup = InlineKeyboardMarkup(
      [
        [
          InlineKeyboardButton(" โ ุฃุถูู ุงูุจููุช ุฅููู ูุฌููุนุชูู โ ", url = f"https://t.me/YTXIBOT?startgroup=true"),
        ],
        [
          InlineKeyboardButton(" ููุงุฉ ุงูุชุญุฏูุซุงุช ๐  ", url = f"https://t.me/TD_T1"),
          InlineKeyboardButton(" ุงููุทููุฑ ๐จโ๐ป ", url = f"https://t.me/a7mednegm"),
        ],
        [
          InlineKeyboardButton(" ุงุณุชุฎุฏุงู ุงูู Inline ๐พ ", switch_inline_query_current_chat = f""),
        ]
      ]
    )
  )


@app.on_message(filters.regex(r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$"))
async def ytdl(client, message):
  await message.reply_text(
    f"๐ฌ  : {message.text}",
    disable_web_page_preview = True,
    reply_markup = InlineKeyboardMarkup(
      [
        [
          InlineKeyboardButton("๐ง ููุทุน ุตูุชู .", callback_data="audio"),
          InlineKeyboardButton("๐ฌ ููุทุน ููุฏูู .", callback_data="video"),
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


@app.on_message(filters.command("ุจุญุซ",None))
async def search(client, message):
  try:
    query = message.text.split(None, 1)[1]
    if not query:
      await message.reply_text("** ุงุณุชุฎุฏู ุงูุงูุฑ ููุฐุง ( ุจุญุซ + ุงููููู ) **")
      return

    m = await message.reply_text("** ูุชู ุงูุจุญุซ ุงูุชุถุฑ ููููุง ... **")
    results = YoutubeSearch(query, max_results = 5).to_dict()
    i = 0
    text = ""
    while i < 5:
      text += f"**๐ค ุงูุนููุงู :** `{results[i]['title']}`\n"
      text += f"**๐ ุงููุฏูโ :** `{results[i]['duration']}`\n"
      text += f"**๐ ุนุฏุฏ ุงููุดุงูุฏุงุช :** `{results[i]['views']}`\n"
      text += f"**๐ ุงููุตุฏุฑ : {results[i]['channel']}**\n"
      text += f"**๐ ุงูุฑุงุจุท :** `https://www.youtube.com{results[i]['url_suffix']}`\n\n"
      text += f"          โโโโโโ ๐ โโโโโโ\n\n"
      i += 1
      await m.edit(text, reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("ููุงุฉ ุงูุชุญุฏูุซุงุช ๐ ", url="https://t.me/TD_T1")]]), disable_web_page_preview = True)
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
      switch_pm_text="โ ุงูุชูุจ ุนูููุงู ููุฏููู ุงูููุชูููุจ",
      switch_pm_parameter="start",
      cache_time = 0,
    )
  else:
    results = YoutubeSearch(search_query).to_dict()
    for result in results:
      answers.append(
        InlineQueryResultArticle(
          title = result["title"],
          description = "ุงูููุฏู : {} โข ุงููุดุงููุฏุงุช {}".format(
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
          switch_pm_text="ุญุฏุซ ุฎุทุฃ !",
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
