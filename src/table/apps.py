# -*- coding: utf-8 -*-


from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class TableConfig(AppConfig):
    name = 'table'
    verbose_name = _('Table')
