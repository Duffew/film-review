# Generated by Django 5.1.6 on 2025-02-23 21:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0007_remove_comment_downvotes_remove_comment_upvotes_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Vote',
        ),
    ]
