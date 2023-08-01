from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from user.models import Member, CarList
from user.serializers import CarListSerializers

# Create your views here.

# 데이터 업로드 API
@api_view(['POST'])
def Data(request):
    if request.method == 'POST':
        dataset = {}
        for i in request.data:
            dataset[i] = request.data[i]
        serializer = CarListSerializers(data=dataset)
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)
            return JsonResponse({'message': 'error'}, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'message':"successfully"}, status=status.HTTP_200_OK)
    return JsonResponse({'message': 'error'}, status=status.HTTP_400_BAD_REQUEST)
