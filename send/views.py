from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from user.models import Member, CarList
from user.serializers import CarListSerializers, ReportListSerializers
from datetime import timedelta, datetime
import pytz
from haversine import haversine
# Create your views here.

# 데이터 업로드 API
@api_view(['POST'])
def Data(request):
    #UnboundLocalError: local variable 'recent_5min' referenced before assignment 에러발생
    recent_5min=None
    if request.method == 'POST':
        if CarList.objects.filter(CarNum=request.data["CarNum"], ReportStatus='F').exists():
            #다음 코드는 똑같은 값이 여러개 있을 때 에러가 남
            #recent_5min=CarList.objects.get(CarNum=request.data["CarNum"])
            recent_5min = CarList.objects.filter(CarNum=request.data["CarNum"], ReportStatus='F').order_by('-Date').first()
            if recent_5min and datetime.strptime(request.data["Date"], '%Y-%m-%d %H:%M:%S').replace(tzinfo=pytz.UTC)-recent_5min.Date >= timedelta(minutes=1):
                
                # 여기에 위도, 경도 비교 기능 작성

                # 전 데이터 위도와 경도
                # center_latitude = recent_5min.Latitude
                # center_longitude = recent_5min.Longitube
                current= (recent_5min.Latitude,recent_5min.Longitube)

                # 새로운 위도와 경도
                # new_latitude = request.data["Latitude"]
                # new_longitude = request.data["Longitube"]
                new = (request.data["Latitude"],request.data["Longitube"])

                # 거리 계산
                #print(haversine(current, new, unit = 'm'))
                if haversine(current, new, unit = 'm')<=1.75:
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
                        get_fcm_token_by_member_id(recent_5min.MemberID)
                        get_fcm_token_by_member_id(request.data["MemberID"])
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
        if recent_5min!=None and recent_5min.ReportStatus == 'T':
            dataset['ReportStatus'] = 'T'
        serializer = CarListSerializers(data=dataset)
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)
            return JsonResponse({'message': 'serializer error', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'message':"successfully"}, status=status.HTTP_200_OK)
    return JsonResponse({'message': 'error'}, status=status.HTTP_400_BAD_REQUEST)

from firebase_admin import messaging

def get_fcm_token_by_member_id(member_id):
    try:
        member = Member.objects.get(MemberID=member_id)
        fcm_token = member.fcm_token
        send_to_firebase_cloud_messaging(fcm_token)
    except Member.DoesNotExist:
        return None  # 멤버를 찾지 못한 경우 None을 반환


#안드로이드로 알림 보내기
def send_to_firebase_cloud_messaging(token):
    # This registration token comes from the client FCM SDKs.
    registration_token = token
    print(registration_token)

    # See documentation on defining a message payload.
    message = messaging.Message(
    notification=messaging.Notification(
        title='불법 주정차 차량이 발견됐어요!',
        body='내역을 확인하고 신고를 접수해주세요.',
    ),
    token=registration_token,
    )

    response = messaging.send(message)
    # Response is a message ID string.
    print('Successfully sent message:', response)