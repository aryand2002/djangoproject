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

    def put(self, request, pk):
        decoration = self.get_object(pk)
        if decoration is None:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = DecorationSerializer(decoration, data=request.data, partial=True)  # ✅ Allow partial update
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
    def get(self, request):
        posts = BlogPost.objects.all().order_by('-created_at')
        serializer = BlogPostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request):
        try:
            serializer = BlogPostSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("❌ Error:", str(e))
            traceback.print_exc()
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CatalogItemAPIView(APIView):
    def get(self, request):
        items = CatalogItem.objects.all()
        serializer = CatalogItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CatalogItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GalleryView(APIView):
    def post(self, request):
        serializer = GalleryImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
    def get(self, request):
        items = Gallery.objects.all()
        serializer = GalleryImageSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
