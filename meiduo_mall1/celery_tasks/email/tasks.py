from django.core.mail import send_mail

from apps.users.utils import email_token
from celery_tasks.main import app


@app.task
def send_active_email(id, email):
   subject = "美多激活邮件"
   message = ""
   from_emial = "美多商城<Heywei0603@163.com>"
   recipient_list = ["2452279129@qq.com"]
   active_url = email_token(id, email)
   html_message = '<p>尊敬的用户您好！</p>' \
                   '<p>感谢您使用美多商城。</p>' \
                   '<p>您的邮箱为：%s 。请点击此链接激活您的邮箱：</p>' \
                   '<p><a href="%s">激活链接</a></p>' % (email, active_url)
   send_mail(
       subject=subject,
       message=message,
       from_email=from_emial,
       html_message=html_message,
       recipient_list=recipient_list
   )


