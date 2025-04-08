from django.urls import path
from app.views.auth.auth import LoginView, RegisterView
from app.views.management.management import DashboardView, VoteDetailView


urlpatterns = [
    path("", LoginView.as_view(), name="login"),
    path("register", RegisterView.as_view(), name="register"),
    path('dashboard', DashboardView.as_view(), name='dashboard'),
    path("poll/<str:pk>", VoteDetailView.as_view(), name="vote_detail"),
]