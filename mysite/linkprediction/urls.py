from django.urls import path
from . import views

# app_name 是应用的命名空间，用来区分不同应用的名称相同的 url(比如 name 都叫 detail)
app_name = 'linkprediction'

# urls 用作通过查找 urlpatterns 选取 url 定向到 views 中对应的函数，path 的第一个参数会从地址栏中输入的 url(经过ROOT_URLCONF剥去了一部分) 匹配对应的 url(即Route)，
# 然后定向到对应的view 函数，然后执行函数展示函数对应的页面
urlpatterns = [
    path(r'',views.login,name='login'),
    path(r'index',views.index,name='index'),
    path(r'logout',views.logout,name='logout'),
    path(r'upload',views.upload_action,name='upload_action'),
    path(r'recommend',views.recommend,name='recommend'),
    path(r'train',views.train,name='train'),
    path(r'presentation',views.presentation,name='presentation'),
    path(r'logout_action',views.logout_action,name='logout_action'),
    path(r'movies_process',views.movies_process,name='movies_process'),
    path(r'users_process',views.users_process,name='users_process'),
    path(r'ratings_process',views.ratings_process,name='ratings_process'),
    path(r'other_process',views.other_process,name='other_process'),
    path(r'none_process',views.none_process,name='none_process'),
]

