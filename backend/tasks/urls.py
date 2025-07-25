from django.urls import path

from tasks.views import DeleteTaskView, TaskViewSet
from . import views

urlpatterns = [
    path('tasks/', TaskViewSet.as_view({'get':'list','post':'create'})),
    path('tasks/<int:pk>/', TaskViewSet.as_view({'get': 'retrieve','put' : 'update','delete' : 'destroy'})),
    path('tasks/<int:pk>/delete/', DeleteTaskView.as_view()),
    path('register/', views.RegisterView.as_view() , name="register"),
    path('login/',views.LoginView.as_view() , name='login'),
    path('logout/',views.Logout.as_view() , name='logout'),
    path('me',views.MeView.as_view() , name='fetchMe'),
]
