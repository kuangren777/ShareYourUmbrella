# -*- coding: utf-8 -*-
# @Time    : 2023/12/4 23:06
# @Author  : KuangRen777
# @File    : dict_tags.py
# @Tags    :
from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
