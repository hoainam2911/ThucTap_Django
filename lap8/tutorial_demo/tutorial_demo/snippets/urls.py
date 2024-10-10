from django.urls import path, include
from rest_framework.routers import DefaultRouter
from snippets import views

# Tạo router và đăng ký các ViewSets
router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet, basename='snippet')
router.register(r'users', views.UserViewSet, basename='user')

# Các URL của API sẽ tự động được xác định bởi router
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
