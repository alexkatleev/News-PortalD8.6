# Generated by Django 4.2 on 2023-04-22 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_category_subscribers_alter_post_categorytype_post2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='categoryType',
            field=models.CharField(choices=[('AR', 'Статья'), ('NW', 'Новость')], default='AR', max_length=20),
        ),
        migrations.AlterField(
            model_name='post2',
            name='view',
            field=models.CharField(choices=[('AR', 'Статья'), ('NW', 'Новость')], default='NW', max_length=2),
        ),
    ]
