#!/bin/python
# -*- coding: utf-8 -*-
import os
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from model.WorkingHours import WorkingHours
from model.Employee import Employee
from google.appengine.api import users
from google.appengine.ext import db
import sys
type = sys.getfilesystemencoding()
import time, datetime
import calendar

class MainPage(webapp.RequestHandler):
    def get(self):
         
        em_query = Employee.all()
        employee = em_query.fetch(100)        
        
        now = datetime.datetime.now()
        time_format = "%Y-%m-%d"        
        daycount = calendar.monthrange(int(now.year),int(now.month))[1] 
        bday = str(now.year)+"-"+str(now.month)+"-1"
        endday = str(now.year)+"-"+str(now.month)+"-"+str(daycount)                       
        sdate = datetime.datetime.fromtimestamp(time.mktime(time.strptime(bday, time_format)))
        sdate2 = datetime.datetime.fromtimestamp(time.mktime(time.strptime(endday, time_format)))
        working_query = db.GqlQuery("SELECT * FROM WorkingHours WHERE working_date >= :1 AND working_date <= :2", sdate, sdate2)        
        working_hours = working_query.fetch(1000)
        
        seq1 = ()#key值陣列
        seq2 = []#時數
        for em in employee:
            seq1 += em.id,#設key id
            seq2.append(0)#放初值
        
        d = dict(zip(seq1,seq2))
        for work in working_hours:
            for i in range(len(employee)):
                if work.worker == employee[i].mail:
                    d[int(employee[i].id)] +=  work.subtotal

#        start=3
#        count=6
#        for x in xrange(len(employee)):
#            print x
#        print enumerate(employee)
        personal_data = zip(d.values(),employee)
#        for x,y in test:
#            print x,y.mail

        template_values = {}
        if users.get_current_user():
            template_values['userName'] = users.get_current_user().nickname().split('@')[0]
            template_values['logout'] = users.create_logout_url('/')    
        template_values['personal_data'] =  personal_data      

        path = os.path.join(os.path.dirname(__file__), '../../templates/admin/admin_employee.html')
        self.response.out.write(template.render(path, template_values))        

class Add_Record(webapp.RequestHandler):
    def post(self):

        max=0
        em_query = WorkingHours.all().order('-id')
        result = em_query.fetch(10)
        for work in result :
            if max<work.id:
                max = work.id

        bhour = int(self.request.get('bhour').split(':')[0])
        ehour = int(self.request.get('ehour').split(':')[0])
        bminutes = int(self.request.get('bhour').split(':')[1])
        eminutes = int(self.request.get('ehour').split(':')[1])
        subtotal = float((ehour-bhour) + float(eminutes-bminutes)/60)
        time_format = "%Y-%m-%d"

        em_query = db.GqlQuery("SELECT * FROM Employee WHERE mail = :1", users.get_current_user())        
        em_data = em_query.fetch(2)
        hourly_pay=0
        for result in em_data:
            hourly_pay = result.hourly_pay    
        working = WorkingHours()            
        working.id = max+1
        working.worker = users.get_current_user()
        working.working_date = datetime.date.fromtimestamp(time.mktime(time.strptime(self.request.get('date'), time_format)))
        working.working_bhour = self.request.get('bhour')
        working.working_ehour = self.request.get('ehour')
        working.working_area = self.request.get('area')
        working.working_content = self.request.get('content')
        working.subtotal = subtotal
        working.pay = int(subtotal*hourly_pay)
        working.put()
        
        self.redirect('/employee/')    

class Delete_Record(webapp.RequestHandler):
    def post(self):

        delete_id = self.request.get('delete_id')
        worker = self.request.get('worker')
        
        q = db.GqlQuery("SELECT * FROM WorkingHours WHERE id = :1", int(delete_id))
        results = q.fetch(10)
        for result in results:
            result.delete()
        
        if users.is_current_user_admin():
            self.redirect('/employee/show_workinghours/'+worker)
        else:
            self.redirect('/employee/')
        

class Update_Record(webapp.RequestHandler):
    def post(self):
        """
        ifupdate = self.request.get('update')              
        if ifupdate=='true':
            id = self.request.get('id')  
            q = db.GqlQuery("SELECT * FROM Publish WHERE id = :1", int(id))
            results = q.fetch(10)
            for data in results:
                data.title = self.request.get('new_title')
                data.content = self.request.get('new_content')
                data.type = self.request.get('new_type')

                timestring = "2005-09-01"
                time_format = "%Y-%m-%d"
                                
                data.publish_date = datetime.datetime.fromtimestamp(time.mktime(time.strptime(self.request.get('new_date'), time_format)))
                #data.publish_date = self.request.get('new_date')
            db.put(results)
            self.redirect('/admin')        
        else :       
            update_title = self.request.get('update_id')
            q = db.GqlQuery("SELECT * FROM Publish WHERE id = :1", int(update_title))
            results = q.fetch(10)
    
            template_values = {'publishs': results}
              
            path = os.path.join(os.path.dirname(__file__), '../../templates/updatepublish.html')
            self.response.out.write(template.render(path, template_values))
"""
class Add_Employee(webapp.RequestHandler):
    def post(self):

        max=0
        em_query = Employee.all().order('-id')
        result = em_query.fetch(10)
        for work in result :
            if max<work.id:
                max = work.id

        employee = Employee()            
        employee.id = max+1
        employee.name = self.request.get('name')
        employee.mail = users.User(self.request.get('mail'))
        employee.hourly_pay = int(self.request.get('hourly_pay'))
        employee.put()
        #self.response.out.write(self.request.get('mail'))
        self.redirect('/admin/employee')    
class Delete_Employee(webapp.RequestHandler):
    def post(self, delete_id):

        q = db.GqlQuery("SELECT * FROM Employee WHERE id = :1", int(delete_id))
        results = q.fetch(10)
        for result in results:
            result.delete()
            
        self.redirect('/admin/employee')

class Edit_Employee(webapp.RequestHandler):
    def post(self, edit_id):
               
        q = db.GqlQuery("SELECT * FROM Employee WHERE id = :1", int(edit_id))
        results = q.fetch(10)  
        template_values = {}  
        if users.get_current_user():
            template_values['userName'] = users.get_current_user().nickname().split('@')[0]
            template_values['logout'] = users.create_logout_url('/') 
        template_values['employee'] = results              
        path = os.path.join(os.path.dirname(__file__), '../../templates/admin/update_employee.html')
        self.response.out.write(template.render(path, template_values))
        
class Update_Employee(webapp.RequestHandler):
    def post(self, update_id):
        
        q = db.GqlQuery("SELECT * FROM Employee WHERE id = :1", int(update_id))
        results = q.fetch(10)
        for data in results:
            data.name = self.request.get('new_name')
#            data.mail = users.User(self.request.get('new_mail')+'@gmail.com')
            data.hourly_pay = int(self.request.get('new_pay'))

        db.put(results)
        self.redirect('/admin/employee') 

class Show_WorkingHours(webapp.RequestHandler):
    def get(self, worker_mail):
        now = datetime.datetime.now()
        nowy=[]
        for i in range(5):
            nowy.append(now.year-i)
        mon=[1,2,3,4,5,6,7,8,9,10,11,12]  
        user = users.User(worker_mail+'@gmail.com')
        em_query = db.GqlQuery("SELECT * FROM Employee WHERE mail = :1", user)        
        em_data = em_query.fetch(1)
        working_query = db.GqlQuery("SELECT * FROM WorkingHours WHERE worker = :1", user)        
        working_hours = working_query.fetch(100)
 
        total_hour = 0
        total_pay = 0
        for work in working_hours:
            total_hour += work.subtotal
            total_pay += work.pay

        template_values = {}
        if users.get_current_user():
            template_values['userName'] = users.get_current_user().nickname().split('@')[0]
            template_values['logout'] = users.create_logout_url('/')
            template_values['em_data'] = em_data  
            template_values['working_hours'] = working_hours
            template_values['total_hour'] = total_hour
            template_values['total_pay'] = total_pay
            template_values['nowy'] = nowy
            template_values['mon'] = mon  
        try:
            em_mail = str(em_data.__getitem__(0).mail)
            template_values['em_mail'] = em_mail   
            path = os.path.join(os.path.dirname(__file__), '../../templates/admin/browse_employee.html')
            self.response.out.write(template.render(path, template_values))                   
        except:               
            self.response.out.write('找不到此人的資料。')

class Personal_Record(webapp.RequestHandler):
    def get(self):
        now = datetime.datetime.now()
        nowy=[]
        for i in range(5):
            nowy.append(now.year-i)
        mon=[1,2,3,4,5,6,7,8,9,10,11,12]  
        user = users.get_current_user()       
        em_query = db.GqlQuery("SELECT * FROM Employee WHERE mail = :1", user)        
        em_data = em_query.fetch(2)       
        working_query = db.GqlQuery("SELECT * FROM WorkingHours WHERE worker = :1", user)        
        working_hours = working_query.fetch(100)    
        template_values = {}
        if users.get_current_user():
            template_values['userName'] = users.get_current_user().nickname().split('@')[0]
            template_values['logout'] = users.create_logout_url('/')  
            template_values['em_data'] = em_data
            template_values['working_hours'] = working_hours 
            template_values['nowy'] = nowy
            template_values['mon'] = mon                      
        try:
            em_mail = str(em_data.__getitem__(0).mail)
            template_values['em_mail'] = em_mail     
            path = os.path.join(os.path.dirname(__file__), '../../templates/admin/employee.html')
            self.response.out.write(template.render(path, template_values))                 
        except:   
            self.response.out.write('系統找不到您的的資料。')     

class Print_WorkingHours(webapp.RequestHandler):
    def post(self):
        
        mail = self.request.get('select_user_mail')
        year = self.request.get('select_year')
        month = self.request.get('select_month')  
        
        user = users.User(mail+'@gmail.com')
        #user = users.User(mail)
        em_query = db.GqlQuery("SELECT * FROM Employee WHERE mail = :1", user)        
        em_data = em_query.fetch(2)
        
        time_format = "%Y-%m-%d"
        try:       
            daycount = calendar.monthrange(int(year),int(month))[1]
             
            bday = year+"-"+month+"-"+'1'
            endday = year+"-"+month+"-"+str(daycount)                       
            sdate = datetime.datetime.fromtimestamp(time.mktime(time.strptime(bday, time_format)))
            sdate2 = datetime.datetime.fromtimestamp(time.mktime(time.strptime(endday, time_format)))
            working_query = db.GqlQuery("SELECT * FROM WorkingHours WHERE worker = :1 AND working_date >= :2 AND working_date <= :3", user, sdate, sdate2)        
            working_hours = working_query.fetch(100)
     
            template_values = {'working_hours': working_hours,
                               'em_data':em_data}
    
            path = os.path.join(os.path.dirname(__file__), '../../templates/table.html')
            self.response.out.write(template.render(path, template_values))
        except:
            self.response.out.write("請先選擇月份，初始畫面是所有的工讀紀錄。")
     
class Show_Month_Record(webapp.RequestHandler):
    def post(self):
        now = datetime.datetime.now()
        nowy=[]
        for i in range(5):
            nowy.append(now.year-i)
        mon=[1,2,3,4,5,6,7,8,9,10,11,12]        
        mail = self.request.get('user_mail')
        year = self.request.get('year')
        month = self.request.get('month')         
        user = users.User(mail+'@gmail.com')     

        time_format = "%Y-%m-%d"        
        daycount = calendar.monthrange(int(year),int(month))[1] 
        bday = year+"-"+month+"-"+'1'
        endday = year+"-"+month+"-"+str(daycount)                       
        sdate = datetime.datetime.fromtimestamp(time.mktime(time.strptime(bday, time_format)))
        sdate2 = datetime.datetime.fromtimestamp(time.mktime(time.strptime(endday, time_format)))
        em_query = db.GqlQuery("SELECT * FROM Employee WHERE mail = :1", user)        
        em_data = em_query.fetch(100)
        working_query = db.GqlQuery("SELECT * FROM WorkingHours WHERE worker = :1 AND working_date >= :2 AND working_date <= :3", user, sdate, sdate2)        
        working_hours = working_query.fetch(100)
        total_hour = 0
        total_pay = 0
        for work in working_hours:
            total_hour += work.subtotal
            total_pay += work.pay
        template_values = {}
        if users.get_current_user():
            template_values['userName'] = users.get_current_user().nickname().split('@')[0]
            template_values['logout'] = users.create_logout_url('/')  
            template_values['em_data'] = em_data
            template_values['working_hours'] = working_hours
            template_values['total_hour'] = total_hour
            template_values['total_pay'] = total_pay
            template_values['select_year'] = year
            template_values['select_month'] = month
            template_values['nowy'] = nowy
            template_values['mon'] = mon            
        try:
            em_mail = str(em_data.__getitem__(0).mail)
            template_values['em_mail'] = em_mail      
        except:   
            ''
        if users.is_current_user_admin():
            path = os.path.join(os.path.dirname(__file__), '../../templates/admin/browse_employee.html')
            self.response.out.write(template.render(path, template_values)) 
        else:
            path = os.path.join(os.path.dirname(__file__), '../../templates/admin/employee.html')
            self.response.out.write(template.render(path, template_values))            

application = webapp.WSGIApplication([('/admin/employee', MainPage),                                      
                                      ('/employee/add_record', Add_Record),
                                      ('/employee/delete_record', Delete_Record),
                                      ('/employee/update_record', Update_Record),
                                      ('/employee/add_employee', Add_Employee),
                                      ('/employee/delete_employee/(.*)', Delete_Employee),
                                      ('/employee/update_employee/(.*)', Update_Employee),
                                      ('/employee/edit_employee/(.*)', Edit_Employee),
                                      ('/employee/show_workinghours/(.*)', Show_WorkingHours),
                                      ('/employee/', Personal_Record),
                                      ('/employee/print_workinghours/',Print_WorkingHours),                           
                                      ('/employee/show_monthrecord/', Show_Month_Record)], debug=True)        
        
def main():
    run_wsgi_app(application)
    

if __name__ == "__main__":
    main()

