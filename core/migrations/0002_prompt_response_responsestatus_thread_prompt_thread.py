# Generated by Django 5.0b1 on 2023-11-11 20:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Prompt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prompt_text', models.CharField(max_length=2048)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('framework', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.framework')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.programminglanguage')),
                ('option', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.option')),
            ],
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original_text', models.TextField(blank=True, null=True)),
                ('first_snippet', models.TextField(blank=True, null=True)),
                ('second_snippet', models.TextField(blank=True, null=True)),
                ('comparison_text', models.TextField(blank=True, null=True)),
                ('api_response_id', models.CharField(max_length=128)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('prompt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.prompt')),
            ],
        ),
        migrations.CreateModel(
            name='ResponseStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField()),
                ('err_msg', models.TextField()),
                ('response', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.response')),
            ],
        ),
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='prompt',
            name='thread',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.thread'),
        ),
    ]
