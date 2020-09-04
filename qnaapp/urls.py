from django.urls import path
from . import views

urlpatterns = [
    path("", views.qnaread, name="qnaread"),
    path("qnacreate", views.qnacreate, name="qnacreate"),
    path('answer/<int:pk>', views.admin_answer, name='admin_answer'),
    path("qnadetail/<int:pk>", views.qnadetail, name="qnadetail"),
    path('qnaregister/', views.qnaregister, name="qnaregister"),
    path('qnalogin/', views.qnalogin, name="qnalogin"),
    path('qnalogout/', views.qnalogout, name="qnalogout"),
    path('qnamember/', views.qnamember, name="qnamember"),
]