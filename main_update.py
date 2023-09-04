from aiogram import Bot, Dispatcher, types, executor
from config import token
import os, time, logging, requests, random

bot = Bot(token=token)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}!")

@dp.message_handler()
async def download_send_video(message: types.Message):
    try:
        get_id_video = message.text.split('?')
        current_id = get_id_video[0].split('/')[5]

        video_api = requests.get(f'https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/feed/?aweme_id={current_id}').json()

        video_info = video_api.get('aweme_list')[0]
        author_video = video_info.get('author').get('nickname')
        id_video = video_info.get('statistics').get('aweme_id')
        comment_video = video_info.get('statistics').get('comment_count')
        digg_count = video_info.get('statistics').get('digg_count')
        download_count = video_info.get('statistics').get('download_count')
        play_count = video_info.get('statistics').get('play_count')
        share_count = video_info.get('statistics').get('share_count')

        await message.answer(f"Имя автора: {author_video}")
        await message.answer(f"id видео: {id_video}")
        await message.answer(f"Количество комментариев в видео: {comment_video}")

        video_url = video_info.get('video').get('play_addr').get('url_list')[0]

        if video_url:
            title_video = video_info.get('desc') or f"video_{random.randint(1111, 22222)}"
            video_response = requests.get(video_url)

            if video_response.status_code == 200:
                video_file_path = f'video/{title_video}.mp4'
                with open(video_file_path, 'wb') as video_file:
                    video_file.write(video_response.content)

                await message.answer("Видео успешно скачано, отправляю...")
                
                with open(video_file_path, 'rb') as send_file:
                    await message.answer_video(send_file)
            else:
                await message.answer("Ошибка при скачивании видео.")
        else:
            await message.answer("Не удалось получить URL видео.")
    except Exception as error:
        await message.answer(f"Произошла ошибка: {error}")

executor.start_polling(dp, skip_updates=True)
