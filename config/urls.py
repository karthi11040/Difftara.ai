from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.shortcuts import redirect

from accounts.views import login_view, logout_view, firebase_login_view
from projects.views import (
    dashboard_view, project_list_view, upload_project_view, 
    project_detail_view, start_review_view, project_findings_view, 
    project_report_view, activities_view
)
from projects.api_views import (
    api_login, api_projects, api_project_detail, api_start_review,
    api_get_findings, api_save_mentor_review, api_get_report, api_activities
)
from reviews.code_review import code_review_view

urlpatterns = [
    path('admin/', admin.site.urls),

    # Web Auth
    path('', lambda req: redirect('dashboard')),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('auth/firebase/', firebase_login_view, name='firebase_login'),

    # Web Dashboard & Projects
    path('dashboard/', dashboard_view, name='dashboard'),
    path('projects/', project_list_view, name='project_list'),
    path('projects/upload/', upload_project_view, name='upload_project'),
    path('projects/<int:pk>/', project_detail_view, name='project_detail'),
    path('projects/<int:pk>/start-review/', start_review_view, name='start_review'),
    path('projects/<int:pk>/findings/', project_findings_view, name='project_findings'),
    path('projects/<int:pk>/report/', project_report_view, name='project_report'),
    path('projects/<int:pk>/reviews/<int:review_id>/report/', project_report_view, name='review_report'),
    path('activities/', activities_view, name='activities'),
    path('code-review/', code_review_view, name='code_review'),

    # REST APIs (SRS Section 25 & Appendix A)
    path('api/login/', api_login, name='api_login'),
    path('api/projects/', api_projects, name='api_projects'),
    path('api/projects/<int:pk>/', api_project_detail, name='api_project_detail'),
    path('api/projects/<int:pk>/review/', api_start_review, name='api_start_review'),
    path('api/projects/<int:pk>/findings/', api_get_findings, name='api_get_findings'),
    path('api/findings/<int:finding_pk>/review/', api_save_mentor_review, name='api_save_mentor_review'),
    path('api/projects/<int:pk>/report/', api_get_report, name='api_get_report'),
    path('api/activities/', api_activities, name='api_activities'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
