# -*- coding: utf-8 -*-
import telebot
from telebot import types
import re
from robobrowser import RoboBrowser
import os
'''from telebot import types
import telegram_send
from functools import wraps
from io import StringIO
import telegram_send'''

API_TOKEN = '703046139:AAH8uLwxJYHtCVMTdiGHm6ZCxItoQibPZDg'
bot = telebot.TeleBot(API_TOKEN)
global ppr,pper
ppr=[]
pper=[]
ppr.append('17881A0526')
ppr.append('#6UYS')
'''@bot.message_handler(commands=['outing'])
def out_datetime(message):
	chat_id = message.chat.id
	try:
		msg=bot.reply_to(message,"Enter outdate and time")
		bot.register_next_step_handler(msg, in_datetime)
	except Exception as e:
		bot.reply_to(message, 'oooops\nSomething went wrong.\nsend a mail to vardhamanassistant@gmail.com stating the issue.\n')


def in_datetime(message):
	chat_id = message.chat.id
	out_time=message.text
	pper.append(out_time)
	try:
		msg=bot.reply_to(message,"Enter indate and time")
		bot.register_next_step_handler(msg, reason)
	except Exception as e:
		bot.reply_to(message, 'oooops')


def reason(message):
	chat_id = message.chat.id
	in_time = message.text
	#user = user_dict[chat_id]
	#user.in_time = in_time
	pper.append(in_time)
	try:
		msg=bot.reply_to(message,"Enter reason :)")
        	
		bot.register_next_step_handler(msg, yes_no)
	except Exception as e:
		bot.reply_to(message, 'oooops')
def yes_no(message):
	chat_id = message.chat.id
	reas = message.text
	pper.append(reas)
	markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
	markup.add('Yes', 'No')
	msg = bot.reply_to(message, 'Do you want to apply', reply_markup=markup)
	bot.register_next_step_handler(msg, applying)
            
def applying(message):
	chat_id = message.chat.id
	ask = message.text
	if(ask == u'Yes'):
		print(ppr,pper)
		br = RoboBrowser(parser="html.parser")
		br = RoboBrowser(user_agent='Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6')
		br.open('http://studentscorner.vardhaman.org')
		form = br.get_form(action="")
		print(ppr)
		form["rollno"] =ppr[0]# user.rno
		form["wak"] = ppr[1]#user.pas
		br.submit_form(form)
		print(pper)
		form = br.get_form(action="insert_permission.php")
		br.open("http://studentscorner.vardhaman.org/students_permission_form.php")
		form = br.get_form(action="insert_permission.php")
		form['out_time']=pper[0]
		form['in_time']=pper[1]
		form['reason']=pper[2]
	#br.submit_form(form, submit=br.submit_fields['__CONFIRM__'])
		#payload = {'rollno': '17881A0526', 'wak': 'hodit@vardhaman', 'ok' : 'SignIn' }
	#br.open("http://studentscorner.vardhaman.org/students_permission_form.php", method='post',data=payload)
		br.submit_form(form)
		tt=str(br.select)
		print(tt)
		if("Permission Form Submitted Successfully" in tt):
			bot.reply_to(message,"Permission Form Submitted Successfully")
		else:
			bot.reply_to(message,"Something went wrong")
	elif(ask == u'No'):
		return("You have cancelled to submit the form.")
# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()
'''
@bot.message_handler(commands=['start'])
def start(message):
	chat_id = message.chat.id
	br = RoboBrowser(parser="html.parser")
	br = RoboBrowser(user_agent='Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6')
	br.open('http://studentscorner.vardhaman.org')
	form = br.get_form(action="")
	print(ppr)
	form["rollno"] =ppr[0]# user.rno
	form["wak"] = ppr[1]#user.pas
	br.submit_form(form)
	br.open("http://studentscorner.vardhaman.org/students_permission_form.php")
#	br.open("http://studentscorner.vardhaman.org/students_permission_form.php")
	bt=str(br.select)
	file=open("testing.html",'w')
	file.write(bt)
	file.close()
	print(file)
	bot.send_document(chat_id, document=file, caption="PermissionFrom", disable_notification=False, reply_to_message_id=None, reply_markup=None, timeout=20, parse_mode=None)

bot.polling()
