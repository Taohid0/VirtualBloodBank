from django.contrib import admin
from bloodBank import models as bloodBank_models
# Register your models here.

admin.site.register(bloodBank_models.Donor)
admin.site.register(bloodBank_models.Blood_seeker)
admin.site.register(bloodBank_models.Blocked_List)
admin.site.register(bloodBank_models.District_info)
admin.site.register(bloodBank_models.Blood_group_info)
