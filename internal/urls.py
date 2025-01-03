from django.urls import path
from .views import EditTelecallerView

urlpatterns = [
    path('telecaller/<int:t_id>/edit/', EditTelecallerView.as_view(), name='edit-telecaller'),
]