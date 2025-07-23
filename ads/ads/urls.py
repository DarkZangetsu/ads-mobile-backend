
from django.contrib import admin
from django.urls import path
from django.conf import settings
from graphene_file_upload.django import FileUploadGraphQLView
from django.views.decorators.csrf import csrf_exempt
from graphql_jwt.decorators import jwt_cookie
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql/', csrf_exempt(FileUploadGraphQLView.as_view(graphiql=True))),
    path('graphql/jwt/', csrf_exempt(jwt_cookie(FileUploadGraphQLView.as_view(graphiql=True)))),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)