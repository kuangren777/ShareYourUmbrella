from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.db.models.signals import pre_save


class User(AbstractUser):
    user_id = models.CharField(verbose_name="用户ID", max_length=20, unique=True)
    user_name = models.CharField(verbose_name="用户真实姓名", max_length=50, unique=True)
    user_number = models.CharField(verbose_name="用户学工号", max_length=50)
    user_school = models.CharField(verbose_name="用户学校", max_length=50)
    user_balance = models.DecimalField(verbose_name="用户账户余额", max_digits=10, decimal_places=2, default=0.00)
    user_umbrella_id = models.CharField(verbose_name="用户目前使用的伞号", max_length=50)
    user_photo = models.ImageField(verbose_name='头像', blank=True, default='default_logo.jpg',
                                   upload_to='upload/user_logo/')
    user_phone = models.CharField(verbose_name="用户手机号", max_length=11, unique=True)
    user_password = models.CharField(verbose_name="用户登录密码", max_length=50)
    user_last_login_date = models.DateTimeField(verbose_name="用户上次登录时间", null=True, blank=True, auto_now=True)
    user_registration_date = models.DateTimeField(verbose_name="用户注册日期", default=timezone.now)

    class Meta:
        verbose_name = "用户信息表"
        verbose_name_plural = verbose_name

    # 设置返回值
    def __str__(self):
        return self.user_name


class Umbrella(models.Model):
    umbrella_id = models.CharField(verbose_name="伞ID", max_length=20, unique=True)
    umbrella_warehousing_date = models.DateTimeField(verbose_name="入库日期")
    umbrella_available = models.BooleanField(verbose_name="是否可用")
    umbrella_type_id = models.CharField(verbose_name="伞类型ID", max_length=20)
    umbrella_type = models.CharField(verbose_name="伞类型", max_length=50)
    site_id = models.CharField(verbose_name="站点ID", max_length=20, unique=True)
    lay_id = models.CharField(verbose_name="放置序号", max_length=50)
    umbrella_last_used_date = models.DateTimeField(verbose_name="上次使用日期")
    umbrella_cost_price = models.FloatField(verbose_name="伞成本价")

    class Meta:
        verbose_name = "雨伞信息表"
        verbose_name_plural = verbose_name


class UmbrellaType(models.Model):
    umbrella_type_id = models.CharField(verbose_name="伞类型ID", max_length=20, unique=True)
    umbrella_type = models.CharField(verbose_name="伞类型", max_length=50)

    class Meta:
        verbose_name = "雨伞类型表"
        verbose_name_plural = verbose_name


class SiteStorage(models.Model):
    site_id = models.CharField(verbose_name="站点ID", max_length=20)
    lay_id = models.CharField(verbose_name="放置序号", max_length=50)
    umbrella_id = models.CharField(verbose_name="伞ID", max_length=20)

    class Meta:
        verbose_name = "站点存放表"
        verbose_name_plural = verbose_name


class Site(models.Model):
    site_id = models.CharField(verbose_name="站点ID", max_length=20, unique=True)
    site_address = models.CharField(verbose_name="站点地址", max_length=50)

    class Meta:
        verbose_name = "站点表"
        verbose_name_plural = verbose_name


class Diary(models.Model):
    diary_id = models.CharField(verbose_name="日志ID", max_length=20, unique=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    umbrella_id = models.ForeignKey(Umbrella, on_delete=models.CASCADE)
    lending_site_id = models.CharField(verbose_name="借出站点ID", max_length=20)
    lending_lay_id = models.CharField(verbose_name="借出详细序号", max_length=50)
    lending_time = models.DateTimeField(verbose_name="借出时间")
    return_site_id = models.CharField(verbose_name="归还站点ID", max_length=20)
    return_lay_id = models.CharField(verbose_name="归还详细序号", max_length=50)
    return_time = models.DateTimeField(verbose_name="归还时间")
    order_price = models.FloatField(verbose_name="本次费用")

    class Meta:
        verbose_name = "日志表"
        verbose_name_plural = verbose_name


class Repair(models.Model):
    repair_id = models.CharField(verbose_name="维护ID", max_length=20, unique=True)
    repair_type_id = models.ForeignKey('RepairType', on_delete=models.SET_NULL, null=True)
    notes = models.CharField(verbose_name="备注", max_length=50)
    umbrella_id = models.ForeignKey(Umbrella, on_delete=models.CASCADE)
    repair_time = models.DateTimeField(verbose_name="维护时间")

    class Meta:
        verbose_name = "维修表"
        verbose_name_plural = verbose_name


class RepairType(models.Model):
    repair_type_id = models.CharField(verbose_name="维护类型ID", max_length=20, unique=True)
    repair_type = models.CharField(verbose_name="维护类型", max_length=50)

    class Meta:
        verbose_name = "维修类型表"
        verbose_name_plural = verbose_name


class Recharge(models.Model):
    recharge_id = models.CharField(verbose_name="充值记录ID", max_length=20, unique=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    recharge_time = models.DateTimeField(verbose_name="充值时间")
    recharge_amount = models.FloatField(verbose_name="充值金额")

    class Meta:
        verbose_name = "充值表"
        verbose_name_plural = verbose_name


class Alarm(models.Model):
    alarm_id = models.CharField(verbose_name="警报ID", max_length=20, unique=True)
    umbrella_id = models.ForeignKey(Umbrella, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    alarm_type_id = models.ForeignKey('AlarmType', on_delete=models.SET_NULL, null=True)
    alarm_available = models.BooleanField(verbose_name="是否报警")

    class Meta:
        verbose_name = "警报表"
        verbose_name_plural = verbose_name


class AlarmType(models.Model):
    alarm_type_id = models.CharField(verbose_name="警报类型ID", max_length=20, unique=True)
    alarm_type = models.CharField(verbose_name="警报类型", max_length=50)

    class Meta:
        verbose_name = "警报类型表"
        verbose_name_plural = verbose_name


class Coupon(models.Model):
    coupon_id = models.CharField(verbose_name="优惠券ID", max_length=20, unique=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    coupon_type = models.CharField(verbose_name="优惠券类型", max_length=50)
    discount_price = models.FloatField(verbose_name="折扣力度")
    satisfied_amount = models.FloatField(verbose_name="满足金额")
    effective_time = models.DateTimeField(verbose_name="生效时间")
    expire_time = models.DateTimeField(verbose_name="失效时间")

    class Meta:
        verbose_name = "优惠券表"
        verbose_name_plural = verbose_name


class Comment(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    umbrella_id = models.ForeignKey(Umbrella, on_delete=models.CASCADE)
    diary_id = models.ForeignKey(Diary, on_delete=models.CASCADE)
    comment_content = models.CharField(verbose_name="评论内容", max_length=255)
    comment_score = models.FloatField(verbose_name="评价分数")

    class Meta:
        verbose_name = "评论表"
        verbose_name_plural = verbose_name
