import datetime
import random

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404

from django.db.models import F, Value, Count
from django.db.models import IntegerField
from django.db.models import ExpressionWrapper

from .filters import OrderFilter
from .forms import *

from django.db.models.functions import Cast
from django.http import JsonResponse, Http404

from django.utils import timezone

from decimal import Decimal


def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            messages.info(request, '用户名或密码不正确，请重新输入~')
            # return render(request, 'login.html', context)
    context = {}
    return render(request, 'login230205.html', context)


def logoutUser(request):
    logout(request)
    return redirect('/login/')
    # if request.method == "GET":
    #     return render(request, "login.html")
    # else:
    #     data_all = UserInfo.objects.all()
    #     data_list = []
    #     for user in data_all:
    #         data_list.append((user.user, user.pwd))
    #
    #     username = request.POST.get("user")
    #     password = request.POST.get("pwd")
    #
    #     if (username, password) in data_list:
    #         # return HttpResponse("登陆成功")
    #         return redirect("https://www.baidu.com")
    #     else:
    #         # return HttpResponse("登陆失败")
    #         return render(request, "login.html", {"error_msg": "登陆失败"})


def register(request):
    form = CreateUserForm()
    context = {'form': form}
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        # print(form)
        if form.is_valid():
            form.save()
            context = {"form": form}
            return redirect('/login/')
        else:
            context = {"form": form}
    return render(request, 'registration.html', context)
    # if req.method == "GET":
    #     return render(request, "register.html")
    # else:
    #     user = request.POST.get("user")
    #     userid = request.POST.get("userid")
    #     school = request.POST.get("school")
    #     pwd = request.POST.get("pwd")
    #     UserInfo.objects.create(user=user, userid=userid, school=school, pwd=pwd)
    #
    #     # return render(request, "register.html", {"success": "注册成功，请前往登录页！"})
    #     return redirect("/login/")


@login_required(login_url='/login/')
def userinfo(request):
    user_list = User.objects.all()
    return render(request, "UserInfo.html", {"user_list": user_list})


@login_required(login_url='/login/')
# @allowed_users(allowed_roles=['admin'])
def test(request):
    class msg_user:
        user_id = ''
        detail = ''

    msg = False
    if request.method == "POST":
        # print(request.POST)
        user_id = request.POST.getlist('user')
        option = request.POST.get('option')
        if option == '查看信息':
            msg = []
            for i in user_id:
                temp = msg_user()
                user = User.objects.filter(id=i).first()
                temp.username = user.username
                temp.user_id = user.user_id
                temp.detail = Diary.objects.filter(user_id=user.user_id).order_by('lending_time')
                msg.append(temp)

        elif option == '删除用户':
            for i in user_id:
                User.objects.filter(id=i).delete()
    # User.objects.create(username='dusadsasidj', name='kuaddden78', userid=1256166, password="129a456", phone="15694954999")

    User_list = User.objects.all().order_by('-user_last_login_date')

    # 获取雨伞列表和相关的站点存放信息
    umbrella_list_with_positions = []
    for umbrella in Umbrella.objects.select_related('umbrella_type_id').all().order_by('umbrella_id'):
        site_storage = SiteStorage.objects.filter(umbrella_id=umbrella).first()
        if site_storage:
            position = f"{site_storage.site_id} - {site_storage.lay_id}"
        else:
            position = "尚未放置"

        status = "不可用"  # 默认状态
        is_alarm = Alarm.objects.filter(umbrella_id=umbrella, alarm_available=True).exists()
        is_in_repair = Repair.objects.filter(umbrella_id=umbrella, repair_time=None).exists()
        is_rented = Diary.objects.filter(umbrella_id=umbrella, return_time__isnull=True).exists()
        is_in_storage = SiteStorage.objects.filter(umbrella_id=umbrella).exists()

        if is_alarm:
            status = "警报中"
        elif is_in_repair:
            status = "待维修"
        elif is_rented:
            status = "占用"
        elif is_in_storage and umbrella.umbrella_available:
            status = "可用"

        umbrella_list_with_positions.append({
            'umbrella': umbrella,
            'position': position,
            'status': status,
            'is_alarm': is_alarm
        })

    log_list = Diary.objects.annotate(
        diary_id_as_int=Cast(F('diary_id'), IntegerField())
    ).order_by('-diary_id_as_int')
    umbrella_type_list = UmbrellaType.objects.all().order_by('umbrella_type_id')

    num_user = User.objects.count()
    num_umbrella = Umbrella.objects.count()
    num_use = Diary.objects.count()
    num_place = Site.objects.count()
    loc_num = Site.objects.count()

    income = 0
    for item in log_list:
        if item.order_price is not None:
            income += item.order_price

    income = round(income, 2)

    # 站点统计
    location_list = Site.objects.all().order_by('site_id')
    for loc in location_list:
        # 筛选与该站点关联的所有SiteStorage记录
        site_storage_records = SiteStorage.objects.filter(site_id=loc.site_id)

        # 初始化可用伞的数量
        loc.num = 0

        # 对于每条记录，检查关联的伞是否可用
        for record in site_storage_records:
            # 确保有伞与此位置相关联
            if not record.umbrella_id:
                loc.num += 1

                # 检查伞是否可用
                # if not record.umbrella_id.umbrella_available:
                #     loc.num += 1
            # else:

    Import_Umbrella_Form = ImportUmbrellaForm()
    place_umbrella = PlaceUmbrella()
    #
    # class pl:
    #     def __init__(self):
    #         self.table = [[0] * 5 for _ in range(5)]
    #         self.id = 0
    #         self.name = ''

    pls = []

    for place in location_list:
        place_info = {
            'id': place.site_id,
            'name': place.site_address,
            'table': [[None for _ in range(5)] for _ in range(5)]  # 假设每个站点有 5x5 的位置表
        }
        pls.append(place_info)

    for place_info in pls:
        # 获取当前站点的所有伞的位置信息
        umbrellas_at_place = SiteStorage.objects.filter(site_id=place_info['id'])

        for umbrella_record in umbrellas_at_place:
            if umbrella_record.umbrella_id:
                # 计算放置位置的行和列，这取决于你的具体布局
                tt = int(umbrella_record.lay_id) - 1
                row = tt // 5
                col = tt % 5
                # 填充位置和伞号信息
                place_info['table'][row][
                    col] = f"{umbrella_record.umbrella_id.umbrella_id}号-{umbrella_record.umbrella_id.umbrella_type_id.umbrella_type}"

    # print(pls)
    # for place in pls:
    #     print(place['name'])
    #     print(place['table'])

    # User_list = User_list[:20]
    # Umbrella_list = Umbrella_list[:20]
    # log_list = log_list[:20]
    report_repair_umbrella_form = ReportRepairUmbrellaForm()
    repair_umbrella_form = RepairUmbrellaForm()
    repair_types = RepairType.objects.all()

    context = {
        "UserInfo_list": User_list,
        "Umbrella_list_with_positions": umbrella_list_with_positions,
        "location_list": location_list,
        "log_list": log_list,
        "num_user": num_user,
        "num_umbrella": num_umbrella,
        "income": income,
        "num_use": num_use,
        "Import_Umbrella_Form": Import_Umbrella_Form,
        "place_umbrella": place_umbrella,
        # "tables": tables,
        "pls": pls,
        "loc_num": loc_num,
        "msg": msg,
        # "cons": cons,
        "ReportRepairUmbrellaForm": report_repair_umbrella_form,
        "RepairUmbrellaForm": repair_umbrella_form,
        "repair_types": repair_types,
    }
    return render(request, "1.html", context)


@login_required(login_url='/login/')
def main(request):
    return render(request, '1.html')


@login_required(login_url='/login/')
def myinfo(req):
    pass


@login_required(login_url='/login/')
def user(request, pk):
    user = User.objects.filter(username=pk).first()

    if request.method == "POST":
        # print(request.POST)
        form = UpdateUserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect(f'/user/{pk}/')

    user_logs = Diary.objects.filter(user_id=user).order_by('-lending_time')

    # print(user_logs)
    use_number = Diary.objects.filter(user_id=user).count()

    my_filter = OrderFilter(request.GET, queryset=user_logs)
    user_logs = my_filter.qs

    update_user_form = UpdateUserForm(instance=user)

    change_password_form = ChangePasswordForm(user=request.user)

    for log in user_logs:
        log.has_comment = Comment.objects.filter(diary_id=log).exists()
        log.comment = Comment.objects.filter(diary_id=log).first() if log.has_comment else None
        # print(log.comment, log.has_comment)

    order_form = OrderForm()

    context = {
        "user": user,
        "user_logs": user_logs,
        "use_number": use_number,
        "my_filter": my_filter,
        "update_user_form": update_user_form,
        "change_password_form": change_password_form,
        "order_form": order_form
    }
    return render(request, 'account.html', context)


@login_required(login_url='/login/')
def user_delete(request):
    name = request.GET.get("name")
    User.objects.filter(username=name).delete()
    return redirect('/')


@login_required(login_url='/login/')
def creat_order(request):
    order_form = OrderForm()

    context = {"order_form": order_form}
    return render(request, 'creat_order.html', context)


# @login_required(login_url='/login/')
# def creat_order_borrow(request):
#     if request.method == "POST":
#         print(request.POST)
#         user_name = request.POST.get('username')
#         req_lending_site_id = request.POST.get('lending_site_id')
#         user = User.objects.filter(username=user_name).first()
#         borrow_place = Site.objects.filter(lending_site_id=req_lending_site_id).first()
#
#         umbrella_place_id = request.POST.get('umbrella_place_id')
#
#         if not umbrella_place_id.isdigit():
#             messages.info(request, '请输入位置的编号')
#             return redirect('/creat_order/')
#
#         umbrella_place_id = int(umbrella_place_id) - 1
#
#         umbrella = Umbrella.objects.filter(place=borrow_place, umbrella_place_id=umbrella_place_id).first()
#
#         if umbrella is None:
#             messages.info(request, '这个位置没有伞')
#             return redirect('/creat_order/')
#
#         if user.umbrella is None:
#             # 更新日志
#             Diary.objects.create(username=user,
#                                  umbrella=umbrella,
#                                  borrow_place=borrow_place)
#
#             # 更新用户借的伞
#             User.objects.filter(username=user_name).update(umbrella=umbrella)
#
#             # 更新伞可用性
#             Umbrella.objects.filter(id=umbrella.id).update(can_use=False, place=None, umbrella_place_id=None)
#
#             # # 更新地点表中的数据
#             # num = location.objects.filter(name=borrow_place).first().get('num')
#             # num -= 1
#             # location.objects.filter(name=borrow_place).update(num=num)
#
#         else:
#             messages.info(request, '您有伞尚未归还，请归还后再借~')
#
#     return redirect('/creat_order/')


@login_required(login_url='/login/')
def creat_order_borrow(request):
    if request.method == "POST":
        user_name = request.POST.get('user')
        req_lending_site_id = request.POST.get('lending_site_id')
        req_lay_id = request.POST.get('umbrella_place_id')

        # 获取用户和站点对象
        user = get_object_or_404(User, username=user_name)
        lending_site = get_object_or_404(Site, site_id=req_lending_site_id)

        # 验证位置序号是否为数字
        if not req_lay_id.isdigit():
            messages.error(request, '请输入有效的位置编号')
            return redirect('/creat_order/')

        # 获取SiteStorage对象来查找相应的伞
        site_storage = SiteStorage.objects.filter(
            site_id=lending_site.site_id,
            lay_id=req_lay_id
        ).first()

        if site_storage and site_storage.umbrella_id and site_storage.umbrella_id.umbrella_available:
            umbrella = site_storage.umbrella_id

            if user.user_umbrella_id is None:
                # 创建借伞记录
                Diary.objects.create(
                    user_id=user,
                    umbrella_id=umbrella,
                    lending_site_id=lending_site,
                    lending_lay_id=req_lay_id,
                    lending_time=timezone.now(),
                    order_price=0.00  # 假设初始费用为0
                )

                # 更新伞的可用状态
                umbrella.umbrella_available = False
                umbrella.save()

                # 更新用户的当前伞
                user.user_umbrella_id = umbrella
                user.save()

                # 清空 SiteStorage 表中对应的伞位置
                site_storage.umbrella_id = None
                site_storage.save()

                messages.success(request, '伞已成功借出')
            else:
                messages.error(request, '您已经借了一把伞')
        else:
            messages.error(request, '选定位置没有可用的伞或伞不存在')

    return redirect('/creat_order/')


# @login_required(login_url='/login/')
# def creat_order_back(request):
#     if request.method == "POST":
#         print(request.POST)
#         user_name = request.POST.get('user')
#         user = User.objects.filter(username=user_name).first()
#         back_place = Site.objects.filter(name=request.POST.get('back_place')).first()
#         umbrella = user.umbrella
#
#         now = 0
#         while Umbrella.objects.filter(place=back_place, umbrella_place_id=now).first():
#             now += 1
#
#             if now == 25:
#                 messages.info(request, '这个地方放满啦~请换个还伞点~')
#                 return redirect('/creat_order/')
#
#         if user.umbrella is not None:
#             the_log = Diary.objects.filter(username=user_name, back_place__isnull=True).first()
#             str_time = the_log.borrow_time
#             str_time = str(str_time)[:19]
#             print(str_time)
#
#             # 计算金额
#             origin_time = datetime.datetime.strptime(str_time, '%Y-%m-%d %H:%M:%S')
#             now_time = datetime.datetime.now()
#             total_time = now_time - origin_time
#             price = total_time.seconds * 0.0002 - 5.76
#
#             # 更新还伞地点和余额
#             Diary.objects.filter(username=user_name, back_place__isnull=True).update(back_place=back_place,
#                                                                                      price=price,
#                                                                                      back_time=datetime.datetime.now())
#
#             # 更新余额和用户借的伞
#             balance = float(user.balance) - price
#             print(balance)
#             User.objects.filter(username=user_name).update(balance=balance, umbrella=None)
#
#             # 更新伞的可用性
#             Umbrella.objects.filter(id=umbrella.id).update(can_use=True, place=back_place, umbrella_place_id=now)
#
#             # # 更新地点表中可用伞的数量
#             # num = location.objects.filter(name=back_place).first().get('num')
#             # num += 1
#             # location.objects.filter(name=back_place).update(num=num)
#             message = f'归还成功，请把您的伞放到{back_place}{now}号处~'
#             messages.info(request, message)
#             return redirect('/creat_order/')
#         else:
#             messages.info(request, '您的账号尚未借伞~')
#     return redirect('/creat_order/')

@login_required(login_url='/login/')
def creat_order_back(request):
    if request.method == "POST":
        user_name = request.POST.get('user')
        req_return_site_id = request.POST.get('return_site_id')
        req_return_lay_id = request.POST.get('return_lay_id')

        user = get_object_or_404(User, username=user_name)
        return_site = get_object_or_404(Site, site_id=req_return_site_id)

        if not req_return_lay_id.isdigit():
            messages.info(request, '请输入有效的归还位置编号')
            return redirect('/creat_order/')

        req_return_lay_id = int(req_return_lay_id)

        print(req_return_site_id, req_return_lay_id)

        print(SiteStorage.objects.filter(site_id=req_return_site_id, lay_id=req_return_lay_id).first().umbrella_id)

        umbrella_place = SiteStorage.objects.filter(site_id=req_return_site_id, lay_id=req_return_lay_id).first()
        umbrella_in_this_place = umbrella_place.umbrella_id

        # 检查该位置是否空闲
        if umbrella_in_this_place:
            messages.info(request, '选定的位置已有伞，请选择其他位置')
            return redirect('/creat_order/')

        # 检查用户是否有借伞记录
        if user.user_umbrella_id:
            umbrella = user.user_umbrella_id

            # 查找用户的借伞记录
            the_log = Diary.objects.filter(user_id=user, return_time__isnull=True).first()
            if the_log:
                # 计算费用
                lending_time = the_log.lending_time
                now_time = timezone.now()
                total_time = now_time - lending_time
                price = total_time.seconds * 0.0002

                # 更新日志记录
                the_log.return_site_id = return_site
                the_log.return_lay_id = req_return_lay_id
                the_log.return_time = now_time
                the_log.order_price = price
                the_log.save()

                # 更新用户余额和伞的状态
                user.user_balance -= Decimal(price)
                user.user_umbrella_id = None
                user.save()

                # 更新伞的可用性和位置
                umbrella.umbrella_available = True
                umbrella.save()

                # 更新 SiteStorage 表中的数据
                # SiteStorage.objects.create(site_id=return_site, lay_id=req_return_lay_id, umbrella_id=umbrella)
                umbrella_place.umbrella_id = umbrella
                umbrella_place.save()

                messages.success(request, f'伞已归还到位置: {req_return_lay_id}，费用: {price}')
                return redirect('/creat_order/')
            else:
                messages.info(request, '没有找到您的借伞记录')
        else:
            messages.info(request, '您没有借出的伞')

    return redirect('/creat_order/')


@login_required(login_url='/login/')
def import_umbrella(request):
    if request.method == "POST":
        n = request.POST.get("quantity")
        type = request.POST.get("umbrella_type_id")
        price = request.POST.get("umbrella_cost_price")
        n = int(n)

        tp = UmbrellaType.objects.filter(umbrella_type_id=type).first()

        for i in range(n):
            Umbrella.objects.create(
                umbrella_warehousing_date=datetime.datetime.now(),  # 设置当前时间为入库日期
                umbrella_available=False,  # 新伞默认设置为不可用
                umbrella_type_id=tp,  # 设置伞类型
                umbrella_cost_price=price  # 设置伞成本价
            )

    return redirect('/')


@login_required(login_url='/login/')
def report_repair_umbrella(request):
    if request.method == 'POST':
        form = ReportRepairUmbrellaForm(request.POST)
        if form.is_valid():
            repair = form.save(commit=False)
            # repair.repair_time = timezone.now()  # 设置当前时间为维修时间
            repair.save()
            return redirect('/')  # 重定向到合适的页面
    else:
        form = ReportRepairUmbrellaForm()
    return redirect('/')

    # return render(request, '1.html', {'RepairUmbrellaForm': form})


# @login_required(login_url='/login/')
# def repair_umbrella(request):
#     if request.method == 'POST':
#         form = RepairUmbrellaForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('/')  # 重定向到合适的页面
#         # else:
#     # 筛选出需要维修的伞
#     # pending_repairs = Repair.objects.filter(repair_time__isnull=True)
#     # form = RepairUmbrellaForm()
#     return redirect('/')
#
#     # return render(request, '1.html', {'RepairUmbrellaForm': form, 'pending_repairs': pending_repairs})

@login_required(login_url='/login/')
def repair_umbrella(request):
    if request.method == 'POST':
        form = RepairUmbrellaForm(request.POST)
        if form.is_valid():
            umbrella_id = form.cleaned_data['umbrella_id']
            # 获取或创建相应的维修记录
            repair, created = Repair.objects.get_or_create(umbrella_id=umbrella_id, repair_time__isnull=True)
            # 更新维修记录
            repair.repair_type_id = form.cleaned_data['repair_type_id']
            repair.notes = form.cleaned_data['notes']
            if form.cleaned_data['is_repaired']:
                repair.repair_time = datetime.now()
            else:
                repair.notes += " 已报废。"
                repair.umbrella_id.umbrella_scrapped = True
                repair.umbrella_id.save()
            repair.save()
            return redirect('/')  # 重定向到合适的页面
        # 如果表单无效，重新渲染表单
    else:
        form = RepairUmbrellaForm()

    # 筛选出需要维修的伞
    pending_repairs = Repair.objects.filter(repair_time__isnull=True)
    return render(request, '1.html', {'RepairUmbrellaForm': form, 'pending_repairs': pending_repairs})


@login_required(login_url='/login/')
def get_pending_repairs(request):
    repairs = Repair.objects.filter(repair_time__isnull=True)
    data = [{'umbrella_id': repair.umbrella_id.umbrella_id,
             'repair_type_id': repair.repair_type_id.repair_type_id if repair.repair_type_id else '',
             'notes': repair.notes} for repair in repairs]
    if data:
        return JsonResponse({'repairs': data})
    return JsonResponse({'error': 'No pending repairs found'})


@login_required(login_url='/login/')
def get_umbrellas_for_repair(request, repair_type_id=None):
    if repair_type_id:
        umbrellas = Repair.objects.filter(repair_type_id=repair_type_id, repair_time__isnull=True)
        data = [{'umbrella_id': repair.umbrella_id.umbrella_id} for repair in umbrellas]
        return JsonResponse({'umbrellas': data})


@login_required(login_url='/login/')
def get_repair_notes(request, umbrella_id=None):
    if umbrella_id:
        try:
            repair = Repair.objects.get(umbrella_id=umbrella_id, repair_time__isnull=True)
            return JsonResponse({'notes': repair.notes})
        except Repair.DoesNotExist:
            return JsonResponse({'notes': '没有找到对应的备注信息。'})



@login_required(login_url='/login/')
def place_umbrella(request):
    if request.method == "POST":
        # print(request.POST)
        start = request.POST.get('start')
        end = request.POST.get('end')
        if not (start.isdigit() and end.isdigit()):
            messages.info(request, '请输入数字')
            return redirect('/')
        start = int(start)
        end = int(end)
        place = request.POST.get('place')
        place_name = Site.objects.filter(id=request.POST.get('place')).first().name
        now = 0
        flag = False
        for i in range(min(start, end), max(start, end) + 1):
            if Umbrella.objects.filter(place=place, id=i).first():
                messages.info(request, f'第{i}号伞已经在{place_name}啦~')
            else:
                while Umbrella.objects.filter(place=place, umbrella_place_id=now).first():
                    now += 1
                    if now == 25:
                        messages.info(request, '此处已放满，请重新放置')
                        flag = True

                if flag:
                    break
                else:
                    Umbrella.objects.filter(id=i).update(can_use=True, place=place, umbrella_place_id=now)

        messages.info(request, '已成功放置~')
        return redirect(f'/place_detail/{place}/')


@login_required(login_url='/login/')
def place_detail(request, pk):
    place = Site.objects.filter(id=pk).first()
    table = [[0] * 5 for _ in range(5)]
    for i in range(25):
        a = Umbrella.objects.filter(place=place, umbrella_place_id=i).first()
        if a:
            table[i // 5][i % 5] = str(a.id) + '号-' + str(a.type)
        else:
            table[i // 5][i % 5] = False
    context = {
        "table": table,
        "place": place,
    }
    return render(request, 'place_detail.html', context)


def add_comment(request, diary_id):
    user = request.user
    if request.method == 'POST':
        diary = get_object_or_404(Diary, diary_id=diary_id)
        comment_content = request.POST.get('comment_content')
        comment_score = request.POST.get('comment_score', 0)

        # 创建并保存评论
        Comment.objects.create(
            user_id=request.user,
            umbrella_id=diary.umbrella_id,
            diary_id=diary,
            comment_content=comment_content,
            comment_score=comment_score,
            comment_time=timezone.now()
        )
        return redirect(f"/user/{user.username}/")  # 重定向到合适的页面
    else:
        return redirect(f'/user/{user.username}/')  # GET 请求时的重定向


def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, user=request.user)
        if form.is_valid():
            cleanData = form.cleaned_data
            request.user.set_password(cleanData['password'])
            request.user.save()
            messages.success(request, '操作成功！')
            return redirect('/')
        else:
            text = """
            修改密码错误！
            1. 新密码与账户信息过于相似
            2. 原密码输入错误
            3.前后两次密码不一致~
            请查正后再输入~
            """
            messages.info(request, text)
            return redirect(f'/user/{request.user.username}/')
    change_password_form = ChangePasswordForm(user=request.user)
    context = {
        'title': "修改密码",
        'change_password_form': change_password_form,
    }
    return render(request, 'change_password.html', context)


def account_login_page(request):
    return redirect('/login/')


@login_required(login_url='/login/')
def get_empty_positions(request, site_id):
    # 获取站点的所有位置和对应的伞号
    positions_with_umbrellas = SiteStorage.objects.filter(
        site_id=site_id,
        umbrella_id__isnull=False  # 确保位置上有伞
    ).values_list('lay_id', 'umbrella_id')

    # 构建一个字典，包含位置和对应的伞号
    positions_info = {lay_id: umbrella_id for lay_id, umbrella_id in positions_with_umbrellas}

    return JsonResponse({'positions_info': positions_info})


@login_required(login_url='/login/')
def get_free_positions(request, site_id):
    # 确保站点存在
    site = get_object_or_404(Site, site_id=site_id)
    # site = Site.objects.filter(site_id=site_id)

    # 获取指定站点的所有空闲位置
    free_positions = SiteStorage.objects.filter(
        site_id=site.site_id,
        umbrella_id__isnull=True
    ).values_list('lay_id', flat=True)

    # 将查询结果转换为列表
    free_positions_list = list(free_positions)

    # 返回空闲位置的列表
    return JsonResponse({'free_positions': free_positions_list})


def ran(request):
    LOCATIONS = [
        '信工楼-1',
        '信工楼-2',
        '信工楼-3',
        '物流楼-1',
        '物流楼-2',
        '物流楼-3',
        '法学院-1',
        '法学院-2',
        '法学院-3',
        '图书馆-1',
        '图书馆-2',
        '图书馆-3',
        '图书馆-4',
        '教学区-1-1',
        '教学区-1-2',
        '教学区-1-3',
        '教学区-2-1',
        '教学区-2-2',
        '教学区-2-3',
        '教学区-3-1',
        '教学区-3-2',
        '教学区-3-3',
        '海馨食堂-1',
        '海馨食堂-2',
        '海联食堂-1',
        '海联食堂-2',
        '海琴食堂-1',
        '海琴食堂-2',
    ]

    UMBRELLA_NUM = int(len(LOCATION) * 0.7 * 25)
    UMBRELLA_TYPE = [
        '伸缩伞',
        '长柄伞',
        '晴雨伞',
        '自动伞',
        '透明伞',
    ]
    USER_NUM = random.randint(200, 500)

    def random_time():
        YEAR = [
            '2020',
            '2021',
            '2022',
        ]
        MONTH = 12
        DATE = [31, 28, 31, 30, 31, 30, 31, 30, 31, 30, 31, 30]
        HOUR_START = 7
        HOUR_END = 23
        MINUTE = 59
        SECOND = 59
        year = random.choice(YEAR)
        month = random.randint(1, MONTH)
        date = random.randint(1, DATE[MONTH])
        hour = random.randint(HOUR_START, HOUR_END)
        minute = random.randint(1, MINUTE)
        second = random.randint(1, SECOND)
        return datetime.datetime(year, month, date, hour, minute, second)

    for loc in LOCATIONS:
        Site.objects.create(name=loc, num_sum=25)

    for t in UMBRELLA_TYPE:
        UmbrellaType.objects.create(type=t)

    for i in range(UMBRELLA_NUM):
        type = UmbrellaType.objects.filter(type=random.choice(UMBRELLA_TYPE)).first()
        place = Site.objects.filter(name=random.choice(LOCATIONS)).first()
        num = 1
        while Umbrella.objects.filter(place=place, umbrella_place_id=num).first():
            place = Site.objects.filter(name=random.choice(LOCATIONS)).first()
            num = random.randint(1, 25)

        tm = random_time()
        tm_ = tm + datetime.timedelta(hours=random.randint(1, 9), minutes=random.randint(1, 59))
        tm__ = tm + datetime.timedelta(days=random.randint(1, 10))
        Umbrella.objects.create(import_time=tm,
                                can_use=True,
                                type=type,
                                place=place,
                                umbrella_place_id=num,
                                last_use=tm__,
                                price=random.randint(20, 35))

    use = User.objects.filter(id=1).first()
    umbrella = Umbrella.objects.filter(id=1).first()
    loc = Site.objects.filter(id=1).first()
    import datetime
    dt = datetime.datetime(2019, 6, 10, 10, 20, 5)
    Diary.objects.create(username=use, umbrella=umbrella, borrow_place=loc, borrow_time=dt)
    return HttpResponse("添加成功")
