# Generated by Django 4.1.3 on 2022-12-31 09:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upload', models.ImageField(upload_to='uploads/')),
                ('name', models.CharField(default='name', max_length=20)),
                ('extension', models.CharField(default='extension', max_length=20)),
                ('thumbnail', models.ImageField(upload_to='uploads/thumbs/')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('description', models.TextField(blank=True, null=True)),
                ('expiring_links', models.BooleanField(default=False)),
                ('original_photo', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ThumbnailImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size_height', models.IntegerField()),
                ('thumbnail', models.ImageField(default='none', upload_to='thumbs/')),
                ('img', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='website.image')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ExpiresLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('time', models.IntegerField()),
                ('link', models.CharField(default=uuid.uuid4, max_length=36)),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.image')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
