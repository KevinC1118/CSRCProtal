'''
Created on 2011/5/9

@author: korprulu
'''
from google.appengine.api import users
from django.shortcuts import redirect

def login(request):
    
    return redirect('/admin/') if users.is_current_user_admin() else redirect('/employee/')