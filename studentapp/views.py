from django.shortcuts import render, redirect, reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.core.signing import Signer
from django.contrib import messages
from .models import Student
from datetime import datetime

# Create your views here.
def register(request):
    enc_data = None
    if request.method == 'POST':
        sname = request.POST['name']
        sroll = request.POST['roll']
        sbirth = request.POST['birth']
        session_1st = request.POST['1st_session']
        session_2nd = request.POST['2nd_session']
        shift = request.POST['shift']
        exist = Student.objects.filter(roll=sroll).exists()
        if exist:
            messages.error(request, "Student already Exist in database")
            
        else:
            stud = Student.objects.create(name=sname, roll=sroll, birth_date=sbirth, shift=shift, session=f"{session_1st} to {session_2nd}")
            stud.save()
            s = Signer()
            enc_data = s.sign_object({sroll: sbirth})
            messages.success(request, "Student added in database")
    return render(request, "register.html", {'data': enc_data})

def login(request):
    if request.method == 'POST':
        roll = request.POST.get("roll")
        birth = request.POST.get("dateofbirth")
        if student:=student_authenticate(roll, birth):
            s = Signer()
            enckey = s.sign_object({roll:birth})
            return redirect('dashboard', pk=enckey)
            #TODO: redirect with encrypted roll and birthdate
    
    return render(request, "login.html")

def student_authenticate(roll=None, birth=None):
        try:
            student = Student.objects.get(roll = roll)
        except ValueError as e:
            print(e)
        except Student.DoesNotExist as e:
            print(e)

        else:
            if datetime.strftime(student.birth_date, "%Y-%m-%d") == birth:
                return student
            else:
                return False

def dashboard(request, pk):
    s = Signer()
    roll_birth = s.unsign_object(pk)
    roll, birth = tuple(roll_birth.items())[0]
    
    return render(request, 'dashboard.html',{'student':{'name':birth, "roll":roll}, "qr_data":pk})

@staff_member_required
def all_student(request):
    all_s = Student.objects.all()
    return render(request, "all_student.html", {'student_list': all_s})

@staff_member_required
def student_details(request, pk):
    try:
        student = Student.objects.get(pk=pk)
        session1, session2 = student.session.split(" to ")
        if request.method == 'POST':
            update_name = request.POST.get('name')
            update_birth_date = request.POST.get("birth_date")
            update_session1 = request.POST.get("session1")
            update_session2 = request.POST.get("session2")
            u_session = f"{update_session1} to {update_session2}"
            student.name = update_name
            student.birth_date = update_birth_date
            student.session = u_session
            student.save()
            return redirect("all-student")
        else:
            messages.error(request ,"Can't update details")
    except Exception as a:
        print(a)
    return render(request, 'student_details.html', {'student': student, 'student_session1':session1, 'student_session2': session2})