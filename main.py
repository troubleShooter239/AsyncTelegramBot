from aiogram import Bot, types, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from additional_functions import get_joke, get_weather, get_news, get_compliment, get_insult, answers
from random import choice
from asyncio import sleep
import string


def telegram_bot():
    bot_token = ''  # Ваш токен бота
    weather_token = ''  # Токен openweather

    if not bot_token and not weather_token:
        print("Вы не ввели токены!")
        return 0

    bot = Bot(bot_token)
    dp = Dispatcher(bot, MemoryStorage())

    @dp.message_handler(commands=['start'])
    async def send_welcome(msg: types.Message):
        await msg.answer(f'Привет, {msg.from_user.username}!')

    @dp.message_handler(commands=['help'])
    async def send_help(msg: types.Message):
        await msg.answer(
            'Бот умеет отправлять:\n'
            '1. Рандомный анекдот.\n'
            '2. Свежие новости IT.\n'
            '3. Сводку погоды для запрошенного города.\n'
            '4. Картинку с текстом пользователя.\n'
            '5. Рандомный комплимент для девушки.\n'
            'Бот умеет вести "общение".\n'
            'Так же бот умеет играть в кубик.\n'
        )

    @dp.message_handler(commands=['dice'])
    async def play_dice(msg: types.Message):
        await msg.answer('Мой кубик: ')
        bot_dice = (await msg.answer_dice())['dice']['value']
        await msg.answer('Ваш кубик: ')
        user_dice = (await msg.answer_dice())['dice']['value']
        await sleep(5)
        
        if user_dice > bot_dice:
            await msg.answer('Вы победили!🥳')
        elif user_dice < bot_dice:
            await msg.answer('Вы проиграли!😛')
        else:
            await msg.answer('Ничья!😊')

    @dp.message_handler(commands=['joke'])
    async def send_joke(msg: types.Message):
        await msg.answer(get_joke() + '\n😆🤣😂\n#Шутка_юмора')

    @dp.message_handler(commands=['news'])
    async def send_joke(msg: types.Message):
        await msg.answer(get_news() + '\n#Новости')

    @dp.message_handler(commands=['weather'])
    async def send_weather(msg: types.Message):
        try:
            user_input = msg.text.split(' ', 1)[1]
            await msg.answer(get_weather(user_input, weather_token) + '\n#Погода')
        except:
            await msg.answer("Вы не ввели название города!" + '\n#Погода')

    @dp.message_handler(commands=['compliment'])
    async def send_compliment(msg: types.Message):
        await msg.answer(get_compliment() + '\n😍🥰😘\n#Комплимент_девушке')

    @dp.message_handler(content_types=['text'])
    async def get_text_messages(msg: types.Message):
        if msg.get_command() is None:
            exclude = set(string.punctuation + string.digits)
            # Фильтрация строки от мусора
            text_msg = ''.join(ch for ch in msg.text.lower() if ch not in exclude)

            if text_msg in answers.keys():
                await msg.answer(choice(answers[text_msg]))
            else:
                await msg.answer(get_insult())

    executor.start_polling(dp)


if __name__ == '__main__':
    telegram_bot()
