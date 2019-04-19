from django.shortcuts import render
from django.shortcuts import redirect

from django.template import loader
from django.http import Http404,HttpResponse
from django.shortcuts import render,get_object_or_404
from django.urls import reverse
from django.views import generic
from . import models
import os

content = None

def index(request):
    return render(request,'linkprediction/index.html')


def login(request):
    if request.session.get('is_login', None):
        return redirect('linkprediction:index')

    if request.method == "POST":
        username = request.POST.get('username',None)
        password = request.POST.get('password','PASSWARD')
        message = None
        if username and password:
            username = username.strip()
            try:
                user = models.User.objects.get(name=username)
                if user.password == password:
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('linkprediction:index')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'linkprediction/login.html',{'message':message})
    else:
        return render(request, 'linkprediction/login.html')


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect('linkprediction:logout_action')
    request.session.flush()
    return redirect('linkprediction:logout_action')

def logout_action(request):
    return render(request,'linkprediction/nologin.html')

def upload_action(request):
    message = '文件上传完成！'
    info = {'message': message}
    if request.method == 'POST':  # 获取对象
        content = request.FILES.get('myfile')
        if content == None:
            return render(request, 'linkprediction/processResult.html')
        elif content.name == 'movies.dat':
            # for m in content.chunks():
            #     data = m.decode().strip().split("::")
            #     movieID = data[0]
            #     temp = data[1].split("(")
            #     name = temp[0]
            #     tags = data[2].split("|")
            #     models.Movie.objects.bulk_create([models.Movie(name=name,tags=models.Tag.objects.get(tag_name=tags[i])) for i in range(len(tags))])
            return render(request, 'linkprediction/processResult.html', info)
        elif content.name == 'users.dat':
            for i in content:
                data = i.strip().split("::")
                name = data[0]
                pwd = data[0]
                gender =  lambda x:'male' if x=='M' else 'female'
                sex = gender(data[1])
            return render(request, 'linkprediction/processResult.html', info)
        elif content.name == 'ratings.dat':
            return render(request, 'linkprediction/processResult.html', info)
        else:
            info['message'] = '你上传了其他文件！'
            return render(request, 'linkprediction/processResult.html', info)


def recommend(request):
    return render(request,'linkprediction/recommend.html')


# 处理前端开始训练的请求
def train(request):
    return HttpResponse("好的，我开始训练，将要获得当前节点 TopK 个节点~")

# 接收训练结果产生的前top K 个节点，使用 result.html 渲染到前端
def presentation(request):
    return render(request,'linkprediction/result.html')
    # return HttpResponse("好的，我开始执行推荐算法，展示 TopK 个节点的电影信息")


