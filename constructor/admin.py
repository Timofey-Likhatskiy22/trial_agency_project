from django.contrib import admin
from .models import *

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'phone', 'email']
    
    def has_add_permission(self, request):
        # Разрешаем только одну запись
        return not SiteSettings.objects.exists()

class HeroSectionInline(admin.TabularInline):
    model = HeroSection
    extra = 1
    classes = ['collapse']

class TextImageSectionInline(admin.TabularInline):
    model = TextImageSection
    fk_name = 'page'
    extra = 1
    classes = ['collapse']

class TextHtmlSectionInline(admin.TabularInline):
    model = TextHtmlSection
    fk_name = 'page'
    extra = 1
    classes = ['collapse']

class SlideInline(admin.TabularInline):
    model = Slide
    extra = 1
    classes = ['collapse']

class SliderSectionInline(admin.TabularInline):
    model = SliderSection
    extra = 1
    classes = ['collapse']

class FeatureInline(admin.TabularInline):
    model = Feature
    fk_name = 'section'
    extra = 1
    classes = ['collapse']

class FeaturesSectionInline(admin.TabularInline):
    model = FeaturesSection
    fk_name = 'page'
    extra = 1
    classes = ['collapse']

class ServiceCardInline(admin.TabularInline):
    model = ServiceCard
    fk_name = 'section'
    extra = 1
    classes = ['collapse']

class ServicesSectionInline(admin.TabularInline):
    model = ServicesSection
    fk_name = 'page'
    extra = 1
    classes = ['collapse']

class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    fk_name = 'section'
    extra = 1
    classes = ['collapse']

class GallerySectionInline(admin.TabularInline):
    model = GallerySection
    fk_name = 'page'
    extra = 1
    classes = ['collapse']

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'category', 'is_published', 'show_in_menu', 'menu_order']
    list_filter = ['category', 'is_published', 'show_in_menu']
    search_fields = ['title', 'slug', 'meta_description']
    prepopulated_fields = {'slug': ['title']}
    list_editable = ['show_in_menu', 'menu_order']
    
    inlines = [
        HeroSectionInline,
        SliderSectionInline,
        TextImageSectionInline,
        TextHtmlSectionInline,
        ServicesSectionInline,
        FeaturesSectionInline,
        GallerySectionInline,
    ]
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'meta_description', 'category')
        }),
        ('Настройки меню', {
            'fields': ('show_in_menu', 'menu_order'),
            'classes': ('collapse',)
        }),
        ('Настройки публикации', {
            'fields': ('is_published',),
            'classes': ('collapse',)
        }),
    )

# Регистрируем остальные модели отдельно для прямого доступа
@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'page', 'order']
    list_filter = ['page']

@admin.register(TextImageSection)
class TextImageSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'page', 'order']
    list_filter = ['page']

@admin.register(TextHtmlSection)
class TextHtmlSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'page', 'order']
    list_filter = ['page']

@admin.register(SliderSection)
class SliderSectionAdmin(admin.ModelAdmin):
    list_display = ['page', 'autoplay', 'order']
    list_filter = ['page']
    inlines = [SlideInline]

@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ['title', 'slider', 'order']
    list_filter = ['slider']

@admin.register(ServicesSection)
class ServicesSectionAdmin(admin.ModelAdmin):
    list_display = ['main_title', 'page', 'order']
    list_filter = ['page']
    inlines = [ServiceCardInline]

@admin.register(ServiceCard)
class ServiceCardAdmin(admin.ModelAdmin):
    list_display = ['title', 'section', 'order']
    list_filter = ['section']

@admin.register(FeaturesSection)
class FeaturesSectionAdmin(admin.ModelAdmin):
    list_display = ['main_title', 'page', 'order']
    list_filter = ['page']
    inlines = [FeatureInline]

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ['title', 'section', 'order']
    list_filter = ['section']

@admin.register(GallerySection)
class GallerySectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'page', 'order']
    list_filter = ['page']
    inlines = [GalleryImageInline]

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'section', 'order']
    list_filter = ['section']