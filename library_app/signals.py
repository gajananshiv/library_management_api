from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import BorrowRequest

@receiver(post_save,sender=BorrowRequest)
def update_book_copies(sender,instance,created,**kwargs):
    book=instance.book

    if created:
        return
    if instance.status=="Approved":
        if book.available_copies>0:
            book.available_copies-=1
            book.save(update_fields=['available_copies'])
    elif instance.status=='Returned':
        book.available_copies+=1
        book.save(update_fields=['available_copies'])

