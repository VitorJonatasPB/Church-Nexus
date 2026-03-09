from django.contrib.auth.models import User, Group
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import django.forms as forms

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'is_superuser', 'groups']

class UserListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = User
    template_name = 'core/users/user_list.html'
    context_object_name = 'usuarios'

class UserCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = 'core/users/user_form.html'
    success_url = reverse_lazy('core:user-list')

    def form_valid(self, form):
        user = form.save(commit=False)
        # Define a senha padrão como 123456
        user.set_password('123456')
        user.save()
        form.save_m2m()
        return super().form_valid(form)

class UserUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'core/users/user_form.html'
    success_url = reverse_lazy('core:user-list')

class UserDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = User
    template_name = 'core/users/user_confirm_delete.html'
    success_url = reverse_lazy('core:user-list')

class GroupListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Group
    template_name = 'core/users/group_list.html'
    context_object_name = 'grupos'

class GroupCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Group
    fields = ['name', 'permissions']
    template_name = 'core/users/group_form.html'
    success_url = reverse_lazy('core:group-list')

class GroupUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Group
    fields = ['name', 'permissions']
    template_name = 'core/users/group_form.html'
    success_url = reverse_lazy('core:group-list')

class GroupDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Group
    template_name = 'core/users/group_confirm_delete.html'
    success_url = reverse_lazy('core:group-list')
