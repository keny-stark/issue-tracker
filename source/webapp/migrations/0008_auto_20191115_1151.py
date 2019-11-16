# Generated by Django 2.2 on 2019-11-15 11:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import webapp.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('webapp', '0007_auto_20191115_1009'),
    ]

    operations = [
        migrations.AddField(
            model_name='tracker',
            name='assigned_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tracker_assigned', to=settings.AUTH_USER_MODEL, verbose_name='assigned to'),
        ),
        migrations.AlterField(
            model_name='tracker',
            name='created_by',
            field=models.ForeignKey(default=webapp.models.get_admin, on_delete=django.db.models.deletion.PROTECT, related_name='tracker_by', to=settings.AUTH_USER_MODEL, verbose_name='created by'),
        ),
    ]
