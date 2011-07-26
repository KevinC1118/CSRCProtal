import gdata.docs.client
from django.shortcuts import render_to_response, redirect
from file.youtube import clientLogin, YOUTUBE_DEFAULT_USER_FEED_URI
from model.Youtube import Account
from model.GDocs import DocAccount


def index(request):
    client = clientLogin()
    
    if client:
        youtube_feed = client.GetYouTubeVideoFeed(YOUTUBE_DEFAULT_USER_FEED_URI)
    else:
        youtube_feed = None
    
    return render_to_response('admin/archive/index.html', 
                              {'youtube_feed' : youtube_feed})


def youtubeAccount(request):
    accounts = Account.all()
    return render_to_response('admin/archive/youtube_account.html',
                              {'account' : accounts.get()})


def editYoutubeAccount(request):
    key = request.POST.get('key', None)
    email = request.POST.get('email', None)
    password = request.POST.get('password', None)
    
    if email and password:
        if key:
            a = Account.get(key)
            a.email = email
            a.password = password
        else:
            a = Account(email=email, password=password)
            
        a.put()
    
    return redirect('/admin/archive/youtube/account/')

def GDocsLogin(request):
    if request.method == "POST":
        key = request.POST.get('key', None)
        user = request.POST.get('email', None)
        password = request.POST.get('password', None)
        if user and password:
            if key:
                a = DocAccount.get(key)
                a.email = user
                a.password = password
            else:
                a = DocAccount(email=user, password=password)
            
        a.put()
        return redirect('/admin/archive/gdocs/view/')
    else:
        accounts = DocAccount.all()
        return render_to_response('admin/archive/gdocs_login.html',
                                  {'account' : accounts.get()})
    

def GDocsView(request):
    accounts = DocAccount.all().get()
    user = accounts.email
    password = accounts.password
    client = gdata.docs.client.DocsClient(source='ohsc98lab2')
    client.ClientLogin(user, password, client.source);  
    feed = client.GetDocList()
    return render_to_response('admin/archive/gdocs_view.html',
                              {'feed' : feed})       
        
