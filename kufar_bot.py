from aiogram import Bot, Dispatcher, executor, types
import logging
from aiogram.dispatcher.filters.builtin import CommandStart
import time
from bs4 import BeautifulSoup
from lxml import etree
import requests

IM = env('TG_ID')
URL = env('URL_KUFAR')
TOKEN = env('BOT_TOKEN')
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.2 Safari/605.1.15',
    'Accept-Language': 'ru',
}
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(CommandStart())
async def search_home(message: types.Message):
    r = requests.get(url=URL,
                     headers=HEADERS)
    not_home = ''
    dom = etree.HTML(str(BeautifulSoup(r.text, "html.parser")))
    await bot.send_message(chat_id=IM, text='Start')
    while True:
        time.sleep(2)
        if dom.xpath(f'//*[@id="content"]/div[1]/div[5]/div/section[1]/a/@href')[0] != not_home:
            not_home = dom.xpath(f'//*[@id="content"]/div[1]/div[5]/div/section[1]/a/@href')[0]
            for i in range(1, 4):
                one = dom.xpath(f'//*[@id="content"]/div[1]/div[5]/div/section[{i}]/a/@href')[0]
                two = dom.xpath(
                    f'//*[@id="content"]/div[1]/div[5]/div/section[{i}]/a/div[2]/div[1]/div[1]/span[1]')[
                    0].text
                three = dom.xpath(f'//*[@id="content"]/div[1]/div[5]/div/section[{i}]/a/div[2]/div[3]')[
                    0].text
                try:
                    four = \
                        dom.xpath(f'//*[@id="content"]/div[1]/div[5]/div/section[{i}]/a/div[2]/div[5]/span[2]')[
                            0].text
                except IndexError:
                    four = \
                        dom.xpath(f'//*[@id="content"]/div[1]/div[5]/div/section[{i}]/a/div[2]/div[4]/span[2]')[
                            0].text
                try:
                    five = dom.xpath(
                        f'//*[@id="content"]/div[1]/div[5]/div/section[{i}]/a/div[1]/div[1]/div[1]/div/div[1]/div/div/img[1]//@data-src')[
                        0]
                except IndexError:
                    five = 'Фото нет'
                await bot.send_message(IM,
                                       'Ссылка на объявление📎:\n {0}\n Стоимость💰:\n {1}\n Кол-во комнат🏢:\n {2}\n Адрес🌍:\n {3}\n Фото📷:\n {4}\n'.format(
                                           one, two, three, four, five)
                                       )
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
