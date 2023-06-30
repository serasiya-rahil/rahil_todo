
from http.client import HTTPResponse
from django.contrib import admin
from django.urls import path
from app.views import home, login, signup, add_todo, signout, delete_todo, change_todo, update_todo


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('login/', login, name='login'),
    path('signup/', signup),
    path('add-todo/', add_todo),
    path('logout/', signout ),
    path('delete-todo/<int:id>', delete_todo),
    path('change-status/<int:id>/<str:status>', change_todo),
    path('update-todo/<int:id>', update_todo),
]
