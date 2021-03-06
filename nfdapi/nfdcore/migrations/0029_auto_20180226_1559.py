# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-26 15:59
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nfdcore', '0028_auto_20180226_1315'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='landanimaldetails',
            name='lifestages',
        ),
        migrations.AddField(
            model_name='landanimaldetails',
            name='lifestages',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='pondlakeanimaldetails',
            name='lifestages',
        ),
        migrations.AddField(
            model_name='pondlakeanimaldetails',
            name='lifestages',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='streamanimaldetails',
            name='lifestages',
        ),
        migrations.AddField(
            model_name='streamanimaldetails',
            name='lifestages',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='wetlandanimaldetails',
            name='lifestages',
        ),
        migrations.AddField(
            model_name='wetlandanimaldetails',
            name='lifestages',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='AnimalLifestages',
        ),
    ]
