from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered, NotRegistered

from .models import (
    Project,
    Skill,
    ContactMessage,
    AboutPage,
    AboutBlock,
    TimelineEntry,
    AboutImage,
)

# ---- Admin Klassen ----

class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "featured", "created_at")
    list_filter = ("featured", "created_at")
    search_fields = ("title", "short_description", "description", "tech_stack")
    prepopulated_fields = {"slug": ("title",)}


class SkillAdmin(admin.ModelAdmin):
    list_display = ("key", "category", "level")
    list_filter = ("category", "level")
    search_fields = ("key", "category")
    ordering = ("-level", "key")


class ContactMessageAdmin(admin.ModelAdmin):
    # Falls deine Felder anders heißen: unten anpassen
    list_display = ("name", "email", "created_at")
    list_filter = ("created_at",)
    search_fields = ("name", "email", "message")
    ordering = ("-created_at",)


class AboutBlockInline(admin.TabularInline):
    model = AboutBlock
    extra = 1


class TimelineEntryInline(admin.TabularInline):
    model = TimelineEntry
    extra = 1


class AboutImageInline(admin.TabularInline):
    model = AboutImage
    extra = 1


class AboutPageAdmin(admin.ModelAdmin):
    inlines = [AboutBlockInline, TimelineEntryInline, AboutImageInline]
    list_display = ("title", "updated_at")
    ordering = ("-updated_at",)




def safe_register(model, admin_class):
    try:
        admin.site.unregister(model)
    except NotRegistered:
        pass

    try:
        admin.site.register(model, admin_class)
    except AlreadyRegistered:
        pass


safe_register(Project, ProjectAdmin)
safe_register(Skill, SkillAdmin)
safe_register(ContactMessage, ContactMessageAdmin)
safe_register(AboutPage, AboutPageAdmin)
