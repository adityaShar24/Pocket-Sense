from django.urls import path
from .views import (
    CategoryListCreateRetrieveUpdateDestroyView,
    ExpenseCreateView,
)

urlpatterns = [
    path('categories/create/', CategoryListCreateRetrieveUpdateDestroyView.as_view() , name='create-categories'),
    path('categories/list/', CategoryListCreateRetrieveUpdateDestroyView.as_view() , name='list-categories'),
    path('categories/retrieve/<int:pk>/', CategoryListCreateRetrieveUpdateDestroyView.as_view() , name='retrieve-categories'),
    path('categories/update/<int:pk>/', CategoryListCreateRetrieveUpdateDestroyView.as_view() , name='update-categories'),
    path('categories/delete/<int:pk>/', CategoryListCreateRetrieveUpdateDestroyView.as_view() , name='delete-categories'),
    
    path('create/', ExpenseCreateView.as_view(), name='create-expense'),
    
]
