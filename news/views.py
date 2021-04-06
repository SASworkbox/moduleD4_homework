from django.views.generic import (ListView, DetailView, UpdateView,
                                  CreateView, DeleteView)

from .models import Post
from .filters import NewsFilter
from .forms import NewsForm
from django.views import View
from django.core.paginator import Paginator


class NewsList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    ordering = ['-posted']
    paginate_by = 2


class NewsView(View):

    def get(self, request):
        news = Post.objects.order_by('-posted')
        # создаём объект класса пагинатор, передаём ему список наших товаров и их количество для одной страницы
        p = Paginator(news, 1)

        # берём номер страницы из get-запроса. Если ничего не передали, будем показывать первую страницу.
        news = p.get_page(request.GET.get('page', 1))
        # теперь вместо всех объектах в списке товаров хранится только нужная нам страница с товарами

        data = {
            'news': news,
        }
        return render(request, 'post_detail.html', data)


class PostDetailView(DetailView):
    template_name = 'post_detail.html'
    queryset = Post.objects.all()


class PostCreateView(CreateView):
    template_name = 'post_create.html'
    form_class = NewsForm
    success_url = '/news'


class PostEditView(UpdateView):
    template_name = 'post_create.html'
    form_class = NewsForm
    success_url = '/news'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(DeleteView):
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news'


class Search(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(
            self.request.GET,
            queryset=self.get_queryset()
        )
        return context
