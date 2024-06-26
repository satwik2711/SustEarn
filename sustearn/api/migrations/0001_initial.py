# Generated by Django 4.2.1 on 2024-04-14 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('life_cycle_stages', models.JSONField()),
                ('weights', models.JSONField()),
                ('weighted_average_emission', models.FloatField()),
                ('optimized_emission', models.FloatField()),
            ],
        ),
    ]
