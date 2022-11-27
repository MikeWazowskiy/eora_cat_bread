import unittest

import handlers

from aiogram_unittest import Requester
from aiogram_unittest.handler import MessageHandler
from aiogram_unittest.types.dataset import MESSAGE

class TestBot(unittest.IsolatedAsyncioTestCase):
    # Проверяем, соответствует ли выводимое ботом сообщение после команды /start ожидаемому
    async def test_start(self):
        requester = Requester(request_handler=MessageHandler(handlers.start, commands=["start"]))

        message = MESSAGE.as_object(text="/start")
        calls = await requester.query(message)

        answer_message = calls.send_message.fetchone().text
        self.assertEqual(answer_message, "<b>Привет!</b>\nЯ помогу отличить кота от хлеба! Объект перед тобой квадратный?")

    # Проверяем, возвращается ли бот в начало диалога после команды /start
    async def test_square_start(self):
        requester = Requester(request_handler=MessageHandler(handlers.square))

        message = MESSAGE.as_object(text="/start")
        calls = await requester.query(message)

        answer_message = calls.send_message.fetchone().text
        self.assertEqual(answer_message, "<b>Привет!</b>\nЯ помогу отличить кота от хлеба! Объект перед тобой квадратный?")

    # Проверяем, соответствует ли выводимое ботом сообщение после ответа словом 'Ага' на первый вопрос ожидаемому
    async def test_square_yes(self):
        requester = Requester(request_handler=MessageHandler(handlers.square))

        message = MESSAGE.as_object(text="Ага")
        calls = await requester.query(message)

        answer_message = calls.send_message.fetchone().text
        self.assertEqual(answer_message, "У него есть уши?")

    # Проверяем, соответствует ли выводимое ботом сообщение после ответа словом 'ноуп' на первый вопрос ожидаемому
    async def test_square_no(self):
        requester = Requester(request_handler=MessageHandler(handlers.square))

        message = MESSAGE.as_object(text="ноуп")
        calls = await requester.query(message)

        answer_message = calls.send_message.fetchone().text
        self.assertEqual(answer_message, "Это кот, а не хлеб! Не ешь его!\nДля возвращения к началу диалога "
                                         "введите команду /start")

    # Проверяем, соответствует ли выводимое ботом сообщение после ответа назнакомым боту словом на первый вопрос ожидаемому
    async def test_square_error(self):
        requester = Requester(request_handler=MessageHandler(handlers.square))

        message = MESSAGE.as_object(text="хорошая идея")
        calls = await requester.query(message)

        answer_message = calls.send_message.fetchone().text
        self.assertEqual(answer_message, 'Я не такой глупый, чтобы понять сообщение "ага", "найн" и другие, '
                                         'но не настолько умный чтобы понять ваше сообщение.\nНапишите ещё раз.')

    # Проверяем, возвращается ли бот в начало диалога после команды /start
    async def test_ears_start(self):
        requester = Requester(request_handler=MessageHandler(handlers.ears))

        message = MESSAGE.as_object(text="/start")
        calls = await requester.query(message)

        answer_message = calls.send_message.fetchone().text
        self.assertEqual(answer_message, "<b>Привет!</b>\nЯ помогу отличить кота от хлеба! Объект перед тобой квадратный?")

    # Проверяем, соответствует ли выводимое ботом сообщение после ответа словом 'да' на второй вопрос ожидаемому
    async def test_ears_yes(self):
        requester = Requester(request_handler=MessageHandler(handlers.ears))

        message = MESSAGE.as_object(text="да")
        calls = await requester.query(message)

        answer_message = calls.send_message.fetchone().text
        self.assertEqual(answer_message, "Это кот, а не хлеб! Не ешь его!\nДля возвращения к началу диалога "
                                         "введите команду /start")

    # Проверяем, соответствует ли выводимое ботом сообщение после ответа словом 'Найн' на второй вопрос ожидаемому
    async def test_ears_no(self):
        requester = Requester(request_handler=MessageHandler(handlers.ears))

        message = MESSAGE.as_object(text="Найн")
        calls = await requester.query(message)

        answer_message = calls.send_message.fetchone().text
        self.assertEqual(answer_message, "Это хлеб, а не кот! Ешь его!\nДля возвращения к началу диалога "
                                         "введите команду /start")

    # Проверяем, соответствует ли выводимое ботом сообщение после ответа назнакомым боту словом на второй вопрос ожидаемому
    async def test_ears_error(self):
        requester = Requester(request_handler=MessageHandler(handlers.ears))

        message = MESSAGE.as_object(text="пожалуй откажусь")
        calls = await requester.query(message)

        answer_message = calls.send_message.fetchone().text
        self.assertEqual(answer_message, 'Я не такой глупый, чтобы понять сообщение "ага", "найн" и другие, '
                                         'но не настолько умный чтобы понять ваше сообщение.\nНапишите ещё раз.')