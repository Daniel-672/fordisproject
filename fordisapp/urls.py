from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf.urls import  include, url
from django.conf import settings


urlpatterns = [
    path('', views.index, name="index"),
    path('register/', views.register, name="register"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),

    path('report/', views.report, name="report"),
    path('board/', views.board, name="board"),

    path('<int:pk>', views.detail, name='detail'),
    path('<slug:btype>/<int:pk>', views.detail, name='detail'),

    path('<int:pk>/update/', views.update, name='update'),
    path('<slug:btype>/<int:pk>/update/', views.update, name='update'),
    path('<slug:btype>/<int:article_pk>/comments/<int:comment_pk>/update/', views.comment_update, name='comment_update'),
    path('<slug:btype>/<int:article_pk>/comments/<int:comment_pk>/update/<int:comment2_pk>/update/', views.comment2_update, name='comment2_update'),

    path('create/', views.create, name='create'),
    path('<slug:btype>/create/', views.create, name='create'),
    path('<slug:btype>/<int:pk>/comments/create/', views.comment_create, name='comment_create'),
    path('<slug:btype>/<int:ppk>/<int:pk>/comments2/create/', views.comment2_create, name='comment2_create'),

    path('<slug:btype>/<int:pk>/delete/', views.delete, name='delete'),
    path('<slug:btype>/<int:article_pk>/comments/<int:comment_pk>/delete/', views.comment_delete, name='comment_delete'),
    path('<slug:btype>/<int:article_pk>/comments/<int:comment_pk>/delete/<int:comment2_pk>/delete/', views.comment2_delete,
         name='comment2_delete'),

    path("search1/<slug:btype>/<nickname>", views.search1, name="search1"),
    path("search2/<slug:btype>/<content>", views.search2, name="search2"),

    path("checknick/", views.checknick, name="checknick"),
    path("checkuseremail/", views.checkuseremail, name="checkuseremail"),

    path("getaccesstoken/", views.getaccesstoken, name="getaccesstoken"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)