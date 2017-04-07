from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User

# Create your models here.


@python_2_unicode_compatible
class System(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Summary(models.Model):
    element_fqn = models.CharField(max_length=1000)
    similar_summaries = models.ManyToManyField("self", symmetrical=False, blank=True)
    system = models.ForeignKey(System, on_delete=models.CASCADE)

    # (elemento1[smell1, smell2, smell3, ...];elemento2[smell1,smell2...];A
    # opcoes de tipo de relacionamento:
    #   - A: Association (biderecional)
    #   - I: Inheritance
    #   - R: Realization
    agglomeration = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.element_fqn

    def answer(self, user):
        result = SummaryAnswer.objects.filter(summary__id=self.id, user__id=user.id)
        if result:
            return result[0]
        return None

    def element_fqn_short(self):
        return self.element_fqn.split(".")[-1]

    def parse_node(self, element):
        if "[" in element:
            fqn = element[:element.find("[")]
            smells = [i.strip() for i in element[element.find("[") + 1: -1].split(",")]
        else:
            fqn = element
            smells = set()
        return {"fqn": fqn, "smells":smells}

    def parse_agglomerations(self):
        self.nodes = set()
        self.edges = set()
        self.smells = {}
        if not self.agglomeration:
            return
        agg_parts = [i.strip() for i in self.agglomeration.split("\n")]
        for part in agg_parts:
            el_from, el_to, rel = part.split(";")
            node_from = self.parse_node(el_from)
            self.nodes.add(node_from["fqn"])
            if node_from["fqn"] not in self.smells:
                self.smells[node_from["fqn"]] = node_from["smells"]

            node_to = self.parse_node(el_to)
            self.nodes.add(node_to["fqn"])
            if node_to["fqn"] not in self.smells:
                self.smells[node_to["fqn"]] = node_to["smells"]

            self.edges.add((node_from["fqn"], node_to["fqn"], rel))


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

    def elements_list(self):
        return [i.strip() for i in self.elements_involved.split("\n")]

    def __str__(self):
        return self.design_pattern.name


@python_2_unicode_compatible
class SummaryAnswer(models.Model):
    summary = models.ForeignKey(Summary, on_delete=models.CASCADE)
    observations = models.TextField(default='')
    user = models.ForeignKey(User)
    IMPORTANCE = (
        ('0', 'Irrelevante'),
        ('1', 'Relevante'),
        ('2', 'Muito Relevante')
    )
    agglomeration_rating = models.CharField(max_length=1, choices=IMPORTANCE, default='0', blank=True, null=True)
    design_patterns_rating = models.CharField(max_length=1, choices=IMPORTANCE, default='0', blank=True, null=True)
    smells_rating = models.CharField(max_length=1, choices=IMPORTANCE, default='0', blank=True, null=True)
    design_principles_rating = models.CharField(max_length=1, choices=IMPORTANCE, default='0', blank=True, null=True)
    examples_rating = models.CharField(max_length=1, choices=IMPORTANCE, default='0', blank=True, null=True)
    non_functional_ratings = models.CharField(max_length=1, choices=IMPORTANCE, default='0', blank=True, null=True)



    def __str__(self):
        return "Answer of %s to %s" % (self.user.username, self.summary.element_fqn)


class SummaryAnswerCodeSmell(models.Model):
    summary_answer = models.ForeignKey(SummaryAnswer, on_delete=models.CASCADE)
    instance = models.ForeignKey(CodeSmellInstance, on_delete=models.CASCADE)
    is_smell = models.BooleanField()


class UserSubject(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    system = models.ForeignKey(System, on_delete=models.CASCADE)
    on_experiment = models.BooleanField(default=True)