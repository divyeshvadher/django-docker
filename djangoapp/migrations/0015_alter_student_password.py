# Generated by Django 4.2.3 on 2024-12-09 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangoapp', '0014_remove_student_role_alter_student_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='password',
            field=models.CharField(max_length=255),
        ),
    ]