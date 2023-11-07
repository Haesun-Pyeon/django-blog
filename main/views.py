# main/views.py
from blog.models import Category, Post
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['popular'] = Post.objects.all().order_by('-view_count')[0]
        context['popular_list1'] = Post.objects.all().order_by(
            '-view_count')[1:3]
        context['popular_list2'] = Post.objects.all().order_by(
            '-view_count')[3:5]
        return context


index = IndexView.as_view()
about = TemplateView.as_view(
    template_name='main/about.html',
    extra_context={'category_list': Category.objects.all()}
)
contact = TemplateView.as_view(
    template_name='main/contact.html',
    extra_context={'category_list': Category.objects.all()}
)
