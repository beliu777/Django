from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainGIAB', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WordTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('template_type', models.CharField(choices=[('title', 'Титульный лист'), ('assignment', 'Задание'), ('diary', 'Дневник')], max_length=20, unique=True, verbose_name='Тип шаблона')),
                ('file', models.FileField(upload_to='word_templates/', verbose_name='Файл .docx')),
                ('comment', models.CharField(blank=True, max_length=255, verbose_name='Комментарий')),
                ('uploaded_at', models.DateTimeField(auto_now=True, verbose_name='Загружен')),
            ],
            options={
                'verbose_name': 'Word-шаблон',
                'verbose_name_plural': 'Word-шаблоны',
            },
        ),
    ]
