from django.test import TestCase
from django.urls import reverse

from .models import Project, Skill, ContactMessage


class ProjectModelTests(TestCase):
    def test_project_slug_autocreated(self):
        p = Project.objects.create(
            title="My First Project",
            short_description="Short",
            description="Long description",
            tech_stack="Django, CSS",
            featured=True,
        )
        self.assertTrue(p.slug)
        self.assertEqual(str(p), "My First Project")


class ViewsTests(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            title="Demo Project",
            short_description="Short",
            description="Long description",
            tech_stack="Django",
            featured=True,
        )
        Skill.objects.create(name="Django", level=4, category="Backend")

    def test_home_page(self):
        r = self.client.get(reverse("home"))
        self.assertEqual(r.status_code, 200)
        self.assertTemplateUsed(r, "portfolio/home.html")

    def test_projects_list(self):
        r = self.client.get(reverse("projects"))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Demo Project")

    def test_project_detail(self):
        r = self.client.get(reverse("project_detail", kwargs={"slug": self.project.slug}))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Demo Project")

    def test_skills_page(self):
        r = self.client.get(reverse("skills"))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Django")

    def test_contact_post_creates_message(self):
        r = self.client.post(
            reverse("contact"),
            data={
                "name": "Test User",
                "email": "test@example.com",
                "subject": "Hello",
                "message": "Test message",
            },
            follow=True,
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), 1)
