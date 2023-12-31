# Hello, Detector!
* 어린이 보호구역에 있는 불법 주정차를 신고하는 프로그램
* 제 10회 대한민국 SW융합 해커톤 대회에서 진행한 프로젝트

> 민식이 사건 이후 20만명이 넘는 국민 청원과 함께 법안이 발의된 후 민식이 법이 시행되었습니다. 하지만 최근 5년간 어린이 보호 구역 내 어린이 교통사고 현황을 살펴본 결과 실질적인 큰 감소율이 보이지 않았습니다. 저희 팀이 원인을 분석해보았을 때, 불법 주정차로 인한 사각지대 발생이 문제라고 판단했고 이에 대해서는 아직 해결책이 제시되지 않고 있음을 확인했습니다 이를 개선하고자 Hello Detector를 개발하였고 Hello Detector의 휴대폰 앱 혹은 블랙박스 기기를 이용하여 불법 주정차량을 인식하고 신고하게 만들었습니다

## 플로우 설명
![플로우차트](<./readmeImage/flowchart.png>)

## api 명세서

- 회원가입 http://127.0.0.1:8000/user/signup
    
    응답: 'message':"successfully” or 'message':"error”
    
    ```json
    {
        "UniqueNumber": "1234",
        "Name": "JohnDoe",
        "ResidentRegistration": "1234567890123",
        "ResidentialArea": "City",
        "PhoneNumbe": 1234567890,
        "MemberID": "mseo",
        "Password": "1234",
        "Age": 30,
        "CarNumber": "1234",
        "BankAccount": "1234567890123456"
    }
    ```
    
- 로그인 http://127.0.0.1:8000/user/signin
    
    응답: 'message':"successfully” or 'message':"error”
    
    ```json
    {
        "MemberID":"mseo",
        "Password":"1234",
        "fcm_token": "d33nSHjUSvGg4qB62mB_UF:APA91bF-vwUMJ0OIEl0ipV5mmTJGBKm9LnlkIVpTimrlctRdeuKOk9e8EtSl8WLyuP8z9ZAUmZkFpDMpLJZ0_MhHg7uKf1rK_O8FpRRa4dbN-xgTj0TZStSiTPpI09t0sTTyKK4FpLrC"
    }
    ```
- 회원탈퇴 http://127.0.0.1:8000/user/delete
    
    응답: 'message':"successfully” or 'message':"error”
    
    ```json
    {
        "MemberID":"mseo",
        "Password":"1234"
    }
    ```
    
- 회원아이디중복 http://127.0.0.1:8000/user/useridcheck
    
    응답: 'message':"successfully” or 'message':"error”
    
    ```json
    {
         "MemberID":"mseo"
    }
    ```
    
- 데이터 업로드 http://127.0.0.1:8000/send/Data

    응답: 'message':"successfully” or 'message':"error”

    ```json
    {
        "Date":"2023-08-11 11:45:00",
        "Latitude":36.7790501,
        "Longitube":126.9337827,
        "CarNum":"ABC123",
        "UniqueNumber":"123",
        "MemberID":"mseo",
        "ReportStatus":"F"
    }
    ```

- 내 자동차가 신고된 목록 http://127.0.0.1:8000/reportcheck/mycar

    응답
    "message": "등록되지 않은 ID입니다.”

    "message": "신고 내역이 없습니다.”

    ```json
    {
        "CarNum":"27바3456"
    }
    ```

- 내가 신고한 목록 http://127.0.0.1:8000/reportcheck/myreport


    응답: "message": "신고 내역에 없는 차량 번호 입니다.”
    ```json
    {
        "MemberID":"mseo"
    }
    ```

## 구현환경
```
python==3.9.6
Django==4.2.3
firebase-admin==6.2.0
djangorestframework==3.14.0
mysqlclient==2.2.0
```