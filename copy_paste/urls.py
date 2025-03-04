from django.urls import path
from django.http import HttpResponse
from django.views import View
from django.contrib.auth import views as auth_views
from django.views.decorators.csrf import csrf_exempt
from pastes import views as paste_views

class HealthCheckView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("OK", status=200)

# Exempt health check from CSRF
HealthCheckView = csrf_exempt(HealthCheckView.as_view())

urlpatterns = [
    path('health/', HealthCheckView, name='health-check'),

    path('', paste_views.paste_list, name='paste_list'),
    path('create/', paste_views.create_paste, name='create_paste'),
    path('extend/<int:paste_id>/', paste_views.extend_paste, name='extend_paste'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', paste_views.signup, name='signup'),
]
