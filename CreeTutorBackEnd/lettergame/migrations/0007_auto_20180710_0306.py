# Generated by Django 2.0.5 on 2018-07-10 03:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lettergame', '0006_auto_20180710_0259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='letterpair',
            name='first_letter',
            field=models.ForeignKey(blank=True, db_column='first_letter', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='lettergame.Alphabet'),
        ),
        migrations.AlterField(
            model_name='letterpair',
            name='second_letter',
            field=models.ForeignKey(blank=True, db_column='second_letter', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='lettergame.Alphabet'),
        ),
    ]
