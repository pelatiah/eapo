from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('services_app.urls')),
    path('', include('order_app.urls')),

]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

handler404 = 'services_app.views.error_404'
handler500 = 'services_app.views.error_500'
