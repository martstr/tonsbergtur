from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from nested_admin import NestedModelAdmin, NestedTabularInline

from .models import *

class GeoResponseInline(NestedTabularInline):
    model = GeoResponse
    extra = 0
    readonly_fields = ('created_at', )

class GeoProblemInline(NestedTabularInline):
    model = GeoProblem
    extra = 0
    inlines = [GeoResponseInline]

class KnowledgeTextResponseInline(NestedTabularInline):
    model = KnowledgeTextResponse
    extra = 0
    readonly_fields = ('created_at', )

class KnowledgeTextProblemInline(NestedTabularInline):
    model = KnowledgeTextProblem
    extra = 0
    inlines = [KnowledgeTextResponseInline]

class KnowledgeNumberResponseInline(NestedTabularInline):
    model = KnowledgeNumberResponse
    extra = 0
    readonly_fields = ('created_at', )

class KnowledgeNumberProblemInline(NestedTabularInline):
    model = KnowledgeNumberProblem
    extra = 0
    inlines = [KnowledgeNumberResponseInline]

class OpenResponseInline(NestedTabularInline):
    model = OpenResponse
    extra = 0
    readonly_fields = ('created_at', )

class OpenProblem(NestedTabularInline):
    model = OpenProblem
    extra = 0
    inlines = [OpenResponseInline]

class LocationAdmin(NestedModelAdmin):
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

class TeamNameInline(admin.StackedInline):
    model = ExtendedUser
    can_delete = False

class UserAdmin(BaseUserAdmin):
    inlines = (TeamNameInline, )
  
admin.site.unregister(User)
admin.site.register(User, UserAdmin)