# Generated by Django 3.0.6 on 2020-06-01 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compiler', '0025_quizes_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizes',
            name='disc',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
