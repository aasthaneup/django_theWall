# Generated by Django 2.2.4 on 2021-03-28 17:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_wall', '0004_auto_20210328_1646'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='comments_for_msg',
            new_name='comment_for_message',
        ),
    ]
