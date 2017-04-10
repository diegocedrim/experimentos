from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from .models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template.defaulttags import register
# Create your views here.


@login_required
def index(request):
    user_subject = UserSubject.objects.get(user__id=request.user.id)
    # usuario encerrou o experimento, nao mostra nada
    if not user_subject.on_experiment:
        return HttpResponseRedirect(reverse('summaries:the_end'))

    summaries = Summary.objects.filter(experiment__id=user_subject.experiment.id)
    answers = []
    for summary in summaries:
        answers.append({"summary":summary, "answer":summary.answer(request.user)})
    context = {'answers': answers}
    return render(request, 'summaries/index.html', context)


@register.filter
def get_item(dictionary, key):
    if len(dictionary[key]) == 0:
        return 'Nenhuma anomalia encontrada'
    return ", ".join(list(dictionary.get(key)))

@login_required
def details(request, summary_id):
    user_subject = UserSubject.objects.get(user__id=request.user.id)
    # usuario encerrou o experimento, nao mostra nada
    if not user_subject.on_experiment:
        return HttpResponseRedirect(reverse('summaries:the_end'))

    summary = get_object_or_404(Summary, pk=summary_id)
    answer = summary.answer(request.user)
    smells_instances = summary.codesmellinstance_set.all()
    if answer:
        # consulta pra cada usuario se ele marcou se a instancia eh smell ou nao
        for instance in smells_instances:
            result = SummaryAnswerCodeSmell.objects.filter(summary_answer__id=answer.id, instance__id=instance.id)
            if result:
                instance.opinion = result[0].opinion
    else:
        answer = SummaryAnswer()
    answer.initialize_ratings()
    opinions = CodeSmellOpinion.objects.all()
    summary.parse_agglomerations()
    context = {'summary': summary,
               'answer':answer,
               'smells_instances':smells_instances,
               'importance': SummaryAnswer.IMPORTANCE,
               'opinions': opinions}
    return render(request, 'summaries/detail.html', context)


def get_smell_answer(answer, instance):
    result = SummaryAnswerCodeSmell.objects.filter(summary_answer__id=answer.id, instance__id=instance.id)
    if result:
        return result[0]
    else:
        sacs = SummaryAnswerCodeSmell()
        sacs.summary_answer = answer
        sacs.instance = instance
        return sacs

@login_required
def save(request, summary_id):
    user_subject = UserSubject.objects.get(user__id=request.user.id)
    # usuario encerrou o experimento, nao mostra nada
    if not user_subject.on_experiment:
        return HttpResponseRedirect(reverse('summaries:the_end'))

    summary = get_object_or_404(Summary, pk=summary_id)
    answer = summary.answer(request.user)
    if answer is None:
        answer = SummaryAnswer()
        answer.user = request.user
        answer.summary = summary
    answer.agglomeration_rating = request.POST.get('rel_aglomeracao', None)
    answer.design_patterns_rating = request.POST.get('rel_dpatterns', None)
    answer.smells_rating = request.POST.get('rel_smells', None)
    answer.design_principles_rating = request.POST.get('rel_dprinciples', None)
    answer.examples_rating = request.POST.get('rel_examples', None)
    answer.non_functional_ratings = request.POST.get('rel_nonfunc', None)
    answer.observations = request.POST['observations']
    answer.save()

    if not summary.experiment.type.is_complete:
        for sinstance in summary.codesmellinstance_set.all():
            smell_answer = get_smell_answer(answer, sinstance)
            opinion_id = request.POST["smell_opinion_%s" % sinstance.id]
            opinion = get_object_or_404(CodeSmellOpinion, pk=opinion_id)
            smell_answer.opinion = opinion
            smell_answer.save()

    return HttpResponseRedirect(reverse('summaries:index'))


@login_required
def the_end(request):
    return render(request, 'summaries/the_end.html')


@login_required
def finish(request):
    subject = UserSubject.objects.get(user__id=request.user.id)
    subject.on_experiment = False
    subject.save()
    return HttpResponseRedirect(reverse('summaries:the_end'))