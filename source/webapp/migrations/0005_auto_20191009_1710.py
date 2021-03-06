from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0004_auto_20191009_1659'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.ForeignKey(default='active', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='tracker', to='webapp.ProjectStatus', verbose_name='Project status'),
        ),
    ]