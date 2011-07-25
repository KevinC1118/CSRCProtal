# -*- coding: utf-8 -*-

#import cgi
import os
import urllib
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from datetime import timedelta, datetime
from google.appengine.api import urlfetch
from google.appengine.api import users
from model.Activity import *

#list of activities   
class MainPage(webapp.RequestHandler):
    def get(self):
        #people_query = People.all()
        #people = people_query
        activity_query = Activitydb.all()
        #data = []

        #self.response.out.write(result)
        #activity = activity
        #self.response.out.write(id)
        template_values = {'activity': activity_query}
        if users.get_current_user():
            template_values['userName'] = users.get_current_user().nickname().split('@')[0]
            template_values['logout'] = users.create_logout_url('/')     
                         

        path = os.path.join(os.path.dirname(__file__),'../templates/activity.html')
        self.response.out.write(template.render(path, template_values))
        #中文

#select what activity
class Activities(webapp.RequestHandler):
    def get(self):
        
        url = str(self.request.url)
        value = url.split('?')[-1]
        
        #self.response.out.write(value.split('=')[0])
        global id
        #if(value.split('=')[0] == "id"):
        id = int(value.split('=')[-1])
        #else:
        #   id = "32"
        #  self.response.out.write("asd")
        
        #self.response.out.write(id) #test

        activity_query = db.GqlQuery("SELECT FROM Activitydb WHERE activity_id = :1" , id)
        #forum_query = db.GqlQuery("SELECT FROM Forumdb WHERE activity_id = :1 ORDER BY forum_id ,sequence", id) #fetch the same activity's forum
                                                                                                                #maybe order by time?
        #self.response.out.write(activity_query)
        forum_query = db.GqlQuery("SELECT * FROM Forumdb WHERE activity_id = :1 ORDER BY forum_id DESC,sequence DESC",id)  #get activity info.
        #for forums in forum_query:
            #x.append(forums.)
        #self.response.out.write(x)
        
        #留言資訊包裝
        seq_questioner = []; #儲存第一個發問資訊
        seq_temp = [];#暫存
        seq_reply = []; #對應的回應資訊
        
        for forumss in forum_query:
            if forumss:
                if forumss.sequence == 0: #發問者
                    seq_questioner.append([forumss.editor,forumss.content,forumss.forum_id]) #[發問者,內容,forum.id]
                    seq_reply.append(seq_temp); #將對應發問者的回應塞入陣列
                    seq_temp = [];#清空回應暫存陣列
                else: #回應者
                    seq_temp.insert(0,[forumss.editor,forumss.content,forumss.sequence]);#[回應者,回應內容,第幾回應]

                
        template_values = {'id': id,
                           'activity' : activity_query,
                           'forum' : forum_query,
                           'obj':zip(seq_questioner,seq_reply)}

        if users.get_current_user():
            template_values['userName'] = users.get_current_user().nickname().split('@')[0]
            template_values['logout'] = users.create_logout_url('/')

        path = os.path.join(os.path.dirname(__file__),'../templates/selected_activity.html')
        self.response.out.write(template.render(path, template_values))

class Attend(webapp.RequestHandler):
    def get(self):
        template_values = {'id': id}
        
        if users.get_current_user():
            template_values['userName'] = users.get_current_user().nickname().split('@')[0]
            template_values['logout'] = users.create_logout_url('/')
        #self.response.out.write("sass")
        path = os.path.join(os.path.dirname(__file__),'../templates/attend.html')
        self.response.out.write(template.render(path, template_values))
        
        
class SignUp(webapp.RequestHandler):
    def post(self):
        people = Peopledb()
    
        people.name = self.request.get('name')
        #people.stu_id = int(self.request.get('stu_id'))
        people.mail = self.request.get('mail')
        people.phone = self.request.get('phone')
        #people.content = self.request.get('content')
        people.activity_id = int(self.request.get('activity_id'))
        #self.response.out.write(id)
        people.put()
        
        
        
        if int(self.request.get('activity_id')) < 10000:
        
            para = {'u_name':self.request.get('name'),'u_email':self.request.get('mail'),'community':self.request.get('community'),
                    'u_company':self.request.get('company'),'u_captaincy0':self.request.get('department'),'u_captaincy1':self.request.get('job_title'),
                    'reg_id':'activity_id','action':'add','reg_stat':'','activity_id':''} 

            form_data = urllib.urlencode(para)
            urlfetch.fetch('http://swan.iis.sinica.edu.tw/signup/reg.php',
                            form_data,
                            urlfetch.POST)
                              
        #para = {'name':'aaqqq', 'stu_id':'12', 'mail':'222', 'phone':'123', 'activity_id':'1111'}
        #form_data = urllib.urlencode(para)

        #result = urlfetch.fetch('http://testcreateactivity.appspot.com/signup',
        #                form_data,
        #                urlfetch.POST
        #                )
        self.redirect('/activity/selected_activity?id='+str(id))

class Discuss(webapp.RequestHandler):
    def post(self):
            
        #url = str(self.request.url)    #option
        #value = url.split('?')[-1]     #option
        #id = int(value.split('=')[-1]) #option 
        
        forum_id_query = db.GqlQuery("SELECT FROM Forumdb WHERE activity_id = :1 ORDER BY forum_id DESC", id) #fetch the same activity's forum
        #sequence_query = db.GqlQuery("SELECT FROM Forumdb WHERE activity_id = :1 and forum_id = :2")
        
        forum = Forumdb()
        
        forum.activity_id = id
        if(forum_id_query.count() == 0):
            forum.forum_id = 1
        else:
            forum.forum_id = forum_id_query.get().forum_id + 1 #have to use the better way
        forum.content = self.request.get('content')
        forum.sequence = int(0)
        forum.editor = self.request.get('editor1')
        forum.time = datetime.now()+timedelta(hours=8)
        forum.put()
        #self.response.out.write('<html> <body onload="javascript:history.back(-1)"></body></html>') #redirect previous page
        #url = 'selected_activity?name=' + str(id)
        #self.response.out.write(url)
        self.redirect('/activity/selected_activity?id='+str(id))
class AddForum(webapp.RequestHandler):
    def post(self):
        #getId = int(str(self.request.url).split('/Modify/AddForum/id_')[1])
        getForumId = int(self.request.get("forum_id"))
        searchForuminfos = db.GqlQuery("SELECT * FROM Forumdb WHERE activity_id = :1 and forum_id = :2",id,getForumId)  #get activity info.
        Forumcount = searchForuminfos.count()
        
        forumdb = Forumdb()
        forumdb.activity_id = id
        forumdb.forum_id = getForumId
        forumdb.content = self.request.get("content")
        #forumdb.time =
        forumdb.sequence = Forumcount #because base is "0"
        forumdb.editor = self.request.get("editor")
        forumdb.put()
        self.redirect('/activity/selected_activity?id='+str(id))
        
application = webapp.WSGIApplication(
                                     [('/activity', MainPage), #list of activities
                                      ('/activity/selected_activity', Activities), #select what activity
                                      ('/activity/sign', Attend),  # sign interface
                                      ('/activity/signup', SignUp),  # sign
                                      ('/activity/discuss', Discuss),
                                      ('/activity/add_forum', AddForum)],
                                        debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()