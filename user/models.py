from django.db import models

# Create your models here.
class Member(models.Model):
    UniqueNumber = models.CharField(max_length=12, primary_key=True)
    Name = models.CharField(max_length=12)
    ResidentRegistration = models.CharField(max_length=13)
    ResidentialArea = models.CharField(max_length=13)
    PhoneNumbe = models.IntegerField
    MenberID = models.CharField(max_length=6)
    Password = models.CharField(max_length=100)
    Age = models.IntegerField
    CarNumber = models.IntegerField
    BankAccount = models.CharField(max_length=16)

    class Meta:
        db_table = 'Member'

class CarList(models.Model):
    status=(
        ('T', 'true'),
        ('F','false')
    )
    Date = models.DateTimeField
    Latitude= models.DecimalField(max_digits=18, decimal_places=10)
    Longitube= models.DecimalField(max_digits=18, decimal_places=10)
    CarNum = models.CharField(max_length=8)
    UniqueNumber=models.ForeignKey(Member, related_name="carlist_UniqueNumber", on_delete=models.CASCADE)
    MenberID = models.CharField(max_length=6)
    ReportStatus = models.CharField(max_length=1, choices=status)

    class Meta:
        db_table = 'CarList'

class ReportList(models.Model):
    BeforeDate= models.DateTimeField
    AfterDate = models.DateTimeField
    CarNum = models.CharField(max_length=8)
    BeforeUniqueNumber=models.ForeignKey(Member, related_name="before_UniqueNumber", on_delete=models.CASCADE)
    AfterUniqueNumber=models.ForeignKey(Member, related_name="after_UniqueNumber", on_delete=models.CASCADE)

    class Meta:
        db_table = 'ReportList'