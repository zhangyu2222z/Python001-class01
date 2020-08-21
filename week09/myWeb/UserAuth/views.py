from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .form import LoginForm

# Create your views here.

# 跳转登录页
def logon(request):
    login_form = LoginForm()
    return render(request, 'login.html', {'form': login_form})

# 登录验证接口
def enter(request):
    # 创建用户：python manage.py migrate
    #          python manage.py shell
    #          >>>from django.contrib.auth.models import User
    #          >>>user = User(username='zhangy',password='zhangy123456') # 此保存方式密码会明文保存不会加密
    #          >>>user = User.objects.create_user('zhangy2', 'zhangy4321@qq.com', 'zhangy123456')
    #          >>>user.save()
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # 读取表单的返回值
            cd = login_form.cleaned_data 
            print(cd['username'])
            print(cd['password'])
            user = authenticate(username=cd['username'], password=cd['password'])
            if user:
                login(request, user)  
                return render(request, 'welcome.html')
            else:
                login_form = LoginForm()
                return render(request, 'login.html', {'form': login_form, 'errorInfo':'用户名或密码错误！'})
    if request.method == "GET":
        login_form = LoginForm()
        return render(request, 'login.html', {'form': login_form})