#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Ricardo Ruiz

import telebot
import logging

from emoji import emojize
from telebot.util import extract_arguments
from functools import partial

from config import TOKEN, TOKEN_DEV, ADMIN
from userstatehandler import UserStateHandler
from fileutils import FileSender
from math_eval import evaluate
from helpers import ActionHelpers, load_data

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

bot = telebot.TeleBot(TOKEN_DEV)
states = UserStateHandler('../datos/respuestas')
sender = FileSender(bot, media_folder="../media")
action = ActionHelpers(bot)
replies = load_data('../json/data.json')

# Partial functions

emj = partial(emojize, use_aliases=True)
bot.send_message = partial(bot.send_message, parse_mode="Markdown")

# Command handlers

@bot.message_handler(commands=['start'])
def send_welcome(message):

    usuario = message.chat.first_name
    start_messages = replies['start']

    for msg in start_messages:

        formated = emj(msg.format(usuario))
        action.typing_wait(message.chat.id, 2)
        bot.send_message(message.chat.id, formated)


@bot.message_handler(commands=['info'])
def send_info(message):

    usuario = message.chat.first_name
    info_messages = replies['info']

    for msg in info_messages:

        info_formated = emj(msg.format(usuario))
        action.typing_wait(message.chat.id, 2)
        bot.send_message(message.chat.id, info_formated)


@bot.message_handler(commands=['document'])
@action.uploading(doctype='photo')
def send_random_gif(message):

    gif = sender.file_handler.random_open("document")
    sender.send_file(message.chat.id, gif, "document")


@bot.message_handler(commands=['img'])
@action.uploading(doctype='photo')
def send_random_photo(message):

    photo = sender.file_handler.random_open("photo")
    sender.send_file(message.chat.id, photo, "photo")


@bot.message_handler(commands=['audio'])
@action.uploading(doctype='audio')
def send_random_audio(message):

    audio = sender.file_handler.random_open('audio')
    sender.send_file(message.chat.id, audio, "audio")


@bot.message_handler(commands=['estado'])
@action.typing
def send_estado(message):

    user = message.chat.id

    if not user in states:
        states.add_user(user)

    state = states.pop_state(user)
    bot.send_message(user, state)


@bot.message_handler(commands=['mates'])
def send_math(message):

    operacion = extract_arguments(message.text)
    try:
        resultado = evaluate(operacion)
    except Exception as error:
        
        math_reply = emj('\n'.join(replies['math']))
        bot.send_message(message.chat.id, math_reply)

        math_error = replies['math_error'].format(     # Math feedback
            operacion=message.text,
            error=error.message,
            usuario=message.chat.first_name)
        bot.send_message(ADMIN, error.message)

    else:
        bot.send_message(message.chat.id, "Mmm...")
        bot.send_message(message.chat.id, resultado)


@bot.message_handler(commands=['cosas'])
@action.typing
def send_cosas(message):

    cosas = '\n'.join(replies['cosas'])
    bot.send_message(message.chat.id, emj(cosas), parse_mode="HTML")


@bot.message_handler(commands=['registrar'])
@action.typing
def registrar(message):

    state = extract_arguments(message.text)
   
    if state:
        states.add(state)
        reply = emj(replies["estado_registrado"])
    else:
        reply = emj(replies["estado_vacios"])

    bot.send_message(message.chat.id, reply)

# Gestion de sugerencias


@bot.message_handler(commands=['sugerencias', 'sugerencia'])
def sugerencia_comando(message):

    sugerencia = extract_arguments(message.text)
    gestionar_sugerencia(sugerencia, message)


@bot.message_handler(func=lambda message: message.reply_to_message)
def sugerencia_reply(message):
    sugerencia = message.text.encode('utf-8')
    gestionar_sugerencia(sugerencia, message)


def gestionar_sugerencia(sugerencia, message):

    if not sugerencia:
        pide_sugerencia(message)
    else:
        enviar_sugerencia(sugerencia, message)


@action.typing
def pide_sugerencia(message):

    mensaje = emj(
        u'*¿Mmmm ninguna?* Vaya, gracias pues sí que soy perfecto :grin:')
    bot.send_message(message.chat.id, mensaje)
    mensaje = u"Anda anda, mándame algo"
    markup = telebot.types.ForceReply(selective=True)
    bot.send_message(message.chat.id, mensaje,
                     parse_mode="Markdown", reply_markup=markup)


def enviar_sugerencia(sugerencia, message):

    mensaje = emj(
        u'Gracias por ayudar :kissing_heart:')
    bot.send_message(message.chat.id, mensaje)

    # Enviar feedback al admin
    feedback = "{user} le ha enviado la siguiente sugerencia: *{sugerencia}*".format(
        user=message.chat.first_name, sugerencia=sugerencia)
    bot.send_message(ADMIN, feedback)


@bot.message_handler(commands=['ipan'])
@action.uploading('photo')
def ailo(message):
    ipan = sender.file_handler.open('ipan.jpg')
    sender.send_file(message.chat.id, ipan, 'photo')
    mensaje = emj("*AILO*:exclamation:")
    bot.send_message(message.chat.id, mensaje)


@bot.message_handler(func=lambda message: message.text.startswith('/'))
@action.typing
def commando_no_soportado(message):

    strange = message.text.split()[0]

    for mensaje in replies['comando_no_soportado']:

        mensaje = emj(mensaje.format(strange))
        action.typing_wait(message.chat.id)
        bot.send_message(message.chat.id, mensaje)

bot.polling(none_stop=True)
states.close()
