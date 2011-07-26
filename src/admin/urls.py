'''
Created on 2011/5/6

@author: korprulu
'''
from django.conf.urls.defaults import patterns, include
from admin.index import mainPage

urlpatterns = patterns('',
                       (r'^/?$', mainPage),
                       (r'^employee/', include('admin.employee.urls')),
                       (r'^archive/', include('admin.archive.urls')),
                       (r'^publish/', include('admin.publish.urls'))
                       )