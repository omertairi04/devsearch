from django.contrib import admin
from django.urls import path,  include

from django.conf import settings
from django.conf.urls.static import static

# RESET PASSWORDS
from django.contrib.auth import views as auth_views
# nven se views.ViewName e bojm auth_views


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

    # api
    path('api/',include('api.urls')),

    # RESET PASSWORDS
    # per me ndrru templatin default , mrena as_view(template_name="template_name.html")
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name="reset_password.html") ,
        name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="reset_password_sent.html"),
        name="password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="reset.html"),
        name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = "reset_password_complete.html"),
        name="password_reset_complete"),
    #<uidb64> - Encrypts user emails into a base 64 encryption

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# PASSWORD RESET EMAIL
"""
# 1 - User submits email for reset              //PasswordResetView.as_view         // name="reset_password"
# 2 - Email sent message                        //PasswordResetDoneView.as_view     // name="password_reset_done"
# 3 - Email with link and reset instructions    //PasswordResetConfigView           // name="password_reset_confirm"
# 4 - Password successfully reset message       //PasswordResetCompleteView         // name="password_reset_complete"
"""