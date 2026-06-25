from django.db import models
from django.contrib.auth.models import User


class Document(models.Model):
    name = models.TextField()

    class Meta:
        managed = False
        db_table = 'document'

    def __str__(self):
        return self.name or f'Документ {self.pk}'


class DataSet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='practice_data')

    familia = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    otchestvo = models.TextField(blank=True, null=True)
    tip = models.TextField(blank=True, null=True)
    tip_title = models.TextField(blank=True, null=True)
    module = models.TextField(blank=True, null=True)
    module_code = models.TextField(blank=True, null=True)
    specialization = models.TextField(blank=True, null=True)
    kurs = models.IntegerField(blank=True, null=True)
    group = models.TextField(blank=True, null=True)
    date_begin = models.TextField(blank=True, null=True)
    date_finish = models.TextField(blank=True, null=True)
    head1 = models.TextField(blank=True, null=True)
    head2 = models.TextField(blank=True, null=True)
    ruc_pract = models.TextField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    fio_genitive = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'data_set'

    def __str__(self):
        fio = ' '.join(filter(None, [self.familia, self.name, self.otchestvo]))
        return fio or (self.user.username if self.user else f'Анкета {self.pk}')


class WordTemplate(models.Model):
    TITLE = 'title'
    ASSIGNMENT = 'assignment'
    DIARY = 'diary'

    TEMPLATE_TYPES = [
        (TITLE, 'Титульный лист'),
        (ASSIGNMENT, 'Задание'),
        (DIARY, 'Дневник'),
    ]

    template_type = models.CharField('Тип шаблона', max_length=20, choices=TEMPLATE_TYPES, unique=True)
    file = models.FileField('Файл .docx', upload_to='word_templates/')
    comment = models.CharField('Комментарий', max_length=255, blank=True)
    uploaded_at = models.DateTimeField('Загружен', auto_now=True)

    class Meta:
        verbose_name = 'Word-шаблон'
        verbose_name_plural = 'Word-шаблоны'

    def __str__(self):
        return self.get_template_type_display()
