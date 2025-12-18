from django.db import models
from django.utils.text import slugify


class Project(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    short_description = models.CharField(max_length=220)
    description = models.TextField()
    tech_stack = models.CharField(max_length=220, blank=True)
    repo_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    cover_image = models.ImageField(upload_to="projects/", blank=True, null=True)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-featured", "-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)[:120] or "project"
            slug = base
            i = 1
            while Project.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                i += 1
                slug = f"{base}-{i}"
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title



SKILL_CHOICES = [
    ("python", "Python"),
    ("html5", "HTML"),
    ("css3", "CSS"),
    ("django", "Django"),
    ("flask", "Flask"),
    ("r", "R"),
    ("rstudio", "RStudio"),
    ("notion", "Notion"),
    ("sql", "SQL"),
    ("git", "Git"),
    ("github", "GitHub"),
    ("gitlab", "GitLab"),
    ("linux", "Linux"),
    ("docker", "Docker"),
    ("postgresql", "PostgreSQL"),
    ("sqlite", "SQLite"),
    ("mongodb", "MongoDB"),
    ("neo4j", "Neo4j"),
    ("jupyter", "Jupyter"),
    ("sklearn", "Scikit-learn"),
    ("numpy", "NumPy"),
    ("pandas", "Pandas"),
    ("matplotlib", "Matplotlib"),
    ("seaborn", "Seaborn"),
    ("pytest", "Pytest"),
    ("vscode", "VS Code"),
    ("excel", "Excel"),
    ("powerbi", "Power BI"),
    ("opencv", "OpenCV"),
]

CATEGORY_CHOICES = [
    ("coding", "Coding"),
    ("data", "Data"),
    ("web", "Web"),
    ("database", "Database"),
    ("tools", "Tools"),
    ("devops", "DevOps"),
]

class Skill(models.Model):
    key = models.CharField(max_length=40, choices=SKILL_CHOICES, unique=True)
    category = models.CharField(max_length=40, choices=CATEGORY_CHOICES, default="tools")
    level = models.PositiveSmallIntegerField(default=3)

    class Meta:
        ordering = ["-level", "key"]

    def __str__(self):
        return dict(SKILL_CHOICES).get(self.key, self.key)


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    subject = models.CharField(max_length=160)
    message = models.TextField(max_length=500, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.subject} — {self.email}"
    
    
class AboutPage(models.Model):
    title = models.CharField(max_length=120, default="About")
    subtitle = models.CharField(max_length=220, blank=True, default="")
    intro = models.TextField(blank=True, default="")
    profile_image = models.ImageField(upload_to="about/", blank=True, null=True)
    cv_file = models.FileField(upload_to="cv/", blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "About Page"
        verbose_name_plural = "About Page"

    def __str__(self):
        return "About Page"

class AboutBlock(models.Model):
    page = models.ForeignKey(AboutPage, on_delete=models.CASCADE, related_name="blocks")
    heading = models.CharField(max_length=120)
    body = models.TextField(blank=True, default="")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.heading

class TimelineEntry(models.Model):
    page = models.ForeignKey(AboutPage, on_delete=models.CASCADE, related_name="timeline")
    year_from = models.CharField(max_length=20, blank=True, default="")
    year_to = models.CharField(max_length=20, blank=True, default="")
    title = models.CharField(max_length=120)
    subtitle = models.CharField(max_length=160, blank=True, default="")
    body = models.TextField(blank=True, default="")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title

class AboutImage(models.Model):
    page = models.ForeignKey(AboutPage, on_delete=models.CASCADE, related_name="gallery")
    image = models.ImageField(upload_to="about/gallery/")
    caption = models.CharField(max_length=160, blank=True, default="")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.caption or "About Image"