# Generated by Django 5.0.6 on 2024-05-13 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('canvas', '0005_rename_customer_segments_channel_customer_segment'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='description',
            field=models.CharField(blank=True, max_length=1023, null=True),
        ),
        migrations.AddField(
            model_name='customersegment',
            name='description',
            field=models.CharField(blank=True, max_length=1023, null=True),
        ),
        migrations.AddField(
            model_name='revenuestreams',
            name='description',
            field=models.CharField(blank=True, max_length=1023, null=True),
        ),
        migrations.AlterField(
            model_name='coststructure',
            name='description',
            field=models.CharField(blank=True, max_length=1023, null=True),
        ),
        migrations.AlterField(
            model_name='customerrelationship',
            name='description',
            field=models.CharField(blank=True, max_length=1023, null=True),
        ),
        migrations.AlterField(
            model_name='keyactivities',
            name='description',
            field=models.CharField(blank=True, max_length=1023, null=True),
        ),
        migrations.AlterField(
            model_name='keypartnership',
            name='description',
            field=models.CharField(blank=True, max_length=1023, null=True),
        ),
        migrations.AlterField(
            model_name='keyresources',
            name='description',
            field=models.CharField(blank=True, max_length=1023, null=True),
        ),
        migrations.AlterField(
            model_name='valueproposition',
            name='description',
            field=models.CharField(blank=True, max_length=1023, null=True),
        ),
    ]
