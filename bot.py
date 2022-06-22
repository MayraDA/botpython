import requests
from sympy import true
from telegram import *
from telegram.ext import * 
from requests import *
import json


updater = Updater(token="5431808491:AAH8eMshotdUGwvDXJ10z_IlDereTn6JQIk")
dispatcher = updater.dispatcher
climaText = "¡Quiero saber el clima! 🌞"
contarText = "¡Quiero contar!  🔢"
climaUrl = "http://api.openweathermap.org/data/2.5/weather?"
count = 0
city = False
apiKey = "d53a8198079d43e824576f3abb377f95"
allowedUsernames = ["MayraDA"]

def startCommand(update: Update, context: CallbackContext):
    global count
    buttons = [[KeyboardButton(climaText)], [KeyboardButton(contarText)]]
    context.bot.send_message(chat_id=update.effective_chat.id, text="¡Hola, ¿Qué necesitas?!!", reply_markup=ReplyKeyboardMarkup(buttons))

def messageHandler(update: Update, context: CallbackContext):
    global count
    global city
    count += 1
    if update.effective_chat.username not in allowedUsernames:
        context.bot.send_message(chat_id=update.effective_chat.id, text="No estás habilitado para usar este bot")
        return
    if climaText in update.message.text:
        context.bot.send_message(chat_id=update.effective_chat.id, text="En qué ciudad?")
        city = True
    if contarText in update.message.text:
        context.bot.send_message(chat_id=update.effective_chat.id, text="La cantidad de mensajes es: "+ str(count))
        city = False
    if city and update.message.text!=climaText:
        complete_url = climaUrl + "appid=" + apiKey + "&lang=sp" + "&units=standard" + "&q=" + update.message.text
        response = requests.get(complete_url)

        res =  response.json()
        #print (res)

        if res["cod"] != "404":

            # guardamos el valor de main
            y = res["main"]
        
            # guardamos temperatura que se encuentra en main
            temperature = y["temp"]
            temperature = round(temperature - 273.15,2)
            print (temperature)
            
            # guardamos humedad que se encuentra en main
            humidity = y["humidity"]
        
            # guardamos los datos del tiempo
            z = res["weather"]
        
            # guardamos la variable descripción del índice 0 de z
            description = z[0]["description"]

            context.bot.send_message(chat_id=update.effective_chat.id, text="Temperatura = " + str(temperature) + " C°")
            context.bot.send_message(chat_id=update.effective_chat.id, text="Estado = " + str(description))
            context.bot.send_message(chat_id=update.effective_chat.id, text="Humedad = " + str(humidity) + " %")      
        else:
            print("Ciudad no encontrada")
        city = False

def queryHandler(update: Update, context: CallbackContext):
    query = update.callback_query.data
    update.callback_query.answer()

dispatcher.add_handler(CommandHandler("start", startCommand))
dispatcher.add_handler(MessageHandler(Filters.text, messageHandler))
dispatcher.add_handler(CallbackQueryHandler(queryHandler))

updater.start_polling()