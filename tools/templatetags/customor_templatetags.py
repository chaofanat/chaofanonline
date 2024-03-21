from django import template
# 下面代码会直接使用register
register = template.Library()


#清理字符串前后空格以及换行符
@register.filter(is_safe=False, name='trim')
def trim(value):
    return value.replace('\n','').strip()

