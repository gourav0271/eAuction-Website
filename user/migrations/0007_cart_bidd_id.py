# Generated by Django 4.2.4 on 2024-05-27 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='bidd_ID',
            field=models.CharField(default=1, max_length=10),
            preserve_default=False,
        ),
    ]
