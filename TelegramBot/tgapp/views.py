from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext
# Create your views here.
from TelegramBot.settings import API_URL
from .models import *
import requests as re


def start(update: Update, context: CallbackContext):
    user = update.effective_user
    log = User.objects.filter(user_id=user.id).first()
    if log is None:
        log = User()
        log.user_id = user.id
    update.message.reply_text(f'Assalomu alaykum {user.first_name}. Honani tanlang', reply_markup=inline_btns())
    log.log = {'state': 0}
    log.save()


# def received_message(update: Update, context: CallbackContext):
#     msg = update.message.text
#     user = update.effective_user
#     log = User.objects.filter(user_id=user.id).first()
#     state = log.log
#     if state['state'] == 0:
#         room_number = msg
#         update.message.reply_text('Modelardan brini tanlang', reply_markup=btns(type='room_1', room=room_number))
#         state['state'] = 1
#     elif state['state'] == 1:
#         if msg == '⬅️Orqaga':
#             update.message.reply_text(f'Assalomu alaykum {user.first_name}. Honani tanlang', reply_markup=btns(type='room'))
#             state['state'] = 0
#         else:
#
#             update.message.reply_text("Mana")
#
#             context.bot.sendPhoto(photo=open())
#     log.log = state
#     log.save()
#
#
# def btns(type=None, room=None):
#     btn = []
#     if type == 'room':
#         product = get()
#         for i in range(0, len(product) - 1, 2):
#             btn.append(
#                 [KeyboardButton(product[i]['room_number']), KeyboardButton(product[i + 1]['room_number'])]
#             )
#         if len(product) % 2 != 0:
#             btn.append([KeyboardButton(product[-1]['room_number'])])
#     if type == 'room_1':
#         product = get(room=room)
#         for i in range(0, len(product) - 1, 2):
#             btn.append([KeyboardButton(product[i]['model_id']), KeyboardButton(product[i + 1]['model_id'])])
#         if len(product) % 2 != 0:
#             btn.append(([KeyboardButton(product[-1]['model_id'])]))
#         btn.append([KeyboardButton('⬅️Orqaga')])
#     return ReplyKeyboardMarkup(btn, resize_keyboard=True)


def inline_btns(type=None, room_number=None, user_id=None, id=None):
    btn = []
    if type == 'room':
        product = get(room=room_number)
        for i in range(0, len(product) - 1, 2):
            btn.append(
                [InlineKeyboardButton(f"{product[i]['id']} {product[i]['model_id']}", callback_data=f"{product[i]['id']}"),
                 InlineKeyboardButton(f"{product[i + 1]['id']} {product[i + 1]['model_id']}", callback_data=f"{product[i + 1]['id']}")]
            )
        if len(product) % 2 != 0:
            btn.append([InlineKeyboardButton(f"{product[-1]['id']} {product[-1]['model_id']}", callback_data=f"{product[-1]['id']}")])
        btn.append([InlineKeyboardButton("⬅️Orqaga", callback_data=f'orqaga_{user_id}')])
    else:
        product = get()
        l = []
        for i in product:
            l.append(i['room_number'])
        for i in l:
            if i not in btn:
                btn.append(i)

        print(btn)
        s = []
        for i in range(0, len(btn) - 1, 2):
            s.append([InlineKeyboardButton(btn[i], callback_data=f'{btn[i]}'), InlineKeyboardButton(btn[i + 1], callback_data=f'{btn[i + 1]}')])
        if len(btn) % 2 != 0:
            s.append([InlineKeyboardButton(btn[-1], callback_data=f"{btn[-1]}")])
        return InlineKeyboardMarkup(s)
    return InlineKeyboardMarkup(btn)


def inline_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    user = query.from_user
    data = query.data
    data = data.split('_')

    log = User.objects.filter(user_id=user.id).first()
    state = log.log
    if state['state'] == 0:
        room = data[0]
        query.message.edit_text('Modelardan brini tanlang', reply_markup=inline_btns(type='room', room_number=room, user_id=user.id))
        state['state'] = 1
    elif state['state'] == 1:
        if data[0] == 'orqaga':
            query.message.edit_text(f'Assalomu alaykum {user.first_name}. Honani tanlang', reply_markup=inline_btns())
            state['state'] = 0
        else:
            id = int(data[0])
            product = get(id=id)[0]
            img = product['qr_code']
            # img = 'https://images.unsplash.com/photo-1566275529824-cca6d008f3da?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8NHx8cGhvdG98ZW58MHx8MHx8&w=1000&q=80'
            context.bot.send_photo(chat_id=user.id, photo=f"{img}")

    log.log = state
    log.save()


def get(room=None, id=None):
    result = []
    response = re.get(API_URL).json()
    if room:
        for i in response:
            if i['room_number'] == room:
                result.append(i)
    elif id:
        for i in response:
            if i['id'] == id:
                result.append(i)
    else:
        result = response
    return result


