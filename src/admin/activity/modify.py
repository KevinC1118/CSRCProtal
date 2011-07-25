# -*- coding: utf-8 -*-
import os

from datetime import datetime, date, time
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from model.Activity import Activitydb, Forumdb

class MainPage(webapp.RequestHandler):
    def get(self):
        template_values = {'id': 0,
                           'userName': users.get_current_user().nickname().split('@')[0],
                           'logout': users.create_logout_url('/')}
        path = os.path.join(os.path.dirname(__file__),'../../templates/modify_activity.html')
        self.response.out.write(template.render(path, template_values))
        
class ModifyActivityInfo(webapp.RequestHandler):
    def get(self):
        getId = int(str(self.request.url).split('/Modify/Activity/id_')[1])
        searchinfo = db.GqlQuery("SELECT * FROM Activitydb WHERE activity_id = :1",getId)  #get activity info.
        dealtime = searchinfo.get()
        
        SignStart = str(dealtime.sign_start)
        SignEnd = str(dealtime.sign_end)
        ActivityStart = str(dealtime.activity_start)
        ActivityEnd = str(dealtime.activity_end)
        
        #Activitydb end
        searchForuminfos = db.GqlQuery("SELECT * FROM Forumdb WHERE activity_id = :1 ORDER BY forum_id DESC,sequence DESC",getId)  #get activity info.
        #Forumdb end
        
        
        #留言資訊包裝
        seq_questioner = []; #儲存第一個發問資訊
        seq_temp = [];#暫存
        seq_reply = []; #對應的回應資訊
        
        for forums in searchForuminfos:
            if forums:
                if forums.sequence == 0: #發問者
                    seq_questioner.append([forums.editor,forums.content,forums.forum_id]) #[發問者,內容,forum.id]
                    seq_reply.append(seq_temp); #將對應發問者的回應塞入陣列
                    seq_temp = [];#清空回應暫存陣列
                else: #回應者
                    seq_temp.insert(0,[forums.editor,forums.content,forums.sequence]);#[回應者,回應內容,第幾回應] 後回覆的放前面

        
        template_values = {
                           'searchinfos':searchinfo,
                           'id': getId,
                           'sign_start': SignStart,
                           'sign_end': SignEnd,
                           'activity_start': ActivityStart,
                           'activity_end':ActivityEnd,
                           'obj':zip(seq_questioner,seq_reply),
                           'userName': users.get_current_user().nickname().split('@')[0],
                           'logout': users.create_logout_url('/')
                           }
                           #'searchForuminfos': searchForuminfos

        path = os.path.join(os.path.dirname(__file__),'../../templates/modify_activity.html')
        self.response.out.write(template.render(path, template_values))
        
class ModifyActivity(webapp.RequestHandler):
    def post(self):
        getId = int(self.request.get('activity_id'))
        deltemp = db.GqlQuery("SELECT * FROM Activitydb WHERE activity_id = :1",getId)
        result = deltemp.get()
        db.delete(result)
        
        activity = Activitydb()
        activity.activity_name = self.request.get('activity_name')
        activity.content = self.request.get('content')
        
        sign_start_Date = str(self.request.get('sign_StartDateTime')).split(" ")[0]
        sign_start_Time = str(self.request.get('sign_StartDateTime')).split(" ")[1]
        sign_end_Date = str(self.request.get('sign_EndDateTime')).split(" ")[0]
        sign_end_Time = str(self.request.get('sign_EndDateTime')).split(" ")[1]
        activity_start_Date = str(self.request.get('activity_StartDateTime')).split(" ")[0]
        activity_start_Time = str(self.request.get('activity_StartDateTime')).split(" ")[1]
        activity_end_Date = str(self.request.get('activity_EndDateTime')).split(" ")[0]
        activity_end_Time = str(self.request.get('activity_EndDateTime')).split(" ")[1]
        
        arr_sign_start_Date = str(sign_start_Date).split("-")
        arr_sign_start_Time = str(sign_start_Time).split(":")
        arr_sign_end_Date = str(sign_end_Date).split("-")
        arr_sign_end_Time = str(sign_end_Time).split(":")
        arr_activity_start_Date = str(activity_start_Date).split("-")
        arr_activity_start_Time = str(activity_start_Time).split(":")
        arr_activity_end_Date = str(activity_end_Date).split("-")
        arr_activity_end_Time = str(activity_end_Time).split(":")
        
        #input time formula: datetime.combine(Date,Time)
        #Date : date( int(Year),int(Month),int(Date) )   Time : time( int(hour),int(minute) )
        activity.sign_start = datetime.combine(date(int(arr_sign_start_Date[0]),int(arr_sign_start_Date[1]),int(arr_sign_start_Date[2])),time(int(arr_sign_start_Time[0]),int(arr_sign_start_Time[1]),int(arr_sign_start_Time[2])))
        activity.sign_end = datetime.combine(date(int(arr_sign_end_Date[0]),int(arr_sign_end_Date[1]),int(arr_sign_end_Date[2])),time(int(arr_sign_end_Time[0]),int(arr_sign_end_Time[1]),int(arr_sign_end_Time[2])))
        activity.activity_start = datetime.combine(date(int(arr_activity_start_Date[0]),int(arr_activity_start_Date[1]),int(arr_activity_start_Date[2])),time(int(arr_activity_start_Time[0]),int(arr_activity_start_Time[1]),int(arr_activity_start_Time[2])))
        activity.activity_end = datetime.combine(date(int(arr_activity_end_Date[0]),int(arr_activity_end_Date[1]),int(arr_activity_end_Date[2])),time(int(arr_activity_end_Time[0]),int(arr_activity_end_Time[1]),int(arr_activity_end_Time[2])))
        activity.site = self.request.get('site')
        activity.limit_num = int(self.request.get('limit_num'))
        activity.activity_id = int(self.request.get('activity_id'))
        activity.put()
        #self.redirect('/ActivityModify/Main')
        self.response.out.write( " <script> self.close(); </script> ")
        
class AddForum(webapp.RequestHandler):
    def post(self):
        getId = int(str(self.request.url).split('/Modify/AddForum/id_')[1])
        getForumId = int(self.request.get("forum_id"))
        searchForuminfos = db.GqlQuery("SELECT * FROM Forumdb WHERE activity_id = :1 and forum_id = :2",getId,getForumId)  #get activity info.
        Forumcount = searchForuminfos.count()
        
        forumdb = Forumdb()
        forumdb.activity_id = getId
        forumdb.forum_id = getForumId
        forumdb.content = self.request.get("content")
        #forumdb.time =
        forumdb.sequence = Forumcount #because base is "0"
        forumdb.editor = "admin"
        forumdb.put()
        self.redirect("/Modify/Activity/id_"+str(getId))
        
class ModifyPeopleInfo(webapp.RequestHandler):  #not imp.
    def get(self):
        getId = int(str(self.request.url).split('/Modify/People/id_')[1])
        searchactivity = db.GqlQuery("SELECT * FROM Peopledb WHERE activity_id = :1",getId)  #get who sign up the activity.
        searchinfo = db.GqlQuery("SELECT * FROM Activitydb WHERE activity_id = :1",getId)  #get activity info.
        strtemp =""
        titletemp= ""
        line_count = 0
        page_count = 0
        activityinfo = searchinfo.get()
        
        titletemp = titletemp +' <table width="100%" border="1">\n'
        titletemp = titletemp +'     <tr>\n'
        titletemp = titletemp +'         <td width="20%" class="activityInfo">'+u'活動名稱：'+'</td>\n'
        titletemp = titletemp +'         <td width="30%" class="activityInfo">'+activityinfo.activity_name+'</td>\n'
        titletemp = titletemp +'         <td width="20%" class="activityInfo">'+u'活動編號：'+'</td>\n'
        titletemp = titletemp +'         <td width="30%" class="activityInfo">'+str(activityinfo.activity_id)+'</td>\n'
        titletemp = titletemp +'     </tr>\n'
        titletemp = titletemp +'     <tr>\n'
        titletemp = titletemp +'         <td class="activityInfo">'+u'活動時間：'+'</td>\n'
        titletemp = titletemp +'         <td colspan="3"  class="activityInfo">'+ str(activityinfo.activity_start)+' ~ '+str(activityinfo.activity_end)+'</td>\n'
        titletemp = titletemp +'     </tr>\n'
        titletemp = titletemp +'     <tr>\n'
        titletemp = titletemp +'         <td class="activityInfo">'+u'報名人數：'+'</td>\n'
        titletemp = titletemp +'         <td class="activityInfo">'+str(searchactivity.count())+'</td>\n'
        titletemp = titletemp +'         <td class="activityInfo">'+u'活動地點：'+'</td>\n'
        titletemp = titletemp +'         <td class="activityInfo">'+activityinfo.site+'</td>\n'
        titletemp = titletemp +'     </tr>\n'
        titletemp = titletemp +' </table><br />\n'
         
        strtemp = strtemp + titletemp
        strtemp = strtemp + '<table width="100%" border="0" style="page-break-after:always"><tr>\n' #first page start
            
        for search_result in searchactivity:
            if line_count == 25:    #change column
                strtemp = strtemp + '</table></td>\n'
                line_count = 0
                page_count = page_count + 1
                #if page_count == 2: #2大欄位使用
                if page_count == 3:
                    strtemp = strtemp + '</tr></table>\n' # end of page
                    strtemp =  strtemp + u'<!–[if IE 7]>'+'&nbsp;'+u'<![endif]–>\n' #change a new page
                    strtemp = strtemp + titletemp
                    strtemp = strtemp + '<table width="100%" border="0" style="page-break-after:always"><tr>\n' # page start
                    page_count = 0
            if line_count == 0:
                #strtemp =  strtemp + '<td width="50%" valign="top">\n<table width="100%" border="1" cellpadding="2" cellspacing="5">\n'#2大欄位
                strtemp =  strtemp + '<td width="33%" valign="top">\n<table width="100%" border="1" cellpadding="2" cellspacing="5">\n'#3大欄位
                strtemp =  strtemp + '<tr>\n'
                strtemp =  strtemp + '    <td width="50%" align="center" class="namelist">'+ u'姓名' +'</td>\n'
                #strtemp =  strtemp + '    <td width="30%" class="namelist">'+ u'學號' +'</td>\n'
                strtemp =  strtemp + '    <td width="50%" align="center" class="namelist">'+ u'簽到' +'</td>\n'
                strtemp =  strtemp + '</tr>\n'
                
            strtemp = strtemp + '<tr>\n'
            strtemp = strtemp + '    <td class="namelist">'+search_result.name+'</td>\n' 
            #strtemp = strtemp + '    <td class="namelist">'+str(search_result.stu_id)+'</td>\n'
            strtemp = strtemp + '    <td></td><!-- check in -->\n'
            strtemp = strtemp + '</tr>\n'
            line_count = line_count + 1
            
        if page_count == 0: #if don't have three column (have one column)
            strtemp =  strtemp + '</table>\n</td>\n<td width="33%" valign="top">\n<table width="100%" border="1" cellpadding="2" cellspacing="5">\n </table>\n</td>\n<td width="33%" valign="top">\n<table width="100%" border="1" cellpadding="2" cellspacing="5">\n' #to setting two column format
        if page_count == 1: #if don't have three column (have two column)
            strtemp = strtemp + '</table>\n</td>\n<td width="33%" valign="top">\n<table width="100%" border="1" cellpadding="2" cellspacing="5">\n' #to setting one column format
        strtemp = strtemp + '</table></td>\n' 
        strtemp = strtemp + '</tr></table>\n' # end of page        
        
        template_values = {
            'search_id': getId,
            'search_results': searchactivity,
            'activityinfo': searchinfo.get(),    #only one activity.
            'change_line_count':0,
            'printcontent':strtemp,
            'sign_num':searchactivity.count()
            }
        path = os.path.join(os.path.dirname(__file__),'../../templates/print.html')
        self.response.out.write(template.render(path, template_values))
        
application = webapp.WSGIApplication([('/Modify', MainPage),('/Modify/Activity/.*',ModifyActivityInfo),('/Modify/SaveActivity',ModifyActivity),('/Modify/People/.*',ModifyPeopleInfo),(('/Modify/AddForum/.*'),AddForum)],debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
