# Generated by Django 5.1.7 on 2025-04-18 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('citas', '0009_especialista_cita_especialista'),
    ]

    operations = [
        migrations.AlterField(
            model_name='especialista',
            name='especialidades',
            field=models.ManyToManyField(blank=True, related_name='especialistas', to='citas.tratamiento'),
        ),
    ]
