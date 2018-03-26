import django_tables2 as tables
from django.contrib.auth import get_user_model
from django.utils.html import format_html

class LinkImageColumn(tables.Column):
    def __init__(self, *args, **kwargs):
        tables.Column.__init__(self)
        self.orderable = False
        self.verbose_name = kwargs['verbose_name']

    def render(self, value):
        return format_html('<a href="{}"><img src="/static/img/{}" /></a>', value[0], value[1])

class LinkColumn(tables.Column):
    def __init__(self, *args, **kwargs):
        tables.Column.__init__(self)
        self.orderable = False

    def render(self, value):
        return format_html('<a href="{}">{}</a>', value[0], value[1])

class UserJoinTable(tables.Table):
    perm_column = LinkColumn(verbose_name='Permissions')
    remove_column = LinkImageColumn(verbose_name='Remove')

    class Meta:
        model = get_user_model()
        template_name = 'django_tables2/bootstrap-responsive.html'
        fields = ('username', 'is_active',)

class PermissionsUserTable(tables.Table):
    codename_column = tables.Column(verbose_name='Codename')
    description_column = tables.Column(verbose_name='Description')
    checkbox_column = tables.Column(verbose_name='On/Off')

    class Meta:
        template_name = 'django_tables2/bootstrap-responsive.html'
