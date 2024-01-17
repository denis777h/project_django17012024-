from datetime import datetime

from django.shortcuts import render
from django.template.loader import render_to_string

from .models import Post_news, Appointment
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, View
from django.views.generic.edit import CreateView
from django.core.paginator import Paginator

from django.shortcuts import redirect, render
from django.core.mail import send_mail, mail_managers, EmailMultiAlternatives
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


# Create your views here.

class AppointmentView(View):
  def get(self, request, *args, **kwargs):
    return render(request, 'make_appointment.html', {})

  def post(self, request, *args, **kwargs):
    appointment = Appointment(
      date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),
      client_name=request.POST['client_name'],
      message=request.POST['message'],
    )
    appointment.save()


    html_content = render_to_string(
      'appointment_created.html',
      {
        'appointment': appointment,
      }
    )


    msg = EmailMultiAlternatives(
      subject=f'{appointment.client_name} {appointment.date.strftime("%Y-%M-%d")}',
      body=appointment.message,  # это то же, что и message
      from_email='peterbadson@yandex.ru',
      to=['skavik46111@gmail.com'],  # это то же, что и recipients_list
    )
    msg.attach_alternative(html_content, "text/html")  # добавляем html
    msg.send()

    return redirect('appointments:make_appointment')



class NewsList(ListView):
  model = Post_news
  template_name = 'news.html'
  context_object_name = 'news'
  queryset = Post_news.objects.order_by('-dateCreation')
  paginate_by = 10

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['list_in_page'] = self.paginate_by
    return context


class NewsItem(DetailView):
  model = Post_news
  template_name = 'news_item.html'
  context_object_name = 'news_item'


class Search(ListView):
  model = Post_news
  template_name = 'search.html'
  context_object_name = 'post_search'
  ordering = ['-dateCreation']
  paginate_by = 10

  def get_queryset(self):
    queryset = super().get_queryset()
    self.filter = self.filter_class(self.request.GET, queryset=queryset)
    return self.filter.qs.all()

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['filter'] = self.filter
    context['list_in_page'] = self.paginate_by
    context['all_posts'] = Post_news.objects.all()
    return context