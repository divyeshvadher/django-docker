# Generated by Django 4.2.3 on 2024-12-03 07:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangoapp', '0007_rename_subject_subject_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subject',
            old_name='name',
            new_name='subject',
        ),
    ]
