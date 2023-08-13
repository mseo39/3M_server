from rest_framework import serializers
from .models import Member,CarList,ReportList

class MemberSerializers(serializers.ModelSerializer):
    class Meta:
        model=Member
        fields='__all__'

class CarListSerializers(serializers.ModelSerializer):
    class Meta:
        model=CarList
        fields='__all__'

class ReportListSerializers(serializers.ModelSerializer):
    class Meta:
        model=ReportList
        fields='__all__'
