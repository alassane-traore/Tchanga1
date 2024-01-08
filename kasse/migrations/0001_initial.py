# Generated by Django 3.2.1 on 2024-01-07 23:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=89)),
                ('name', models.CharField(max_length=59)),
                ('begin', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('budget', models.FloatField()),
                ('automate', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=89)),
                ('name', models.CharField(max_length=69)),
                ('booked', models.BooleanField(default=False)),
                ('s', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='goods', to='kasse.sector')),
            ],
        ),
        migrations.CreateModel(
            name='Basket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=89)),
                ('d', models.DateTimeField()),
                ('costs', models.FloatField()),
                ('comment', models.CharField(blank=True, max_length=205, null=True)),
                ('kaufliste', models.ManyToManyField(blank=True, related_name='busket', to='kasse.Goods')),
                ('sector', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='buskets', to='kasse.sector')),
            ],
        ),
    ]