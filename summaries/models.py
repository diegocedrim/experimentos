# coding=utf-8
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

# se é um sumário pra identificar problemas de design
@python_2_unicode_compatible
class ExperimentType(models.Model):
    description = models.CharField(max_length=100)

    # se é completo ou se é só sobre smells
    is_complete = models.BooleanField(default=True)

    def __str__(self):
        return self.description


@python_2_unicode_compatible
class System(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Experiment(models.Model):
    system = models.ForeignKey(System, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)
    type = models.ForeignKey(ExperimentType, on_delete=models.CASCADE, null=True)

    # se a gente deve mostrar o painel "Qual a relevância desta seção?"
    should_get_feedback = models.BooleanField(default=True)

    # se True, omite os campos de feedback das secoes de code smells e "principios de qualidade"
    # tambem troca o nome do campo de principios de qualidade pra Concerns
    is_bene_experiment = models.BooleanField(default=False)

    # se a gente deve mostrar o painel "Validação do Problema"
    should_present_validation_field = models.BooleanField(default=True)

    def __str__(self):
        if self.system is not None:
            return "%s/%s" % (self.system.name, self.name)
        else:
            return self.name


@python_2_unicode_compatible
class Summary(models.Model):
    element_fqn = models.CharField(max_length=1000)
    similar_summaries = models.ManyToManyField("self", symmetrical=False, blank=True)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, null=True)


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

    def similar_by_smell(self, user):
        smells_instances = self.codesmellinstance_set.all()
        already_similar = self.similar_summaries.all()
        similar = set()
        for instance in smells_instances:
            answers = SummaryAnswerCodeSmell.objects.filter(summary_answer__user_id=user.id,
                                              instance__smell__name=instance.smell.name,
                                              opinion__is_smell=True)
            for answer in answers:
                summary_candidate = answer.summary_answer.summary
                if summary_candidate not in already_similar and summary_candidate.id != self.id:
                    similar.add(summary_candidate)
        return similar

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
            if ";" not in part:
                node = self.parse_node(part)
                self.nodes.add(node["fqn"])
                self.smells[node["fqn"]] = node["smells"]
                continue

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
class DesignProblem(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class DesignPrincipleInstance(models.Model):
    summary = models.ForeignKey(Summary, on_delete=models.CASCADE, blank=True, null=True)
    design_principle = models.ForeignKey(DesignPrinciple, on_delete=models.CASCADE)
    reason = models.TextField(null=True, blank=True)

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
    reason = models.TextField(null=True, blank=True)

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
    reason = models.TextField(null=True, blank=True)

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
        ('1', 'Pouco Relevante'),
        ('2', 'Bastante Relevante'),
        ('3', 'Muito Relevante')
    )
    agglomeration_rating = models.CharField(max_length=1, choices=IMPORTANCE, default=None, blank=True, null=True)
    design_patterns_rating = models.CharField(max_length=1, choices=IMPORTANCE, default=None, blank=True, null=True)
    smells_rating = models.CharField(max_length=1, choices=IMPORTANCE, default=None, blank=True, null=True)
    design_principles_rating = models.CharField(max_length=1, choices=IMPORTANCE, default=None, blank=True, null=True)
    examples_rating = models.CharField(max_length=1, choices=IMPORTANCE, default=None, blank=True, null=True)
    non_functional_ratings = models.CharField(max_length=1, choices=IMPORTANCE, default=None, blank=True, null=True)

    NAMES = {
        'agglomeration_rating': 'Aglomerações',
        'design_patterns_rating': ' Padrões de Projeto',
        'smells_rating': 'Anomalias de Código (Code Smells)',
        'design_principles_rating': ' Princípios de Design Violados',
        'examples_rating': 'Sumários com Características Similares',
        'non_functional_ratings': 'Atributos Não Funcionais Violados',
    }

    def validate(self):
        for prop, value in vars(self).iteritems():
            if "_ratings" in prop and value is None:
                return prop
        return None

    def __str__(self):
        return "Answer of %s to %s" % (self.user.username, self.summary.element_fqn)


#  opiniao dos desenvolvedores para cada uma das instancias de code smell
@python_2_unicode_compatible
class CodeSmellOpinion(models.Model):
    opinion = models.TextField()
    is_smell = models.BooleanField(default=False)

    def __str__(self):
        return self.opinion


#  representa dados associados a uma instancia de um code smell respondidos por um usuario
@python_2_unicode_compatible
class SummaryAnswerCodeSmell(models.Model):
    summary_answer = models.ForeignKey(SummaryAnswer, on_delete=models.CASCADE)
    instance = models.ForeignKey(CodeSmellInstance, on_delete=models.CASCADE)
    opinion = models.ForeignKey(CodeSmellOpinion, on_delete=models.CASCADE, null=True)

    # se foi importante para detectar um problema de design
    was_important = models.NullBooleanField()

    def __str__(self):
        return "%s of %s by %s" % (self.instance.smell.name, self.summary_answer.summary, self.summary_answer.user)


@python_2_unicode_compatible
class UserSubject(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, null=True)
    on_experiment = models.BooleanField(default=True)

    def __str__(self):
        return "%s" % self.user
