"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from psycho_forms import views
from django.views.generic.base import RedirectView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = routers.DefaultRouter()
router.register(r'organisations', views.OrganizationViewSet)
router.register(r'test-data', views.TestDataViewSet)
router.register(r'questions', views.QuestionViewSet)
router.register(r'answers', views.AnswerSelectableViewSet)
router.register(r'questionaries', views.QuestionaryDataViewSet)
router.register(r'test-results', views.TestResultViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'usernames', views.UserNamesViewSet)


urlpatterns = [
    path('', RedirectView.as_view(url='/api')),
    path('api/users/me/', views.get_me),
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/test-running/save/', views.save_test_running_data, name='save_test_running_data'),
]
