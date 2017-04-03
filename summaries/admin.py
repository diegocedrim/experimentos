from django.contrib import admin

# Register your models here.
from .models import *


class CodeSmellInstanceInline(admin.StackedInline):
    model = CodeSmellInstance
    extra = 1
    exclude = ('is_smell',)


class DesignPrincipleInstanceInline(admin.StackedInline):
    model = DesignPrincipleInstance
    extra = 1


class NonFunctionalAttributeInstanceInline(admin.StackedInline):
    model = NonFunctionalAttributeInstance
    extra = 1


class DesignPatternInstanceInline(admin.StackedInline):
    model = DesignPatternInstance
    extra = 1


class SummaryAdmin(admin.ModelAdmin):
    inlines = [CodeSmellInstanceInline, DesignPrincipleInstanceInline,
               NonFunctionalAttributeInstanceInline, DesignPatternInstanceInline]
    list_display = ('element_fqn',)


admin.site.register(AgglomerationElement)
admin.site.register(ElementRelationship)
admin.site.register(Agglomeration)
admin.site.register(CodeSmell)
admin.site.register(DesignPrinciple)
admin.site.register(DesignPattern)
admin.site.register(NonFunctionalAttribute)
admin.site.register(Summary, SummaryAdmin)
