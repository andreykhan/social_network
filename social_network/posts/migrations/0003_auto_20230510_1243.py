# Generated by Django 2.2.19 on 2023-05-10 06:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20230510_1240'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='pud_date',
            new_name='pub_date',
        ),
    ]