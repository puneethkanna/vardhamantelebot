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
import telebot
from telebot import types
import requests  
import threading
import os
import marks as gpa
import applyper as papply
import attendance as atd
#from selenium import webdriver
#from webdriver_manager.chrome import ChromeDriverManager
#from selenium.webdriver.common.keys import Keys
API_TOKEN = '510512298:AAGQ41ooEVrk_hgh959nhKLg_JbneDE3I2o'
bot = telebot.TeleBot(API_TOKEN)
server = Flask(__name__)

PORT = int(os.environ.get('PORT', '8443'))
#upd	ater = Updater(API_API_TOKEN)
global br,gid,rid,pid,finalurl,ppr,pper#,checkrno
finalurl = "http://studentscorner.vardhaman.org/"
gid=[]  # Global storage 
rid=[]  # Roll no storage
pid=[]  # Password storage
pper=[] # Temporary storage of outing
ppr=[]  # Temporary storage of outing
ttt=[]  # Temp storage of rno and pass for logging
rege=["attendance", "details", "name", "cgpa", "c.g.p.a", "CGPA", "C.G.P.A", "sgpa", "SGPA", "s.g.p.a", "S.G.P.A", "outing", "logout"]
rege_attendance = ["attendance"]
rege_details = ["details"]
rege_cgpa = ["cgpa"]
rege_outing = ["outing"]
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
	#starts.acquire()
	bot.reply_to(message, """\
Hi there, I am Vbot here to give you, your things!
For logging in please type "/login"
For help type '/help'\
""")

#For seeing the commands in my bot.
@bot.message_handler(commands=['help'])
def help(message):
	#helps.acquire()
	bot.reply_to(message,"""
      '/login',
      '/details',
      '/attendance',
      '/cgpa',
      '/sgpa',
      '/logout' 
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
@bot.message_handler(commands=['login'])
def login(message):
	tid = str(message.from_user.id)
	m=message.text
	if tid in gid :
		tindex=gid.index(tid)
		rno=rid[tindex]
		pas=pid[tindex]
		gid.remove(tid)
		rid.remove(rno)
		pid.remove(pas)
		bot.send_message(tid,"Try again, logged out old user.")
	else:
		msg=bot.send_message(tid,"Enter your Roll no")
		bot.register_next_step_handler(msg, roll_no)
		
def roll_no(message):
	chat_id = message.chat.id
	rno = message.text
	rno = rno.upper()
	ttt.append(rno)
	try:
		msg=bot.send_message(chat_id,"Enter your password")
		bot.register_next_step_handler(msg, passd)
	except Exception as e:
		Bot.send_message(chat_id,'oooops\nSomething went wrong.\nsend a mail to vardhamanassistant@gmail.com stating the issue.\n')
def passd(message):
	chat_id = message.chat.id
	pas=''
	pas = message.text
	ttt.append(pas)
	rno = ttt[0]
	finalurl = "http://studentscorner.vardhaman.org/"
	finalurl=check_pas(rno,pas)
	tid = str(chat_id)
	print(finalurl)
	if(finalurl == "http://studentscorner.vardhaman.org/Students_Corner_Frame.php"):
		f='1'
		print(f)
		sin_id(tid,rno,pas)
		bot.reply_to(message,'Correct credentials, what do you want?')
	else:
		bot.reply_to(message,'Incorrect credentials!, try again')
	del ttt[:]

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
	#bot.send_chat_action(chat_id=tid, action=telegram.ChatAction.TYPING)
	if(tid in gid):
		tindex=gid.index(tid)
		rno=rid[tindex]
		pas=pid[tindex]
		t = atd.attendance(tid,rno,pas)
		
	else:
		bot.reply_to(message,"First login to get details")
	#atds.release()
'''@bot.message_handler(commands=['outing'])
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
'''
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
'''def get_atd(tid):

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
		bot.send_message(tid,"*Attendance is Freezed*.\nIf attendance is not freezed you can see it in the website. If you have any issue please feel free to send mail to \n *vardhamanassistant@gmail.com*\n stating the issue.",parse_mode= 'Markdown')
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
'''
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
@bot.message_handler(commands=['outing'])
def outing(message):
	tid = str(message.from_user.id)
	if tid in gid:
		tindex=gid.index(tid)
		rno=rid[tindex]
		pas=pid[tindex]
		#out_date=out.out_datetime(tid)
		#in_date=out.in_datetime(tid)
		#reason=out.reason(tid)
		#status=
		c=papply.check_hostel(rno,pas)
		if(c=="True"):
			out_datetime(rno,pas,tid)
		else:
			bot.reply_to(message,"You are not a hosteler! :).\nIf it is wrong please send a mail to vardhamanassistant@gmail.com stating the issue.")
		#bot.reply_to(message,status)
		#driver = webdriver.Firefox()
		#driver.get('http://studentscorner.vardhaman.org/students_permission_form.php')
		#driver.save_screenshot('permission.png')
		#driver.quit()
		#n=str(tid)+'.png'
		#bot.send_photo(message, open(n, 'rb'))
		
	else:
		bot.reply_to(message,"First login to apply permission")
def out_datetime(rno,pas,tid):
	chat_id = tid
	ppr.append(rno)
	ppr.append(pas)
	#name="user"
	#user = User(name)
	#user_dict[chat_id] = user
	#user.rno=rno
	#user.pas=pas
	#user.tid=tid
	try:
		msg=bot.send_message(chat_id,"Enter outdate and time")
		bot.register_next_step_handler(msg, in_datetime)
	except Exception as e:
		Bot.send_message(chat_id,'oooops\nSomething went wrong.\nsend a mail to vardhamanassistant@gmail.com stating the issue.\n')


def in_datetime(message):
	chat_id = message.chat.id
	#user = user_dict[chat_id]
	out_time=message.text
	pper.append(out_time)
	
	#user.out_time = out_time
	print(out_time)
	try:
		msg=bot.reply_to(message,"Enter indate and time")
        #if not age.isdigit():
        #    msg = bot.reply_to(message, 'Age should be a number. How old are you?')
        #    bot.register_next_step_handler(msg, process_age_step)
        #    return
        
        #markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        #markup.add('Yes', 'No')
        #msg = bot.reply_to(message, 'Do you want to apply', reply_markup=markup)
		bot.register_next_step_handler(msg, reason)
	except Exception as e:
		bot.send_message(message,'oops\nSomething went wrong.\nsend a mail to vardhamanassistant@gmail.com stating the issue.\n')



def reason(message):
	chat_id = message.chat.id
	#user = user_dict[chat_id]
	in_time = message.text
	pper.append(in_time)
	#user = user_dict[chat_id]
	#user.in_time = in_time
	try:
		msg=bot.reply_to(message,"Enter reason :)")
        	
		bot.register_next_step_handler(msg, yes_no)
        	#bot.send_message(chat_id, 'Nice to meet you ' + user.name + '\n Age:' + str(user.age) + '\n Sex:' + user.sex)
	except Exception as e:
		bot.send_message(message,'oooops\nSomething went wrong.\nsend a mail to vardhamanassistant@gmail.com stating the issue.\n')

def yes_no(message):
	chat_id = message.chat.id
	reas = message.text
	#user = user_dict[chat_id]
	#user.reas = reas
	pper.append(reas)
	markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
	markup.add('Yes', 'No')
	msg = bot.reply_to(message, 'Do you want to apply', reply_markup=markup)
	bot.register_next_step_handler(msg, applying)
            
def applying(message):
	chat_id = message.chat.id
	ask = message.text
        #user = user_dict[chat_id]
	if(ask == u'Yes'):
		#tindex=gid.index(tid)
		#rno=rid[tindex]
		#pas=pid[tindex]
		tt=papply.applyf(ppr[0],ppr[1],pper[0],pper[1],pper[2])
		'''br = RoboBrowser(history=True, parser="html.parser")
		br = RoboBrowser(user_agent='Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6')
		br.open('http://studentscorner.vardhaman.org')
		form = br.get_form(action="")
		form["rollno"] = ppr[0]
		form["wak"] = ppr[1]
		br.submit_form(form)
		checkper=str(br.select)
		#if(checkper)
		br.open("http://studentscorner.vardhaman.org/students_permission_form.php")
		#pform =br.get_form(name="cl_form")
		#pform=br.get_form(action="insert_permission.php")
		pform = br.get_forms()[0]
		print(pper[0:])
		pform['out_time'].value=pper[0]
		pform['in_time'].value=pper[1]
		pform['reason'].value=pper[2]
		br.submit_form(pform,submit='cl')
		#bt=br.parsed()
		checkper=str(br.select)
		print(checkper)'''
		tt = papply.form(ppr[0], ppr[1])
		f = StringIO()
		# write some content to 'f'
		f.write("tt 'test.html'")
		f.seek(0)
		file_data = open('test.html', 'rb')
		tb = telebot.TeleBot(API_TOKEN)
		ret_msg = tb.send_document(chat_id, file_data)
		assert ret_msg.message_id
		del ppr[:]
		del pper[:]
		bot.reply_to(message,tt)
	elif(ask == u'No'):
		bot.reply_to(message,"You have cancelled to submit the form.")	
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

@bot.message_handler(commands=['sgpa','SGPA','S.G.P.A','s.g.p.a'])
def Sgpa(message):
	chat_id = message.chat.id
	tid = str(chat_id)
	if tid in gid :
		try:
			msg=bot.send_message(chat_id,"Enter semester number")
			bot.register_next_step_handler(msg, Sgpan)
		except Exception as e:
			Bot.send_message(chat_id,'oooops\nSomething went wrong.\nsend a mail to vardhamanassistant@gmail.com stating the issue.\n')
	else:
		bot.reply_to(message,"First Login")
def Sgpan(message):
	tid = str(message.chat.id)
	mtext=str(message.text)
#	semid=str(semid)
	print(gid,rid, pid)
	tindex=gid.index(tid)
	rno=rid[tindex]
	pas=pid[tindex]
	data=gpa.sgpa(rno,pas,mtext)
	bot.reply_to(message,data)
	print(rno,pas)
@bot.message_handler(func=lambda message:True)
def regular_expression(message):
	print("Entered into rege_expression")
	m = message.text
	tid = str(message.from_user.id)
	if tid in gid :
		tindex=gid.index(tid)
		rno=rid[tindex]
		pas=pid[tindex]
		tokens = word_tokenize(m)
		same_token = list(set(tokens) & set(rege))
		print(type(same_token))
		print(same_token, same_token[0])
		if(same_token[0] in rege_attendance):
			l=atd.attendance(tid,rno,pas)
		if(same_token[0] in rege_details):
			details(message)
		if(same_token[0] in rege_cgpa):
			Cgpa(message)
		if(same_token[0] in rege_outing):
			outing(message)
#if(same_token in rege_attendance):
	else:
		bot.reply_to(message,'First login to access me!')	
@server.route('/' + API_TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://vardhamantelebottest.herokuapp.com/' + API_TOKEN)
    return "!", 200


if __name__ == "__main__":
	server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
'''updater.start_webhook(listen="0.0.0.0",
                      port=5000,
                      url_path=API_API_TOKEN)
updater.bot.set_webhook("https://vteletest.herokuapp.com/" + API_TOKEN)
updater.idle()'''
