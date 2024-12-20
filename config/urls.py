"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from django.conf.urls.i18n import i18n_patterns

import debug_toolbar

urlpatterns = [
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    path("selfadminapp/", include("selfadminapp.urls", namespace="selfadminapp_namespace")),
    path("", RedirectView.as_view(url="mainapp/")),
    path("social_auth/", include("social_django.urls", namespace="social")),
    path("mainapp/", include("mainapp.urls", namespace="mainapp_namespace")),
    path("authapp/", include("authapp.urls", namespace="authapp_namespace")),


]

if settings.DEBUG:
    urlpatterns.append(path("__debug__/", include(debug_toolbar.urls)))
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # urlpatterns += i18n_patterns(
    #     path("", RedirectView.as_view(url='mainapp/'), name='mainapp')
    # )