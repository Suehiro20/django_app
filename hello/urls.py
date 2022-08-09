from django.urls import path
from . import views
from django.conf.urls import url
from .views import HelloView

urlpatterns = [
    url(r'form/7/', HelloView.as_view(), name="formseventh"),
    path('', views.index, name='index'),
    path('next', views.next, name='next'),
    path('form', views.form, name='form'),
    path('form/1/', views.formfirst, name='formfirst'),
    path('form/2/', views.formsecond, name='formsecond'),
    path('form/3/', views.formthird, name='formthird'),
    path('form/4/', views.formfourth, name='formfourth'),
    path('form/5/', views.formfifth, name='formfifth'),
    path('form/6/', views.formsixth, name='formsixth'),
    path('query', views.query, name='query'),
    path('queries/<int:id>/<nickname>/', views.queries, name='queries'),
    path('users', views.users, name='users'),
    path('users/userid', views.userid, name='userid'),
    path('manager', views.manager, name='manager'),
    path('manager/values', views.managervalues, name='managervalues'),
    path('manager/values/lim', views.managervalueslim, name='managervalueslim'),
    path('manager/values/list', views.managervalueslist, name='managervalueslist'),
    path('manager/values/others', views.managervaluesothers, name='managervaluesothers'),
    path('manager/queryset', views.managerqueryset, name='managerqueryset'),
    path('crud', views.crudindex, name='crudindex'),
    path('crud/create', views.create, name='create'),
    path('crud/create/meta', views.createmeta, name='createmeta'),
    path('crud/edit/<int:num>', views.edit, name='edit'),
    path('crud/delete/<int:num>', views.delete, name='delete'),
]
