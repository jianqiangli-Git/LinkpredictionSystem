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
        elif content.name == 'age.txt':
            with open(r'F:\myweb\env\movilens\million-ml-data\age.txt') as f:
                while (1):
                    data = f.readline()
                    if data != "":
                        data = data.strip().split(":")
                        age = data[0]
                        description = data[1]
                        # print(age, description)
                        models.Range.objects.bulk_create([models.Range(age=age, description=description)])
                    else:
                        break
            return render(request, 'linkprediction/processResult.html', info)
        elif content.name == 'occupation.txt':
            with open(r'F:\myweb\env\movilens\million-ml-data\occupation.txt') as f:
                while (1):
                    data = f.readline()
                    if data != "":
                        data = data.strip().split(":")
                        id = data[0]
                        discription = data[1]
                        models.Occupation.objects.bulk_create([models.Occupation(id=id, discription=discription)])
                    else:
                        break
            return render(request, 'linkprediction/processResult.html', info)
        elif content.name == 'tag.txt':
            with open(r'F:\myweb\env\movilens\million-ml-data\tag.txt') as f:
                while (1):
                    data = f.readline()
                    if data != "":
                        name = data.strip()
                        models.Tag.objects.bulk_create([models.Tag(tag_name=name)])
                    else:
                        break
            return render(request, 'linkprediction/processResult.html', info)

        elif content.name == 'movies.dat':
            with open(r'F:\myweb\env\mysite\million-ml-data\movies.dat') as f:
                while(1):
                    data = f.readline()
                    if data != '':
                        data = data.strip().split("::")
                        mid = data[0]
                        temp = data[1].split("(")
                        name = temp[0]
                        tags = data[2].split("|")
                        for i in range(len(tags)):
                            models.Movie.objects.create(mid=mid,name=name,tags=models.Tag.objects.get(tag_name=tags[i]))
                    else:
                        break
            return render(request, 'linkprediction/processResult.html', info)
        elif content.name == 'users.dat':
            with open(r'F:\myweb\env\mysite\million-ml-data\users.dat') as f:
                while(1):
                    data = f.readline().strip().split("::")
                    if data != '':
                        name = data[0]
                        password = name
                        sex = data[1]
                        ageRange = data[2]
                        occupation = data[3]
                        models.User.objects.create(name=name,password = password,sex = sex,ageRange=models.Range.objects.get(age=ageRange),occupation=models.Occupation.objects.get(id=occupation))
                    else:
                        break
            return render(request, 'linkprediction/processResult.html', info)
        elif content.name == 'ratings.dat':
            with open(r'F:\myweb\env\mysite\million-ml-data\ratings.dat') as f:
                while (1):
                    data = f.readline()
                    if data != '':
                        data = data.strip().split(" ")
                        #UserID::MovieID::Rating:
                        uid = data[0]
                        mid = data[1]
                        rating = data[2]
                        models.Rating.objects.create(user=models.User.objects.get(name=uid),movie=models.Movie.objects.filter(mid=mid)[0],rating=rating)
                    else:
                        break
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


