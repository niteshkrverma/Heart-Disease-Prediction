from xml.etree.ElementTree import Comment
from django.shortcuts import render,redirect
from django.contrib.auth.models import User,Group
from django.http import HttpResponseRedirect
from . import forms
from django.contrib import messages
from datetime import datetime
from .models import register_table,subscribe,Heart_Disease,feedbackd,Contact
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
import joblib
from . import forms,models
# Create your views here.
def index(request):
    return render(request,"index.html")
def about(request):
    return render(request,"users/about.html")
def contact(request):
    return render(request,"users/contact.html")
def register(request):
    if request.method=="POST":
        fname = request.POST["first"]
        last = request.POST["last"]
        un = request.POST["uname"]
        pwd = request.POST["password"]
        em = request.POST["email"]
        gn = request.POST["gender"]
        ag = request.POST["age"]
        ct = request.POST["city"]
        con = request.POST["contact"]
        tp = request.POST["utype"]
        userty=request.POST["utype"]
        
        usr = User.objects.create_user(un,em,pwd)
        usr.first_name = fname
        usr.last_name = last
        
        if tp=="doctor":
            usr.is_staff = True
        usr.save()
        
        reg = register_table(user=usr, contact_number=con,usertype=userty,gender=gn,city=ct,age=ag)
        if userty=="doctor":
            reg.usertype="doctor"
            reg.save()
            return render(request,"base.html",{"status":"Mr/Miss. {} your Account created Successfully".format(fname)})
        else:
            reg.usertype="client"
            reg.save()
            return render(request,"base.html",{"status":"Mr/Miss. {} your Account created Successfully".format(fname)})
    return render(request,"base.html",{"status":"Sorry Try Again!"})

def login_user(request):
    if request.method=="POST":
        un = request.POST["username"]
        pwd = request.POST["password"]

        user = authenticate(username=un,password=pwd)
        if user:
            login(request,user)
            if user.is_superuser:

                return HttpResponseRedirect("/admin-dashboard")
            if user.is_staff:
                messages.success(request,'Login Successfully! !')
                return HttpResponseRedirect("/doctor-dashboard")
            if user.is_active:
                messages.success(request,'Login Successfully!')
                return HttpResponseRedirect("/user-dashboard",{'user':'user'})
        else:
            return render(request,"base.html",{"status":"Invalid Username or Password"})

    return render(request,"base.html")
def user_logout(request):
    logout(request)
    return redirect('/')

def Subscribe(request):
    if request.method=="POST":
        email=request.POST['email']
        sub=subscribe(email=email)
        sub.save()
        messages.success(request,'Now you are subscribe user !')
    return HttpResponseRedirect("/")
@login_required(login_url='/login')
def test(request):
    m=messages.success(request,'Login Successfully!')
    return render(request,"users/DataInput.html",{'m':m})
@login_required(login_url='/login')
def result(request):
    b=models.User.objects.filter(id=request.user.id).values('id')
    bb=models.User.objects.get(id=request.user.id)
    print(b)
    print(bb)
    cls=joblib.load('final_model.sav')
    lis=[]
    
    city=request.GET['city']
    a1=request.GET['age']
    a2=request.GET['gender']
    a3=request.GET['cp']
    a4=request.GET['rbp']
    a5=request.GET['sc']
    a6=request.GET['BS']
    a7=request.GET['elec']
    a8=request.GET['mhr']
    a9=request.GET['exang']
    a10=request.GET['op']
    a11=request.GET['Slope']
    a12=request.GET['ca']
    a13=request.GET['thal']
    dic={'1':a1,'2':a2,'3':a3,'4':a4,'5':a5,'6':a6,'7':a7,'8':a8,'9':a9,'10':a10,'11':a11,'12':a12,'13':a13}
    
    lis.append(a1)
    lis.append(a2)
    lis.append(a3)
    lis.append(a4)
    lis.append(a5)
    lis.append(a6)
    lis.append(a7)
    lis.append(a8)
    lis.append(a9)
    lis.append(a10)
    lis.append(a11)
    lis.append(a12)
    lis.append(a13)
    for i in range(0, len(lis)):
        lis[i] = int(lis[i])
    ans=cls.predict([lis])
    print(dic)
    heart=Heart_Disease(user=bb,city=city,age=a1,sex=a2,cp=a3,trestbps=a4,chol=a5,fbs=a6,restecg=a7,thalach=a8,exang=a9,oldpeak=a10,slope=a11,ca=a12,thal=a13,Date=datetime.today(),result=ans)
    heart.save()
    return render(request,"users/result.html",{'ans':ans,'dic':dic})

# -------User----
@login_required(login_url='/login')
def user_dashboard(request):
    context = {}
    check = register_table.objects.filter(user__id=request.user.id)
    if len(check)>0:
        data = register_table.objects.get(user__id=request.user.id)
        context["data"] = data
    return render(request,'users/Dashboard.html',context)
@login_required(login_url='/login')
def DataInput(request):
    # m=messages.success(request,'For Predict ')
    return render(request,"users/DataInput.html")
@login_required(login_url='/login')
def report(request):
    id=models.User.objects.get(id=request.user.id)
    data=models.Heart_Disease.objects.all().filter(user=id)
    return render(request,'users/report.html',{'id':id,'data':data})
@login_required(login_url='/login')
def feedback(request):
    b=models.User.objects.filter(id=request.user.id).values('id')
    bb=models.User.objects.get(id=request.user.id)
    if request.method == "POST":
        experience = request.POST.get('experience')
        comments = request.POST.get('comments')
        print(bb,experience,comments)
        d = feedbackd(user=bb,experience=experience, comment=comments,date=datetime.today())
        d.save()
        messages.success(request,'Thank you!')
        return redirect('/')
    return render(request,'users/feedback.html')
# ----------Doctors------------
@login_required(login_url='/login')
def doctor_dashboard(request):
    return render(request,'doctors/Dashboard.html')
@login_required(login_url='/login')
def Patient(request):
    p=register_table.objects.all().filter(usertype="client")
    return render(request,'doctors/Patient1.html',{'p':p})
#-------------------------------Admin----------
@login_required(login_url='/login')
def admin_dashboard(request):
    dic={
        'total_customer':User.objects.all().filter(is_staff=False).count(),
        'x':register_table.objects.all().filter(usertype="doctor").count(),
        # 'y':feedbackd.objects.count(),
        'y':Heart_Disease.objects.count(),
        }
    return render(request,'admin/Dashboard.html',context=dic)

@login_required(login_url='/login')
def Admin_View_Patient(request):
    p=register_table.objects.all().filter(usertype="client")
    return render(request,'Admin/Patient.html',{'p':p})
@login_required(login_url='/login')
def Admin_View_Doctor(request):
    p=register_table.objects.all().filter(usertype="doctor")
    return render(request,'Admin/Doctor.html',{'p':p})
def Admin_View_Feedback(request):
    p=feedbackd.objects.all()
    return render(request,'Admin/feedbacklist.html',{'p':p}) 

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')
        contact = Contact(name=name, email=email, phone=phone, desc=desc, date = datetime.today())
        contact.save()
        messages.success(request,'Your message has been sent!')
    return render(request,'users/contact.html')  

@login_required(login_url='/login')
def contact_views(request):
    x=Contact.objects.all()
    return render(request,'admin/contact.html',{'x':x})
def admin_view_report(request):
    x=Heart_Disease.objects.all()
    return render(request,'admin/report.html',{'x':x})

