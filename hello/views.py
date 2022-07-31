from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from .forms import HelloForm

# def index(request):
#     msg = request.GET['msg']
#     return HttpResponse('you typed: "' + msg + '".')

# def index(request):
#     if 'msg' in request.GET:
#         msg = request.GET['msg']
#         result = 'you typed: "' + msg + '".'
#     else:
#         result = 'please send msg parameter!'
#     return HttpResponse(result)

# def index(request):
#     params = {
#         'title': 'Hello/Index',
#         'msg': 'これは、サンプルで作ったページです。',
#         'goto': 'next',
#     }
#     return render(request, 'hello/index.html', params)

# def next(request):
#     params = {
#         'title': 'Hello/Next',
#         'msg': 'これは、もう一つのページです。',
#         'goto': 'index',
#     }
#     return render(request, 'hello/index.html', params)

# def form(request):
#     msg = request.POST['msg']
#     params = {
#         'title': 'Hello/Form',
#         'msg': 'こんにちは、' + msg + 'さん。',
#         'goto': 'index'
#     }
#     return render(request, 'hello/index.html', params)

# def index(request):
#     params = {
#         'title': 'Hello',
#         'message': 'your data:',
#         'form': HelloForm(),
#     }
#     if (request.method == 'POST'):
#         params['message'] = '名前：' + request.POST['name'] + \
#             '<br>メール：' + request.POST['mail'] + \
#             '<br>年齢：' + request.POST['age']
#         params['form'] = HelloForm(request.POST)
#     return render(request, 'hello/index.html', params)

class HelloView(TemplateView):
    def __init__(self):
        self.params = {
            'title': 'Hello',
            'form': HelloForm(),
            'result': None,
        }
    
    def get(self, request):
        return render(request, 'hello/index.html', self.params)
    
    def post(self, request):
        ch = request.POST.getlist('choice')
        result = '<ol><b>selected:</b>'
        for i in ch:
            result += '<li>' + i + '</li>'
        result += '</ol>'
        self.params['result'] = result
        self.params['form'] = HelloForm(request.POST)
        return render(request, 'hello/index.html', self.params)
