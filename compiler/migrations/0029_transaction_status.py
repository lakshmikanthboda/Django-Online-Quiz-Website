# Generated by Django 3.0.6 on 2020-06-02 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compiler', '0028_auto_20200602_0739'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]