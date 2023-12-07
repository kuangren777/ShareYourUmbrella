from datetime import datetime

from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.forms.widgets import ClearableFileInput

from .admin import *
from .models import *


# class CreatUserForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2', 'school', 'name', 'userid', 'phone']
#
#         labels = {
#             'username': '用户名',
#             'email': '邮箱',
#             'password1': '密码',
#             'password2': '确认密码',
#             'school': '学校',
#             'name': '姓名',
#             'userid': '学号',
#             'phone': '电话号码',
#         }
#
#         widgets = {
#             'username': forms.TextInput(attrs={'class': 'form-control'}),
#             'email': forms.TextInput(attrs={'class': 'form-control'}),
#             'password1': forms.TextInput(attrs={'class': 'form-control'}),
#             'password2': forms.TextInput(attrs={'class': 'form-control'}),
#             'school': forms.TextInput(attrs={'class': 'form-control'}),
#             'name': forms.TextInput(attrs={'class': 'form-control'}),
#             'userid': forms.TextInput(attrs={'class': 'form-control'}),
#             'phone': forms.TextInput(attrs={'class': 'form-control'}),
#             # 'name': forms.TextInput(attrs={'class': 'form-control'}),
#             # 'umbrella': forms.Select(attrs={'class': 'form-select'}),
#             # 'borrow_place': forms.Select(attrs={'class': 'form-select'}),
#             # 'back_place': forms.Select(attrs={'class': 'form-select'}),
#             # 'summary': forms.TextInput(attrs={'class': 'form-control'}),
#         }

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'user_school', 'user_real_name', 'user_number',
                  'user_phone']

        labels = {
            'username': '用户昵称',
            'email': '邮箱',
            'password1': '密码',
            'password2': '确认密码',
            'user_school': '学校',
            'user_real_name': '真实姓名',
            'user_number': '学号',
            'user_phone': '电话号码',
        }

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
            'user_school': forms.TextInput(attrs={'class': 'form-control'}),
            'user_real_name': forms.TextInput(attrs={'class': 'form-control'}),
            'user_number': forms.TextInput(attrs={'class': 'form-control'}),
            'user_phone': forms.TextInput(attrs={'class': 'form-control'}),
        }


# class ForgetUserForm(UserCreationForm):
#     class Meta:
#         model = myuser
#         fields = ['new_password1', 'new_password2']
#
#         labels = {
#             'new_password1': '新密码',
#             'new_password2': '确认密码',
#         }

# class MyClearableFileInput(ClearableFileInput):
#     initial_text = '当前头像'
#     input_text = '修改'
#     clear_checkbox_label = '清除'


# class UpdateUserForm(ModelForm):
#     class Meta:
#         model = User
#         # fields = ['email']
#         fields = ['email', 'school', 'name', 'userid', 'phone', 'photo']
#         # exclude = ['password', 'Superuser status', 'Groups']
#
#         labels = {
#             'email': '邮箱',
#             'school': '学校',
#             'name': '姓名',
#             'userid': '学号',
#             'phone': '电话号码',
#             'photo': '头像',
#         }
#
#         widgets = {
#             'email': forms.TextInput(attrs={'class': 'form-control'}),
#             'school': forms.TextInput(attrs={'class': 'form-control'}),
#             'name': forms.TextInput(attrs={'class': 'form-control'}),
#             'userid': forms.TextInput(attrs={'class': 'form-control'}),
#             'phone': forms.TextInput(attrs={'class': 'form-control'}),
#             'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
#             # 'name': forms.TextInput(attrs={'class': 'form-control'}),
#             # 'umbrella': forms.Select(attrs={'class': 'form-select'}),
#             # 'borrow_place': forms.Select(attrs={'class': 'form-select'}),
#             # 'back_place': forms.Select(attrs={'class': 'form-select'}),
#             # 'summary': forms.TextInput(attrs={'class': 'form-control'}),
#         }
#
#         # photo = forms.ImageField(label='选择头像', required=True, widget=MyClearableFileInput, allow_empty_file=)
#
#
# class OrderForm(ModelForm):
#     class Meta:
#         model = Diary
#         fields = ['umbrella', 'borrow_place', 'back_place']
#         labels = {
#             'umbrella': '伞',
#             'borrow_place': '借的地方',
#             'back_place': '归还地方',
#         }
#
#         widgets = {
#             # 'title': forms.TextInput(attrs={'class': 'form-control'}),
#             'umbrella': forms.Select(attrs={'class': 'form-select'}),
#             'borrow_place': forms.Select(attrs={'class': 'form-select'}),
#             'back_place': forms.Select(attrs={'class': 'form-select'}),
#             # 'summary': forms.TextInput(attrs={'class': 'form-control'}),
#         }
#
#
# class ImportUmbrellaForm(ModelForm):
#     class Meta:
#         model = Umbrella
#         fields = ['type', 'price']
#         labels = {
#             'type': '类型',
#             'price': '成本价',
#         }
#
#         widgets = {
#             # 'umbrella': forms.(attrs={'class': 'form-control'}),
#             # 'umbrella': forms.Select(attrs={'class': 'form-select'}),
#             'type': forms.Select(attrs={'class': 'form-select'}),
#             'price': forms.TextInput(attrs={'class': 'form-control'}),
#             # 'summary': forms.TextInput(attrs={'class': 'form-control'}),
#         }
#
#
# class PlaceUmbrella(ModelForm):
#     class Meta:
#         model = Umbrella
#         fields = ['can_use', 'place']
#         labels = {
#             'can_use': '可用性',
#             'place': '放置地点',
#         }
#
#         widgets = {
#             'can_use': forms.CheckboxInput(attrs={'class': 'form-check'}),
#             'place': forms.Select(attrs={'class': 'form-select'}),
#         }
#
#
# class ChangePasswordForm(forms.Form):
#     """
#     修改密码表单
#     """
#     old_password = forms.CharField(label='旧密码', max_length=32, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
#     password = forms.CharField(label='密码', max_length=32, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
#     re_password = forms.CharField(label='重复密码', max_length=32, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
#
#     def __init__(self, *args, **kwargs):
#         self.user = kwargs.pop('user')
#         super().__init__(*args, **kwargs)
#
#     def clean(self):
#         cleaned_data = super().clean()
#         old_password = cleaned_data.get("old_password")
#         password = cleaned_data.get("password")
#         re_password = cleaned_data.get("re_password")
#         if not authenticate(username=self.user.username, password=old_password):
#             self.add_error('old_password', '旧密码验证错误')
#         if password != re_password:
#             self.add_error('re_password', '两次输入的密码不一致')
#         try:
#             validate_password(password, self.user)
#         except ValidationError as e:
#             self.add_error('password', e)
#         return self.cleaned_data

class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'user_school', 'user_real_name', 'user_id', 'user_phone', 'user_photo']  # 更新字段

        labels = {
            'email': '邮箱',
            'user_school': '学校',
            'user_real_name': '真实姓名',
            'user_id': '学号',
            'user_phone': '电话号码',
            'user_photo': '头像',
        }

        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'user_school': forms.TextInput(attrs={'class': 'form-control'}),
            'user_real_name': forms.TextInput(attrs={'class': 'form-control'}),
            'user_id': forms.TextInput(attrs={'class': 'form-control'}),
            'user_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'user_photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

        # 请注意：不需要在此定义 'user_password' 字段，因为用户密码不应该在此表单中更新


class ChangePasswordForm(forms.Form):
    """
    修改密码表单
    """
    old_password = forms.CharField(label='旧密码', max_length=32,
                                   widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='密码', max_length=32, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    re_password = forms.CharField(label='重复密码', max_length=32,
                                  widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get("old_password")
        password = cleaned_data.get("password")
        re_password = cleaned_data.get("re_password")
        if not authenticate(username=self.user.username, password=old_password):
            self.add_error('old_password', '旧密码验证错误')
        if password != re_password:
            self.add_error('re_password', '两次输入的密码不一致')
        try:
            validate_password(password, self.user)
        except ValidationError as e:
            self.add_error('password', e)
        return self.cleaned_data


class OrderForm(forms.ModelForm):
    lending_site_id = forms.ModelChoiceField(
        queryset=Site.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'site-select'}),
        label='借出地'
    )

    class Meta:
        model = Diary
        fields = ['umbrella_id', 'lending_site_id', 'return_site_id']  # 更新字段

        labels = {
            'umbrella_id': '伞',
            'lending_site_id': '借的地方',
            ''
            'return_site_id': '归还地方',
        }

        widgets = {
            'umbrella_id': forms.Select(attrs={'class': 'form-select'}),
            'lending_site_id': forms.TextInput(attrs={'class': 'form-control'}),
            'return_site_id': forms.Select(attrs={'class': 'form-select'}),
        }


class ImportUmbrellaForm(forms.ModelForm):
    class Meta:
        model = Umbrella
        fields = ['umbrella_type_id', 'umbrella_cost_price']  # 更新字段

        labels = {
            'umbrella_type_id': '类型id',
            'umbrella_cost_price': '成本价',
        }

        widgets = {
            'umbrella_type_id': forms.Select(attrs={'class': 'form-select'}),
            'umbrella_cost_price': forms.TextInput(attrs={'class': 'form-control'}),
        }


class PlaceUmbrella(forms.ModelForm):
    class Meta:
        model = Umbrella
        # fields = ['umbrella_available', 'site_id']  # 更新字段
        fields = ['umbrella_available']  # 更新字段

        labels = {
            'umbrella_available': '可用性',
            # 'site_id': '放置地点',
        }

        widgets = {
            'umbrella_available': forms.CheckboxInput(attrs={'class': 'form-check'}),
            # 'site_id': forms.Select(attrs={'class': 'form-select'}),
        }


class ReportRepairUmbrellaForm(forms.ModelForm):
    class Meta:
        model = Repair
        # fields = ['umbrella_id', 'repair_type_id', 'notes', 'repair_time']
        fields = ['umbrella_id', 'repair_type_id', 'notes']

        labels = {
            'umbrella_id': '伞编号',
            'repair_type_id': '维修类型',
            'notes': '备注',
            # 'repair_time': '维修时间',
        }

        widgets = {
            'umbrella_id': forms.Select(attrs={'class': 'form-select'}),
            'repair_type_id': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control'}),
            # 'repair_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }


class RepairUmbrellaForm(forms.ModelForm):
    is_repaired = forms.BooleanField(required=False, label='维修完成，不报废')

    class Meta:
        model = Repair
        fields = ['umbrella_id', 'repair_type_id', 'notes', 'is_repaired']

        labels = {
            'umbrella_id': '伞编号',
            'repair_type_id': '维修类型',
            'notes': '备注',
            # 'repair_time': '维修时间',
            "is_repaired": '维修完成，不报废',
        }

        widgets = {
            'umbrella_id': forms.Select(attrs={'class': 'form-select'}),
            'repair_type_id': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control'}),
        }

    # def save(self, commit=True):
    #     repair = super().save(commit=False)
    #     if self.cleaned_data['is_repaired']:
    #         repair.repair_time = datetime.now()
    #     else:
    #         repair.notes += " 已报废。"
    #         repair.umbrella_id.umbrella_scrapped = True
    #         repair.umbrella_id.save()
    #     if commit:
    #         repair.save()
    #     return repair
