from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import AuthorView,GenreView,BookView,BorrowRequestView,UserRegisterView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view=get_schema_view(
    openapi.Info(
        title="Library Mangement System API",
        default_version='v1',
        description="Api documentation for library_maanagement_system",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)



router=DefaultRouter()
router.register(r'authors',AuthorView,basename='author')
router.register(r'genres',GenreView,basename='genre')
router.register(r'books',BookView,basename='book')
router.register(r'borrow',BorrowRequestView,basename='borrow')


urlpatterns=[
    path('register/',UserRegisterView.as_view(),name='register'),
    path('',include(router.urls)),
    path('docs/',schema_view.with_ui('swagger',cache_timeout=0),name='swagger-docs')

]