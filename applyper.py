import re
from robobrowser import RoboBrowser
from bs4 import BeautifulSoup
def check_hostel(rno,pas):
	br = RoboBrowser(history=True, parser="html.parser")
	br = RoboBrowser(user_agent='Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6')
	br.open('http://studentscorner.vardhaman.org')
	form = br.get_form(action="")
	#print(ppr)
	form["rollno"] =rno# user.rno
	form["wak"] = pas#user.pas
	br.submit_form(form)
	h=str(br.select)
	if("Permission Form" in h):
		return("True")
	else:
		return("False")
def applyf(rno,pas,out,indat,rea):
	br = RoboBrowser(parser="html.parser")
	br = RoboBrowser(user_agent='Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6')
	br.open('http://studentscorner.vardhaman.org')
	form = br.get_form(action="")
	#print(ppr)
	form["rollno"] =rno#ppr[0]# user.rno
	form["wak"] = pas#ppr[1]#user.pas
	br.submit_form(form)
	#print(pper)
	form = br.get_form(action="insert_permission.php")
	br.open("http://studentscorner.vardhaman.org/students_permission_form.php")
	form = br.get_form(action="insert_permission.php")
	form['out_time']=out#pper[0]
	form['in_time']=indat#pper[1]
	form['reason']=rea#pper[2]
	#br.submit_form(form, submit=br.submit_fields['__CONFIRM__'])
	#payload = {'rollno': '17881A0526', 'wak': 'hodit@vardhaman', 'ok' : 'SignIn' }
	#br.open("http://studentscorner.vardhaman.org/students_permission_form.php", method='post',data=payload)
	#br.submit_form(form)
	#tt=str(br.select)
	#br.submit_form(form, submit=br.submit_fields['__CONFIRM__'])
	#payload = {'rollno': '17881A0526', 'wak': 'hodit@vardhaman', 'ok' : 'SignIn' }
	#br.open("http://studentscorner.vardhaman.org/students_permission_form.php", method='post',data=payload)
	br.submit_form(form)
	tt=str(br.select)
	print(tt)
	if("Permission Form Submitted Successfully" in tt):
		return("Permission Form Submitted Successfully")
	else:
		return("Something went wrong.Apply the form manually and mail to vardhamanassistant@gmail.com stating the issue.")

	print(checkper)
	return("applied")
