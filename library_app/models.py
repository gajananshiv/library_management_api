from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    STUDENT='STUDENT'
    LIBRARIAN='LIBRARIAN'
    ROLE_CHOICES=[(STUDENT,'Student'),(LIBRARIAN,'Librarian')]
    Role=models.CharField(max_length=255,choices=ROLE_CHOICES,default=STUDENT)

    def is_librarian(self):
        return self.Role==self.LIBRARIAN


class Author(models.Model):
    name=models.CharField(max_length=20)
    bio=models.TextField(null=True,blank=True)


    def __str__(self):
        return self.name
class Genre(models.Model):
    name=models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Book(models.Model):
    title=models.CharField(max_length=255)
    author=models.ForeignKey(Author,on_delete=models.CASCADE,related_name='books')
    genres=models.ManyToManyField(Genre,related_name="books")
    ISBN=models.CharField(max_length=255,unique=True)
    available_copies=models.PositiveBigIntegerField(default=1)
    total_copies=models.PositiveBigIntegerField(default=1)

    def __str__(self):
        return self.title
    
class BorrowRequest(models.Model):
    STATUS_CHOICES=[('Pending','Pending'),('Approved','Approved'),('Rejected','Rejected'),('Returned','Returned')]
    book=models.ForeignKey(Book,on_delete=models.CASCADE,related_name='borrow_record')
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='borrow_record')
    status=models.CharField(max_length=255,choices=STATUS_CHOICES,default='Pending')
    requested_at=models.DateTimeField(auto_now_add=True)
    approved_at=models.DateTimeField(null=True,blank=True)
    returned_at=models.DateTimeField(null=True,blank=True)

    def __str(self):
        return f"{self.book} {self.user} {self.status}"

class BookReview(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    book=models.ForeignKey(Book,on_delete=models.CASCADE,related_name="reviews")
    rating=models.PositiveSmallIntegerField()
    comment=models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)


    


    
