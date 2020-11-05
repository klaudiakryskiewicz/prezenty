"""prezenty URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from wishes import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='main'),
    path('add-wish/', views.AddWishView.as_view(), name='add-wish'),
    path('my-wish-list/', views.MyWishListView.as_view(), name='my-wish-list'),
    path('wish-list/', views.WishView.as_view(), name='wish-list'),
    path('present-list/', views.PresentListView.as_view(), name='present-list'),
    path('add-main-member/<int:id>', views.AddMainMemberView.as_view(), name='add-main-member'),
    path('add-member/', views.AddMemberView.as_view(), name='add-member'),
    path('add-family/', views.AddFamilyView.as_view(), name='add-family'),
    path("accounts/", include('django.contrib.auth.urls')),
    path('accounts/signup/', views.SignUpView.as_view(), name='signup'),
    path('accounts/signup/family/<int:id>/', views.SignUpFamilyView.as_view(), name='signup'),
    path('book-wish/', views.BookWish.as_view(), name='book-wish'),
    path('delete-wish/', views.DeleteWish.as_view(), name='delete-wish'),
    path('edit-wish/<int:id>', views.EditWish.as_view(), name='edit-wish'),
    path('delete-present/', views.DeletePresent.as_view(), name='delete-present'),
    path('buy-present/', views.BuyPresent.as_view(), name='buy-present'),
]

