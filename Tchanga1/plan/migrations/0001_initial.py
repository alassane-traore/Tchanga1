# Generated by Django 3.2.1 on 2024-01-07 23:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Kategories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=85)),
                ('kategorie', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='weecklines',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=85)),
                ('week', models.IntegerField()),
                ('line', models.CharField(max_length=89)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(null=True)),
                ('author', models.CharField(max_length=85)),
                ('begin', models.TimeField()),
                ('end', models.TimeField()),
                ('task', models.CharField(max_length=89)),
                ('classi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='plan.kategories')),
            ],
        ),
        migrations.CreateModel(
            name='dates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=85)),
                ('date', models.DateField()),
                ('actitivies', models.ManyToManyField(blank=True, related_name='dates', to='plan.Task')),
            ],
        ),
    ]