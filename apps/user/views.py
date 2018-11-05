from django.shortcuts import render, redirect
from django.urls import reverse
from user.models import User
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from django.conf import settings
from django.views.generic import View
from django.http import HttpResponse
from django.core.mail import send_mail

import re

# Create your views here.


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        '''接收参数，数据校验'''
        username = request.POST.get('user_name')
        pwd = request.POST.get('pwd')
        cpwd = request.POST.get('cpwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')
        if not all([username, pwd, cpwd]):
            '''数据不完整'''
            return render(request, 'register.html', {'errmsg': '数据不完整'})
        '''校验邮箱'''
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errmsg': '邮箱格式不正确'})
        '''验证协议'''
        if allow != 'on':
            return render(request, 'register.html', {'errmsg': '请同意协议'})
        '''是否重名'''
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None

        if user:
            return render(request, 'register.html', {'errmsg': '已有该用户名'})

        '''业务处理'''
        user = User.objects.create_user(username, email, pwd)
        user.is_active = False
        user.save()
        # user.username = username
        # user.password = pwd
        # user.email = email
        # user.save()
        '''发送激活邮件'''
        # 激活用户需要判断用户的激活信息并且加密 链接：/user/active/xx
        # 加密用户身份信息
        serializer = Serializer(settings.SECRET_KEY, 60 * 10)
        info = {'conf': user.id}
        token = serializer.dumps(info).decode('utf-8')
        # 发送邮件
        subject = '天天生鲜欢迎信息'
        message = ''
        htmlmessage = '<h1>欢迎 %s 加入天天生鲜</h1></br><a href = "http://127.0.0.1:8000/user/active/%s">http://127.0.0.1:8000/user/active/%s</a>' % (username, token, token)
        sender = settings.EMAIL_FROM  # 发件人
        receiver = [email]  # 收件人列表
        send_mail(subject, message, sender, recipient_list=receiver, html_message=htmlmessage)
        '''返回应答跳转到首页'''
        # /goods/index
        url = reverse('goods:index')
        print(url)
        return redirect(url)


class ActiveView(View):
    def get(self, request, token):
        serializer = Serializer(settings.SECRET_KEY, 60 * 10)
        try:
            info = serializer.loads(token)
            user_id = info['conf']
            user = User.objects.get(id=user_id)
            user.is_active = True
            user.save()
            return redirect(reverse('user:login'))
        except SignatureExpired:
            # 激活链接国企
            return HttpResponse("激活链接过期")


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('pwd')
