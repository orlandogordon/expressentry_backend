# Generated by Django 4.2.3 on 2023-07-28 02:18

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_alter_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=django_resized.forms.ResizedImageField(crop=None, default='avatar.png', force_format=None, keep_meta=True, quality=-1, scale=None, size=[10, 10], upload_to=''),
        ),
    ]
