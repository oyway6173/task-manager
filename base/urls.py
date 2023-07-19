from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('logout/', views.logoutPage, name='logout'),

    path('issue/<str:pk>/', views.issue, name='issue'),
    path('issues/<str:pk>/', views.issues, name='issues'),
    path('board/<str:pk>/', views.board, name='board'),
    path('boards/', views.boards, name='boards'),

    path('create_issue/', views.createIssue, name='create-issue'),

    path('update_issue/<str:pk>/', views.updateIssue, name='update-issue'),

    path('delete_comment/<str:pk>', views.deleteComment, name='delete-comment'),
    path('delete_issue/<str:pk>', views.deleteIssue, name='delete-issue'),
]
