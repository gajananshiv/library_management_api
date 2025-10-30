from django.shortcuts import render,get_object_or_404
from rest_framework import viewsets,generics,permissions,status,filters
from rest_framework.decorators import action,api_view,permission_classes
from rest_framework.response import Response
from .permissions import IsLibrarian,IsOwnerOrReadOnly
from .models import User,Author,Genre,Book,BorrowRequest,Book
from .serializers import UserRegisterSerializer,AuthorSerializer,GenreSerializer,BookSerializers,BorrowRequestSerializer,BookReviewSerializer,BookCreateUpdateSerializer
#from .permissions import IsLibrarian
from django.utils import timezone




# Create your views here.
class UserRegisterView(generics.CreateAPIView):
    serializer_class=UserRegisterSerializer
    permission_classes=[permissions.AllowAny]

class AuthorView(viewsets.ModelViewSet):
    queryset=Author.objects.all()
    serializer_class=AuthorSerializer

    def get_permissions(self):
        if self.action in ['create','update','partial_update','destroy']:
            return [IsLibrarian()]
        return[permissions.AllowAny()]
class GenreView(viewsets.ModelViewSet):
    queryset=Genre.objects.all()
    serializer_class=GenreSerializer

    def get_permissions(self):
        if self.action in ['create','update','partial_update','destroy']:
            return [IsLibrarian()]
        return [permissions.AllowAny()]
    
class BookView(viewsets.ModelViewSet):
    queryset=Book.objects.all()
    serializer_class=BookSerializers

    def get_permissions(self):
        if self.action in ['create','update','partial_update','destroy']:
            return [IsLibrarian()]
        return [permissions.AllowAny()]
    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return BookCreateUpdateSerializer
        return BookSerializers
    @action(detail=True,methods=['post'],permission_classes=[permissions.IsAuthenticated])
    def reviews(self,request,pk=None):
        book=self.get_object()
        serializer=BookReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user,book=book)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    @action(detail=True,methods=['get'],permission_classes=[permissions.AllowAny])
    def list_reviews(self,request,pk=None):
        book=self.get_object()
        qs=book.reviews.all()
        serializer=BookReviewSerializer(qs,many=True)
        return Response(serializer.data)
    


    
from rest_framework.exceptions import ValidationError   
class BorrowRequestView(viewsets.ModelViewSet):
    serializer_class=BorrowRequestSerializer
    permission_classes=[permissions.IsAuthenticated]


    def get_queryset(self):
        user=self.request.user
        if user.is_librarian():
            return BorrowRequest.objects.all()
        return BorrowRequest.objects.filter(user=user)
    '''def get_queryset(self):
        user=self.request.user
        if not user.is_authenticated:
            return BorrowRequest.objects.none()
        if user.is_librarian():
            return BorrowRequest.objects.all()
        return BorrowRequest.objects.filter(user=user)'''
    def create(self,request,*args,**kwargs):
        user=request.user
        if user.Role!=User.STUDENT:
            return Response({"detail":"only student can borrow books"},status=403)
        book_id=request.data.get("book")
        book=get_object_or_404(Book,id=book_id)
        if book.available_copies<=0:
            return Response({"detail":"No available copies"},status=400)
        
        borrow=BorrowRequest.objects.create(user=user,book=book)
        serializer=self.get_serializer(borrow)
        return Response(serializer.data,status=201)

    '''def perform_create(self, serializer):
        book=serializer.validated_data['book']
        if book.available_copies<1:
            raise ValidationError("No copies available for this book")
        book.available_copies -=1
        book.save()

        serializer.save(user=self.request.user)'''
    @action(detail=True,methods=['patch'],permission_classes=[IsLibrarian])
    def approve(self,request,pk=None):
        borrow=self.get_object()
        borrow.status="Approved"
        borrow.approved_at=timezone.now()
        borrow.book.available_copies-=1
        borrow.book.save()
        borrow.save()
        return Response({"detail":"Request Approved"})
    @action(detail=True,methods=['patch'],permission_classes=[IsLibrarian])
    def reject(self,request,pk=None):
        borrow=self.get_object()
        borrow.status="Rejected"
        borrow.approved_at=timezone.now()
        
        borrow.save()
        return Response({"detail":"Request Rejected"})
    @action(detail=True,methods=['patch'],permission_classes=[permissions.IsAuthenticated])
    def return_book(self,request,pk=None):
        borrow=self.get_object()
        borrow.status="Returned"
        borrow.returned_at=timezone.now()
        borrow.book.available_copies+=1
        borrow.book.save()
        borrow.save()
        return Response({"detail":"Book Returned"})
    
    

    

    


'''@api_view(['POST'])
#@permission_classes([IsAuthenticated,IsLibrarian])
def approve_borrow_request(request,pk):
    borrow=get_object_or_404(BorrowRequest,pk=pk)

    if borrow.status !='Pending':
        return Response({'message':'Borrow request Approved'})

@api_view(['POST'])

def return_borrow_request(request,pk):
    borrow=get_object_or_404(BorrowRequest,pk=pk)
    if borrow.status !='Approved':
        return Response({'message':'only approved requests can be returned'},status=400)
    borrow.status='Returned'
    borrow.book.available_copies+=1
    borrow.book.save()
    borrow.save()
    return Response({'message':'Book returns successfully'})
'''
    


        
    

