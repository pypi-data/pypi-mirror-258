#!/usr/bin/envpython
# -*-coding:UTF-8-*-
'''
@File    :   base.py
@Contact :   308711822@qq.com
@License :   (C) Copyright 2021-2225, Personal exclusive right.

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2023/6/16 22:40   小钟同学      1.0         None
'''

# 定义策略接口或抽象基类
from abc import ABC, abstractmethod
from agoku.libs.events.event_type import EventType


# 封装事件信息的类
class Event:

    def __init__(self, event_type: EventType = EventType.ERROR_LOGIN, data=None):
        self.event_type: EventType = event_type  # 事件类型 1: 逻辑错误，2：程序错误
        self.data = data  # 相关数据

class Strategy(ABC):
    event: Event
    def execute(self, notification_service,event: Event):
        '''
        该函数在发送事件的时候会进行触发调用
        :param event:
        :return:
        '''
        self.event = event
        self.notification_service=notification_service
        self.processor(event)  # 调用受子类实现的内部逻辑

    @abstractmethod
    def processor(self, event: Event):
        pass
