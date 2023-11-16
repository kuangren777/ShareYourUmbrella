# -*- coding: utf-8 -*-
# @Time    : 2023/11/16 22:28
# @Author  : KuangRen777
# @File    : models1.py.py
# @Tags    :

# from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.models import User
# from django.db import models
# from django.utils import timezone
# from django.db.models.signals import pre_save
#
# # Create your models here.
# """
# python manage.py makemigrations
# python manage.py migrate
# """
#
#
# class myuser(AbstractUser):
#     name = models.CharField(verbose_name='真实姓名', max_length=50)
#     userid = models.CharField(verbose_name="学号", max_length=64)
#     school = models.CharField(verbose_name="学校", max_length=64)
#     balance = models.DecimalField(verbose_name="账户余额",
#                                   default=0,
#                                   max_digits=5,
#                                   decimal_places=2)
#     umbrella = models.ForeignKey(verbose_name="目前正在使用的伞的序号",
#                                  to="Umbrella",
#                                  to_field="id",
#                                  default=None,
#                                  null=True,
#                                  blank=True,
#                                  on_delete=models.SET_NULL)
#     photo = models.ImageField(verbose_name='头像',
#                               blank=True,
#                               default='default_logo.jpg')
#                               # upload_to='upload/user_logo/')
#     phone = models.CharField(verbose_name="手机号", max_length=11, unique=True)
#     last_login = models.DateTimeField(verbose_name="上次登录", null=True, blank=True, auto_now=True)
#     registration_time = models.DateTimeField(verbose_name='注册时间', default=timezone.now)
#
#     class Meta:
#         verbose_name = "用户信息表"
#         verbose_name_plural = verbose_name
#
#     # 设置返回值
#     def __str__(self):
#         return self.username
#
#
# # class UserInfo(models.Model):
# #     def __str__(self):
# #         return self.user
# #
# #     user = models.CharField(verbose_name="用户名", max_length=64)
# #     userid = models.CharField(verbose_name="学号", max_length=64)
# #     school = models.CharField(verbose_name="学校", max_length=64)
# #     pwd = models.CharField(verbose_name="密码", max_length=64)
# #     balance = models.DecimalField(verbose_name="账户余额",
# #                                   default=0,
# #                                   max_digits=5,
# #                                   decimal_places=2)
# #     umbrella = models.ForeignKey(verbose_name="目前正在使用的伞的序号",
# #                                  to="Umbrella",
# #                                  to_field="umbrella_id",
# #                                  default=None,
# #                                  null=True,
# #                                  blank=True,
# #                                  on_delete=models.SET_NULL)
# #     registration_time = models.DateTimeField(default=timezone.now)
# #     recent_use_time = models.DateTimeField(auto_now=True)
#
#
# class Umbrella(models.Model):
#     def __str__(self):
#         return str(self.id) + '号-' + str(self.type)
#
#     # choice = {
#     #     ("太阳伞", "太阳伞"),
#     #     ("雨伞", "雨伞"),
#     #     ("透明伞", "透明伞"),
#     #     # ("s", "太阳伞"),
#     # }
#     id = models.BigAutoField(verbose_name="伞的序号", unique=True, primary_key=True)
#     import_time = models.DateTimeField(verbose_name="入库日期", default=timezone.now)
#     can_use = models.BooleanField(verbose_name="是否可用", default=True)
#     # type = models.CharField(verbose_name="伞的类型", max_length=64, choices=choice)
#     type = models.ForeignKey(verbose_name="伞序号",
#                              to="umbrella_type",
#                              to_field="type",
#                              default=None,
#                              null=True,
#                              on_delete=models.SET_NULL)
#     place = models.ForeignKey(verbose_name="放置区域",
#                               to="location",
#                               to_field="id",
#                               default=None,
#                               null=True,
#                               blank=True,
#                               on_delete=models.SET_NULL)
#     umbrella_place_id = models.IntegerField(verbose_name="放置点序号",
#                                             null=True,
#                                             blank=True, )
#     last_use = models.DateTimeField(verbose_name="上次使用", null=True, blank=True, auto_now=True)
#     price = models.IntegerField(verbose_name="成本价")
#
#     class Meta:
#         verbose_name = "雨伞信息表"
#         verbose_name_plural = verbose_name
#
#
# class umbrella_type(models.Model):
#     class Meta:
#         verbose_name = "雨伞类型表"
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return self.type
#
#     type = models.CharField(verbose_name="类型", max_length=128, unique=True)
#
#
# # class place(models.Model):
# #     def __str__(self):
# #         return str(self.umbrella) + '位于' + str(self.place_id) + '的' + str(self.umbrella_place_id)
# #
# #     umbrella = models.OneToOneField(verbose_name="伞序号",
# #                                     to="Umbrella",
# #                                     to_field="id",
# #                                     default=None,
# #                                     null=True,
# #                                     blank=True,
# #                                     on_delete=models.SET_NULL)
# #     place = models.OneToOneField(verbose_name="放置区域",
# #                                  to="location",
# #                                  to_field="id",
# #                                  default=None,
# #                                  null=True,
# #                                  blank=True,
# #                                  on_delete=models.SET_NULL)
# #     umbrella_place_id = models.IntegerField(verbose_name="放置点序号",
# #                                             null=True,
# #                                             blank=True, )
# #
# #     class Meta:
# #         verbose_name = "摆放位置表"
# #         verbose_name_plural = verbose_name
#
#
# class log(models.Model):
#     def __str__(self):
#         return str(self.id)
#
#     username = models.ForeignKey(verbose_name="用户",
#                                  to="myuser",
#                                  to_field="username",
#                                  null=True,
#                                  on_delete=models.SET_NULL)
#     umbrella = models.ForeignKey(verbose_name="伞",
#                                  to="Umbrella",
#                                  to_field="id",
#                                  null=True,
#                                  on_delete=models.SET_NULL)
#     borrow_place = models.ForeignKey(verbose_name="借走区域",
#                                      to="location",
#                                      to_field="name",
#                                      related_name="借走区域",
#                                      null=True,
#                                      on_delete=models.SET_NULL)
#     borrow_time = models.DateTimeField(verbose_name="借出时间", default=timezone.now)
#     back_place = models.ForeignKey(verbose_name="返还区域",
#                                    to="location",
#                                    to_field="name",
#                                    default=None,
#                                    null=True,
#                                    blank=True,
#                                    related_name="返还区域",
#                                    on_delete=models.SET_NULL)
#     back_time = models.DateTimeField(verbose_name="归还日期",
#                                      auto_now=True,
#                                      null=True,
#                                      blank=True)
#     price = models.DecimalField(verbose_name="本次花销",
#                                 decimal_places=2,
#                                 max_digits=5,
#                                 null=True,
#                                 blank=True)
#
#     class Meta:
#         verbose_name = "使用日志"
#         verbose_name_plural = verbose_name
#
#
# class location(models.Model):
#     class Meta:
#         verbose_name = "地点表"
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return self.name
#
#     id = models.BigAutoField(verbose_name="地点序号", primary_key=True)
#     name = models.CharField(verbose_name="地点", max_length=128, unique=True)
#     # num = models.IntegerField(verbose_name="区域中的伞的数量", default=0)
#     address = models.CharField(verbose_name="详细地址", max_length=256, unique=False, blank=True, null=True, default='1')
#     num_sum = models.IntegerField(verbose_name="总共可以放置的数量", default=25)
#
# # class UserProfile(AbstractUser):
# #     nick_name = models.CharField(max_length=50, verbose_name='昵称', default='')
# #     birthday = models.DateField(null=True, blank=True, verbose_name='生日')
# #     gender = models.CharField(max_length=6, choices=(('male', '男'), ('female', '女')), default='female', verbose_name='性别')
# #     address = models.CharField(max_length=100, default='', verbose_name='地址')
# #     mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name='手机号')
# #     image = models.ImageField(max_length=100, upload_to='image/%Y/%m', default='image?default.png', verbose_name='头像')
#
#
# # def creat_user(sender, instance, created, **kwargs):
# #     if created:
# #         myuser.objects.create(user=instance)
# #         print('User Created')
# #
# #
# # def update_user(sender, instance, created, **kwargs):
# #     if created == False:
# #         print()
# #         try:
# #             instance.myuser.save()
# #             print('Up Dated')
# #         except:
# #             myuser.objects.create(user=instance)
# #             print('Created For Exist User')