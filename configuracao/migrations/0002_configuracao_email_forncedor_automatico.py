# Generated by Django 5.0.1 on 2024-02-05 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuracao', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuracao',
            name='email_forncedor_automatico',
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
    ]
