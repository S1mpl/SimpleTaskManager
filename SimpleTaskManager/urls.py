
from django.conf.urls import url, include
from django.contrib import admin
admin.autodiscover()
from django.contrib.auth import views
from django.conf import settings
from django.conf.urls.static import static
from User.views import RegisterUser

urlpatterns = [
    url(r'^', include('Project.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^login/', views.login, name="login"),
    url(r'^logout/', views.logout, name="logout"),
    url(r'^register/', RegisterUser.as_view(), name="register"),
    url(r'^users/', include('User.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
