'''
Created on 2011/5/6

@author: korprulu
'''
from django.conf.urls.defaults import patterns
from admin.employee.admin_employee import employeeList, addEmployee,\
    showWorkingHours, deleteEmployee, editEmployee, updateEmployee,\
  Delete_Record, printWorkingHours, showMonthRecord

urlpatterns = patterns('',
                       (r'^/?$', employeeList),
#                       (r'^add_record/?$'),
                       (r'^delete_record/?$', Delete_Record),
#                       (r'^update_record/?$'),
                       (r'^add_employee/?$', addEmployee),
                       (r'^delete_employee/?$', deleteEmployee),
                       (r'^update_employee/?$', updateEmployee),
                       (r'^edit_employee/?$', editEmployee),
                       (r'^show_workinghours/(.*)/?$', showWorkingHours),
                       (r'^show_monthrecord/(.*)/(\d{4})/(\d{1,2})/?$', showMonthRecord),
                       (r'^print_workinghours/(.*)/(\d{4})/(\d{1,2})/?$', printWorkingHours),
#                       (r'^personal?$', personalRecord),
#                       (r'^print_workinghours/?$'),
#                       (r'^show_monthrecord/?$')
                       )