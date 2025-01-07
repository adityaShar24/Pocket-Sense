from django.urls import path
from .views import (
    CategoryListCreateRetrieveUpdateDestroyView,
    ExpenseCreateView,
    GroupListCreateRetrieveUpdateDestroyView
)

urlpatterns = [
    path('categories/create/', CategoryListCreateRetrieveUpdateDestroyView.as_view() , name='create-categories'),
    path('categories/list/', CategoryListCreateRetrieveUpdateDestroyView.as_view() , name='list-categories'),
    path('categories/retrieve/<int:pk>/', CategoryListCreateRetrieveUpdateDestroyView.as_view() , name='retrieve-categories'),
    path('categories/update/<int:pk>/', CategoryListCreateRetrieveUpdateDestroyView.as_view() , name='update-categories'),
    path('categories/delete/<int:pk>/', CategoryListCreateRetrieveUpdateDestroyView.as_view() , name='delete-categories'),
    
    #Expense Add , Split
    path('create/', ExpenseCreateView.as_view(), name='create-expense'),
    
    #Groups
    path('group/create/', GroupListCreateRetrieveUpdateDestroyView.as_view(), name='create-group'),
    path('group/retrieve/<int:pk>/', GroupListCreateRetrieveUpdateDestroyView.as_view(), name='retrieve-group'),
    path('group/list/', GroupListCreateRetrieveUpdateDestroyView.as_view(), name='list-group'),
    path('group/update/<int:pk>/', GroupListCreateRetrieveUpdateDestroyView.as_view(), name='update-group'),
    path('group/delete/<int:pk>/', GroupListCreateRetrieveUpdateDestroyView.as_view(), name='delete-group'),
]
