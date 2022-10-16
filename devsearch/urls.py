from django.contrib import admin
from django.urls import path,  include

from django.conf import settings
from django.conf.urls.static import static
"""
def projects(request):
    return HttpResponse("Here are projects")

def project(request, pk):
    return HttpResponse("Single projects" + ' ' + str(pk))
"""
"""
path('project/<str:___>/', project,name="project"),
duhet me u konen edhe parametri te view njejt
def project(request, ___):
"""

urlpatterns = [
    path('admin/', admin.site.urls),
    path('projects/', include('projects.urls')),
    path('', include('users.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

