# Generated by Django 4.1.3 on 2022-12-31 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_rename_thumbnailimg_image_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='thumbnail',
            field=models.ImageField(upload_to='uploads/thumbs/'),
        ),
    ]
