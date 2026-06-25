# Умные Word-шаблоны

В Word-шаблонах теперь работают обычные поля, условия и циклы.

## Обычные поля

```text
{{ fio }}
{{ familia }}
{{ name }}
{{ otchestvo }}
{{ fio_genitive }}
{{ group }}
{{ kurs }}
{{ specialization }}
{{ module }}
{{ module_code }}
{{ tip }}
{{ tip_title }}
{{ date_begin }}
{{ date_finish }}
{{ practice_period }}
{{ head1 }}
{{ head2 }}
{{ ruc_pract }}
{{ year }}
{{ full_name }}
{{ short_name }}
```

## Условия

```text
{% if head2 %}
Руководитель от организации: {{ head2 }}
{% endif %}
```

```text
{% if ruc_pract %}
Руководитель практики: {{ ruc_pract }}
{% else %}
Руководитель практики не указан
{% endif %}
```

## Циклы

`practice_days` создается автоматически из дат начала и окончания практики.

В таблице Word можно сделать строку-шаблон:

```text
{% for day in practice_days %}
{{ day.number }} | {{ day.date }} | {{ day.weekday }} | {{ day.task }}
{% endfor %}
```

Поля одного дня:

```text
{{ day.number }}
{{ day.date }}
{{ day.weekday }}
{{ day.task }}
```

## После обновления

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Если `docxtpl` не установлен, простые поля будут работать, но условия и циклы - нет.
