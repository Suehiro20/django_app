from django.shortcuts import render
from django.views.generic import ListView, DetailView, FormView
from django.urls import reverse_lazy
from .forms import ContactForm
from django.contrib import messages
from django.core.mail import EmailMessage
from .models import BlogPost

# Create your views here.

class Index(ListView):
    template_name = 'index.html'
    context_object_name = 'orderby_records'
    queryset = BlogPost.objects.order_by('-posted_at')
    paginate_by = 4

class BlogDetail(DetailView):
    template_name = 'post.html'
    model = BlogPost

class ScienceView(ListView):
    template_name = 'science_list.html'
    model = BlogPost
    context_object_name = 'science_records'
    queryset = BlogPost.objects.filter(category='science').order_by('-posted_at')
    paginate_by = 2

class DailylifeView(ListView):
    template_name = 'dailylife_list.html'
    model = BlogPost
    context_object_name = 'dailylife_records'
    queryset = BlogPost.objects.filter(category='dailylife').order_by('-posted_at')
    paginate_by = 2

class MusicView(ListView):
    template_name = 'music_list.html'
    model = BlogPost
    context_object_name = 'music_records'
    queryset = BlogPost.objects.filter(category='music').order_by('-posted_at')
    paginate_by = 2

class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('blogapp:contact')

    def form_valid(self, form):
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        title = form.cleaned_data['title']
        message = form.cleaned_data['message']
        subject = 'お問い合わせ：{}'.format(title)
        message = \
          '送信者：{0}\nメールアドレス：{1}\nタイトル：{2}\nメッセージ：\n{3}'\
          .format(name, email, title, message)
        from_email = 'suematsu.hiroki.fw@gmail.com'
        to_list = ['suematsu.hiroki.fw@gmail.com']
        message = EmailMessage(subject=subject,
                               body=message,
                               from_email=from_email,
                               to=to_list,
                               )
        message.send()
        messages.success(
            self.request, 'お問い合わせは正常に送信されました。'
        )
        return super().form_valid(form)