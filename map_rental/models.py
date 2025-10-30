from django.db import models

class AdBoard(models.Model):
    # Выбор типа рекламного носителя
    AD_TYPE_CHOICES = [
        ('billboard', 'Билборд'),
        ('led_screen', 'LED-экран'),
        ('prismatron', 'Призматрон'),
        ('citylight', 'Ситилайт'),
        ('pillar', 'Столб'),
    ]
    
    # Основные поля модели
    title = models.CharField(max_length=200, verbose_name="Название рекламного носителя")
    ad_type = models.CharField(max_length=20, choices=AD_TYPE_CHOICES, verbose_name="Тип носителя")
    address = models.TextField(verbose_name="Адрес размещения")
    description = models.TextField(blank=True, verbose_name="Описание и характеристики")
    rental_terms = models.TextField(blank=True, verbose_name="Условия и сроки аренды")
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Стоимость аренды")
    contact_info = models.TextField(blank=True, verbose_name="Контактная информация")
    photo = models.ImageField(upload_to='adboards/', blank=True, null=True, verbose_name="Фотография")
    
    # Координаты (значения по умолчанию - Славгород)
    lat = models.FloatField(default=52.9994, verbose_name="Географическая широта")
    lon = models.FloatField(default=78.6459, verbose_name="Географическая долгота")
    
    # Служебные поля
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.get_ad_type_display()})"

    class Meta:
        verbose_name = "Рекламный носитель"
        verbose_name_plural = "Рекламные носители"
        ordering = ['ad_type', 'title']