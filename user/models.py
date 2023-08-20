from django.db import models

# Create your models here.
class Member(models.Model):
    UniqueNumber = models.CharField(max_length=12, primary_key=True)
    Name = models.CharField(max_length=12)
    ResidentRegistration = models.CharField(max_length=13)
    ResidentialArea = models.CharField(max_length=13)
    PhoneNumbe = models.IntegerField
    MemberID = models.CharField(max_length=10)
    Password = models.CharField(max_length=100)
    Age = models.IntegerField
    CarNumber = models.IntegerField
    BankAccount = models.CharField(max_length=16)
    fcm_token = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'Member'

class CarList(models.Model):
    status=(
        ('T', 'true'),
        ('F','false')
    )
    Date = models.DateTimeField( blank=True, null=True)
    Latitude= models.DecimalField(max_digits=20, decimal_places=15)
    Longitube= models.DecimalField(max_digits=20, decimal_places=15)
    CarNum = models.CharField(max_length=8)
    UniqueNumber=models.CharField(max_length=12 ,blank=True, null=True)
    MemberID = models.CharField(max_length=6)
    ReportStatus = models.CharField(max_length=1, choices=status)

    class Meta:
        db_table = 'CarList'

    def __str__(self):
        return str(self.Date) +" "+str(self.CarNum)

class ReportList(models.Model):
    BeforeDate= models.DateTimeField(blank=True, null=True)
    AfterDate = models.DateTimeField(blank=True, null=True)
    CarNum = models.CharField(max_length=8)
    BeforeUniqueNumber=models.CharField(max_length=12,blank=True, null=True)
    AfterUniqueNumber=models.CharField(max_length=12,blank=True, null=True)
    Beforeimage= models.ImageField(upload_to="carimg",blank=True, null=True)
    Afterimage= models.ImageField(upload_to="carimg",blank=True, null=True)

    class Meta:
        db_table = 'ReportList'

    def __str__(self):
        return str(self.CarNum)