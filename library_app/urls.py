from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import AuthorView,GenreView,BookView,BorrowRequestView,UserRegisterView




router=DefaultRouter()
router.register(r'authors',AuthorView,basename='author')
router.register(r'genres',GenreView,basename='genre')
router.register(r'books',BookView,basename='book')
router.register(r'borrow',BorrowRequestView,basename='borrow')


urlpatterns=[
    path('register/',UserRegisterView.as_view(),name='register'),
    path('',include(router.urls)),
    

]