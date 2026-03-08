from django.urls import path
from . import views


urlpatterns = [
    path('<int:company_id>/', views.company_detail),
    path('<int:company_id>/posts/', views.get_posts),
    path('<int:company_id>/posts/<int:post_id>/', views.get_post),
    path('<int:company_id>/posts/<int:post_id>/edit/', views.edit_post),
    path('<int:company_id>/posts/<int:post_id>/comment/', views.create_comment),
    path('<int:company_id>/posts/<int:post_id>/comment/<int:comment_id>/', views.delete_edit_comment),
    path('<int:company_id>/write/', views.create_post),
]
