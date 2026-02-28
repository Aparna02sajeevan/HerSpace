from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Core
    path('', views.landing, name='landing'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='landing'), name='logout'),
    path('signup/', views.signup, name='signup'),

    # Mood
    path('add-mood/', views.add_mood, name='add_mood'),

    # Wellness
    path('meditate/', views.meditate, name='meditate'),
    path('music/', views.music, name='music'),
    path('doodle/', views.doodle, name='doodle'),
    path('drums/', views.drums, name='drums'),

    # Journal
    path('journal/', views.journal, name='journal'),
    path('journal/delete/<int:entry_id>/', views.delete_entry, name='delete_entry'),

    # Growth
    path('goals/', views.goals, name='goals'),
    path('confidence/', views.confidence, name='confidence'),

    # Career
    path('career/', views.career, name='career'),

    # Finance
    path('finance/', views.finance, name='finance'),

    # Emergency
    path('emergency/', views.emergency, name='emergency'),
]