from django.contrib import admin

# Register your models here.
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


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
    list_display = ('element_fqn','experiment')


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class UserSubjectInline(admin.StackedInline):
    model = UserSubject
    can_delete = False
    verbose_name_plural = 'subjects'


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserSubjectInline, )


class SummaryAnswerCodeSmellInline(admin.StackedInline):
    model = SummaryAnswerCodeSmell
    extra = 1


class SummaryAnswerAdmin(admin.ModelAdmin):
    inlines = [SummaryAnswerCodeSmellInline]
    # list_display = ('element_fqn','system')


admin.site.register(CodeSmellOpinion)
admin.site.register(SummaryAnswerCodeSmell)
admin.site.register(Experiment)
admin.site.register(ExperimentType)
admin.site.register(System)
admin.site.register(SummaryAnswer, SummaryAnswerAdmin)
admin.site.register(CodeSmell)
admin.site.register(DesignPrinciple)
admin.site.register(DesignPattern)
admin.site.register(NonFunctionalAttribute)
admin.site.register(Summary, SummaryAdmin)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
