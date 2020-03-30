from django.urls import path
from first_app import views
app_name='first_app'
urlpatterns=[
path('sports/',views.sports,name='sports'),
path('politics/',views.politics.as_view(),name='politics'),
path('login/',views.register,name='register'),
path('user_login/',views.user_login,name='user_login'),
path('',views.index,name="index"),
]
