from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('HospitalSetting.urls')),
    path('patient/', include('APEN.urls')),
    path('prescription/', include('LRPD.urls')),
    path('finance/', include('Finance.urls')),
    path('hrm/', include('Hr.urls')),
    path('report', include('Report.urls')),
    path('inventory/', include('Inventory.urls')),
    path('users/', include('Users.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
