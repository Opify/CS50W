# Generated by Django 4.2.1 on 2023-06-10 08:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wiki', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='article_user',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='comment_user',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='edit',
            old_name='edit_user',
            new_name='user',
        ),
        migrations.CreateModel(
            name='Following',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to='wiki.article')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
