from django.db import models

class Page(models.Model):
    CATEGORY_CHOICES = [
        ('main', 'Главная'),
        ('about', 'О нас'),
        ('outdoor', 'Наружная реклама'),
        ('interior', 'Интерьерная реклама'),
        ('printing', 'Широкоформатная печать'),
        ('souvenirs', 'Сувенирная продукция'),
        ('other', 'Другое'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Заголовок страницы")
    slug = models.SlugField(unique=True, verbose_name="URL")
    meta_description = models.TextField(blank=True, verbose_name="Мета-описание")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other', verbose_name="Категория")
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    show_in_menu = models.BooleanField(default=False, verbose_name="Показывать в меню")
    menu_order = models.PositiveIntegerField(default=0, verbose_name="Порядок в меню")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Страница"
        verbose_name_plural = "Страницы"
        ordering = ['menu_order', 'title']

class SiteSettings(models.Model):
    """Настройки сайта"""
    site_name = models.CharField(max_length=100, default="Триал", verbose_name="Название сайта")
    logo = models.ImageField(upload_to='logo/', blank=True, null=True, verbose_name="Логотип")
    phone = models.CharField(max_length=20, default="+7 (123) 456-78-90", verbose_name="Телефон")
    email = models.CharField(max_length=100, default="info@trial-agency.ru", verbose_name="Email")
    address = models.TextField(default="г. Москва, ул. Рекламная, д. 123", verbose_name="Адрес")
    working_hours = models.CharField(max_length=100, default="Пн-Пт: 9:00 - 18:00", verbose_name="Режим работы")
    
    class Meta:
        verbose_name = "Настройки сайта"
        verbose_name_plural = "Настройки сайта"

    def __str__(self):
        return "Настройки сайта"

    def save(self, *args, **kwargs):
        # Разрешаем только одну запись настроек
        self.__class__.objects.exclude(id=self.id).delete()
        super().save(*args, **kwargs)

class HeroSection(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='hero_sections')
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    subtitle = models.TextField(verbose_name="Подзаголовок")
    background_image = models.ImageField(upload_to='hero/', blank=True, null=True, verbose_name="Фоновое изображение")
    background_gradient = models.CharField(max_length=100, default="from-orange-800 to-orange-600", verbose_name="Градиент")
    gradient_opacity = models.DecimalField(max_digits=3, decimal_places=2, default=1.0, 
                                         verbose_name="Прозрачность градиента",
                                         help_text="От 0.0 (прозрачный) до 1.0 (непрозрачный)")
    text_color = models.CharField(max_length=7, default="#ffffff", verbose_name="Цвет текста")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    
    class Meta:
        verbose_name = "Герой-секция"
        verbose_name_plural = "Герой-секции"
        ordering = ['order']

    def __str__(self):
        return f"Герой: {self.title}"

class TextImageSection(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='text_image_sections')
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержание")
    image = models.ImageField(upload_to='text_images/', verbose_name="Изображение")
    image_position = models.CharField(
        max_length=10,
        choices=[('left', 'Слева'), ('right', 'Справа')],
        default='right',
        verbose_name="Позиция изображения"
    )
    button_text = models.CharField(max_length=50, blank=True, verbose_name="Текст кнопки")
    internal_link = models.ForeignKey(Page, on_delete=models.SET_NULL, null=True, blank=True, 
                                    verbose_name="Ссылка на страницу сайта")
    external_link = models.CharField(max_length=500, blank=True, verbose_name="Внешняя ссылка")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    
    class Meta:
        verbose_name = "Текст с изображением"
        verbose_name_plural = "Тексты с изображением"
        ordering = ['order']

    def __str__(self):
        return f"Текст+изображение: {self.title}"

    def get_link(self):
        if self.internal_link:
            return f"/{self.internal_link.slug}/"
        return self.external_link

class ServicesSection(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='services_sections')
    main_title = models.CharField(max_length=200, default="Наши услуги", verbose_name="Главный заголовок")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    
    class Meta:
        verbose_name = "Секция услуг"
        verbose_name_plural = "Секции услуг"
        ordering = ['order']

    def __str__(self):
        return f"Услуги: {self.main_title}"

class ServiceCard(models.Model):
    section = models.ForeignKey(ServicesSection, on_delete=models.CASCADE, related_name='cards')
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")
    icon = models.CharField(max_length=50, verbose_name="Иконка")
    icon_color = models.CharField(max_length=7, default="#3B82F6", verbose_name="Цвет иконки")
    button_text = models.CharField(max_length=50, blank=True, verbose_name="Текст кнопки")
    internal_link = models.ForeignKey(Page, on_delete=models.SET_NULL, null=True, blank=True, 
                                    verbose_name="Ссылка на страницу сайта")
    external_link = models.CharField(max_length=500, blank=True, verbose_name="Внешняя ссылка")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    
    class Meta:
        verbose_name = "Карточка услуги"
        verbose_name_plural = "Карточки услуг"
        ordering = ['order']

    def __str__(self):
        return f"Услуга: {self.title}"

    def get_link(self):
        if self.internal_link:
            return f"/{self.internal_link.slug}/"
        return self.external_link

class FeaturesSection(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='features_sections')
    main_title = models.CharField(max_length=200, default="Почему выбирают нас", verbose_name="Главный заголовок")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    
    class Meta:
        verbose_name = "Секция преимуществ"
        verbose_name_plural = "Секции преимуществ"
        ordering = ['order']

    def __str__(self):
        return f"Преимущества: {self.main_title}"

class Feature(models.Model):
    section = models.ForeignKey(FeaturesSection, on_delete=models.CASCADE, related_name='features')
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")
    icon = models.CharField(max_length=50, verbose_name="Иконка")
    icon_color = models.CharField(max_length=7, default="#3B82F6", verbose_name="Цвет иконки")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    
    class Meta:
        verbose_name = "Преимущество"
        verbose_name_plural = "Преимущества"
        ordering = ['order']

    def __str__(self):
        return f"Преимущество: {self.title}"

class HtmlSection(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='html_sections')
    content = models.TextField(verbose_name="HTML-код")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    
    class Meta:
        verbose_name = "HTML-секция"
        verbose_name_plural = "HTML-секции"
        ordering = ['order']

    def __str__(self):
        return f"HTML: {self.content[:50]}..."

class TextHtmlSection(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='text_html_sections')
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Текст")
    html_content = models.TextField(verbose_name="HTML-контент", help_text="Будет вставлен как есть")
    html_position = models.CharField(
        max_length=10,
        choices=[('left', 'Слева'), ('right', 'Справа')],
        default='right',
        verbose_name="Позиция HTML-контента"
    )
    button_text = models.CharField(max_length=50, blank=True, verbose_name="Текст кнопки")
    internal_link = models.ForeignKey(Page, on_delete=models.SET_NULL, null=True, blank=True, 
                                    verbose_name="Ссылка на страницу сайта")
    external_link = models.CharField(max_length=500, blank=True, verbose_name="Внешняя ссылка")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    
    class Meta:
        verbose_name = "Текст с HTML"
        verbose_name_plural = "Тексты с HTML"
        ordering = ['order']

    def __str__(self):
        return f"Текст+HTML: {self.title}"

    def get_link(self):
        if self.internal_link:
            return f"/{self.internal_link.slug}/"
        return self.external_link

class SliderSection(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='slider_sections')
    autoplay = models.BooleanField(default=True, verbose_name="Автопрокрутка")
    autoplay_interval = models.PositiveIntegerField(default=5000, verbose_name="Интервал автопрокрутки (мс)")
    show_controls = models.BooleanField(default=True, verbose_name="Показывать кнопки управления")
    show_indicators = models.BooleanField(default=True, verbose_name="Показывать индикаторы")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    
    class Meta:
        verbose_name = "Слайдер"
        verbose_name_plural = "Слайдеры"
        ordering = ['order']

    def __str__(self):
        return f"Слайдер: {self.page.title}"

class Slide(models.Model):
    slider = models.ForeignKey(SliderSection, on_delete=models.CASCADE, related_name='slides')
    title = models.CharField(max_length=200, blank=True, verbose_name="Заголовок")
    subtitle = models.TextField(blank=True, verbose_name="Подзаголовок")
    image = models.ImageField(upload_to='slides/', verbose_name="Изображение")
    button_text = models.CharField(max_length=50, blank=True, verbose_name="Текст кнопки")
    internal_link = models.ForeignKey(Page, on_delete=models.SET_NULL, null=True, blank=True, 
                                    verbose_name="Ссылка на страницу сайта")
    external_link = models.CharField(max_length=500, blank=True, verbose_name="Внешняя ссылка")
    background_color = models.CharField(max_length=100, default="from-blue-800 to-blue-600", verbose_name="Градиент")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    
    class Meta:
        verbose_name = "Слайд"
        verbose_name_plural = "Слайды"
        ordering = ['order']

    def __str__(self):
        return f"Слайд: {self.title or 'Без заголовка'}"

    def get_link(self):
        if self.internal_link:
            return f"/{self.internal_link.slug}/"
        return self.external_link

class GallerySection(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='gallery_sections')
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    
    class Meta:
        verbose_name = "Галерея"
        verbose_name_plural = "Галереи"
        ordering = ['order']

    def __str__(self):
        return f"Галерея: {self.title}"

class GalleryImage(models.Model):
    section = models.ForeignKey(GallerySection, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='gallery/', verbose_name="Изображение")
    title = models.CharField(max_length=200, blank=True, verbose_name="Заголовок")
    description = models.TextField(blank=True, verbose_name="Описание")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    
    class Meta:
        verbose_name = "Изображение галереи"
        verbose_name_plural = "Изображения галереи"
        ordering = ['order']

    def __str__(self):
        return f"Изображение: {self.title}"