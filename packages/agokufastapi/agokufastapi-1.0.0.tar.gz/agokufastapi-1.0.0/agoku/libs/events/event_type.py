#!/usr/bin/env
# -*-coding:UTF-8-*-
'''
@File    :   base.py
@Contact :   308711822@qq.com
@License :   (C) Copyright 2021-2225, Personal exclusive right.

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2023/6/16 22:40   小钟同学      1.0         None
'''

from enum import Enum


class SubjectEventType(Enum):
    # 程序错误异常类型
    NOTIFICATION_ERROR = 'notification_error'
    # 通知回调异常类型
    CALLBACK_FOUND = 'callback_found'
    # 后天任务异步请求处理类型
    ASYNC_REQUEST = 'async_request'
    # 通知咪咕渠道触发了请求处理的异常
    ERROR_MIGU_NAIVE_ERROR = 'error_for_migu_native'
    # 通知咪咕的破解渠道发生异常错误的信息
    ERROR_MIGU_CRACK = 'error_for_migu_crack'
    # 咪咕号码按时间同步订购状态任务执行，因为咪咕的特殊性，我们需要使用同步机制处理
    MIGU_MM_ORDER_SYNC = 'migu_mm_order_sync'
    # 咪咕活动开通检测告警事件
    MIGU_MM_CK_ORDER_ELARM = 'migu_mm_ck_order_alarm'
    # 订单回调通知合作渠道
    CallbackNotificationChannel = 'callback_notification_channel'
    # 订单提交通知合作渠道
    SubmitNotificationChannel = 'submit_notification_channel'


class EventType(Enum):
    # 程序错误异常类型
    ERROR_PROGRAM = 'error_program'
    # 通知回调异常类型
    ERROR_LOGIN = 'error_login'
