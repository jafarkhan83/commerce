from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<int:listing_id>", views.listing_view, name="listing"),
    path("create<int:user_id>", views.create_listing, name="createListing"),
    path("watchlist/<int:listing_id>", views.watchlist_view, name='watchlist'),
    path('closed', views.closed_listing_view, name='closedListing'),
    path('category', views.categories, name='categories'),
    path('category/<str:category>', views.category_view, name='category')
]
