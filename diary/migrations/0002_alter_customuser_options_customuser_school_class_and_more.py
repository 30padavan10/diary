# Generated by Django 4.0.4 on 2022-06-03 10:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'verbose_name': 'Ученик', 'verbose_name_plural': 'Ученики'},
        ),
        migrations.AddField(
            model_name='customuser',
            name='school_class',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='diary.schoolclass', verbose_name='Номер класса'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='school_number',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='diary.school', verbose_name='Номер школы'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='second_name',
            field=models.CharField(blank=True, max_length=100, verbose_name='Отчество'),
        ),
    ]