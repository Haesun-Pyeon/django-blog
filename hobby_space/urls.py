# hobby_space/urls.py
from ckeditor_uploader import views as ckviews
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import include, path, re_path
from django.views.decorators.cache import never_cache
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('accounts/', include('accounts.urls')),
    path('blog/', include('blog.urls')),
    path('ckeditor/upload/', login_required(ckviews.upload), name='ckeditor_upload'),
    path('ckeditor/browse/', never_cache(ckviews.browse), name='ckeditor_browse'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
else:
    urlpatterns.append(re_path(r'^media/(?P<path>.*)$', serve,
                       {'document_root': settings.MEDIA_ROOT}))
    urlpatterns.append(re_path(r'^static/(?P<path>.*)$', serve,
                       {'document_root': settings.STATIC_ROOT}))
