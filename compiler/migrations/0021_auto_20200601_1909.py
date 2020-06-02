# Generated by Django 3.0.6 on 2020-06-01 13:39

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('compiler', '0020_quizquestions_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizes',
            name='time',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quizes',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]