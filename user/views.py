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

# Create your views here.

# 회원가입 API
@api_view(['POST'])
def signup(request):
    if request.method=='POST':
        data={} # 딕셔너리 생성
        for i in request.data: # 클라이언트 요청 데이터(딕셔너리, 쿼리셋)을 개별적으로 반복, 처리
            if i=="Password": # i가 비밀번호인 경우
                data[i]=bcrypt.hashpw(request.POST["Password"].encode("UTF-8"), bcrypt.gensalt()).decode("UTF-8") # 비밀번호 해싱하여 딕셔너리에 저장
            elif i in ("ResidentRegistration", "PhoneNumber","Age"): # i가 주민번호, 전화번호, 나이 중 하나인 경우
                data[i]=int(request.POST[i]) # i값을 정수 변환 후 딕셔너리에 저장
            else: # 그 외의 경우(이름, 주거지, ID, 계좌번호)
                data[i]=request.POST[i] # 딕셔너리에 저장
        serializer = MemberSerializers(data=data) # data 딕셔너리로 시리얼라이저 객체 생성
        if serializer.is_valid(): # 시리얼라이저 유효성 검사
            serializer.save() # 유효하면 회원정보 저장
        else:
            print(serializer.errors) # 유효하지 않을 경우 에러메세지 출력
            return JsonResponse({'message': 'error'}, status=status.HTTP_400_BAD_REQUEST) # 시리얼라이저 유효하지 않을 경우
        return JsonResponse({'message':"successfully"}, status=status.HTTP_201_CREATED) 
    return JsonResponse({'message': 'error'}, status=status.HTTP_400_BAD_REQUEST) # request 메소드가 POST가 아닐 경우

# 로그인 API
@api_view(['POST'])
def signin(request):
    if Member.objects.filter(MenberID=request.POST["MemberID"]).exists(): # 클라이언트가 회원 데이터베이스와 부합하는 ID 값을 보낸 경우
        user=Member.objects.get(MenberID=request.POST["MemberID"]) # 데이터베이스에서 해당 회원을 불러옴
        if bcrypt.checkpw(request.POST['Password'].encode('UTF-8'), user.Password.encode('UTF-8'))==True: # 클라이언트가 회원 데이터베이스와 부합하는 PW 값을 보낸 경우
            return JsonResponse({'message':"successfully"}, status=status.HTTP_200_OK) # 성공 메세지 출력
    return JsonResponse({'message': 'error'}, status=status.HTTP_400_BAD_REQUEST) # 아니면 에러 메세지 출력

# 사용자 ID 체크 API
@api_view(['POST'])
def useridcheck(request):
    if Member.objects.filter(MenberID=request.POST["MemberID"]).exists(): # 클라이언트가 회원 데이터베이스와 부합하는 ID 값을 보낸 경우
        return JsonResponse({'message':"successfully"}, status=status.HTTP_200_OK) # 성공 메세지 출력
    return JsonResponse({'message': 'error'}, status=status.HTTP_400_BAD_REQUEST) # 아니면 에러 메세지 출력

# 회원탈퇴 API
@api_view
def delete(request):
    if Member.objects.filter(MenberID=request.POST["MemberID"]).exists(): # 클라이언트가 회원 데이터베이스와 부합하는 ID 값을 보낸 경우
        user=Member.objects.get(MenberID=request.POST["MemberID"]) # 데이터베이스에서 해당 회원을 불러옴
        if bcrypt.checkpw(request.POST['Password'].encode('UTF-8'), user.Password.encode('UTF-8'))==True: # 클라이언트가 회원 데이터베이스와 부합하는 PW 값을 보낸 경우
            Member.objects.get(MenberID=request.POST["MemberID"]).delete() # 데이터베이스에서 해당 회원을 불러온 뒤 삭제
            return JsonResponse({'message':"successfully"}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'message': 'error'}, status=status.HTTP_400_BAD_REQUEST) # 클라이언트가 보낸 PW 값이 해당 회원의 PW 값과 다른 경우
    return JsonResponse({'message': 'error'}, status=status.HTTP_400_BAD_REQUEST) # 클라이언트가 회원 데이터베이스에 없는 ID 값을 보낼 경우