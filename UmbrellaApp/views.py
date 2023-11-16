import datetime
import random

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, HttpResponse

from .filters import OrderFilter
from .forms import *


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
    form = CreatUserForm()
    context = {'form': form}
    if request.method == "POST":
        form = CreatUserForm(request.POST)
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
        name = ''
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
                temp.name = user.name
                temp.detail = Diary.objects.filter(username=user.name).order_by('borrow_time')
                msg.append(temp)

        elif option == '删除用户':
            for i in user_id:
                User.objects.filter(id=i).delete()
    # User.objects.create(username='dusadsasidj', name='kuaddden78', userid=1256166, password="129a456", phone="15694954999")

    User_list = User.objects.all().order_by('-user_registration_date')
    Umbrella_list = Umbrella.objects.all().order_by('umbrella_id')
    location_list = Site.objects.all().order_by('site_id')
    log_list = Diary.objects.all().order_by('-diary_id')

    num_user = User.objects.count()
    num_umbrella = Umbrella.objects.count()
    num_use = Diary.objects.count()
    num_place = Site.objects.count()
    loc_num = Site.objects.count()

    income = 0
    for item in log_list:
        if item.price is not None:
            income += item.price

    for loc in location_list:
        loc.num = Umbrella.objects.filter(place=loc.id, can_use=True).count()

    Import_Umbrella_Form = ImportUmbrellaForm()
    place_umbrella = PlaceUmbrella()

    class pl:
        def __init__(self):
            self.table = [[0] * 5 for _ in range(5)]
            self.id = 0
            self.name = ''

    location_num = Site.objects.all().count()
    pls = [pl() for _ in range(location_num)]
    # tables = [[[0] * 5 for _ in range(5)] for _ in range(location_num)]
    for place_num in range(location_num):
        place = Site.objects.filter(id=place_num + 1).first()
        pls[place_num].id = place_num + 1
        pls[place_num].name = place.name
        for i in range(25):
            umbrella = Umbrella.objects.filter(place=place, umbrella_place_id=i).first()
            if umbrella:
                pls[place_num].table[i // 5][i % 5] = str(umbrella.id) + '号-' + str(umbrella.type)
                # tables[i // 5][i % 5][place_num] = str(a.id) + '号-' + str(a.type)
            else:
                pls[place_num].table[i // 5][i % 5] = False
                # tables[i // 5][i % 5][place_num] = False

    # print(pls[0].id, pls[1].id, pls[0].name, pls[1].name)

    context = {
        "UserInfo_list": User_list,
        "Umbrella_list": Umbrella_list,
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
        print(request.POST)
        form = UpdateUserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect(f'/user/{pk}/')

    user_logs = Diary.objects.filter(username=pk).order_by('-id')
    use_number = Diary.objects.filter(username=pk).count()

    my_filter = OrderFilter(request.GET, queryset=user_logs)
    user_logs = my_filter.qs

    update_user_form = UpdateUserForm(instance=user)

    change_password_form = ChangePasswordForm(user=request.user)

    context = {
        "user": user,
        "user_logs": user_logs,
        "use_number": use_number,
        "my_filter": my_filter,
        "update_user_form": update_user_form,
        "change_password_form": change_password_form,
    }
    return render(request, 'account.html', context)


@login_required(login_url='/login/')
def user_delete(request):
    name = request.GET.get("name")
    User.objects.filter(username=name).delete()
    return redirect('/')


@login_required(login_url='/login/')
def creat_order(request):
    form = OrderForm()

    context = {"form": form}
    return render(request, 'creat_order.html', context)


@login_required(login_url='/login/')
def creat_order_borrow(request):
    if request.method == "POST":
        print(request.POST)
        user_name = request.POST.get('user')
        user = User.objects.filter(username=user_name).first()
        borrow_place = Site.objects.filter(name=request.POST.get('borrow_place')).first()

        umbrella_place_id = request.POST.get('umbrella_place_id')

        if not umbrella_place_id.isdigit():
            messages.info(request, '请输入位置的编号')
            return redirect('/creat_order/')

        umbrella_place_id = int(umbrella_place_id) - 1

        umbrella = Umbrella.objects.filter(place=borrow_place, umbrella_place_id=umbrella_place_id).first()

        if umbrella is None:
            messages.info(request, '这个位置没有伞')
            return redirect('/creat_order/')

        if user.umbrella is None:
            # 更新日志
            Diary.objects.create(username=user,
                               umbrella=umbrella,
                               borrow_place=borrow_place)

            # 更新用户借的伞
            User.objects.filter(username=user_name).update(umbrella=umbrella)

            # 更新伞可用性
            Umbrella.objects.filter(id=umbrella.id).update(can_use=False, place=None, umbrella_place_id=None)

            # # 更新地点表中的数据
            # num = location.objects.filter(name=borrow_place).first().get('num')
            # num -= 1
            # location.objects.filter(name=borrow_place).update(num=num)

        else:
            messages.info(request, '您有伞尚未归还，请归还后再借~')

    return redirect('/creat_order/')


@login_required(login_url='/login/')
def creat_order_back(request):
    if request.method == "POST":
        print(request.POST)
        user_name = request.POST.get('user')
        user = User.objects.filter(username=user_name).first()
        back_place = Site.objects.filter(name=request.POST.get('back_place')).first()
        umbrella = user.umbrella

        now = 0
        while Umbrella.objects.filter(place=back_place, umbrella_place_id=now).first():
            now += 1

            if now == 25:
                messages.info(request, '这个地方放满啦~请换个还伞点~')
                return redirect('/creat_order/')

        if user.umbrella is not None:
            the_log = Diary.objects.filter(username=user_name, back_place__isnull=True).first()
            str_time = the_log.borrow_time
            str_time = str(str_time)[:19]
            print(str_time)

            # 计算金额
            origin_time = datetime.datetime.strptime(str_time, '%Y-%m-%d %H:%M:%S')
            now_time = datetime.datetime.now()
            total_time = now_time - origin_time
            price = total_time.seconds * 0.0002 - 5.76

            # 更新还伞地点和余额
            Diary.objects.filter(username=user_name, back_place__isnull=True).update(back_place=back_place,
                                                                                   price=price,
                                                                                   back_time=datetime.datetime.now())

            # 更新余额和用户借的伞
            balance = float(user.balance) - price
            print(balance)
            User.objects.filter(username=user_name).update(balance=balance, umbrella=None)

            # 更新伞的可用性
            Umbrella.objects.filter(id=umbrella.id).update(can_use=True, place=back_place, umbrella_place_id=now)

            # # 更新地点表中可用伞的数量
            # num = location.objects.filter(name=back_place).first().get('num')
            # num += 1
            # location.objects.filter(name=back_place).update(num=num)
            message = f'归还成功，请把您的伞放到{back_place}{now}号处~'
            messages.info(request, message)
            return redirect('/creat_order/')
        else:
            messages.info(request, '您的账号尚未借伞~')
    return redirect('/creat_order/')


@login_required(login_url='/login/')
def import_umbrella(request):
    if request.method == "POST":
        n = request.POST.get("quantity")
        type = request.POST.get("type")
        price = request.POST.get("price")
        n = int(n)

        tp = UmbrellaType.objects.filter(type=type).first()

        for i in range(n):
            Umbrella.objects.create(type=tp, price=price, can_use=False)

    return redirect('/')


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
            1. 新密码与账户信息过于相似fatkun
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
