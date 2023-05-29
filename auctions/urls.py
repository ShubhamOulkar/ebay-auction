from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
    path("createlisting/", views.create_listing, name="create_listing"),
    path("categorylisting/", views.category_listing, name="category_listing"),
    path("details/<int:pk>/", views.details, name="details"),
    path("details/<int:pk>/edit/", views.EditListing.as_view(), name="edit_listing"),
    path("details/<int:pk>/delete", views.DeleteListing.as_view(), name="delete_listing"),
    path("details/<int:pk>/add",views.add_watchlist, name="add_watchlist"),
    path("details/<int:pk>/remove",views.remove_watchlist, name="remove_watchlist"),
    path("details/<int:pk>/inactive/", views.inactive, name="inactive"),
    path("details/<int:pk>/active/", views.active, name="active"),
    path("details/<int:pk>/do_bid/", views.do_bid, name="do_bid"),
    path("details/<int:pk>/add_comment/", views.add_comment, name="add_comment"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("my_listing/", views.my_listing, name="my_listing"),
    path("create_listing/add_category/", views.add_category, name="add_category"),
]
