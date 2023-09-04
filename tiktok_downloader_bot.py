
from aiogram import Bot, Dispatcher, types, executor
from config import token
import os, time, logging, requests, random


bot = Bot(token=token)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer(f"Привет {message.from_user.full_name}")

@dp.message_handler()
async def download_send_video(message: types.Message):
       
    get_id_video = message.text.split('?')
    
    current_id = get_id_video[0].split('/')[5]
    
    video_api = requests.get(f'https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/feed/?aweme_id={current_id}').json()

    id_video = video_api.get("aweme_list")[0].get('statistics').get('aweme_id')
    comment_video = video_api.get("aweme_list")[0].get('statistics').get('comment_count')
    digg_count = video_api.get("aweme_list")[0].get('statistics').get('digg_count')
    dowload_count = video_api.get("aweme_list")[0].get('statistics').get('download_count')
    play_count = video_api.get("aweme_list")[0].get('statistics').get('play_count')
    share_count = video_api.get("aweme_list")[0].get('statistics').get('share_count')

    await message.answer(f"Имя автора : {author_video}")
    await message.answer(f"id видео  : {id_video}")
    await message.answer(f"Количества коментариев в видео  : {comment_video}")
    await message.answer(f"id видео  : {id_video}")
    
    if video_url:
        title_video = video_api.get('aweme_list')[0].get('desc')

        if title_video != ' ':
            title_video = random.randint(1111, 22222)
        try:
            # Сохраняем видео в локальный файл.
            with open(f'video/{title_video}.mp4', 'wb') as video_file:
                video_file.write(requests.get(video_url).content)
            await message.answer("Видео успешно скачано, отправляю...")
        except Exception as error:
            print(f"Error: {error}")
        
        # Отправляем скачанное видео в Telegram.
        try:
            with open(f'video/{title_video}.mp4', 'rb') as send_file:
                await message.answer_video(send_file)
        except Exception as error:
            await message.answer(f"Ошибка: {error}")


executor.start_polling(dp, skip_updates=True)
