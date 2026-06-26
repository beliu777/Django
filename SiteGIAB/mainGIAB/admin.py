from django import forms
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

from .models import Document, DataSet, WordTemplate


class WordTemplateAdminForm(forms.ModelForm):
    class Meta:
        model = WordTemplate
        fields = '__all__'
        help_texts = {
            'file': (
                'Можно использовать простые поля {{ fio }}, {{ group }}, {{ date_begin }}. '
                'Для условий: {% if head2 %}текст{% endif %}. '
                'Для циклов: {% for day in practice_days %}{{ day.date }}{% endfor %}.'
            )
        }


class DataSetInline(admin.StackedInline):
    model = DataSet
    can_delete = False
    extra = 0
    verbose_name = 'Данные пользователя для документов'
    verbose_name_plural = 'Данные пользователя для документов'
    fields = (
        'familia', 'name', 'otchestvo', 'fio_genitive',
        'tip', 'tip_title', 'module', 'module_code', 'specialization',
        'kurs', 'group', 'date_begin', 'date_finish',
        'head1', 'head2', 'ruc_pract', 'year',
    )


admin.site.unregister(User)


@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'practice_data__familia', 'practice_data__name')
    inlines = (DataSetInline,)


@admin.register(WordTemplate)
class WordTemplateAdmin(admin.ModelAdmin):
    form = WordTemplateAdminForm
    list_display = ('template_type', 'file', 'uploaded_at', 'comment')
    list_filter = ('template_type',)
    search_fields = ('file', 'comment')
    readonly_fields = ('uploaded_at',)


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
    list_editable = ['name']


@admin.register(DataSet)
class DataSetAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'familia', 'name', 'otchestvo', 'group', 'kurs']
    search_fields = ['user__username', 'familia', 'name', 'otchestvo', 'group']
    list_filter = ['kurs', 'group']
