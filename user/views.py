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

@api_view(['POST'])
def signup(request):
    if request.method=='POST':
        data={}
        for i in request.data:
            if i=="Password":
                data[i]=bcrypt.hashpw(request.POST["Password"].encode("UTF-8"), bcrypt.gensalt()).decode("UTF-8")
            elif i in ("ResidentRegistration", "PhoneNumber","Age"):
                data[i]=int(request.POST[i])
            else:
                data[i]=request.POST[i]
        serializer = MemberSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)
            return JsonResponse({'message': 'error'}, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'message':"successfully"}, status=status.HTTP_201_CREATED) 
    return JsonResponse({'message': 'error'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def signin(request):
    if Member.objects.filter(MenberID=request.POST["MemberID"]).exists():
        user=Member.objects.get(MenberID=request.POST["MemberID"])
        if bcrypt.checkpw(request.POST['Password'].encode('UTF-8'), user.Password.encode('UTF-8'))==True:
            return JsonResponse({'message':"successfully"}, status=status.HTTP_200_OK)
    return JsonResponse({'message': 'error'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def useridcheck(request):
    if Member.objects.filter(MenberID=request.POST["MemberID"]).exists():
        return JsonResponse({'message':"successfully"}, status=status.HTTP_200_OK)
    return JsonResponse({'message': 'error'}, status=status.HTTP_400_BAD_REQUEST)