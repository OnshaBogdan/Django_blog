# Generated by Django 2.1 on 2018-09-23 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20180916_2220'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='rating',
            field=models.IntegerField(blank=True, default=0, max_length=8),
        ),
    ]