from django.shortcuts import redirect
from django.urls import reverse

class AdminAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        #aqui nos verifica si el usuario esta utenticado y si esta tratando de acceder al administrativo de django 
        if request.path.startswith('/admin/') and hasattr(request, 'user') and not request.user.is_superuser:
            return redirect(reverse('home'))
        response = self.get_response(request)
        return response
