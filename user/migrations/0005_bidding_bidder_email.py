# Generated by Django 4.2.4 on 2024-05-20 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_alter_bidding_bidd_product_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='bidding',
            name='bidder_email',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
