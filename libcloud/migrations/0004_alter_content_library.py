# Generated by Django 4.0.2 on 2022-02-27 19:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('libcloud', '0003_remove_contentfeature_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='library',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='libcloud.library'),
        ),
    ]
