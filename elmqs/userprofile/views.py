from django.shortcuts import render

# Create your views here.
from .forms import UserLoginForm,UserRegisterForm

from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.http import  HttpResponse

def user_login(request):
    if request.method == 'POST':
        user_login_form = UserLoginForm(request.POST)
        if user_login_form.is_valid():
            username = user_login_form.cleaned_data.get('username')
            password = user_login_form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect("article:article_list")
            else:
                return HttpResponse('登陆账号或密码错误，无效的登陆')
    elif request.method == 'GET':
        # 创建一个新的 UserLoginForm 实例，用于处理用户登录
        user_login_form = UserLoginForm()

        # 将表单实例放入上下文字典中，以便在模板中使用
        context = {'form': user_login_form}

        # 渲染 'userprofile/login.html' 模板，并将上下文传递给模板
        return render(request, 'userprofile/login.html', context)

    else:
        return HttpResponse('非法的方法')

def user_logout(request):
    logout(request)
    return redirect("article:article_list")


def user_register(request):
    if request.method == 'POST':
        user_register_form = UserRegisterForm(request.POST)
        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            #设置密码
            new_user.set_password(user_register_form.cleaned_data['password'])
            new_user.save()
            #保存完数据立即登陆并返回博客列表页面
            login(request,new_user)
            return redirect("article:article_list")
        else:
            return HttpResponse('注册失败')
    elif request.method == 'GET':
        # 创建一个新的 UserRegisterForm 实例，用于处理用户注册
        user_register_form = UserRegisterForm()

        # 将表单实例放入上下文字典
        context = {'form': user_register_form}

        # 渲染 'userprofile/register.html' 模板，并将上下文传递给模板
        return render(request, 'userprofile/register.html', context)

    else:
        return HttpResponse('非法的方法')