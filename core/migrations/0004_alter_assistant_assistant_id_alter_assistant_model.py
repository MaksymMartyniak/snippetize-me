# Generated by Django 5.0b1 on 2024-01-02 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_assistant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assistant',
            name='assistant_id',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='assistant',
            name='model',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
