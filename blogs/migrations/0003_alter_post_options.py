# Generated by Django 4.0 on 2021-12-28 05:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0002_alter_post_content'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-updated_on'], 'verbose_name': 'Post', 'verbose_name_plural': 'Posts'},
        ),
    ]