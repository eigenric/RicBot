#author: Ricardo Ruiz
#encoding:utf-8

from emoji import Emoji
from config import TOKEN
import telebot
import random

cache = open('respuestas', 'r')
respuestas = cache.readlines()

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['info'])
def send_info(message):
	info = '''Saludos, este es el Bot AdaSaludosBot
		  los comandos disponibles son:
			/info : informa de los comandos
			/start : obvio para comenzar
			/image : le envia un precioso gif
			/audio le envia un precioso audio
			/estado : le envia estados random
			/registrar <estado> : memorizo el estado
			/math <operacion> : le devuelve la solucion
			/sugerencias <sugerencia> Buzon de sugerencias
			/ipan : misteriosa funcion
		  Agradecimientos a: Cristina y Putilla
		'''
	bot.send_message(message.chat.id, info)

@bot.message_handler(commands=['start'])
def send_start(message):
	send_info(message)
	print message.chat.id
	bot.send_message(message.chat.id, "Saludos")

@bot.message_handler(commands=['image'])
def send_image(message):
	image = open('media/giphy ('+str(random.randint(0, 3))+').gif', 'rb')
	bot.send_document(message.chat.id, image)
	image.close()

@bot.message_handler(commands=['audio'])
def send_audio(message):
	audio = open('media/nyan_song.mp3')
	bot.send_audio(message.chat.id, audio)
	audio.close()

@bot.message_handler(commands=['estado'])
def send_estado(message):
	file = open('datos/respuestas', 'r')
	respuestas = file.readlines()
	file.close()
	numero = random.randint(0, len(respuestas)-1)
	bot.send_message(message.chat.id, respuestas[numero])

@bot.message_handler(commands=['math'])
def send_math(message):
	operacion = message.text[6:]
	try:
		resultado = eval(operacion)
		bot.send_message(message.chat.id, resultado)
	except:
		bot.send_message(message.chat.id, "Solo permitidas operaciones matematicas, pillin")

@bot.message_handler(commands=['registrar'])
def registrar(message):
	estado = message.text[11:]
	fichero = open('respuestas', 'a')
	fichero.write(estado.encode('utf8')+'\n')
	fichero.close()
	bot.send_message(message.chat.id, "Estado registrado, Gracias")


@bot.message_handler(commands=['sugerencias'])
def recibir_sugerencias(message):
	sugerencia = message.text[13:]
	bot.send_message(ADMIN,sugerencia)
	bot.send_message(message.chat.id, "Gracias, por ayudar :D")


@bot.message_handler(commands=['ipan')
def ailo(message):
	bot.send_message(message.chat.id, "AILO")

bot.polling()
