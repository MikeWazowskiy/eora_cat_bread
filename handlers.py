from main import bot, dp
from aiogram.types import Message
from aiogram import types
from aiogram.dispatcher import FSMContext
from states import UserState
from main import db
from image_recongition import image_recognize

from datetime import datetime

yes = ['да', 'конечно', 'ага', 'пожалуй']
no = ['нет', 'нет, конечно', 'ноуп', 'найн']

hello_message = '<b>Привет!</b>\nЯ помогу отличить кота от хлеба! Объект перед тобой квадратный?'
cat_message = 'Это кот, а не хлеб! Не ешь его!\nДля возвращения к началу диалога введите команду /start\n' \
              'Для анализа картинки введите команду /image'
bread_message = 'Это хлеб, а не кот! Ешь его!\nДля возвращения к началу диалога введите команду /start\n' \
                'Для анализа картинки введите команду /image'
error_message = 'Я не такой глупый, чтобы понять сообщение "ага", "найн" и другие, но не настолько ' \
                'умный чтобы понять ваше сообщение.\nНапишите ещё раз.'

@dp.message_handler(commands='start')
async def start(message: Message, state: FSMContext):
    if (not db.user_exists(message.from_user.id)):
        db.add_user(message.from_user.id)
    await message.answer(hello_message, parse_mode=types.ParseMode.HTML)
    db.add_message(message.from_user.id, message.chat.id, message.message_id, message.text, message.date)
    db.add_message(bot.id, message.chat.id, message.message_id + 1, hello_message,
                   datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    await state.set_state(UserState.square)

@dp.message_handler(commands='image')
async def image(message: Message, state:FSMContext):
    await message.answer('Отправь фотографию и я помогу определить кто на ней, кот или хлеб!', parse_mode=types.ParseMode.HTML)
    await state.set_state(UserState.image)

@dp.message_handler(state=UserState.image, content_types=['photo'])
async def recognize(message: Message, state: FSMContext):
    await message.photo[-1].download('images/image.jpg')
    if 'bread' in image_recognize('images/image.jpg'):
        db.update_bread(message.from_user.id)
        await message.answer(bread_message)
        await state.finish()
    elif 'cat' in image_recognize('images/image.jpg'):
        db.update_cat(message.from_user.id)
        await message.answer(cat_message)
        await state.finish()
    else:
        await message.answer('Не получилось определить объект на картинке!\n/start - начало диалога\n/image - анализ картинки')
        await state.finish()

@dp.message_handler(state=UserState.square)
async def square(message: Message, state: FSMContext):
    db.add_message(message.from_user.id, message.chat.id, message.message_id, message.text, message.date)
    if(message.text == '/start'):
        await message.answer(hello_message, parse_mode=types.ParseMode.HTML)
        db.add_message(bot.id, message.chat.id, message.message_id + 1, hello_message,
                       datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    elif(message.text.lower() in yes):
        await message.answer('У него есть уши?')
        db.add_message(bot.id, message.chat.id, message.message_id + 1, 'У него есть уши?',
                       datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        await state.set_state(UserState.ears)
    elif(message.text.lower() in no):
        db.update_cat(message.from_user.id)
        await message.answer(cat_message)
        db.add_message(bot.id, message.chat.id, message.message_id + 1, cat_message,
                       datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        await state.finish()
    else:
        await message.answer(error_message)
        db.add_message(bot.id, message.chat.id, message.message_id + 1, error_message,
                       datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

@dp.message_handler(state=UserState.ears)
async def ears(message: Message, state: FSMContext):
    db.add_message(message.from_user.id, message.chat.id, message.message_id, message.text, message.date)
    if(message.text == '/start'):
        await message.answer(hello_message, parse_mode=types.ParseMode.HTML)
        db.add_message(bot.id, message.chat.id, message.message_id + 1, hello_message,
                       datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    elif(message.text.lower() in yes):
        db.update_cat(message.from_user.id)
        await message.answer(cat_message)
        db.add_message(bot.id, message.chat.id, message.message_id + 1, cat_message,
                       datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        await state.finish()
    elif(message.text.lower() in no):
        db.update_bread(message.from_user.id)
        await message.answer(bread_message)
        db.add_message(bot.id, message.chat.id, message.message_id + 1, bread_message,
                       datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        await state.finish()
    else:
        await message.answer(error_message)
        db.add_message(bot.id, message.chat.id, message.message_id + 1, error_message,
                       datetime.now().strftime('%Y-%m-%d %H:%M:%S'))