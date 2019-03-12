#This is VardhamanTeleBot its username in telegram is "vardhamanBot"
import re
from robobrowser import RoboBrowser
from bs4 import BeautifulSoup
import imgkit
import telebot
import time
from functools import wraps
#from telebot import types
from flask import Flask, request
import requests  
import threading
import os
import marks as gpa
#from selenium import webdriver
#from webdriver_manager.chrome import ChromeDriverManager
#from selenium.webdriver.common.keys import Keys
API_TOKEN = '714169450:AAH1zbXmCKBFLY46xznM9v6iJc8E4SfQb8A'
bot = telebot.TeleBot(API_TOKEN)
server = Flask(__name__)

PORT = int(os.environ.get('PORT', '8443'))
#upd	ater = Updater(API_API_TOKEN)
global br,gid,rid,pid,finalurl#,checkrno
finalurl = "http://studentscorner.vardhaman.org/"
gid=[]
rid=[]
pid=[]
br = RoboBrowser(history=True, parser="html.parser")

def send_typing_action(func):
    """Sends typing action while processing func command."""

    @wraps(func)
    def command_func(*args, **kwargs):
        bot, update = args
        bot.send_chat_action(chat_id=update.effective_message.chat_id, action=telegram.ChatAction.TYPING)
        return func(bot, update, **kwargs)

    return command_func

@send_typing_action
def my_handler(bot, update):
    pass # Will send 'typing' action while processing the request.
# Handle '/start' and '/help'
@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, """\
Hi there, I am Vbot here to give you, your things!
Enter your RollNo and give one space and type password.
Don't forget the space.
"17881A0500 #ABCD"
For help type '/help'\
""")

#For seeing the commands in my bot.
@bot.message_handler(commands=['help'])
def help(message):
	bot.reply_to(message,"""
      '/details',
      '/attendance',
      '/cgpa'
      '/sgpa'
      '/logout',
     for now.""")
# error handling if user isn't known yet
# (obsolete once known users are saved to file, because all users
#   had to use the /start command and are therefore known to the bot)
'''def get_user_step(uid):
	if uid in userStep:
	        return userStep[uid]
	else:
		knownUsers.append(uid)
	        userStep[uid] = 0
	        print("New user detected, who hasn't used \"/start\" yet")
	 	return 0
'''
#rno=''
# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@send_typing_action
@bot.message_handler(func=lambda message:True if(len(message.text)==16 or len(message.text)>25) else False)
def echo_message(message):
	rno=''
	#one()
	m=message.text
	tid = str(message.from_user.id)
	print(tid)
	if tid in gid :
		tindex=gid.index(tid)
		rno=rid[tindex]
		pas=pid[tindex]
		gid.remove(tid)
		rid.remove(rno)
		pid.remove(pas)
		#bot.reply_to(message,'First logout the other user and then try again')
	if(m[0]=='1'):
		for i in range(0,10):
			rno=rno+m[i]
			#print(rno)
	rno=rno.upper()
	pas=''
	bot.reply_to(message,"wait")
	if(m[11]=='#' or m[11] == 'h'):
		for i in range(11,len(m)):
			pas=pas+m[i]
		br = RoboBrowser(history=True, parser="html.parser")
		br = RoboBrowser(user_agent='Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6')
		br.open('http://studentscorner.vardhaman.org')
		form = br.get_form(action="")
		form["rollno"] = rno
		form["wak"] = pas
		br.submit_form(form)
		finalurl = "http://studentscorner.vardhaman.org/"
		finalurl=check_pas(rno,pas)
		print(finalurl)
		time.sleep(1)
		if(finalurl == "http://studentscorner.vardhaman.org/Students_Corner_Frame.php"):
			f='1'
			#print(f)
			#tid = str(message.from_user.id)
			
			sin_id(tid,rno,pas)
			bot.reply_to(message,'Correct Password, what do you want?')
			
		else:
			bot.reply_to(message,'Incorrect password!, try again')
#Saving rollno and passwords
def sin_id(tid,rno,pas):
	
	print("In sin")
	if tid not in gid :
		rid.append(rno)
		pid.append(pas)
		print(rno,pas)
		print("sin success")
		dic_gid(tid)	
#Saving tokenId of user
def dic_gid(tid):
	print("In dic_gid")
	#id={"1":"11"}
	gid.append(tid)
	if(tid in gid):
		print("dic_gid success")
@bot.message_handler(commands=['attendance','atd'])
def attendance(message):
	tid = str(message.from_user.id)
	if(tid in gid):
		get_atd(tid)
		#bot.reply_to(message,atd)
		
	else:
		bot.reply_to(message,"First login to get details")
@bot.message_handler(commands=['outing'])
def outing(message):
	global finalurl
	print(finalurl)
	tid = str(message.from_user.id)
	if(finalurl != "http://studentscorner.vardhaman.org/"):
		
		out=get_outing(rno,pas,tid)
		#driver = webdriver.Firefox()
		#driver.get('http://studentscorner.vardhaman.org/students_permission_form.php')
		#driver.save_screenshot('permission.png')
		#driver.quit()
		#n=str(tid)+'.png'
		#bot.send_photo(message, open(n, 'rb'))
		
	else:
		bot.reply_to(message,"First login to get details")
@send_typing_action
@bot.message_handler(commands=['details','det'])
def details(message):
	print("In details",finalurl)
	tid = str(message.from_user.id)
	if(tid in gid):
		det=get_det(tid)
		
		bot.reply_to(message,det)
		if(det != "First login to get details!"):
			if tid in gid :
				tindex=gid.index(tid)
				rno=rid[tindex]
			purl="http://resources.vardhaman.org/images/cse/"
			purl=purl+rno
			purl=purl+".jpg"
			print(purl)
			try:
				bot.send_photo(chat_id=tid, photo=purl)
			except:
				bot.reply_to(message,"We cannot send the photo to your phone.\nIf you got the photo previously in the same phone, please send a mail to \n vardhamanassistant@gmail.com stating the issue.")
	else:
		bot.reply_to(message,"First login to get details")
@bot.message_handler(commands=['logout'])
def logout(message):
	tid = str(message.from_user.id)
	if tid in gid :
		tindex=gid.index(tid)
		rno=rid[tindex]
		pas=pid[tindex]
		print(rno,pas)
	#try:
	if(tid in gid):
		tid = str(message.from_user.id)
		tindex=gid.index(tid)
		rno=str(rid[tindex])
		pas=str(pid[tindex])
		br.open("http://studentscorner.vardhaman.org/logout.php")
		finalurl = "http://studentscorner.vardhaman.org/"
		gid.remove(tid)
		rid.remove(rno)
		pid.remove(pas)
		bot.reply_to(message,	"loggedout successfully!")
	else:
		bot.reply_to(message,"I think you have not loggedIn.")

def check_pas(rno,pas):
	br = RoboBrowser(history=True, parser="html.parser")
	br = RoboBrowser(user_agent='Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6')
	br.open('http://studentscorner.vardhaman.org')
	form = br.get_form(action="")
	form["rollno"] = rno
	form["wak"] = pas
	br.submit_form(form)
	checkrno=str(br.select)
	#time.sleep(5)
	#print(finalurl)
	if(rno in checkrno):
		finalurl="http://studentscorner.vardhaman.org/Students_Corner_Frame.php"
		print("In check_pas",finalurl)
		return(finalurl)
	else:
		return False
def get_atd(tid):

	tindex=gid.index(tid)
	rno=rid[tindex]
	pas=pid[tindex]
	print(rno,pas)
#Below code can also be written in if block. This is also correct as else returns below code will not execute.
	br = RoboBrowser(history=True, parser="html.parser")
	br = RoboBrowser(user_agent='Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6')
	br.open('http://studentscorner.vardhaman.org')
	form = br.get_form(action="")
	form["rollno"] = rno
	form["wak"] = pas
	br.submit_form(form)
	br.open("http://studentscorner.vardhaman.org/student_attendance.php")
	bt=br.parsed()
	th=br.select("th")#3
	td=br.select("td")#8
	#print str(th[55].text.strip())+":"+str(th[56].text.strip())#attend
	try:
		for i in range(46,56):
			if(str(th[i].text.strip())=="Attendance Percentage"):
				#if(finalurl != "http://studentscorner.vardhaman.org/"):
				bot.send_message(tid,str(th[i].text.strip())+" : *"+str(th[i+1].text.strip())+"*",parse_mode= 'Markdown')#attend
				 
	except IndexError:
		bot.send_message(tid,"*Attendance is Freesed*.\nIf attendance is not freesed you can see it in the website send the mail to \n *vardhamanassistant@gmail.com*\nstating the issue.",parse_mode= 'Markdown')
	try:
		for i in range(9,37,4):
			t=td[i+3].text.strip()
			p=td[i+1].text.strip()
			d=td[i+2].text.strip()
			t=t.upper()
			d=d[0].upper()+d[1:].lower()
			if(t=="PRESENT"):
				bot.send_message(tid,str(td[i].text.strip())+"   "+str(td[i+1].text.strip())	+"   "+d+"  -  <b>"+t+"</b>",parse_mode= 'Html')#attend)
			else:
				bot.send_message(tid,str(td[i].text.strip())+"   "+p+"   "+d+"  -  ~<i>"+t+"</i>~",parse_mode= 'Html')#attend)
		#break
	except IndexError:
		pass		
def get_det(tid):
	tindex=gid.index(tid)
	rno=rid[tindex]
	pas=pid[tindex]
	print(rno,pas)
	br = RoboBrowser(history=True, parser="html.parser")
	br = RoboBrowser(user_agent='Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6')
	br.open('http://studentscorner.vardhaman.org')
	form = br.get_form(action="")
	form["rollno"] = rno
	form["wak"] = pas
	br.submit_form(form)
	#br.open("http://studentscorner.vardhaman.org")'''
	print(rno)
	#bot.reply_to(m,"wait")
	br.open("http://studentscorner.vardhaman.org/student_information.php")
	bt=br.parsed()
	th=br.select("th")#3
	td=br.select("td")#8
	print("In details "+rno)
	#print(z.geturl())
	#if finalurl != "http://studentscorner.vardhaman.org/":
	try:
		return(str(th[3].text.strip())+":"+str(td[8].text.strip())+"\n"+str(th[10].text.strip())+":"+str(td[17].text.strip())+"\n"+str(th[29].text.strip())+":"+(str(td[33].text.strip()))+"\n"+str(th[31].text.strip())+":"+str(td[35].text.strip()))#details
	except IndexError:
		return("Something is wrong")
	#else:
	#	return("First login to get details!")
	#return 0
	
def get_outing(rno,pas,tid):
	br = RoboBrowser(history=True, parser="html.parser")
	br = RoboBrowser(user_agent='Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6')
	#out_time=bot.reply_to(message,"Enter outdate and time")
	#in_time=bot.reply_to(message,"Enter in date and time")
	#reason=bot.reply_to(message,"Enter Reasson")
	br.open("http://studentscorner.vardhaman.org/students_permission_form.php")
	#form = br.get_form(action="insert_permission.php")
	#br.form['out_time']=outtime
	#br.form['in_time']=intime
	#br.form['reason']=reason
	#br.submit_form(form)
	#DRIVER = 'chromedriver'
	#driver = webdriver.Chrome(DRIVER)
	
	#driver.get('http://studentscorner.vardhaman.org/students_permission_form.php')
	#img = imgkit.from_url('http://google.com', False)
	imgkit.from_url('http://google.com', 'out.jpg')
	#img = Image.open(n)
	#img.show()
	#n=str(tid)+'.png'
	#driver.save_screenshot(n)
	#bot.reply_to(message,z)
	#link="/home/puneeth/Desktop/work/tele/"+str(tid)+".png"
	#bot.reply_to(chat_id=tid,img)
	bot.send_photo(message,open(out, 'rb'))
	#driver.quit()
@bot.message_handler(commands=['cgpa','CGPA','C.G.P.A','c.g.p.a'])
def Cgpa(message):
	tid = str(message.from_user.id)
	if tid in gid :
		tindex=gid.index(tid)
		rno=rid[tindex]
		pas=pid[tindex]
		data=gpa.cgpa(rno,pas)
		bot.reply_to(message,data)
		print(rno,pas)
	else:
		bot.reply_to(message,"First Login")

@bot.message_handler(func=lambda message:True if(len(message.text)==5 or len(message.text)==6) else False)
def Sgpa(message):
	tid = str(message.from_user.id)
	mtext=message.text
	#semid=bot.reply_to(message,"Enter the semester number")
	if(len(message.text)==5):
		semid=mtext[0]
	if(len(message.text)==6):
		semid=mtext[-1] # last character of string
	if tid in gid :
		tindex=gid.index(tid)
		rno=rid[tindex]
		pas=pid[tindex]
		data=gpa.sgpa(rno,pas,semid)
		bot.reply_to(message,data)
		print(rno,pas)
	else:
		bot.reply_to(message,"First Login")
	
@server.route('/' + API_TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=' https://vardhamantelebottest.herokuapp.com/' + API_TOKEN)
    return "!", 200


if __name__ == "__main__":
	server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
'''updater.start_webhook(listen="0.0.0.0",
                      port=5000,
                      url_path=API_API_TOKEN)
updater.bot.set_webhook("https://vteletest.herokuapp.com/" + API_TOKEN)
updater.idle()'''
