from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from .forms import HelloForm, FirstForm, SecondForm, ThirdForm, FourthForm, FifthForm, SixthForm, \
    IdForm, Create, FriendForm, FindForm, CheckForm, MessageForm
from .models import Friend, Message
from django.db.models import QuerySet, Count, Sum, Avg, Min, Max
from django.core.paginator import Paginator

def index(request):
    params = {
        'title': 'Index',
        'msg': 'これは、トップページです。',
        'goto': 'next',
        'form': 'form',
        'users': 'users',
        'manager': 'manager',
    }
    return render(request, 'hello/index.html', params)

# def index(request):
#     msg = request.GET['msg']
#     return HttpResponse('you typed: "' + msg + '".')

def query(request):
    if 'msg' in request.GET:
        msg = request.GET['msg']
        result = 'you typed: "' + msg + '".'
    else:
        result = 'please send msg parameter!'
    return HttpResponse(result)

def queries(request, id, nickname):
    result = 'your id: ' + str(id) + ', name: "' + nickname + '".'
    return HttpResponse(result)

def next(request):
    params = {
        'title': 'Next',
        'msg': 'これは、もう一つのページです。',
        'goto': 'index',
        'form': 'form',
        'users': 'users',
        'manager': 'manager',
    }
    return render(request, 'hello/index.html', params)

def form(request):
    params = {
        'title': 'Default',
        'msg': 'フォームトップページです。<br>クリックは無効ですよ。',
    }
    return render(request, 'hello/form.html', params)

def formfirst(request):
    params = {
        'title': 'Field',
        'msg': 'your data:',
        'form': FirstForm(),
    }
    if (request.method == 'POST'):
        params['msg'] = '名前：' + request.POST['name'] + \
            '<br>メール：' + request.POST['mail'] + \
            '<br>年齢：' + request.POST['age']
        params['form'] = FirstForm(request.POST)
    return render(request, 'hello/form.html', params)

def formsecond(request):
    params = {
        'title': 'Checkbox',
        'msg': None,
        'form': SecondForm(),
    }
    if (request.method == 'POST'):
        if ('check' in request.POST):
            params['msg'] = 'Checked!!'
        else:
            params['msg'] = 'not checked...'
        params['form'] = SecondForm(request.POST)
    return render(request, 'hello/form.html', params)

def formthird(request):
    params = {
        'title': 'NullBoolean',
        'msg': None,
        'form': ThirdForm(),
    }
    if (request.method == 'POST'):
        chk = request.POST['check']
        params['msg'] = 'you selected: "' + chk + '".'
        params['form'] = ThirdForm(request.POST)
    return render(request, 'hello/form.html', params)

def formfourth(request):
    params = {
        'title': 'PullDown',
        'msg': None,
        'form': FourthForm(),
    }
    if (request.method == 'POST'):
        ch = request.POST['choice']
        params['msg'] = 'you selected: "' + ch + '".'
        params['form'] = FourthForm(request.POST)
    return render(request, 'hello/form.html', params)

def formfifth(request):
    params = {
        'title': 'Radio',
        'msg': None,
        'form': FifthForm(),
    }
    if (request.method == 'POST'):
        ch = request.POST['choice']
        params['msg'] = 'you selected: "' + ch + '".'
        params['form'] = FifthForm(request.POST)
    return render(request, 'hello/form.html', params)

def formsixth(request):
    params = {
        'title': 'List',
        'msg': None,
        'form': SixthForm(),
    }
    if (request.method == 'POST'):
        ch = request.POST['choice']
        params['msg'] = 'you selected: "' + ch + '".'
        params['form'] = FifthForm(request.POST)
    return render(request, 'hello/form.html', params)

class HelloView(TemplateView):
    def __init__(self):
        self.params = {
            'title': 'Multiple',
            'msg': None,
            'form': HelloForm(),
        }
    
    def get(self, request):
        return render(request, 'hello/form.html', self.params)
    
    def post(self, request):
        ch = request.POST.getlist('choice')
        result = '<ol><b>selected:</b>'
        for i in ch:
            result += '<li>' + i + '</li>'
        result += '</ol>'
        self.params['msg'] = result
        self.params['form'] = HelloForm(request.POST)
        return render(request, 'hello/form.html', self.params)

def users(request):
    data = Friend.objects.all()
    params = {
        'title': 'Userall',
        'message': 'all freinds.',
        'data': data,
    }
    return render(request, 'hello/users.html', params)

def userid(request):
    params = {
        'title': 'Userid',
        'message': 'all friends.',
        'form': IdForm(),
        'data': [],
    }
    if (request.method == 'POST'):
        num = request.POST['id']
        item = Friend.objects.get(id=num)
        params['data'] = [item]
        params['form'] = IdForm(request.POST)
    else:
        params['data'] = Friend.objects.all()
    return render(request, 'hello/users.html', params)

def manager(request):
    data = Friend.objects.all()
    params = {
        'title': 'Default',
        'data': data,
    }
    return render(request, 'hello/manager/index.html', params)

def managervalues(request):
    data = Friend.objects.all().values()
    params = {
        'title': 'Values',
        'data': data,
    }
    return render(request, 'hello/manager/index.html', params)

def managervalueslim(request):
    data = Friend.objects.all().values('id', 'name')
    params = {
        'title': 'ValuesLim',
        'data': data,
    }
    return render(request, 'hello/manager/index.html', params)

def managervalueslist(request):
    data = Friend.objects.all().values_list('id', 'name', 'age')
    params = {
        'title': 'ValuesList',
        'data': data,
    }
    return render(request, 'hello/manager/index.html', params)

def managervaluesothers(request):
    num = Friend.objects.all().count()
    first = Friend.objects.all().first()
    last = Friend.objects.all().last()
    data = [num, first, last]
    params = {
        'title': 'ValuesOthers',
        'data': data,
    }
    return render(request, 'hello/manager/index.html', params)

def __new_str__(self):
    result = ''
    for item in self:
        result += '<tr>'
        for k in item:
            result += '<td>' + str(k) + '=' + str(item[k]) + '</td>'
        result += '</tr>'
    return result

QuerySet.__str__ = __new_str__

def managerqueryset(request):
    data = Friend.objects.all().values('id', 'name', 'age')
    params = {
        'title': 'QuerySet',
        'data': data,
    }
    return render(request, 'hello/manager/queryset.html', params)

def crudindex(request):
    data = Friend.objects.all()
    params = {
        'title': 'Default',
        'data': data,
    }
    return render(request, 'hello/crud/index.html', params)

def create(request):
    params = {
        'title': 'Create',
        'form': Create(),
    }
    if (request.method == 'POST'):
        name = request.POST['name']
        mail = request.POST['mail']
        gender = 'gender' in request.POST
        age = int(request.POST['age'])
        birth = request.POST['birthday']
        friend = Friend(name=name, mail=mail, gender=gender, age=age, birthday=birth)
        friend.save()
        return redirect(to='/hello/crud')
    return render(request, 'hello/crud/create.html', params)

def createmeta(request):
    if (request.method == 'POST'):
        obj = Friend()
        friend = FriendForm(request.POST, instance=obj)
        friend.save()
        return redirect(to='/hello/crud')
    params = {
        'title': 'CreateMeta',
        'form': FriendForm(),
    }
    return render(request, 'hello/crud/create.html', params)

def edit(request, num):
    obj = Friend.objects.get(id=num)
    if (request.method == 'POST'):
        friend = FriendForm(request.POST, instance=obj)
        friend.save()
        return redirect(to='/hello/update')
    params = {
        'title': 'Update',
        'id': num,
        'form': FriendForm(instance=obj)
    }
    return render(request, 'hello/crud/edit.html', params)

def delete(request, num):
    friend = Friend.objects.get(id=num)
    if (request.method == 'POST'):
        friend.delete()
        return redirect(to='/hello/crud')
    params = {
        'title': 'Delete',
        'id': num,
        'obj': friend
    }
    return render(request, 'hello/crud/delete.html', params)

def find(request):
    if (request.method == 'POST'):
        msg = 'serch result:'
        form = FindForm(request.POST)
        str = request.POST['find']
        data = Friend.objects.filter(name__icontains=str)
    else:
        msg = 'serch words ...'
        form = FindForm()
        data = Friend.objects.all()
    params = {
        'title': 'Find',
        'message': msg,
        'form': form,
        'data': data,
    }
    return render(request, 'hello/find.html', params)

def age(request):
    data = Friend.objects.all().order_by('age')
    params = {
        'title': 'Hello',
        'message': '',
        'data': data,
    }
    return render(request, 'hello/data/index.html', params)

def agerev(request):
    data = Friend.objects.all().order_by('age').reverse()
    params = {
        'title': 'Hello',
        'message': '',
        'data': data,
    }
    return render(request, 'hello/data/index.html', params)

def select(request):
    if (request.method == 'POST'):
        msg = 'serch result:'
        form = FindForm(request.POST)
        str = request.POST['find']
        list = str.split()
        data = Friend.objects.all()[int(list[0]):int(list[1])]
    else:
        msg = 'serch words ...'
        form = FindForm()
        data = Friend.objects.all()
    params = {
        'title': 'Find',
        'message': msg,
        'form': form,
        'data': data,
        'path': 'select',
    }
    return render(request, 'hello/data/find.html', params)

def syukei(request):
    data = Friend.objects.all()
    re1 = Friend.objects.aggregate(Count('age'))
    re2 = Friend.objects.aggregate(Sum('age'))
    re3 = Friend.objects.aggregate(Avg('age'))
    re4 = Friend.objects.aggregate(Min('age'))
    re5 = Friend.objects.aggregate(Max('age'))
    msg = 'Count:' + str(re1['age__count'])\
        + '<br>Sum:' + str(re2['age__sum'])\
        + '<br>Average:' + str(re3['age__avg'])\
        + '<br>Min:' + str(re4['age__min'])\
        + '<br>Max:' + str(re5['age__max'])
    params = {
        'title': 'Hello',
        'message': msg,
        'data': data
    }
    return render(request, 'hello/data/index.html', params)

def sqlquery(request):
    if (request.method == 'POST'):
        msg = request.POST['find']
        form = FindForm(request.POST)
        sql = 'select * from hello_friend'
        if (msg != ''):
            sql += ' where ' + msg
        data = Friend.objects.raw(sql)
        msg = sql
    else:
        msg = 'serch words...'
        form = FindForm()
        data = Friend.objects.all()
    params = {
        'title': 'Hello',
        'message': msg,
        'form': form,
        'data': data,
        'path': 'sqlquery',
    }
    return render(request, 'hello/data/find.html', params)

def check(request):
    params = {
        'title': 'Hello',
        'message': 'check validation',
        'form': CheckForm(),
    }
    if (request.method == 'POST'):
        form = CheckForm(request.POST)
        params['form'] = form
        if (form.is_valid()):
            params['message'] = 'OK!'
        else:
            params['message'] = 'not good.'
    return render(request, 'hello/check.html', params)

def checktwo(request):
    params = {
        'title': 'Hello',
        'message': 'check validation.',
        'form': FriendForm(),
    }
    if (request.method == 'POST'):
        obj = Friend()
        form = FriendForm(request.POST, instance=obj)
        params['form'] = form
        if (form.is_valid()):
            params['message'] = 'OK!'
        else:
            params['message'] = 'not good.'
    return render(request, 'hello/checks.html', params)

def page(request, num=1):
    data = Friend.objects.all()
    page = Paginator(data, 3)
    params = {
        'title': 'Hello',
        'message': '',
        'data': page.get_page(num),
    }
    return render(request, 'hello/page.html', params)

def message(request, page=1):
    if (request.method == 'POST'):
        obj = Message()
        form = MessageForm(request.POST, instance=obj)
        form.save()
    data = Message.objects.all().reverse()
    paginator = Paginator(data, 5)
    params = {
        'title': 'Message',
        'form': MessageForm(),
        'data': paginator.get_page(page),
    }
    return render(request, 'hello/message.html', params)

def top(request, num=1):
    data = Friend.objects.all()
    page = Paginator(data, 3)
    params = {
        'title': 'Hello',
        'message': '',
        'data': page.get_page(num),
    }
    return render(request, 'hello/top.html', params)