# подключение библиотек
# В google colab добавить: !pip install pyTelegramBotAPI
# В google colab добавить: !pip install Faker
# для установки необходимо в файл requirements.text добавить строки
# 'PyTelegramBotApi'
# 'faker'

from telebot import TeleBot, types
from faker import Faker
from datetime import datetime, timedelta
import unidecode
import random


bot = TeleBot(token='7691376070:AAFwfsvn4NSst72qxsL3rI87ekBDWaQFQSk', parse_mode='html') # создание бота

# объект клавиаутры
card_type_keybaord = types.ReplyKeyboardMarkup(resize_keyboard=True)
# первый ряд кнопок
card_type_keybaord.row(
    types.KeyboardButton(text='VISA'),
    types.KeyboardButton(text='Mastercard'),
)
# второй ряд кнопок
card_type_keybaord.row(
    types.KeyboardButton(text='Maestro'),
    types.KeyboardButton(text='MIR'),
)
    
# обработчик команды '/start'
@bot.message_handler(commands=['start'])
def start_command_handler(message: types.Message):
    # отправляем ответ на команду '/start'
    bot.send_message(
        chat_id=message.chat.id, # id чата, в который необходимо направить сообщение
        text='Привет! Я умею генерировать тестовую банковскую карту\n\nВыбери тип карты:', # текст сообщения
        reply_markup=card_type_keybaord,
    )

# обработчик всех остальных сообщений
@bot.message_handler()
def message_handler(message: types.Message):
    # проверяем текст сообщения на совпадение с текстом какой либо из кнопок
    # в зависимости от типа карты присваем занчение переменной 'card_type'
    if message.text.lower() in ['visa', 'виса', 'виза', 'visа', 'вisa','вiса', 'dbpf', 'dbcf', 'мшыф']:
        card_type = 'visa'
    elif message.text.lower() in ['mastercard', 'мастеркард', 'мастеркарт', 'мастерка', 'мастер', 'ьфыеуксфкв', 'vfcnthrfhl']:
        card_type = 'mastercard'
    elif message.text.lower() in ['maestro', 'маэстро', 'маестро', 'маестр', 'vftcnhj', 'ьфуыекщ']:
        card_type = 'maestro'
    elif message.text.lower() in ['mir', 'мир', 'мiр', 'vbh', 'ьшк']:
        card_type = 'mir'   
    else:
        # если текст не совпал ни с одной из кнопок 
        # выводим ошибку
        bot.send_sticker(
        chat_id=message.chat.id, # id чата, в который необходимо направить сообщение
        sticker="CAACAgIAAxkBAAKHRmcqP7Ykkvkc2PQ-TcXi89JYY6lsAAIbIgACRUxJSZe3xjnICxwWNgQ" # id стикера
      )
        bot.send_message(
            chat_id=message.chat.id,
            text='Ты чего? Напиши по-нормальному :(',
            reply_markup=card_type_keybaord
        )
        return

    @bot.message_handler(content_types=["sticker"])

    def message_handler_sticker(message: types.Sticker):
        bot.send_sticker(
        chat_id=message.chat.id, # id чата, в который необходимо направить сообщение
        sticker="CAACAgIAAxkBAAKHTGcqQQ6nnsYpv-wW2fbOPOjJp7-uAAK2RAACHGI4SBXmEuimiPdNNgQ" # id стикера
      )
        bot.send_message(
        chat_id=message.chat.id, # id чата, в который необходимо направить сообщение
        text='АШАЛЕЕЕТЬ!\n\n⬇️ Попробуй выбрать один из вариантов: ⬇️', # текст сообщения
        reply_markup=card_type_keybaord
      )
        return

    faker = Faker('ru_RU')  # утилита для генерации номеров кредитных карт
    def ru_to_latin(name):
        return unidecode.unidecode(name).replace("'", "")
    # получаем номер тестовой карты выбранного типа
    # card_type может принимать одно из зачений ['maestro', 'mastercard', 'visa13', 'visa16', 'visa19',
    
    # 'amex', 'discover', 'diners', 'mir15', 'mir16']
    card_number = faker.credit_card_number(card_type)
    
    # получаем код безопасности карты
    security_code = faker.credit_card_security_code(card_type)
    
    # получаем срок действия карты 
    start_date = datetime.now() + timedelta(days=365*2)  # Текущая дата + 2 год
    expiry_date = faker.credit_card_expire(start=start_date, end='+12y', date_format='%m/%y')
    
    # Получаем Фамилию и Имя держателя карты (мужские)
    last_name_male = faker.last_name_male()
    first_name_male = faker.first_name_male()

    # Получаем Фамилию и Имя держателя карты (женские)
    last_name_female = faker.last_name_female()
    first_name_female = faker.first_name_female()

    # Определяем Фамилию и Имя держателя карты в переменные для мужчин - male, для женщин - female

    card_holder_male = f"{last_name_male} {first_name_male}"
    card_holder_female = f"{last_name_female} {first_name_female}"
    
    # Рандомно (с шансом 50\50) определяем какого пола будет держатель карты при выдаче

    card_holder_random = random.choice([card_holder_male, card_holder_female]) 

    # Транслитерируем выдачу с кириллицы в латиницу

    card_holder = ru_to_latin(card_holder_random)
    bot.send_message(
    chat_id=message.chat.id,
    text=f'Тестовая карта {card_type.upper()}:  <code>{card_number}</code>\nДержатель карты:  <code>{card_holder}</code>\nКод безопасности:  <code>{security_code}</code>\nСрок действия:  <code>{expiry_date}</code>'
)


# главная функция программы
def main():
    # запускаем нашего бота
    bot.infinity_polling()


if __name__ == '__main__':
    main()
