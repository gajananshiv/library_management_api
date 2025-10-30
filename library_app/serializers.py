from rest_framework import serializers
from .models import User,Author,Genre,Book,BorrowRequest,BookReview

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Author
        fields=['id','name','bio']

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model=Genre
        fields=['id','name']

class BookSerializers(serializers.ModelSerializer):
    author=AuthorSerializer(read_only=True)
    genres=GenreSerializer(many=True,read_only=True)
    author_id=serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(),source='author',write_only=True)
    genre_ids=serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all(),many=True,source='genres',write_only=True)

    class Meta:
        model=Book
        fields=['id','title','author','author_id','genres','genre_ids','ISBN','available_copies','total_copies']

class BookCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Book
        fields=['id','title','author','genres','ISBN','available_copies','total_copies']
class BorrowRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model=BorrowRequest
        fields=['id','book','user','status','requested_at','approved_at','returned_at']

        read_only_fields=['status','requested_at','approved_at','returned_at']

        def create(self,validated_data):
            return super().create(validated_data)

class BookReviewSerializer(serializers.ModelSerializer):
    user=serializers.StringRelatedField(read_only=True)
    class Meta:
        model=BookReview
        fields=['id','user','rating','comment','created_at']

class UserRegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields=['id','username','email','password','Role']

    def create(self,validated_data):
        password=validated_data.pop('password')
        user=User(**validated_data)
        user.set_password(password)
        user.save()
        return user

        
















