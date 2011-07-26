# coding=UTF-8
'''
Created on 2011/5/9

@author: korprulu
'''
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from google.appengine.api import users
from model.Employee import Employee
from model.WorkingHours import WorkingHours
import datetime
import time

def personalRecord(request):
    
    user = users.get_current_user()
    em_data = Employee.gql("WHERE mail = :1", user)
    
    if not em_data.count(1):
        return HttpResponse('系統找不到您的的資料。')
    
    working_hours = WorkingHours.gql("WHERE worker = :1", user)
    
    total_pay = 0
    total_hour = 0
    for work in working_hours:
        total_pay += work.pay
        total_hour += work.subtotal
    
    if user:
        template_values = {
                           'userName': users.get_current_user().nickname().split('@')[0],
                           'logout': users.create_logout_url('/'),
                           'em_data': em_data,
                           'working_hours': working_hours,
                           'total_pay': total_pay,
                           'total_hour': total_hour,
                           'em_mail': user.email()
                           }
    return render_to_response('employee/employee.html', template_values)

def addRecord(request):
    
    bhour = int(request.POST['bhour'].split(':')[0])
    ehour = int(request.POST['ehour'].split(':')[0])
    bminutes = int(request.POST['bhour'].split(':')[1])
    eminutes = int(request.POST['ehour'].split(':')[1])
    subtotal = float((ehour-bhour) + float(eminutes-bminutes)/60)
    time_format = "%Y-%m-%d"

    hourly_pay = Employee.gql("WHERE mail = :1", users.get_current_user()).get().hourly_pay
             
    working = WorkingHours()
    result = WorkingHours.gql('ORDER BY id DESC').get();
    working.id = result.id + 1 if result else 1
    working.worker = users.get_current_user()
    working.working_date = datetime.date.fromtimestamp(time.mktime(time.strptime(request.POST['date'], time_format)))
    working.working_bhour = request.POST['bhour']
    working.working_ehour = request.POST['ehour']
    working.working_area = request.POST['area']
    working.working_content = request.POST['content']
    working.subtotal = subtotal
    working.pay = int(subtotal * hourly_pay)
    working.put()
    
    return redirect('/employee/')

def deleteRecord(request):

    delete_id = request.POST['delete_id']
        
    q = WorkingHours.gql("WHERE id = :1", int(delete_id))

    for result in q:
        result.delete()

    return redirect('/employee/')

def showMonthRecord(request, year, month):

    user = users.get_current_user()

    time_format = "%Y-%m-%d"
    bday = year + "-" + month + "-" + '1'
    endday = year +"-" + unicode(int(month) + 1) + "-" + '1'
    sdate = datetime.date.fromtimestamp(time.mktime(time.strptime(bday, time_format)))
    sdate2 = datetime.date.fromtimestamp(time.mktime(time.strptime(endday, time_format)))
    em_data = Employee.gql("WHERE mail = :1", user)
    working_hours = WorkingHours.gql("WHERE worker = :1 AND working_date >= :2 AND working_date < :3",
                                      user, sdate, sdate2)
    total_hour = 0
    total_pay = 0
    for work in working_hours:
        total_hour += work.subtotal
        total_pay += work.pay
        
    if user:
        template_values = {'userName': users.get_current_user().nickname().split('@')[0],
                           'logout': users.create_logout_url('/'),
                           'em_data': em_data,
                           'working_hours': working_hours,
                           'total_hour': total_hour,
                           'total_pay': total_pay,
                           'select_year': year,
                           'select_month': month,
                           'em_mail': user.email()
                           }

    return render_to_response('employee/browse_employee.html', template_values)

def printWorkingHours(request, year, month):

    user = users.get_current_user()
        #user = users.User(mail)
    em_data = Employee.gql("WHERE mail = :1", user).fetch(1)

    time_format = "%Y-%m-%d"
    try:
        bday = year + '-' + month + '-1'
        endday = year + '-' + unicode(int(month) + 1) + "-1"
        sdate = datetime.date.fromtimestamp(time.mktime(time.strptime(bday, time_format)))
        sdate2 = datetime.date.fromtimestamp(time.mktime(time.strptime(endday, time_format)))
        working_hours = WorkingHours.gql("WHERE worker = :1 AND working_date >= :2 AND working_date < :3",
                                         user, sdate, sdate2)

        template_values = {'working_hours': working_hours,
                               'em_data':em_data}
            
        return render_to_response('table.html', template_values)
    except:
        return HttpResponse("請先選擇月份，初始畫面是所有的工讀紀錄。")