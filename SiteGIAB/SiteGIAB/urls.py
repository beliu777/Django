from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from mainGIAB import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('profile/', views.profile, name='profile'),
    path('', views.register, name='register'),
    path('login/', views.loginf, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('download/title/', views.download_title, name='download_title'),
    path('download/assignment/', views.download_assignment, name='download_assignment'),
    path('download/diary/', views.download_diary, name='download_diary'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
