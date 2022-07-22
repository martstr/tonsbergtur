from django.contrib import admin
from .models import *

class GeoProblemInline(admin.TabularInline):
    model = GeoProblem
    extra = 0

class KnowledgeTextProblemInline(admin.TabularInline):
    model = KnowledgeTextProblem
    extra = 0

class KnowledgeNumberProblemInline(admin.TabularInline):
    model = KnowledgeNumberProblem
    extra = 0

class OpenProblem(admin.TabularInline):
    model = OpenProblem
    extra = 0

class LocationAdmin(admin.ModelAdmin):
    inlines = [
        GeoProblemInline,
        KnowledgeTextProblemInline,
        KnowledgeNumberProblemInline,
        OpenProblem,
    ]

# Register your models here.
admin.site.register(Location, LocationAdmin)
#admin.site.register(GeoProblem)
#admin.site.register(KnowledgeTextProblem)
#admin.site.register(KnowledgeNumberProblem)