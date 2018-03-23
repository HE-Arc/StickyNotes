import django_tables2 as tables
from django.contrib.auth import get_user_model
from django.utils.html import format_html

class LinkImageColumn(tables.Column):
    def render(self, value):
        return format_html('<a href="{}"><img src="/static/img/{}" /></a>', value[0], value[1])

class LinkColumn(tables.Column):
    def render(self, value):
        return format_html('<a href="{}">{}</a>', value[0], value[1])

class UserJoinTable(tables.Table):
    perm_column = LinkColumn(verbose_name='Permissions')
    remove_column = LinkImageColumn(verbose_name='Remove')

    class Meta:
        model = get_user_model()
        template_name = 'django_tables2/bootstrap-responsive.html'
        fields = ('username', 'is_active',)
