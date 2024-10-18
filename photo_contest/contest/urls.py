from django.urls import path
from .import views


urlpatterns = [
    path('home/',views.home,name='index'),
    path('about/',views.about,name = 'about'),
    path('contest/',views.contest,name = 'contest'),
    
    path('login/',views.login_page,name='login'),
    path('signup/',views.signup_page,name='signup'),
    path('login_save/',views.login_save,name='login_save'),
    path('signup_save/',views.signup_save,name='signup_save'),
    path('contest_create/',views.create_contest,name="create_contest"),
    path('add_contest/',views.add_contest,name='add_contest'),
    path('post_contest/<int:contest_id>/', views.contest_details, name='post_contest'),
    path('photo/<int:photo_id>/like/', views.like_photo, name='like_photo'),
    path('winner/<int:contest_id>/', views.show_winner, name='winner'),
    path('logout/', views.logout_view, name='logout'),
   

    
]
