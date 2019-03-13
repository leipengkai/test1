# -*- coding: utf-8 -*-

import time
from celery import task,shared_task
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

# @task
@shared_task
def django_send_email(email, msg):

   message = msg
   try:
        # 使用celery并发处理邮件发送的任务
        logger.info("\n开始发送邮件")
        print(email)
        print(msg)
        send_mail("登录提示信息", "", settings.EMAIL_FROM, [email], html_message=message)
        logger.info("邮件发送成功")
   except Exception as e:
        logger.error("邮件发送失败: {}".format(e))

@shared_task
def longtime_test():
    try:
        time.sleep(4)
    except Exception as e:
        logger.error("sleep: {}".format(e))
