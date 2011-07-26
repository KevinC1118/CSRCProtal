'''
Created on 2011/5/9

@author: korprulu
'''
from django.conf.urls.defaults import patterns
from employee.main import personalRecord, addRecord, showMonthRecord,\
    printWorkingHours, deleteRecord

urlpatterns = patterns('',
                       (r'^/?$', personalRecord),
                       (r'^add_record/?$', addRecord),
                       (r'^show_monthrecord/(\d{4})/(\d{1,2})/?$', showMonthRecord),
                       (r'^print_workinghours/(\d{4})/(\d{1,2})/?$', printWorkingHours),
                       (r'^delete_record/?$', deleteRecord)
                       )