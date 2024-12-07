from .views import TaskList,TaskDetail,TaskCreate,TaskUpdate,TaskDelete,CustomLoginView,RegisterPage
from django.urls import path,include
#from  django.contrib.auth.views import LogoutView
from . import views



urlpatterns = [
    path('',TaskList.as_view(),name='task'),
    path('task-create/',TaskCreate.as_view(),name='task-create'),
    path('task/<int:pk>/',TaskDetail.as_view(),name='tasks-detail'),
    path('task-update/<int:pk>/',TaskUpdate.as_view(),name='tasks-update'),
    path('task-delete/<int:pk>/',TaskDelete.as_view(),name='tasks-delete'),
    path('login/', CustomLoginView.as_view(),name='login'),
    #path('logout/', LogoutView.as_view(next_page='login'), name="logout"),
    path('logout/', views.logout_view , name ='logout'),
    path('register/', RegisterPage.as_view(), name="register"),
    path('api/v1/',include('todo.api.v1.urls'))

    
    
]
