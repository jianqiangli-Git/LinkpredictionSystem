from django.contrib import admin

# Register your models here.
# we need to tell the admin that Question objects have an admin interface. 
from .models import Movie,User,Occupation,Range,Tag


admin.site.register(Movie)
admin.site.register(User)
admin.site.register(Occupation)
admin.site.register(Range)
admin.site.register(Tag)
