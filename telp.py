#!/usr/bin/python
import mechanize
from bs4 import BeautifulSoup
# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.
import telebot
import time
from functools import wraps
from telebot import types
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
API_TOKEN = '714169450:AAGPQyLSTXfY6umwMmJp9nrJWO1c6fCf7e4'
bot = telebot.TeleBot(API_TOKEN)

finalurl = "http://studentscorner.vardhaman.org/"

global br,gid,rid,pid
gid=[]
rid=[]
pid=[]
br=mechanize.Browser()

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
Enter your RollNo as '/rollno' and give one space and type password.
For help type '/help'\
""")

#For seeing the commands in my bot.
@bot.message_handler(commands=['help'])
def help(message):
	bot.reply_to(message,"""
     '/details',
     '/attendance',
     '/logout' 
     for now.""")
	
# error handling if user isn't known yet
# (obsolete once known users are saved to file, because all users
#   had to use the /start command and are therefore known to the bot)
def get_user_step(uid):
	if uid in userStep:
	        return userStep[uid]
	else:
	        knownUsers.append(uid)
	        userStep[uid] = 0
	        print("New user detected, who hasn't used \"/start\" yet")
	 	return 0

#rno=''
# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@send_typing_action
@bot.message_handler(func=lambda message:True if(len(message.text)==16 or len(message.text)>25) else False)
def echo_message(message):
	global m,f,rno,pas,finalurl,tid
	rno=''
	#one()
	m=message.text
	
	if(m[0]=='1'):
		for i in range(0,10):
			rno=rno+m[i]
			#print(rno)
	pas=''
	bot.reply_to(message,"wait")
	if(m[11]=='#' or m[11] == 'h'):
		for i in range(11,len(m)):
			pas=pas+m[i]
		br=mechanize.Browser()
		br.set_handle_robots(False)
		br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
		br.open("http://studentscorner.vardhaman.org")
		br.select_form(nr=0)
		br.form['rollno']=rno
		br.form['wak']=pas
		suburl=br.submit() 
		#global finalurl
		#finalurl = "http://studentscorner.vardhaman.org/"
		finalurl=suburl.geturl()
		print(finalurl)
		time.sleep(1)
		if(finalurl == "http://studentscorner.vardhaman.org/Students_Corner_Frame.php"):
			f='1'
			print(f)
			bot.reply_to(message,'Correct Password, what do you want?')
			tid = message.from_user.id
			sin_id(tid)
		else:
			bot.reply_to(message,'Incorrect password!, try again')
		
#    bot.reply_to(message, "Hello")

#rno=raw_input("Roll No:")
def sin_id(mid):
	print("In sin")
	if tid not in gid :
		rid.append(rno)
		pid.append(pas)
		print(rno,pas)
		print("sin success")
		dic_gid(tid)
def dic_gid(tid):
	print("In dic_gid")
	#id={"1":"11"}
	gid.append(tid)
	if(tid in gid):
		print("dic_gid success")
	
@bot.message_handler(commands=['attendance','atd'])
def attendance(message):
	global finalurl
	print(finalurl)
	tid = message.from_user.id
	if(finalurl != "http://studentscorner.vardhaman.org/"):
		atd=get_atd(rno,pas,tid)
		bot.reply_to(message,atd)
		
	else:
		bot.reply_to(message,"First login to get details")
@bot.message_handler(commands=['outing'])
def outing(message):
	global finalurl
	print(finalurl)
	tid = message.from_user.id
	if(finalurl != "http://studentscorner.vardhaman.org/"):
		
		out=get_outing(rno,pas,tid)
		#driver = webdriver.Firefox()
		#driver.get('http://studentscorner.vardhaman.org/students_permission_form.php')
		#driver.save_screenshot('permission.png')
		#driver.quit()
		n=str(tid)+'.png'
		bot.send_photo(message, open(n, 'rb'))
		
	else:
		bot.reply_to(message,"First login to get details")
@send_typing_action
@bot.message_handler(commands=['details','det'])
def details(message):
	global finalurl
	print(finalurl)
	tid = message.from_user.id
	if(finalurl != "http://studentscorner.vardhaman.org/"):
		det=get_det()
		
		bot.reply_to(message,det)
		purl="http://resources.vardhaman.org/images/cse/"
		purl=purl+rno
		purl=purl+".jpg"
		print(purl)
		
		bot.send_photo(chat_id=tid, photo=purl)
	else:
		bot.reply_to(message,"First login to get details")

@bot.message_handler(commands=['logout'])
def logout(message):
	global finalurl
	if tid in gid :
		tindex=gid.index(tid)
		rno=rid[tindex]
		pas=pid[tindex]
		print(rno,pas)
	else:
		return("First Login")
	if(finalurl != "http://studentscorner.vardhaman.org/"):
		br.open("http://studentscorner.vardhaman.org/logout.php")
		finalurl = "http://studentscorner.vardhaman.org/"
		gid.remove(tid)
		bot.reply_to(message,"loggedout successfully!")
	else:
		bot.reply_to(message,"I think you have not loggedIn.")
def check_pas(rno,pas):
	br=mechanize.Browser()
	br.set_handle_robots(False)
	br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
	br.open("http://studentscorner.vardhaman.org")
	br.select_form(nr=0)
	br.form['rollno']=rno
	br.form['wak']=pas
	print(rno)
	print(pas)
	suburl=br.submit()
	finalurl=suburl.geturl()
	time.sleep(5)
	print(finalurl)
	if(finalurl == "http://studentscorner.vardhaman.org/Students_Corner_Frame.php"):
		#get_det(rno,pas)
		return True
	else:
		return False
def get_atd(rno,pas,tid):
	if tid in gid :
		tindex=gid.index(tid)
		rno=rid[tindex]
		pas=pid[tindex]
		print(rno,pas)
	else:
		return("First Login")
	br=mechanize.Browser()
	br.set_handle_robots(False)
	br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
	br.open("http://studentscorner.vardhaman.org")
	br.select_form(nr=0)
	br.form['rollno']=rno
	br.form['wak']=pas
	br.submit()
	br.open("http://studentscorner.vardhaman.org/student_attendance.php")
	bt=BeautifulSoup(br.response().read(),"lxml")
	th=bt.find_all("th") 
	td=bt.find_all("td") 
	#print str(th[55].text.strip())+":"+str(th[56].text.strip())#attend
	try:
		for i in range(46,56):
			if(str(th[i].text.strip())=="Attendance Percentage"):
				if(finalurl != "http://studentscorner.vardhaman.org/"):
					return str(th[i].text.strip())+":"+str(th[i+1].text.strip())#attend
	except IndexError:
		return("Attendance is Freesed")
def get_det():
	global finalurl
	if tid in gid :
		tindex=gid.index(tid)
		rno=rid[tindex]
		pas=pid[tindex]
		print(rno,pas)
	else:
		return("First Login")
	br=mechanize.Browser()
	br.set_handle_robots(False)
	br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
	br.open("http://studentscorner.vardhaman.org")
	br.select_form(nr=0)
	br.form['rollno']=rno
	br.form['wak']=pas
	br.submit()
	#br.open("http://studentscorner.vardhaman.org")'''
	print(rno)
	#bot.reply_to(m,"wait")
	br.open("http://studentscorner.vardhaman.org/student_information.php")
	bt=BeautifulSoup(br.response().read(),"lxml")
	th=bt.find_all("th") #3
	td=bt.find_all("td") #8
	print("In details "+rno)
	#print(z.geturl())
	if finalurl != "http://studentscorner.vardhaman.org/":
		try:
			return(str(th[3].text.strip())+":"+str(td[8].text.strip())+"\n"+str(th[10].text.strip())+":"+str(td[17].text.strip())+"\n"+str(th[29].text.strip())+":"+(str(td[33].text.strip()))+"\n"+str(th[31].text.strip())+":"+str(td[35].text.strip()))#details
		except IndexError:
			return("Something is wrong")
	else:
		return("First login to get details!")
	#return 0
	
def get_outing(rno,pas,tid):
	br.set_handle_robots(False)
	br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
	#bot.reply_to(message,"Enter outdate and time")
	#bot.reply_to(message,"Enter in date and time")
	#bot.reply_to(message,"Enter Reasson")
	#outtime=raw_input("Enter your out time")
	#intime=raw_input("Enter your in time")
	#reason=raw_input("Enter your outing reason")
	br.open("http://studentscorner.vardhaman.org/students_permission_form.php")
	#br.select_form(nr=0)
	#br.form['out_time']=outtime
	#br.form['in_time']=intime
	#br.form['reason']=reason
	#br.submit()
	DRIVER = 'chromedriver'
	driver = webdriver.Chrome(DRIVER)
	
	driver.get('http://studentscorner.vardhaman.org/students_permission_form.php')
	
	#img = Image.open(n)
	#img.show()
	n=str(tid)+'.png'
	driver.save_screenshot(n)
	#bot.reply_to(message,z)
	link="/home/puneeth/Desktop/work/tele/"+str(tid)+".png"
	
	#bot.send_photo(chat_id=tid,open(n, 'rb'))
	driver.quit()
bot.polling()
