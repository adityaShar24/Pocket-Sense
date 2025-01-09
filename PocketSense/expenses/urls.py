from django.urls import path
from .views import (
    ExpenseCreateView,
    MonthlyAnalysisView,
    GetExpenseCategorizationView,
    GroupListCreateRetrieveUpdateDestroyView,
    BudgetListCreateRetrieveUpdateDestroyView,
    CategoryListCreateRetrieveUpdateDestroyView,
    SettlementListCreateRetrieveUpdateDestroyView,
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
    
    #settlements
    path('settlements/create/' , SettlementListCreateRetrieveUpdateDestroyView.as_view(), name='create-settlement'),
    path('settlements/list/' , SettlementListCreateRetrieveUpdateDestroyView.as_view(), name='list-settlement'),
    path('settlements/retrieve/<int:pk>/' , SettlementListCreateRetrieveUpdateDestroyView.as_view(), name='retrieve-settlement'),
    path('settlements/update/<int:pk>/' , SettlementListCreateRetrieveUpdateDestroyView.as_view(), name='update-settlement'),
    path('settlements/delete/<int:pk>/' , SettlementListCreateRetrieveUpdateDestroyView.as_view(), name='delete-settlement'),
    
    #monthly analysis
    path('monthly-analysis/' , MonthlyAnalysisView.as_view(), name='monthly-analysis'),
    
    #Expense Categorization
    path('expense-categorization/', GetExpenseCategorizationView.as_view(), name='expense-categorization'),
    
    path('budget/create/', BudgetListCreateRetrieveUpdateDestroyView.as_view(), name='create-budget'),
    path('budget/retrieve/<int:pk>/', BudgetListCreateRetrieveUpdateDestroyView.as_view(), name='retrieve-budget'),
    path('budget/list/', BudgetListCreateRetrieveUpdateDestroyView.as_view(), name='list-budget'),
    path('budget/update/<int:pk>/', BudgetListCreateRetrieveUpdateDestroyView.as_view(), name='update-budget'),
    path('budget/delete/<int:pk>/', BudgetListCreateRetrieveUpdateDestroyView.as_view(), name='delete-budget'),
]
