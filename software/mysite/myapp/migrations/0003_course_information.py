# Generated by Django 5.0.6 on 2024-11-10 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_course_curriculum'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='information',
            field=models.CharField(default=1, max_length=5000, verbose_name='課程資訊'),
            preserve_default=False,
        ),
    ]