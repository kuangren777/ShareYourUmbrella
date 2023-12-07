from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.db.models.signals import pre_save


# """
# python manage.py makemigrations
# python manage.py migrate
# """


class UmbrellaType(models.Model):
    umbrella_type_id = models.AutoField(primary_key=True, verbose_name="伞类型ID")
    umbrella_type = models.CharField(verbose_name="伞类型", max_length=50)

    class Meta:
        verbose_name = "雨伞类型表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.umbrella_type


class Site(models.Model):
    site_id = models.AutoField(primary_key=True, verbose_name="站点ID")
    site_address = models.CharField(verbose_name="站点地址", max_length=50)
    site_store_num = models.IntegerField(verbose_name="站点存放数量", null=True, blank=True)

    class Meta:
        verbose_name = "站点表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.site_address


class Umbrella(models.Model):
    umbrella_id = models.AutoField(primary_key=True, verbose_name="伞ID")
    umbrella_warehousing_date = models.DateTimeField(verbose_name="入库日期")
    umbrella_available = models.BooleanField(verbose_name="是否可用")
    umbrella_type_id = models.ForeignKey(UmbrellaType, on_delete=models.SET_NULL, verbose_name="伞类型", null=True)
    umbrella_last_used_date = models.DateTimeField(verbose_name="上次使用日期", null=True, blank=True)
    umbrella_cost_price = models.FloatField(verbose_name="伞成本价")
    umbrella_scrapped = models.BooleanField(verbose_name="是否报废", default=False)

    class Meta:
        verbose_name = "雨伞信息表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.umbrella_id) + '-' + str(self.umbrella_type_id)


class User(AbstractUser):
    user_id = models.AutoField(primary_key=True, verbose_name="用户ID")
    user_real_name = models.CharField(verbose_name="用户真实姓名", max_length=50, unique=True)
    user_number = models.CharField(verbose_name="用户学工号", max_length=50)
    user_school = models.CharField(verbose_name="用户学校", max_length=50)
    user_balance = models.DecimalField(verbose_name="用户账户余额", max_digits=10, decimal_places=2, default=0.00)
    user_umbrella_id = models.ForeignKey(Umbrella, on_delete=models.SET_NULL, verbose_name="用户目前使用的伞号",
                                         null=True, blank=True)
    user_photo = models.ImageField(verbose_name='头像', blank=True, default='default_logo.jpg',
                                   upload_to='upload/user_logo/')
    user_phone = models.CharField(verbose_name="用户手机号", max_length=11, unique=True)
    user_last_login_date = models.DateTimeField(verbose_name="用户上次登录时间", null=True, blank=True, auto_now=True)
    user_registration_date = models.DateTimeField(verbose_name="用户注册日期", default=timezone.now)

    class Meta:
        verbose_name = "用户信息表"
        verbose_name_plural = verbose_name

    # 设置返回值
    def __str__(self):
        return self.username


class SiteStorage(models.Model):
    id = models.AutoField(primary_key=True)  # 添加default参数，指定默认值为1或其他适合您的值
    site_id = models.ForeignKey(Site, on_delete=models.SET_NULL, verbose_name="站点ID", null=True, blank=True,
                                unique=False)
    lay_id = models.CharField(verbose_name="放置序号", max_length=50)
    umbrella_id = models.ForeignKey(Umbrella, on_delete=models.SET_NULL, verbose_name="伞ID", null=True, blank=True)

    class Meta:
        verbose_name = "站点存放表"
        verbose_name_plural = verbose_name


class Diary(models.Model):
    diary_id = models.AutoField(primary_key=True, verbose_name="日志ID")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户ID")
    umbrella_id = models.ForeignKey(Umbrella, on_delete=models.CASCADE, verbose_name="雨伞ID")
    lending_site_id = models.ForeignKey(Site, on_delete=models.SET_NULL, verbose_name="借出站点ID", null=True,
                                        blank=True, related_name='lending_site')
    lending_lay_id = models.CharField(verbose_name="借出详细序号", max_length=50)
    lending_time = models.DateTimeField(verbose_name="借出时间")
    return_site_id = models.ForeignKey(Site, on_delete=models.SET_NULL, verbose_name="归还站点ID", null=True,
                                       blank=True, related_name='return_site')
    return_lay_id = models.CharField(verbose_name="归还详细序号", null=True, blank=True, max_length=50)
    return_time = models.DateTimeField(verbose_name="归还时间", null=True, blank=True, )
    order_price = models.FloatField(verbose_name="本次费用")

    class Meta:
        verbose_name = "日志表"
        verbose_name_plural = verbose_name


class Repair(models.Model):
    repair_id = models.AutoField(primary_key=True, verbose_name="维护ID")
    repair_type_id = models.ForeignKey('RepairType', on_delete=models.SET_NULL, null=True)
    notes = models.CharField(verbose_name="备注", max_length=50)
    umbrella_id = models.ForeignKey(Umbrella, on_delete=models.CASCADE)
    repair_time = models.DateTimeField(verbose_name="维护时间", null=True, blank=True)

    class Meta:
        verbose_name = "维修表"
        verbose_name_plural = verbose_name


class RepairType(models.Model):
    repair_type_id = models.AutoField(primary_key=True, verbose_name="维护类型ID")
    repair_type = models.CharField(verbose_name="维护类型", max_length=50)

    class Meta:
        verbose_name = "维修类型表"
        verbose_name_plural = verbose_name

    def __str__(self):
        # 假设您有一个字段用于描述维修类型，例如 'repair_type_name'
        return str(self.repair_type_id) + '.' + self.repair_type


class Recharge(models.Model):
    recharge_id = models.AutoField(primary_key=True, verbose_name="充值记录ID")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    recharge_time = models.DateTimeField(verbose_name="充值时间")
    recharge_amount = models.FloatField(verbose_name="充值金额")

    class Meta:
        verbose_name = "充值表"
        verbose_name_plural = verbose_name


class Alarm(models.Model):
    alarm_id = models.AutoField(primary_key=True, verbose_name="警报ID")
    umbrella_id = models.ForeignKey(Umbrella, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    alarm_type_id = models.ForeignKey('AlarmType', on_delete=models.SET_NULL, null=True)
    alarm_available = models.BooleanField(verbose_name="是否报警")

    class Meta:
        verbose_name = "警报表"
        verbose_name_plural = verbose_name


class AlarmType(models.Model):
    alarm_type_id = models.AutoField(primary_key=True, verbose_name="警报类型ID")
    alarm_type = models.CharField(verbose_name="警报类型", max_length=50)

    class Meta:
        verbose_name = "警报类型表"
        verbose_name_plural = verbose_name


class Coupon(models.Model):
    coupon_id = models.AutoField(primary_key=True, verbose_name="优惠券ID")
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
    comment_time = models.DateTimeField(verbose_name="评价时间", null=True, blank=True)

    class Meta:
        verbose_name = "评论表"
        verbose_name_plural = verbose_name
