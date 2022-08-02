from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from .forms import HelloForm, FirstForm, SecondForm, ThirdForm, FourthForm, FifthForm, SixthForm, IdForm, Create, CreateForm
from .models import Friend
from django.db.models import QuerySet

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

def createindex(request):
    data = Friend.objects.all()
    params = {
        'title': 'Default',
        'data': data,
    }
    return render(request, 'hello/create/index.html', params)

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
        return redirect(to='/hello/create')
    return render(request, 'hello/create/create.html', params)

def createmeta(request):
    if (request.method == 'POST'):
        obj = Friend()
        friend = CreateForm(request.POST, instance=obj)
        friend.save()
        return redirect(to='/hello/create')
    params = {
        'title': 'CreateMeta',
        'form': CreateForm(),
    }
    return render(request, 'hello/create/create.html', params)
