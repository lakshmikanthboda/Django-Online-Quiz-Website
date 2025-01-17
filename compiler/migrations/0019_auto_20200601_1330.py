# Generated by Django 3.0.6 on 2020-06-01 08:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('compiler', '0018_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='quizes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, unique=True)),
            ],
            options={
                'verbose_name': 'quiz',
                'verbose_name_plural': 'quizes',
                'db_table': '',
                'managed': True,
            },
        ),
        migrations.AlterField(
            model_name='register',
            name='name',
            field=models.CharField(max_length=153),
        ),
        migrations.CreateModel(
            name='quizquestions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000)),
                ('option1', models.CharField(max_length=100)),
                ('option2', models.CharField(max_length=100)),
                ('option3', models.CharField(max_length=100)),
                ('option4', models.CharField(max_length=100)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='compiler.quizes')),
            ],
            options={
                'verbose_name': 'question',
                'verbose_name_plural': 'questions',
                'db_table': '',
                'managed': True,
            },
        ),
    ]
