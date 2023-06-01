import datetime
from django.db import models
from datetime import date
from Hr.models import Employee


# Create your models here.
class MainAccount(models.Model):
    name = models.CharField(max_length=100)
    Account = models.BigIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def get_modified_date(self):
        timedelta = getCurrentDate() - self.update
        seconds = timedelta.days * 24 * 3600 + timedelta.seconds
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        if days > 0:
            return f"{days} {'day' if days == 1 else 'days'} ago"

        if hours > 0:
            return f"{hours} {'hour' if hours == 1 else 'hours'} ago"

        if minutes > 0:
            return f"{minutes} {'minute' if minutes == 1 else 'minutes'} ago"

        return f"{seconds} {'second' if seconds == 1 else 'seconds'} ago"


class IncomeSource(models.Model):    
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def get_modified_date(self):
        timedelta = getCurrentDate() - self.update
        seconds = timedelta.days * 24 * 3600 + timedelta.seconds
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        if days > 0:
            return f"{days} {'day' if days == 1 else 'days'} ago"

        if hours > 0:
            return f"{hours} {'hour' if hours == 1 else 'hours'} ago"

        if minutes > 0:
            return f"{minutes} {'minute' if minutes == 1 else 'minutes'} ago"

        return f"{seconds} {'second' if seconds == 1 else 'seconds'} ago"


def getCurrentDate():
    time = datetime.datetime.now(datetime.timezone.utc)
    return time



class CashTransfer(models.Model):
    reciept = models.ForeignKey(Employee, on_delete=models.RESTRICT,blank=True, null=True)
    mainAcc = models.ForeignKey(MainAccount, on_delete=models.RESTRICT,blank=True, null=True)
    incomeSources = models.ForeignKey(IncomeSource, on_delete=models.RESTRICT, blank=True, null=True)
    Amount =  models.BigIntegerField(blank=True, null=True)    
    # budgeting = models.ForeignKey(Budget, on_delete=models.RESTRICT)
    transferType = models.CharField(max_length=100,)
    receipttype = models.CharField(max_length=100,)
    nonEmployeename = models.CharField(max_length=500,blank=True, null=True)
    usercreated = models.CharField(max_length=500,blank=True, null=True)
    phone_number = models.PositiveBigIntegerField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.transferType
    
    def get_modified_date(self):
        timedelta = getCurrentDate() - self.update
        seconds = timedelta.days * 24 * 3600 + timedelta.seconds
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        if days > 0:
            return f"{days} {'day' if days == 1 else 'days'} ago"

        if hours > 0:
            return f"{hours} {'hour' if hours == 1 else 'hours'} ago"

        if minutes > 0:
            return f"{minutes} {'minute' if minutes == 1 else 'minutes'} ago"

        return f"{seconds} {'second' if seconds == 1 else 'seconds'} ago"
