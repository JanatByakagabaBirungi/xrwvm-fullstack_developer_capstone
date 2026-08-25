#from django.conf.urls.static import static
#from django.conf import settings
from django.urls import path
from . import views

app_name = 'djangoapp'
urlpatterns = [
    urlpatterns = [
   path(route='login', view=views.login_user, name='login'),
   path(route='logout', view=views.logout_request, name='logout'),
   path(route='register', view=views.registration, name='register'),
    # path for dealer reviews view

    # path for add a review view

] 
