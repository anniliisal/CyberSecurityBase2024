from django.urls import path
from . import views
from django.urls import include
app_name = 'polls'

urlpatterns = [
    # Index page
    path('', views.index, name='index'),
    
    # Vote page
    path('<int:question_id>/vote/', views.vote, name='vote'),
    
    # Search results page
    path('search/', views.search, name='search'),
    
    # Create question page
    path('create/', views.create_question, name='create_question'),
    
    # Detail page for a specific question
    path('<int:question_id>/', views.detail, name='detail'),
    
    # Debug info page
    path('debug/', views.debug_info, name='debug_info'),

    #  URLs for registration
    path('register/', views.register, name='register'),  
    path('registrationsuccess/', views.registrationsuccess, name='registrationsuccess'),  

    path('accounts/', include('django.contrib.auth.urls')),
]
