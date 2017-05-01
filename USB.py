'''
Name			:			URL Shortener Bot
Author			:			AmRo
URL				:			Telegram->@AM_RO045	  |   Instagram->@AmRo045	
Created at		:			07:51 ‎11/‎02/‎1396

'''

import requests
import validators
import telegram
from datetime import datetime
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters


TOKEN		=		"<BOT TOKEN>" # Your Bot Token Here
updater 	= 		Updater(token=TOKEN)
dispatcher 	= 		updater.dispatcher

def UrlValidator(url):
	if not validators.url(url):
		return 0
	
	Request = requests.get(url)
	
	if Request.status_code == 200:
		return 1
	else:
		return 2

def Shorter(url):
	Request = requests.get("http://yeo.ir/api.php?url=" + url)
	return Request.text	

def SaveUserInformation(bot, update):

	userInfo = update.message.chat
	userMessage = update.message.text
	userId = userInfo['id']
	userName = userInfo['username']
	CurrentDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	UserFirstName = userInfo['first_name']
	UserLastName = userInfo['last_name']
	
	# Save user information
	UserInfoFileStream = open("UserInformationUrlShorter.chatinfo", "a")
	
	if UserLastName == "" :
		UserLastName = "__NOT FOUND__"
	UserInfoFileStream.write("UserFirstName : %s\nUserLastName : %s\n" % (UserFirstName, UserLastName))
	UserInfoFileStream.write("Username : %s\nUserId : %s\nCurrentDate : %s\n" % (userName, userId, CurrentDate))
	UserInfoFileStream.write("UserMessage : %s\n\n#-------------------#\n\n" % (userMessage))
							
	UserInfoFileStream.close()
	
	
def getCm(bot, update):
	
	try:
		userMessage = update.message.text
		
		if UrlValidator(userMessage) == 0:
			bot.sendMessage(chat_id=update.message.chat_id, text="Not Valid Url")
		elif UrlValidator(userMessage) == 1:
			bot.sendMessage(chat_id=update.message.chat_id, text=Shorter(userMessage))
		else:
			bot.sendMessage(chat_id=update.message.chat_id, text="Url Not Worked.Please Send Health link.")
	except:
		bot.sendMessage(chat_id=update.message.chat_id, text="ConnectionErr: Url Not Worked.Please Send Health link.")
	
	SaveUserInformation(bot, update)
 
cm_handler = MessageHandler([Filters.text], getCm)
dispatcher.add_handler(cm_handler)		


def start(bot, update):
	Message = "\nSend link to shortening\n"
	bot.sendMessage(chat_id=update.message.chat_id, text=Message)
	SaveUserInformation(bot, update)
	
def stop(bot, update):
	Message = "Bye"
	bot.sendMessage(chat_id=update.message.chat_id, text=Message)
	SaveUserInformation(bot, update)
	
def help(bot, update):
	Message = (
			  "\nURL Shortener Bot"
			  "\n[USAGE]:"
			  "\nSend me a link e.g.(https://www.instagram.com/amro045/)\n"
			  )
	bot.sendMessage(chat_id=update.message.chat_id, text=Message)
	SaveUserInformation(bot, update)
	
	
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

start_handler = CommandHandler('stop', stop)
dispatcher.add_handler(start_handler)

start_handler = CommandHandler('help', help)
dispatcher.add_handler(start_handler)
	
updater.start_polling()
updater.idle()
updater.stop()
