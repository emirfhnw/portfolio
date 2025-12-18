from django.test import TestCase
from django.urls import reverse

from .models import Experience, Project, Skill


class PortfolioTests(TestCase):
    def setUp(self):
        self.skill_python = Skill.objects.create(key="python", category="coding", level=5)
        self.skill_django = Skill.objects.create(key="django", category="web", level=4)

        self.project_a = Project.objects.create(
            title="Analyse App",
            short_description="Datenanalyse mit Charts",
            description="Auswertung und Visualisierung.",
            tech_stack="Python",
            featured=True,
        )
        self.project_a.skills.add(self.skill_python)

        self.project_b = Project.objects.create(
            title="Blog",
            short_description="Einfacher Blog",
            description="Schreiben und Veröffentlichen.",
            tech_stack="Django",
        )
        self.project_b.skills.add(self.skill_django)

        Experience.objects.create(title="Werkstudent", company="ACME")

    def test_pages_status_200(self):
        urls = [
            reverse("home"),
            reverse("projects"),
            reverse("skills"),
            
        ]
        for url in urls:
            resp = self.client.get(url)
            self.assertEqual(resp.status_code, 200)

    def test_project_search(self):
        resp = self.client.get(reverse("projects"), {"q": "Analyse"})
        self.assertContains(resp, "Analyse App")
        self.assertNotContains(resp, "Blog")

    def test_project_filter_by_skill(self):
        resp = self.client.get(reverse("projects"), {"skill": str(self.skill_django.id)})
        self.assertContains(resp, "Blog")
        self.assertNotContains(resp, "Analyse App")

    def test_project_skill_relation(self):
        self.assertIn(self.skill_python, self.project_a.skills.all())
        self.assertIn(self.project_a, self.skill_python.projects.all())
        self.assertNotIn(self.skill_python, self.project_b.skills.all())

