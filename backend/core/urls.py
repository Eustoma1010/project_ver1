"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from apps.products.views import home, favorites_list, toggle_favorite, trace_batch_api, blockchain_explorer, get_tx_details_api
from apps.farm.views import admin_reports

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/reports/', admin_reports, name='admin-reports'),
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("products/explorer/", blockchain_explorer, name="blockchain-explorer"),
    path("products/api/tx/<str:tx_hash>/", get_tx_details_api, name="get-tx-details-api"),
    path("products/trace/<str:batch_id>/", trace_batch_api, name="trace-batch-api"),
    path("favorites/", favorites_list, name="favorites"),
    path("favorites/toggle/<int:product_id>/", toggle_favorite, name="toggle-favorite"),
    path("users/", include("apps.users.urls")),
    path("farm/", include("apps.farm.urls")),
    path("orders/", include("apps.orders.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
