from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import auth, user_admin, profile

urlpatterns = [
    # Auth
    path('login/', auth.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='core:login'), name='logout'),
    
    # Profile
    path('perfil/', profile.ProfileUpdateView.as_view(), name='profile'),
    path('perfil/senha/', profile.CustomPasswordChangeView.as_view(), name='password_change'),
    
    # User Management
    path('usuarios/', user_admin.UserListView.as_view(), name='user-list'),
    path('usuarios/novo/', user_admin.UserCreateView.as_view(), name='user-create'),
    path('usuarios/<int:pk>/editar/', user_admin.UserUpdateView.as_view(), name='user-update'),
    path('usuarios/<int:pk>/excluir/', user_admin.UserDeleteView.as_view(), name='user-delete'),
    
    # Group Management
    path('grupos/', user_admin.GroupListView.as_view(), name='group-list'),
    path('grupos/novo/', user_admin.GroupCreateView.as_view(), name='group-create'),
    path('grupos/<int:pk>/editar/', user_admin.GroupUpdateView.as_view(), name='group-update'),
    path('grupos/<int:pk>/excluir/', user_admin.GroupDeleteView.as_view(), name='group-delete'),
]
