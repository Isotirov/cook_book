from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cook_book.cook_book_main_app.urls')),
    path('auth/', include('cook_book.cook_book_auth.urls')),
    path('profile/', include('cook_book.cook_book_profiles.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
