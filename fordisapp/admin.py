from django.contrib import admin
from .models import Users, Article, Comment, Comment2, Qnaboard

admin.site.register(Users)
admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(Comment2)
admin.site.register(Qnaboard)