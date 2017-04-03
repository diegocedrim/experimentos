from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.


@python_2_unicode_compatible
class Summary(models.Model):
    element_fqn = models.CharField(max_length=1000)
    similar_summaries = models.ManyToManyField("self", symmetrical=False)
    agglomeration = models.OneToOneField(
        "Agglomeration",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.element_fqn

    class Meta:
        verbose_name = 'Summary'
        verbose_name_plural = 'Summaries'


@python_2_unicode_compatible
class CodeSmell(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class CodeSmellInstance(models.Model):
    summary = models.ForeignKey(Summary, on_delete=models.CASCADE, blank=True, null=True)
    smell = models.ForeignKey(CodeSmell, on_delete=models.CASCADE)
    is_part_of_agglomeration = models.BooleanField()
    affected_element = models.CharField(max_length=1000)
    reason = models.TextField()

    def __str__(self):
        return "%s em %s" % (self.smell.name, self.affected_element)


@python_2_unicode_compatible
class DesignPrinciple(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class DesignPrincipleInstance(models.Model):
    summary = models.ForeignKey(Summary, on_delete=models.CASCADE, blank=True, null=True)
    design_principle = models.ForeignKey(DesignPrinciple, on_delete=models.CASCADE)

    def __str__(self):
        return self.design_principle.name


@python_2_unicode_compatible
class NonFunctionalAttribute(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class NonFunctionalAttributeInstance(models.Model):
    summary = models.ForeignKey(Summary, on_delete=models.CASCADE, blank=True, null=True)
    non_functional_attribute = models.ForeignKey(NonFunctionalAttribute, on_delete=models.CASCADE)

    def __str__(self):
        return self.non_functional_attribute.name


@python_2_unicode_compatible
class DesignPattern(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class DesignPatternInstance(models.Model):
    summary = models.ForeignKey(Summary, on_delete=models.CASCADE, blank=True, null=True)
    design_pattern = models.ForeignKey(DesignPattern, on_delete=models.CASCADE)
    elements_involved = models.TextField(default='')

    def __str__(self):
        return self.design_pattern.name


class Agglomeration(models.Model):
    elements = models.ManyToManyField("AgglomerationElement", symmetrical=False)
    relationships = models.ManyToManyField("ElementRelationship", symmetrical=False)


@python_2_unicode_compatible
class AgglomerationElement(models.Model):
    fqn = models.CharField(max_length=250)

    def __str__(self):
        return self.fqn


class ElementRelationship(models.Model):
    element_from = models.ForeignKey(AgglomerationElement, on_delete=models.CASCADE, related_name='element_from')
    element_to = models.ForeignKey(AgglomerationElement, on_delete=models.CASCADE, related_name='element_to')
    RELATIONSHIP_CHOICES = (
        ('A', 'Association'),
        ('DA', 'Directed Association'),
        ('AG', 'Aggregation'),
        ('C', 'Composition'),
        ('I', 'Inheritance'),
        ('R', 'Realization'),
    )
    relationship = models.CharField(
        max_length=2,
        choices=RELATIONSHIP_CHOICES,
        default='A'
    )

    def __str__(self):
        return "(%s)-[%s]->(%s)" % (self.element_from.fqn, self.relationship, self.element_to.fqn)

# @python_2_unicode_compatible
# class Agglomeration(models.Model):
#     summary = models.ForeignKey(Summary, on_delete=models.CASCADE)
#
#
#
#
# @python_2_unicode_compatible
# class DesignPatternElement(models.Model):
#     summary = models.ForeignKey(DesignPattern, on_delete=models.CASCADE)
#     element_fqn = models.CharField(max_length=1000)
#
#
# @python_2_unicode_compatible
# class DesignPrinciple(models.Model):
#     name = models.CharField(max_length=200)
#     description = models.TextField()
#     summary = models.ForeignKey(Summary, on_delete=models.CASCADE)