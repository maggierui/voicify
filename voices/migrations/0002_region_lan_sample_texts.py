# Generated by Django 4.0.3 on 2022-03-24 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voices', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='region_lan',
            name='sample_texts',
            field=models.TextField(default='Type in some texts here to convert to voices'),
        ),
    ]
