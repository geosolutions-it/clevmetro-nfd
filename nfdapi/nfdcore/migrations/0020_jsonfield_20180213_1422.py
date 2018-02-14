# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nfdcore', '0019_auto_20180212_1635'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pondlakeanimaldetails',
            name='sampler',
        ),
        migrations.AddField(
            model_name='pondlakeanimaldetails',
            name='sampler',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='pondlakeanimaldetails',
            name='microhabitat',
        ),
        migrations.AddField(
            model_name='pondlakeanimaldetails',
            name='microhabitat',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='pondlakeanimaldetails',
            name='pond_lake_use',
        ),
        migrations.AddField(
            model_name='pondlakeanimaldetails',
            name='pond_lake_use',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='pondlakeanimaldetails',
            name='shoreline_type',
        ),
        migrations.AddField(
            model_name='pondlakeanimaldetails',
            name='shoreline_type',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),


        migrations.RemoveField(
            model_name='streamanimaldetails',
            name='sampler',
        ),
        migrations.AddField(
            model_name='streamanimaldetails',
            name='sampler',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='streamanimaldetails',
            name='channel_type',
        ),
        migrations.AddField(
            model_name='streamanimaldetails',
            name='channel_type',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='streamanimaldetails',
            name='hmfei_local_abundance',
        ),
        migrations.AddField(
            model_name='streamanimaldetails',
            name='hmfei_local_abundance',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='streamanimaldetails',
            name='lotic_habitat_type',
        ),
        migrations.AddField(
            model_name='streamanimaldetails',
            name='lotic_habitat_type',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),


        migrations.RemoveField(
            model_name='wetlandanimaldetails',
            name='sampler',
        ),
        migrations.AddField(
            model_name='wetlandanimaldetails',
            name='sampler',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='wetlandanimaldetails',
            name='water_source',
        ),
        migrations.AddField(
            model_name='wetlandanimaldetails',
            name='water_source',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='wetlandanimaldetails',
            name='habitat_feature',
        ),
        migrations.AddField(
            model_name='wetlandanimaldetails',
            name='habitat_feature',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='wetlandanimaldetails',
            name='wetland_type',
        ),
        migrations.AddField(
            model_name='wetlandanimaldetails',
            name='wetland_type',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),


        migrations.RemoveField(
            model_name='coniferdetails',
            name='aspect',
        ),
        migrations.AddField(
            model_name='coniferdetails',
            name='aspect',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='ferndetails',
            name='aspect',
        ),
        migrations.AddField(
            model_name='ferndetails',
            name='aspect',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='floweringplantdetails',
            name='aspect',
        ),
        migrations.AddField(
            model_name='floweringplantdetails',
            name='aspect',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='mossdetails',
            name='aspect',
        ),
        migrations.AddField(
            model_name='mossdetails',
            name='aspect',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='coniferdetails',
            name='general_habitat_category',
        ),
        migrations.AddField(
            model_name='coniferdetails',
            name='general_habitat_category',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='ferndetails',
            name='general_habitat_category',
        ),
        migrations.AddField(
            model_name='ferndetails',
            name='general_habitat_category',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='floweringplantdetails',
            name='general_habitat_category',
        ),
        migrations.AddField(
            model_name='floweringplantdetails',
            name='general_habitat_category',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='mossdetails',
            name='general_habitat_category',
        ),
        migrations.AddField(
            model_name='mossdetails',
            name='general_habitat_category',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='coniferdetails',
            name='ground_surface',
        ),
        migrations.AddField(
            model_name='coniferdetails',
            name='ground_surface',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='ferndetails',
            name='ground_surface',
        ),
        migrations.AddField(
            model_name='ferndetails',
            name='ground_surface',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='floweringplantdetails',
            name='ground_surface',
        ),
        migrations.AddField(
            model_name='floweringplantdetails',
            name='ground_surface',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='mossdetails',
            name='ground_surface',
        ),
        migrations.AddField(
            model_name='mossdetails',
            name='ground_surface',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='coniferdetails',
            name='landscape_position',
        ),
        migrations.AddField(
            model_name='coniferdetails',
            name='landscape_position',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='ferndetails',
            name='landscape_position',
        ),
        migrations.AddField(
            model_name='ferndetails',
            name='landscape_position',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='floweringplantdetails',
            name='landscape_position',
        ),
        migrations.AddField(
            model_name='floweringplantdetails',
            name='landscape_position',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='mossdetails',
            name='landscape_position',
        ),
        migrations.AddField(
            model_name='mossdetails',
            name='landscape_position',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='coniferdetails',
            name='moisture_regime',
        ),
        migrations.AddField(
            model_name='coniferdetails',
            name='moisture_regime',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='ferndetails',
            name='moisture_regime',
        ),
        migrations.AddField(
            model_name='ferndetails',
            name='moisture_regime',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='floweringplantdetails',
            name='moisture_regime',
        ),
        migrations.AddField(
            model_name='floweringplantdetails',
            name='moisture_regime',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='mossdetails',
            name='moisture_regime',
        ),
        migrations.AddField(
            model_name='mossdetails',
            name='moisture_regime',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='coniferdetails',
            name='slope',
        ),
        migrations.AddField(
            model_name='coniferdetails',
            name='slope',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='ferndetails',
            name='slope',
        ),
        migrations.AddField(
            model_name='ferndetails',
            name='slope',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='floweringplantdetails',
            name='slope',
        ),
        migrations.AddField(
            model_name='floweringplantdetails',
            name='slope',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='mossdetails',
            name='slope',
        ),
        migrations.AddField(
            model_name='mossdetails',
            name='slope',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='ferndetails',
            name='lifestages',
        ),
        migrations.AddField(
            model_name='ferndetails',
            name='lifestages',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='floweringplantdetails',
            name='lifestages',
        ),
        migrations.AddField(
            model_name='floweringplantdetails',
            name='lifestages',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='mossdetails',
            name='lifestages',
        ),
        migrations.AddField(
            model_name='mossdetails',
            name='lifestages',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]
