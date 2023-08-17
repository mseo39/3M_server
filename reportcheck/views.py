from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from user.serializers import Member, CarList, ReportList
from django.http import JsonResponse

# Create your views here.

@api_view(["GET"])
def myreport(request):
    if Member.objects.filter(MemberID=request.data["MemberID"]).exists():
        user = Member.objects.get(MemberID=request.data["MemberID"])
    else:
        return JsonResponse({"message": "등록되지 않은 ID입니다."})
    
    if ReportList.objects.filter(AfterUniqueNumber=user.UniqueNumber).exists():
        report_list = ReportList.objects.filter(AfterUniqueNumber=user.UniqueNumber).order_by('-AfterDate')
        Car_num = [num.CarNum for num in report_list]
        car_list = CarList.objects.filter(MemberID=request.data["MemberID"], CarNum__in=Car_num).order_by('-Date')
    else:
        return JsonResponse({"message": "신고 내역이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
    
    response_data = []
    for report, car in zip(report_list, car_list):
        data = {
            "before_time": report.BeforeDate,
            "after_time": report.AfterDate,
            "car_num": report.CarNum,
            "latitude": car.Latitude,
            "longitude": car.Longitube
        }
        response_data.append(data)

    return JsonResponse(response_data, safe=False)

@api_view(["GET"])
def mycar(request):
    if ReportList.objects.filter(CarNum=request.data["CarNum"]).exists():
        report_list = ReportList.objects.filter(CarNum=request.data["CarNum"]).order_by('-AfterDate')
        Car_num = [num.CarNum for num in report_list]
        car_list = CarList.objects.filter(CarNum__in=Car_num).order_by('-Date')
    else:
        return JsonResponse({"message": "신고 내역에 없는 차량 번호 입니다."})

    response_data = []
    for report, car in zip(report_list, car_list):
        data = {
            "before_time": report.BeforeDate,
            "after_time": report.AfterDate,
            "latitude": car.Latitude,
            "longitude": car.Longitube
        }
        response_data.append(data)
    
    return JsonResponse(response_data, safe=False)


