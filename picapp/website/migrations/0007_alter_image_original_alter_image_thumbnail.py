# Generated by Django 4.1.3 on 2022-12-31 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0006_rename_upload_image_original'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='original',
            field=models.ImageField(upload_to='originals/'),
        ),
        migrations.AlterField(
            model_name='image',
            name='thumbnail',
            field=models.ImageField(upload_to='originals/thumbs/'),
        ),
    ]
