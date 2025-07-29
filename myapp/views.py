from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import *
from rest_framework.parsers import MultiPartParser, FormParser
import traceback

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            tokens = get_tokens_for_user(user)
            return Response({'msg': 'User registered successfully', 'tokens': tokens}, status=201)
        return Response(serializer.errors, status=400)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            tokens = get_tokens_for_user(user)
            return Response({'msg': 'Login successful', 'tokens': tokens}, status=200)
        return Response(serializer.errors, status=400)
    

class DecorationListCreateAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        decorations = Decoration.objects.all()
        serializer = DecorationSerializer(decorations, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DecorationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DecorationDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Decoration.objects.get(pk=pk)
        except Decoration.DoesNotExist:
            return None

    def get(self, request, pk):
        decoration = self.get_object(pk)
        if decoration is None:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = DecorationSerializer(decoration)
        return Response(serializer.data)

    def patch(self, request, pk):
        try:
            decoration = Decoration.objects.get(pk=pk)
        except Decoration.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = DecorationSerializer(decoration, data=request.data, partial=True)  # ✅ partial=True for PATCH
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        decoration = self.get_object(pk)
        if decoration is None:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        decoration.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class BlogPostAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            try:
                post = BlogPost.objects.get(pk=pk)
                serializer = BlogPostSerializer(post)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except BlogPost.DoesNotExist:
                return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            posts = BlogPost.objects.all().order_by('-created_at')
            serializer = BlogPostSerializer(posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BlogPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
            try:
                post = BlogPost.objects.get(pk=pk)
            except BlogPost.DoesNotExist:
                return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

            serializer = BlogPostSerializer(post, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            post = BlogPost.objects.get(pk=pk)
            post.delete()
            return Response({'message': 'Deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except BlogPost.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)


class CatalogItemAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            try:
                item = CatalogItem.objects.get(pk=pk)
                serializer = CatalogItemSerializer(item)
                return Response(serializer.data)
            except CatalogItem.DoesNotExist:
                return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            items = CatalogItem.objects.all()
            serializer = CatalogItemSerializer(items, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = CatalogItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        try:
            item = CatalogItem.objects.get(pk=pk)
        except CatalogItem.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CatalogItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            item = CatalogItem.objects.get(pk=pk)
            item.delete()
            return Response({'message': 'Deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except CatalogItem.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)


class GalleryView(APIView):
    def get(self, request, pk=None):
        if pk:
            try:
                item = Gallery.objects.get(pk=pk)
                serializer = GalleryImageSerializer(item)
                return Response(serializer.data)
            except Gallery.DoesNotExist:
                return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            items = Gallery.objects.all()
            serializer = GalleryImageSerializer(items, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = GalleryImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        try:
            item = Gallery.objects.get(pk=pk)
        except Gallery.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = GalleryImageSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            item = Gallery.objects.get(pk=pk)
            item.delete()
            return Response({'message': 'Deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Gallery.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)


class CategeryItemView(APIView):
    def get(self, request):
        category_id = request.query_params.get('category')

        if category_id:
            items = CatalogItem.objects.filter(category_id=category_id)
        else:
            items = CatalogItem.objects.all()

        serializer = CatalogItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


