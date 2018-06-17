# Generated by Django 2.0.6 on 2018-06-15 18:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_question_author'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_text', models.CharField(max_length=350)),
                ('comment_author', models.CharField(max_length=30)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('com_question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Question')),
            ],
        ),
    ]
