# Generated by Django 5.1.7 on 2025-04-29 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('citas', '0010_alter_especialista_especialidades'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tratamiento',
            name='descripcion',
        ),
        migrations.AddField(
            model_name='tratamiento',
            name='descripcion_corta',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='tratamiento',
            name='descripcion_larga',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tratamiento',
            name='imagen_secundaria',
            field=models.ImageField(blank=True, null=True, upload_to='tratamientos/'),
        ),
    ]
