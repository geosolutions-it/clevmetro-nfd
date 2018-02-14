# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nfdcore', '0020_jsonfield_20180213_1422'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='occurrenceobservation',
            name='record_origin',
        ),
        migrations.AddField(
            model_name='occurrenceobservation',
            name='record_origin',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),

        migrations.RemoveField(
            model_name='naturalarealocation',
            name='reservation',
        ),
        migrations.AddField(
            model_name='naturalarealocation',
            name='reservation',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='taxonlocation',
            name='reservation',
        ),
        migrations.AddField(
            model_name='taxonlocation',
            name='reservation',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='naturalarealocation',
            name='watershed',
        ),
        migrations.AddField(
            model_name='naturalarealocation',
            name='watershed',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='taxonlocation',
            name='watershed',
        ),
        migrations.AddField(
            model_name='taxonlocation',
            name='watershed',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='voucher',
            name='preservative',
        ),
        migrations.AddField(
            model_name='voucher',
            name='preservative',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='voucher',
            name='storage',
        ),
        migrations.AddField(
            model_name='voucher',
            name='storage',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),


        migrations.RemoveField(
            model_name='pondlakeanimaldetails',
            name='diseases_and_abnormalities',
        ),
        migrations.AddField(
            model_name='pondlakeanimaldetails',
            name='diseases_and_abnormalities',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='streamanimaldetails',
            name='diseases_and_abnormalities',
        ),
        migrations.AddField(
            model_name='streamanimaldetails',
            name='diseases_and_abnormalities',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='wetlandanimaldetails',
            name='diseases_and_abnormalities',
        ),
        migrations.AddField(
            model_name='wetlandanimaldetails',
            name='diseases_and_abnormalities',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='landanimaldetails',
            name='diseases_and_abnormalities',
        ),
        migrations.AddField(
            model_name='landanimaldetails',
            name='diseases_and_abnormalities',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='pondlakeanimaldetails',
            name='marks',
        ),
        migrations.AddField(
            model_name='pondlakeanimaldetails',
            name='marks',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='streamanimaldetails',
            name='marks',
        ),
        migrations.AddField(
            model_name='streamanimaldetails',
            name='marks',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='wetlandanimaldetails',
            name='marks',
        ),
        migrations.AddField(
            model_name='wetlandanimaldetails',
            name='marks',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='landanimaldetails',
            name='marks',
        ),
        migrations.AddField(
            model_name='landanimaldetails',
            name='marks',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='pondlakeanimaldetails',
            name='gender',
        ),
        migrations.AddField(
            model_name='pondlakeanimaldetails',
            name='gender',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='streamanimaldetails',
            name='gender',
        ),
        migrations.AddField(
            model_name='streamanimaldetails',
            name='gender',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='wetlandanimaldetails',
            name='gender',
        ),
        migrations.AddField(
            model_name='wetlandanimaldetails',
            name='gender',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='landanimaldetails',
            name='sampler',
        ),
        migrations.AddField(
            model_name='landanimaldetails',
            name='sampler',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='landanimaldetails',
            name='stratum',
        ),
        migrations.AddField(
            model_name='landanimaldetails',
            name='stratum',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='slimemolddetails',
            name='slime_mold_class',
        ),
        migrations.AddField(
            model_name='slimemolddetails',
            name='slime_mold_class',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='slimemolddetails',
            name='slime_mold_media',
        ),
        migrations.AddField(
            model_name='slimemolddetails',
            name='slime_mold_media',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='observedassociations',
            name='gnat_association',
        ),
        migrations.AddField(
            model_name='observedassociations',
            name='gnat_association',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='observedassociations',
            name='ants_association',
        ),
        migrations.AddField(
            model_name='observedassociations',
            name='ants_association',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='observedassociations',
            name='termite_association',
        ),
        migrations.AddField(
            model_name='observedassociations',
            name='termite_association',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='observedassociations',
            name='beetles_association',
        ),
        migrations.AddField(
            model_name='observedassociations',
            name='beetles_association',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='observedassociations',
            name='snow_flea_association',
        ),
        migrations.AddField(
            model_name='observedassociations',
            name='snow_flea_association',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='observedassociations',
            name='slug_association',
        ),
        migrations.AddField(
            model_name='observedassociations',
            name='slug_association',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='observedassociations',
            name='snail_association',
        ),
        migrations.AddField(
            model_name='observedassociations',
            name='snail_association',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='observedassociations',
            name='skunk_association',
        ),
        migrations.AddField(
            model_name='observedassociations',
            name='skunk_association',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='observedassociations',
            name='badger_association',
        ),
        migrations.AddField(
            model_name='observedassociations',
            name='badger_association',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='observedassociations',
            name='easter_gray_squirrel_association',
        ),
        migrations.AddField(
            model_name='observedassociations',
            name='easter_gray_squirrel_association',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='observedassociations',
            name='chipmunk_association',
        ),
        migrations.AddField(
            model_name='observedassociations',
            name='chipmunk_association',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='observedassociations',
            name='other_small_rodent_association',
        ),
        migrations.AddField(
            model_name='observedassociations',
            name='other_small_rodent_association',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='observedassociations',
            name='turtle_association',
        ),
        migrations.AddField(
            model_name='observedassociations',
            name='turtle_association',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='observedassociations',
            name='deer_association',
        ),
        migrations.AddField(
            model_name='observedassociations',
            name='deer_association',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='fungusdetails',
            name='aspect',
        ),
        migrations.AddField(
            model_name='fungusdetails',
            name='aspect',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='fungusdetails',
            name='apparent_substrate',
        ),
        migrations.AddField(
            model_name='fungusdetails',
            name='apparent_substrate',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='fungusdetails',
            name='landscape_position',
        ),
        migrations.AddField(
            model_name='fungusdetails',
            name='landscape_position',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='fungusdetails',
            name='mushroom_growth_form',
        ),
        migrations.AddField(
            model_name='fungusdetails',
            name='mushroom_growth_form',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='fungusdetails',
            name='mushroom_odor',
        ),
        migrations.AddField(
            model_name='fungusdetails',
            name='mushroom_odor',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='fungusdetails',
            name='mushroom_vertical_location',
        ),
        migrations.AddField(
            model_name='fungusdetails',
            name='mushroom_vertical_location',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='fungusdetails',
            name='slope',
        ),
        migrations.AddField(
            model_name='fungusdetails',
            name='slope',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='elementnaturalareas',
            name='aspect',
        ),
        migrations.AddField(
            model_name='elementnaturalareas',
            name='aspect',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='elementnaturalareas',
            name='bedrock_and_outcrops',
        ),
        migrations.AddField(
            model_name='elementnaturalareas',
            name='bedrock_and_outcrops',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='elementnaturalareas',
            name='sensitivity',
        ),
        migrations.AddField(
            model_name='elementnaturalareas',
            name='sensitivity',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='elementnaturalareas',
            name='glaciar_diposit',
        ),
        migrations.AddField(
            model_name='elementnaturalareas',
            name='glaciar_diposit',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='elementnaturalareas',
            name='pleistocene_glaciar_diposit',
        ),
        migrations.AddField(
            model_name='elementnaturalareas',
            name='pleistocene_glaciar_diposit',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='elementnaturalareas',
            name='landscape_position',
        ),
        migrations.AddField(
            model_name='elementnaturalareas',
            name='landscape_position',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='elementnaturalareas',
            name='leap_land_cover_category',
        ),
        migrations.AddField(
            model_name='elementnaturalareas',
            name='leap_land_cover_category',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='elementnaturalareas',
            name='condition',
        ),
        migrations.AddField(
            model_name='elementnaturalareas',
            name='condition',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='elementnaturalareas',
            name='type',
        ),
        migrations.AddField(
            model_name='elementnaturalareas',
            name='type',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='elementnaturalareas',
            name='regional_frequency',
        ),
        migrations.AddField(
            model_name='elementnaturalareas',
            name='regional_frequency',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='elementnaturalareas',
            name='slope',
        ),
        migrations.AddField(
            model_name='elementnaturalareas',
            name='slope',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]
