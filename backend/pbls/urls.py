from django.urls import path
from django.urls.resolvers import URLPattern

from . import views

app_name ="pbls"
urlpatterns = [
    path('view_backlog_all/<int:project_id>', views.view_all, name='view_backlog_all'),
    path('register_offered_sp', views.register_offered_sp, name='register_offered_sp'),
    path('read_pbl',views.read_pbl,name='read_pbl'),
    path('register_backlog', views.register_backlog, name='register_backlog'),
    path('view_offered_sp/<int:selected_backlog_id>', views.view_offered_sp, name='view_offered_sp'),
    path('register_pbl_sp', views.register_pbl_sp, name='register_pbl_sp'),
    path('update_backlog', views.update_backlog, name='update_backlog'),
    path('update_offered_sp', views.update_offered_sp, name='update_offered_sp'),
    path('delete_backlog', views.delete_backlog, name='delete_backlog'),
    path('update_priority', views.update_priority, name='update_priority'),
    path('read_transferred_pbl', views.read_transferred_pbl, name='read_transferred_pbl'),
    path('view_project_all', views.view_project_all, name='view_project_all'),
    path('register_project', views.register_project, name='register_project'),
    path('delete_project', views.delete_project, name='delete_project'),
    path('delete_user_sp', views.delete_user_sp, name='delete_user_sp'),
]
