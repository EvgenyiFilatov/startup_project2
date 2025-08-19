from django.urls import path

from startup.views import (
    wellcome_view,
    startup_list,
    startup_detail,
    startup_edit,
    startup_delete
)

app_name = 'startup'

urlpatterns = [
    path('', wellcome_view, name='wellcome'),
    path('startups/', startup_list, name='startup_list'),
    path('startup/<int:pk>/', startup_detail, name='startup_detail'),
    path('startup/<int:pk>/edit', startup_edit, name='startup_edit'),
    path('startup/<int:pk>/delete', startup_delete, name='startup_delete'),


]
