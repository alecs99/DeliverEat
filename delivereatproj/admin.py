from django.contrib import admin
from . import models


# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('address', 'phone_number', 'birthday')
    search_fields = ('user__username',)


class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant_type', 'open_hour', 'close_hour')
    search_fields = ('name',)


admin.site.register(models.UserProfile, UserProfileAdmin)
admin.site.register(models.Restaurant, RestaurantAdmin)
admin.site.register(models.Product)
admin.site.register(models.Order)
admin.site.register(models.Cart)
admin.site.register(models.Feedback)


