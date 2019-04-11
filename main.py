import telebot
from telebot import types
import my_db

token = '720534541:AAETzDHV2_frgyQ2i8LTPIlimCcsu_lWoTI'
bot = telebot.TeleBot(token)
admins_id = (32319760, 160706375, 381091990)
user = {}
post_parts = ('Введите подробное описание задания.',
              'Введите цену задания.',
              )
channel = '@testchannelVAV'
docs_to_forward = {}


keyboard_main = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_posts = types.ReplyKeyboardMarkup(resize_keyboard=True)
button1 = types.KeyboardButton(text='Создать объявление')
button2 = types.KeyboardButton(text='Мой баланс')
button3 = types.KeyboardButton(text='Пополнить баланс')
button4 = types.KeyboardButton(text='Вывести деньги')
button5 = types.KeyboardButton(text='Мои задания')
button_post1 = types.KeyboardButton(text='Задания, где я заказчик')
button_post2 = types.KeyboardButton(text='Задания, где я исполнитель')
button_post3 = types.KeyboardButton(text='Главное меню')
keyboard_main.row(button1)
keyboard_main.row(button5)
keyboard_main.row(button2, button3, button4)
keyboard_posts.row(button_post1)
keyboard_posts.row(button_post2)
keyboard_posts.row(button_post3)



#TODO TODO TODO iline-regime

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.from_user.id, 'Привет! Если ты тут впервые - обязательно ознакомься с инструкцией '
                                           'к нашему сервису перед началом работы!', reply_markup=keyboard_main)


@bot.message_handler(commands=['admin'])
def handle_admin(message):
    if message.from_user.id not in admins_id:
        bot.send_message(message.from_user.id, 'Раздел только для админов')

    else:
        user.update({message.from_user.id: {'admin': False}})
        bot.send_message(message.from_user.id, 'Айди мне давай')


@bot.message_handler(content_types=['text'])
def buttons(message):
    if message.text == 'Мой баланс':
        response = my_db.get_balance(message.from_user.id)
        bot.send_message(message.from_user.id, response)

    elif message.text == 'Мои задания':
        bot.send_message(message.from_user.id, 'Какие задания ты хочешь увидеть?', reply_markup=keyboard_posts)

    elif message.text == 'Главное меню':
        bot.send_message(message.from_user.id, 'Главное меню', reply_markup=keyboard_main)

    elif message.text == 'Задания, где я заказчик':
        ids = my_db.get_task_id_zakazchik(message.from_user.id)
        if ids == 0:
            bot.send_message(message.from_user.id, 'У вас нет открытых заданий')
        else:
            for i in ids:
                bot.forward_message(message.from_user.id, channel, i['message_id'])

    elif message.text == 'Задания, где я исполнитель':
        ids = my_db.get_task_id_ispolnitel(message.from_user.id)
        if ids == 0:
            bot.send_message(message.from_user.id, 'У вас нет открытых заданий')
        else:
            for i in ids:
                bot.forward_message(message.from_user.id, channel, i['message_id'])

    elif message.text == 'Пополнить баланс':
        bot.send_message(message.from_user.id, '1111 2222 3333 4444')
        bot.send_message(message.from_user.id,
                         'Оплата на карту монобанк (Без комиссий на онлайн переводы). \n'
                         'Добавьте в комментарий к оплате следующее число:')
        bot.send_message(message.from_user.id, message.from_user.id)

    elif message.text == 'Вывести деньги':
        user.update({message.from_user.id: {'get_money': False}})
        bot.send_message(message.from_user.id, 'Введите номер карты и желаемую сумму.')

    elif message.text == 'Создать объявление':
        user.update({message.from_user.id: {'post': False, 'result_post': []}})
        bot.send_message(message.from_user.id, 'Введите название предмета или краткое описание задания.')

    elif message.from_user.id in user:

        if 'get_money' in user[message.from_user.id]:
            bot.reply_to(message, 'Модератор вскоре обработает ваш запрос.', reply_markup=keyboard_main)
            user[message.from_user.id].clear()

        elif 'post' in user[message.from_user.id]:

            if user[message.from_user.id]['post'] is False:
                user[message.from_user.id]['result_post'].append(message.text)
                user[message.from_user.id]['post'] = 0
                bot.send_message(message.from_user.id, post_parts[0])
            elif user[message.from_user.id]['post'] is not False:
                i = user[message.from_user.id]['post']
                try:
                    user[message.from_user.id]['result_post'].append(message.text)
                    bot.send_message(message.from_user.id, post_parts[i + 1])
                    user[message.from_user.id]['post'] += 1
                except:
                    garant_choice = types.InlineKeyboardMarkup()
                    garant = types.InlineKeyboardButton(text='С гарантом', callback_data='garant')
                    bez_garanta = types.InlineKeyboardButton(text='Без гаранта', callback_data='bez_garanta')
                    garant_choice.add(garant, bez_garanta)
                    bot.send_message(message.from_user.id, 'Теперь выберите сделку с гарантом или без. '
                                                           'Настоятельно рекомендуем воспользоваться гарантом. '
                                                           'В объявлении будет указан ваш выбор.', reply_markup=garant_choice)
                    user[message.from_user.id].pop('post')

    elif 'admin' in user[message.from_user.id]:
        # TODO: интеграция с бд
        bot.reply_to(message, 'База обновлена, деньги на балансе')
        user[message.from_user.id].clear()

    elif len(user[message.from_user.id]) == 0:
        bot.send_message(message.from_user.id, 'Неверная команда.')

    @bot.callback_query_handler(func=lambda call: True)
    def inline_button(call):
        if call.data == 'garant':
            post_button = types.InlineKeyboardMarkup()
            button = types.InlineKeyboardButton(text='Опубликовать', callback_data='post')
            post_button.add(button)
            user[call.from_user.id]['result_post'].append('Сделка с гарантом')
            bot.edit_message_text('Теперь пришлите нам фото или документы, которые могут помочь '
                                  'исполнителю, если хотите. Когда всё будет готов нажмите кнопку внизу',
                                  call.from_user.id,
                                  call.message.message_id, reply_markup=post_button)

        elif call.data == 'bez_garanta':
            post_button = types.InlineKeyboardMarkup()
            button = types.InlineKeyboardButton(text='Опубликовать', callback_data='post')
            post_button.add(button)
            user[call.from_user.id]['result_post'].append('Сделка без гаранта')
            bot.edit_message_text('Теперь пришлите нам фото или документы, которые могут помочь '
                                  'исполнителю, если хотите. Когда всё будет готов нажмите кнопку внизу',
                                  call.from_user.id,
                                  call.message.message_id, reply_markup=post_button)

        elif call.data == 'post':
            result_post = ''  # TODO формат поста
            for i in range(0, len(user[call.from_user.id]['result_post'])):
                result_post += user[call.from_user.id]['result_post'][i] + '\n'

            message_id = bot.send_message(channel, result_post)
            my_db.write_task(call.from_user.id, message_id = message_id.message_id, cost = user[call.from_user.id]['result_post'][2], task= user[call.from_user.id]['result_post'][1])

            if call.from_user.id in docs_to_forward:
                for i in range(0, len(docs_to_forward[call.from_user.id])):
                    bot.forward_message(channel, call.from_user.id, docs_to_forward[call.from_user.id][i])

                docs_to_forward[call.from_user.id].clear()

            user[call.from_user.id].clear()

            bot.send_message(call.from_user.id, 'Готово!')


@bot.message_handler(content_types=['photo', 'document'])
def document_handler(message):
    if message.from_user.id not in docs_to_forward:
        docs_to_forward.update({message.from_user.id: [message.message_id]})

    else:
        docs_to_forward[message.from_user.id].append(message.message_id)


bot.polling(none_stop=True, interval=0)