# Generated by Django 5.0b1 on 2024-01-02 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_assistant_assistant_id_alter_assistant_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='thread',
            name='open_ai_run_id',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='thread',
            name='open_ai_thread_id',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='thread',
            name='title',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]