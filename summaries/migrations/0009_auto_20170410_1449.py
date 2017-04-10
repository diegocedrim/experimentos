# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-04-10 17:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('summaries', '0008_auto_20170410_1252'),
    ]

    operations = [
        migrations.CreateModel(
            name='Experiment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('system_name', models.CharField(max_length=200)),
                ('experiment_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name='summary',
            name='system',
        ),
        migrations.RemoveField(
            model_name='usersubject',
            name='system',
        ),
        migrations.AddField(
            model_name='summary',
            name='type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='summaries.SummaryType'),
        ),
        migrations.AlterField(
            model_name='summaryanswer',
            name='agglomeration_rating',
            field=models.CharField(blank=True, choices=[('0', 'Irrelevante'), ('1', 'Pouco Relevante'), ('2', 'Bastante Relevante'), ('3', 'Muito Relevante')], default='0', max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='summaryanswer',
            name='design_patterns_rating',
            field=models.CharField(blank=True, choices=[('0', 'Irrelevante'), ('1', 'Pouco Relevante'), ('2', 'Bastante Relevante'), ('3', 'Muito Relevante')], default='0', max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='summaryanswer',
            name='design_principles_rating',
            field=models.CharField(blank=True, choices=[('0', 'Irrelevante'), ('1', 'Pouco Relevante'), ('2', 'Bastante Relevante'), ('3', 'Muito Relevante')], default='0', max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='summaryanswer',
            name='examples_rating',
            field=models.CharField(blank=True, choices=[('0', 'Irrelevante'), ('1', 'Pouco Relevante'), ('2', 'Bastante Relevante'), ('3', 'Muito Relevante')], default='0', max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='summaryanswer',
            name='non_functional_ratings',
            field=models.CharField(blank=True, choices=[('0', 'Irrelevante'), ('1', 'Pouco Relevante'), ('2', 'Bastante Relevante'), ('3', 'Muito Relevante')], default='0', max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='summaryanswer',
            name='smells_rating',
            field=models.CharField(blank=True, choices=[('0', 'Irrelevante'), ('1', 'Pouco Relevante'), ('2', 'Bastante Relevante'), ('3', 'Muito Relevante')], default='0', max_length=1, null=True),
        ),
        migrations.DeleteModel(
            name='System',
        ),
        migrations.AddField(
            model_name='summary',
            name='experiment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='summaries.Experiment'),
        ),
        migrations.AddField(
            model_name='usersubject',
            name='experiment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='summaries.Experiment'),
        ),
    ]