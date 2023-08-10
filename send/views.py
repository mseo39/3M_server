from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from user.models import Member, CarList
from user.serializers import CarListSerializers
from datetime import timedelta
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
        if CarList.objects.filter(CarNum=request.POST["CarNum"], Date__lte=timezone.now()-timedelta(minutes=5)).exists():
            recent_5min=CarList.objects.get(CarNum=request.POST["CarNum"], Date__lte=timezone.now()-timedelta(minutes=5))
            if recent_5min:
                return JsonResponse({'message':"5분 이내 같은 차량 데이터가 존재합니다."})
            else:
                pass 
        else:
            pass
        return JsonResponse({'message':"successfully"}, status=status.HTTP_200_OK)
    return JsonResponse({'message': 'error'}, status=status.HTTP_400_BAD_REQUEST)