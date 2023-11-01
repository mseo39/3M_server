from django.shortcuts import render
import json
import bcrypt #단방향으로 암호화
import jwt #인증을 위해 사용
from .models import Member, CarList, ReportList
from main.settings import SECRET_KEY
from django.views import View
from django.http import HttpResponse,JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from user.serializers import MemberSerializers
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from firebase_admin import messaging, auth

# Create your views here.

# 회원가입 API
@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        data = {}  # 딕셔너리 생성
        for i in request.data:  # 클라이언트 요청 데이터(딕셔너리, 쿼리셋)을 개별적으로 반복, 처리
            if i == "Password":  # i가 비밀번호인 경우
                data[i] = bcrypt.hashpw(request.data["Password"].encode("UTF-8"), bcrypt.gensalt()).decode("UTF-8")  # 비밀번호 해싱하여 딕셔너리에 저장
            elif i in ("ResidentRegistration", "PhoneNumber", "Age"):  # i가 주민번호, 전화번호, 나이 중 하나인 경우
                data[i] = int(request.data[i])  # i값을 정수 변환 후 딕셔너리에 저장
            else:  # 그 외의 경우(이름, 주거지, ID, 계좌번호)
                data[i] = request.data[i]  # 딕셔너리에 저장
                
        data["fcm_token"]=""
        serializer = MemberSerializers(data=data)  # data 딕셔너리로 시리얼라이저 객체 생성
        if serializer.is_valid():  # 시리얼라이저 유효성 검사
            serializer.save()  # 유효하면 회원정보 저장
            return JsonResponse({'message': "successfully"}, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)  # 유효하지 않을 경우 에러메세지 출력
            return JsonResponse({'message': 'error', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    return JsonResponse({'message': 'error'}, status=status.HTTP_400_BAD_REQUEST)  # request 메소드가 POST가 아닐 경우

#안드로이드로 알림 보내기
def send_to_firebase_cloud_messaging(token):
    # This registration token comes from the client FCM SDKs.
    registration_token = token
    print(registration_token)

    # See documentation on defining a message payload.
    message = messaging.Message(
    notification=messaging.Notification(
        title='3m',
        body='촬영된 차량중에 신고대상인 차량이 있습니다',
    ),
    token=registration_token,
    )

    response = messaging.send(message)
    # Response is a message ID string.
    print('Successfully sent message:', response)

# 로그인 API
@api_view(['POST'])
def signin(request):
    if Member.objects.filter(MemberID=request.data["MemberID"]).exists():  # 수정된 부분
        user = Member.objects.get(MemberID=request.data["MemberID"])  # 수정된 부분
        if bcrypt.checkpw(request.data['Password'].encode('UTF-8'), user.Password.encode('UTF-8')) == True:
            member = Member.objects.get(MemberID=request.data["MemberID"])
            member.fcm_token = request.data["fcm_token"]
            member.save()
            return JsonResponse({'message': "successfully"}, status=status.HTTP_200_OK)
    return JsonResponse({'message': 'error'}, status=status.HTTP_400_BAD_REQUEST)


# 사용자 ID 체크 API
@api_view(['POST'])
def useridcheck(request):
    if Member.objects.filter(MemberID=request.data["MemberID"]).exists():  # 수정된 부분
        return JsonResponse({'message': "successfully"}, status=status.HTTP_200_OK)
    return JsonResponse({'message': 'error'}, status=status.HTTP_400_BAD_REQUEST)


# 회원탈퇴 API
@method_decorator(csrf_exempt, name='dispatch')
@api_view(['POST'])
def delete(request):
    if Member.objects.filter(MemberID=request.data["MemberID"]).exists():  # 수정된 부분
        user = Member.objects.get(MemberID=request.data["MemberID"])  # 수정된 부분
        if bcrypt.checkpw(request.data['Password'].encode('UTF-8'), user.Password.encode('UTF-8')) == True:
            Member.objects.get(MemberID=request.data["MemberID"]).delete()
            return JsonResponse({'message': "successfully"}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'message': 'error'}, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({'message': 'error'}, status=status.HTTP_400_BAD_REQUEST)
