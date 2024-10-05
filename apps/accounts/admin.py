from django.contrib import admin
from .models import User, NumberVerification


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'username', 'first_name', 'last_name', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('phone_number', 'username')
    list_filter = ('is_active', 'is_staff', 'date_joined')
    readonly_fields = ('date_joined',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset


admin.site.register(User, CustomUserAdmin)


class NumberVerificationAdmin(admin.ModelAdmin):
    list_display = ('verification_code', 'phone_number', 'created_at', 'is_verified')
    search_fields = ('verification_code', 'phone_number',)
    list_filter = ('created_at',)


admin.site.register(NumberVerification, NumberVerificationAdmin)
