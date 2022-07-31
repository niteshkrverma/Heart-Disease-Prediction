from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    
    path('',views.index),
    path('about/',views.about),
    path('contact/',views.contact),
    path('register/',views.register),
    path('login/',views.login_user),
    path('user-dashboard',views.user_dashboard),
    path('DataInput',views.DataInput),
    path('report',views.report,name="report"),
    path('doctor-dashboard',views.doctor_dashboard),
    path("user_logout/",views.user_logout),
    path("subscribe",views.Subscribe),
    path('feedback',views.feedback,name="feedback"),
    path('contact/',views.contact,name="contact"),
    # ------admin------urls

    path('admin-dashboard',views.admin_dashboard),
    path('admin-view-doctor',views.Admin_View_Doctor),
    path('admin-view-patient',views.Admin_View_Patient),
    path('admin-view-feedback',views.Admin_View_Feedback),
    path('admin-view-contact',views.contact_views),
    path('viewreport',views.admin_view_report),
    #-----Doctor---
    path('patient',views.Patient),
    path('test>',views.test,name="test"),
    path('result',views.result,name='result'),
]