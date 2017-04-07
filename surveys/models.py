# coding=utf-8
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from summaries.models import UserSubject


# Create your models here.
@python_2_unicode_compatible
class SubjectCharacterizationSurvey(models.Model):
    name = models.CharField(max_length=200)

    EDUCATION = (
        ('Doutorado', 'Doutorado'),
        ('Mestrado', 'Mestrado'),
        ('Graduação', 'Graduação'),
        ('Curso Técnico', 'Curso Técnico'),
        ('Sem Educação Formal', 'Não possuo educação formal em computação'),
    )
    education = models.CharField(max_length=30, choices=EDUCATION, default='Sem Educação Formal',
                                 verbose_name='Selecione sua maior titulação na área de computação ou área afins')

    experience = models.IntegerField(verbose_name='Experiência em desenvolvimento de software (em anos) na indústria')

    experience_java = models.IntegerField(verbose_name='Experiência com linguagem de programação Java (em anos) na indústria')

    projects_java = models.IntegerField(verbose_name='Quantos projetos em Java você trabalhou na indústria?')

    def __str__(self):
        return self.name
