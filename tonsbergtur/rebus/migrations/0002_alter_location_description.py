# Generated by Django 4.0.6 on 2022-07-18 17:58

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rebus', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='description',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]
