from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from font import views as font_views
from document import views as document_views

router = routers.DefaultRouter()
router.register(r'users', font_views.UserViewSet)
router.register(r'groups', font_views.GroupViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/generate_font', font_views.generate_font, name='generate_font'),
    path('api/generate_document', document_views.generate_document, name='generate_document'),
]
