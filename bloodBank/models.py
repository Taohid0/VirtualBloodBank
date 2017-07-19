from django.db import models

class Donor(models.Model):
    user_id = models.CharField(max_length=250)
    #name = models.CharField(max_length=100)
    blood_group = models.CharField(max_length=10)
    district = models.CharField(max_length = 50)
    date = models.DateField(null=True)
    contact_number = models.CharField(max_length=50)
    isDeleted = models.BooleanField(default=False)

    def __str__(self):
        return self.blood_group+ " "+self.district

class Blood_seeker(models.Model):
    phone_number = models.CharField(max_length=100)
    user_id = models.CharField(max_length=100)

    def __str__(self):
        return self.phone_number

class Blocked_List(models.Model):
    phone_number = models.CharField(max_length=100)
    user_id = models.CharField(max_length= 100)

    def __str__(self):
        return self.phone_number

class District_info(models.Model):
    district_name = models.CharField(max_length=100)
    donor_counter = models.IntegerField(default=0)

    def __str__(self):
        return  self.district_name + " "+str(self.donor_counter)

class Blood_group_info(models.Model):
    blood_group=  models.CharField(max_length=50)
    donor_counter = models.IntegerField(default=0)

    def __str__(self):
        return self.blood_group + " "+str(self.donor_counter)
