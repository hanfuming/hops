from django.urls import path
from apps.task import views

urlpatterns = [
    path('execute', views.ExecuteView.as_view(), name="execute"),
    path('file', views.FileView.as_view(), name="file"),
    path('deploy', views.DeployView.as_view(), name="deploy"),
    path('job', views.JobView.as_view(), name="job"),
    path('cron', views.CronView.as_view(), name="cron"),
    path('script', views.ScriptView.as_view(), name="script"),
]