from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    # path('api/v1/', WomenAPIList.as_view()),
    # path('api/v1/<int:pk>/', WomenAPIUpdate.as_view()),
    # path('api/v1/delete/<int:pk>/', WomenAPIDestroy.as_view()),
]
