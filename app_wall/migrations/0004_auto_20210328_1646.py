# Generated by Django 2.2.4 on 2021-03-28 16:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_wall', '0003_auto_20210328_1645'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='comments_by_user',
            new_name='comment_posted_by',
        ),
    ]
