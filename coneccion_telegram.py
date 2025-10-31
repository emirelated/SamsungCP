import telebot
import requests
import json  #No se si usaremos un .json
import os 
from dotenv import load_dotenv

load_dotenv()
# EMIIIIR!
# EMIR, DON'T ABBREVIATE CAPSTONE PROYECT. 
# EMIIIIR! 
# https://imgflip.com/memetemplate/557130211/DONT-ABBREVIATE-CYBERPUNK

TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
GROQ_TOKEN = os.getenv('GROQ_API_KEY')

if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN no está configurado en las variables de entorno")

if not GROQ_TOKEN:
    raise ValueError("GROQ_TOKEN no está configurado en las variables de entorno")



##
## Aca va todo lo del dataset, de veulta, no se si usaremos json o que :/
## Codigo para cargar el archivo del dataset
##

def buscar_en_dataset(pregunta, dataset):
	pregunta = pregunta.strip().lower()
	for item in dataset:
		if item['pregunta'].strip().lower() == pregunta:
			return item['respuesta']
	return None


def respuesta_groq(mensaje):
	headers = {
		'Authorization': f'Bearer {GROQ_TOKEN}',
		'Content-Type': 'application/json'
	}
	data = {
		"model": "llama3-8b-8192",
		"messages": [
			{"role": "user", "content": mensaje}
		]
	}
	try:
		resp = requests.post(GROQ_TOKEN, headers=headers, json=data, timeout=20)
		if resp.status_code == 200:
			respuesta = resp.json()['choices'][0]['message']['content']
			return respuesta.strip()
		else:
			return f"[Error Groq {resp.status_code}]"
	except Exception as e:
		return f"[Error de conexión a Groq: {e}]"


## Mas con el dataset, ver
bot = telebot.TeleBot(TELEGRAM_TOKEN)
dataset = cargar_dataset()


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Saludo")

@bot.message_handler(func=lambda message: True)
def responder(message):
	pregunta = message.text
	respuesta = buscar_en_dataset(pregunta, dataset)
	if respuesta:
		bot.reply_to(message, respuesta)
	else:
		respuesta_ia = respuesta_groq(pregunta)
		bot.reply_to(message, respuesta_ia)

if __name__ == "__main__":
	print("Bot en linea...")
	bot.infinity_polling()