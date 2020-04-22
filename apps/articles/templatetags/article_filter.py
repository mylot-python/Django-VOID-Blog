import logging, mistune, re, hashlib
from django.template import Library


logger = logging.getLogger('django')

register = Library()

@register.filter()
def to_md5(value):
    mail = value
    make_hash = hashlib.md5()
    make_hash.update(mail.encode())
    md5 = make_hash.hexdigest()
    return md5


@register.filter()
def is_odd(num):
    if (num % 2) == 0:
        return 0
    else:
        return 1

@register.filter()
def to_markdown(content):
    to_content = content
    to_content = mistune.markdown(to_content)
    return to_content


@register.filter()
def count_content(value):
    filtrate = re.compile(u'\W+')  # 非中文
    count = len(filtrate.sub(r'', value))
    return count