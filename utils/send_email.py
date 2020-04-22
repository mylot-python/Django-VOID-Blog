from django.core.mail import EmailMultiAlternatives
from django.template import loader

from Django_VOID_Blog import settings


def to_visitor(instance):
    to_author_mail = instance.parent.mail
    context = {
        'parent_author': instance.parent.author,
        'article_id': instance.parent.article.id,
        'article_title': instance.parent.article.title,
        'parent_content': instance.parent.content,
        'parent_id': instance.parent.id,
        'instance_author': instance.author,
        'instance_content': instance.content,
    }
    EMAIL_TITLE = '来自 [breezed | 无风清响] 站点的留言回复'
    # 发送的html模板的名称
    email_template_name = 'send_email.html'
    t = loader.get_template(email_template_name)
    html_content = t.render(context=context)
    msg = EmailMultiAlternatives(EMAIL_TITLE, html_content, settings.EMAIL_HOST_USER, [to_author_mail])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

