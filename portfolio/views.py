from django.views.generic import TemplateView, ListView, DetailView, FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import render
from django.db.models import Q

from .models import Project, Skill, ContactMessage, AboutPage
from .forms import ContactForm


class HomeView(TemplateView):
    template_name = "portfolio/home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["featured_projects"] = Project.objects.filter(featured=True).order_by("-created_at")[:3]
        ctx["latest_projects"] = Project.objects.all().order_by("-created_at")[:6]
        ctx["skills"] = Skill.objects.all().order_by("-level", "key")[:12]
        return ctx



from django.db.models import Q

class ProjectsView(ListView):
    template_name = "portfolio/projects.html"
    model = Project
    context_object_name = "projects"
    paginate_by = 8
    ordering = ["-created_at"]

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get("q")
        skill_id = self.request.GET.get("skill")
        featured = self.request.GET.get("featured")

        if q:
            queryset = queryset.filter(
                Q(title__icontains=q)
                | Q(short_description__icontains=q)
                | Q(description__icontains=q)
                | Q(tech_stack__icontains=q)
            )

        if skill_id:
            queryset = queryset.filter(skills__id=skill_id)

        if featured:
            queryset = queryset.filter(featured=True)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["skills"] = Skill.objects.all()
        context["q"] = self.request.GET.get("q", "")
        context["selected_skill"] = self.request.GET.get("skill", "")
        context["selected_featured"] = self.request.GET.get("featured", "")
        return context




class ProjectDetailView(DetailView):
    template_name = "portfolio/project_detail.html"
    model = Project
    context_object_name = "project"
    slug_field = "slug"
    slug_url_kwarg = "slug"


def about_view(request):
    
    page, _ = AboutPage.objects.get_or_create(id=1, defaults={"title": "About"})
    return render(request, "portfolio/about.html", {"page": page})


class SkillsView(TemplateView):
    template_name = "portfolio/skills.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["skills"] = Skill.objects.all().order_by("-level", "key")
        return ctx


class ContactView(FormView):
    template_name = "portfolio/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("contact")

    def form_valid(self, form):
        ContactMessage.objects.create(
            name=form.cleaned_data["name"],
            email=form.cleaned_data["email"],
            subject=form.cleaned_data["subject"],
            message=form.cleaned_data["message"],
        )
        messages.success(self.request, "Nachricht gespeichert. Danke!")
        return super().form_valid(form)