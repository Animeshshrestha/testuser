from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_list_or_404, get_object_or_404


from .models import UserInfo, UserProfile
from .serializers import UserSerializer, UserProfileSerializer

class UserViewSet(viewsets.ModelViewSet):

	queryset = UserInfo.objects.all()
	serializer_class = UserSerializer

class UserProfileViewSet(viewsets.ModelViewSet):

	queryset = UserProfile.objects.all()
	serializer_class = UserProfileSerializer
	permission_classes = (IsAuthenticated,)

	def retrieve(self, request, pk=None):

		queryset = UserProfile.objects.all()
		user = get_object_or_404(queryset, pk=pk)
		serializer = UserProfileSerializer(user)
		return Response(serializer.data)


	def create(self,request):
		print("User", request.user)
		serializer = UserProfileSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save(user=request.user)
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def update(self, request, *args, **kwargs):

		instance = self.get_object()
		serializer = UserProfileSerializer(instance, data=request.data, partial=True)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response(serializer.data, status=status.HTTP_200_OK)


