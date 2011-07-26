'''
Created on 2011/5/5

@author: korprulu
'''
from django.conf.urls.defaults import patterns, include
from login import login
from index import neo_soa_erp, about, mainPage

urlpatterns = patterns('',
                       (r'^/?$',            mainPage),
                       (r'^about/?$',       about),
                       (r'^NEO_SOA_ERP/?$', neo_soa_erp),
                       (r'^cstp/',          include('cstp.urls')),
                       (r'^mobile/',        include('mobile.urls')),
                       (r'^admin/',         include('admin.urls')),
                       (r'^login/?$',       login),
                       (r'^employee/',      include('employee.urls')), 
                       (r'^file/',          include('file.urls'))
                       )