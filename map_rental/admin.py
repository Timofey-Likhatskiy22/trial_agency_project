from django.contrib import admin
from .models import AdBoard

@admin.register(AdBoard)
class AdBoardAdmin(admin.ModelAdmin):
    list_display = ['title', 'ad_type', 'address', 'price', 'is_active', 'created_at']
    list_filter = ['ad_type', 'is_active', 'created_at']
    search_fields = ['title', 'address', 'description']
    list_editable = ['is_active', 'price']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'ad_type', 'address', 'is_active')
        }),
        ('Детали', {
            'fields': ('description', 'rental_terms', 'price', 'contact_info', 'photo'),
            'classes': ('collapse',)
        }),
        ('Координаты', {
            'fields': ('lat', 'lon'),
            'classes': ('collapse',)
        }),
    )