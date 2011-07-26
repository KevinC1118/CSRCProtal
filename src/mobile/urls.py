'''
Created on 2011/5/6

@author: korprulu
'''
from django.conf.urls.defaults import patterns, include

urlpatterns = patterns('',
                       (r'^cstp/',  include('mobile.cstp.urls'))
                       )