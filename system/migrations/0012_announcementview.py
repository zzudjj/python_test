# Generated by Django 5.0.7 on 2024-08-12 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0011_violationview'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnnouncementView',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=90)),
                ('text', models.TextField()),
                ('date', models.DateField()),
                ('name', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'announcement_view',
                'managed': False,
            },
        ),
    ]
