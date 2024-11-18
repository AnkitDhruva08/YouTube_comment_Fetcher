from django.urls import path
from youtube import views
from rest_framework_simplejwt.views import TokenObtainPairView


urlpatterns = [

    # user
    path('register/', views.UserRegisterView.as_view(), name="register-page"),
    path('login/', views.MyTokenObtainPairView.as_view(), name="login-page"),
    path('user/<int:pk>/', views.UserAccountDetailsView.as_view(), name="user-details"),
    path('comments/', views.fetch_data_videos, name="comments"),
    path('user_update/<int:pk>/', views.UserAccountUpdateView.as_view(), name="user-update"),
    path('user_delete/<int:pk>/', views.UserAccountDeleteView.as_view(), name="user-delete"),
    
    path('fetch-data/', views.FetchDataView.as_view(), name='fetch-data'),
    # path('export-excel/', views.ExportExcelView.as_view(), name='export-excel'),
    path('export-comments/', views.export_to_excel, name='export_comments'),

    # user address
    path('all-address-details/', views.UserAddressesListView.as_view(), name="all-address-details"),
    path('address-details/<int:pk>/', views.UserAddressDetailsView.as_view(), name="address-details"),
    path('create-address/', views.CreateUserAddressView.as_view(), name="create-address"),
    path('update-address/<int:pk>/', views.UpdateUserAddressView.as_view(), name="update-address-details"),
    path('delete-address/<int:pk>/', views.DeleteUserAddressView.as_view(), name="delete-address"),
    
    

    ]