from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("projects/", views.ProjectsView.as_view(), name="projects"),
    path("projects/<slug:slug>/", views.ProjectDetailView.as_view(), name="project_detail"),
    path("about/", views.about_view, name="about"),
    path("skills/", views.SkillsView.as_view(), name="skills"),
    path("contact/", views.ContactView.as_view(), name="contact"),
    path("experiences/", views.experiences, name="experiences"),
]
