# Generated by Django 4.2.3 on 2023-08-09 08:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_member_fcm_token'),
    ]

    operations = [
        migrations.RenameField(
            model_name='member',
            old_name='MenberID',
            new_name='MemberID',
        ),
    ]
