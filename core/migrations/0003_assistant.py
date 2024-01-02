# Generated by Django 5.0b1 on 2024-01-02 13:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_prompt_response_responsestatus_thread_prompt_thread'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assistant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assistant_id', models.CharField(max_length=256)),
                ('name', models.CharField(max_length=128)),
                ('instruction', models.TextField()),
                ('model', models.CharField(max_length=256)),
                ('framework', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.framework')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.programminglanguage')),
                ('option', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.option')),
            ],
        ),
    ]
