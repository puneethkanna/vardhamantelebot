from robobrowser import RoboBrowser
from bs4 import BeautifulSoup
import telebot
import telegram_send
API_TOKEN = '703046139:AAH8uLwxJYHtCVMTdiGHm6ZCxItoQibPZDg'

bot = telebot.TeleBot(API_TOKEN)
def attendance(tid,rno,pas):
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
	l=[]
	att = []
	#print str(th[55].text.strip())+":"+str(th[56].text.strip())#attend
	try:
		for i in range(40,60):
			if(str(th[i].text.strip())=="Attendance Percentage"):
				#if(finalurl != "http://studentscorner.vardhaman.org/"):
				#att.append("\033[1m"+str(th[i].text.strip())+" : *"+str(th[i+1].text.strip())+"*")	
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
				#att.append("\033[1m"+str(td[i].text.strip())+"   "+str(td[i+1].text.strip())	+"   "+d+"  -  <b>"+t+"</b>")
				bot.send_message(tid,str(td[i].text.strip())+"   "+str(td[i+1].text.strip())	+"   "+d+"  -  <b>"+t+"</b>",parse_mode= 'Html')#attend)
			else:
				#att.append("\033[1m"+str(td[i].text.strip())+"   "+p+"   "+d+"  -  ~<i>"+t+"</i>~")
				bot.send_message(tid,str(td[i].text.strip())+"   "+p+"   "+d+"  -  ~<i>"+t+"</i>~",parse_mode= 'Html')#attend)
		#break
	except IndexError:
		pass
	return 1
