from django.urls import path
from .views import matrix_view

urlpatterns = [
    path('matrix/', matrix_view, name='matrix_input'),
]
