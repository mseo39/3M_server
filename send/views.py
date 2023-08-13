from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from user.models import Member, CarList
from user.serializers import CarListSerializers, ReportListSerializers
from datetime import timedelta, datetime
import pytz
# Create your views here.

# 데이터 업로드 API
@api_view(['POST'])
def Data(request):
    if request.method == 'POST':
        if CarList.objects.filter(CarNum=request.data["CarNum"], ReportStatus='F').exists():
            recent_5min=CarList.objects.get(CarNum=request.data["CarNum"])
            if recent_5min and datetime.strptime(request.data["Date"], '%Y-%m-%d %H:%M:%S').replace(tzinfo=pytz.UTC)-recent_5min.Date >= timedelta(minutes=5):
                
                # 여기에 위도, 경도 비교 기능 작성
                
                recent_5min.ReportStatus = 'T' 
                recent_5min.save()
                data = {
                    'BeforeDate': recent_5min.Date,
                    'AfterDate': request.data["Date"],
                    'CarNum': request.data["CarNum"],
                    'BeforeUniqueNumber': recent_5min.UniqueNumber,
                    'AfterUniqueNumber': request.data["UniqueNumber"]  
                }
                serializer = ReportListSerializers(data=data)
                if serializer.is_valid():
                    serializer.save() # ReportList에 저장
                else:
                    print(serializer.errors)
                    return JsonResponse({'message': 'ReportListSerializer error', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            else:
                pass
        else:
            pass
        dataset = {}
        for i in request.data:
            dataset[i] = request.data[i]
        if recent_5min.ReportStatus == 'T':
            dataset['ReportStatus'] = 'T'
        serializer = CarListSerializers(data=dataset)
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)
            return JsonResponse({'message': 'CarListSerializer error', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'message':"데이터 전달이 완료되었습니다."}, status=status.HTTP_200_OK)
    return JsonResponse({'message': 'error: request method is not POST'}, status=status.HTTP_400_BAD_REQUEST)