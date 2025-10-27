from django.shortcuts import render, get_object_or_404
from django.http import Http404
from constructor.models import Page, SiteSettings

def get_menu_items():
    """Получение элементов меню для навигации"""
    menu_pages = Page.objects.filter(
        is_published=True, 
        show_in_menu=True
    ).exclude(category__in=['main', 'about']).order_by('menu_order', 'title')
    
    menu_items = {}
    for page in menu_pages:
        if page.category not in menu_items:
            menu_items[page.category] = []
        menu_items[page.category].append(page)
    
    return menu_items

def page_detail(request, slug):
    """Отображение страницы по slug"""
    try:
        page = get_object_or_404(Page, slug=slug, is_published=True)
        site_settings = SiteSettings.objects.first()
        
        context = {
            'page': page,
            'site_settings': site_settings,
            'menu_items': get_menu_items(),
        }
        
        return render(request, 'pages/page_detail.html', context)
        
    except Page.DoesNotExist:
        raise Http404("Страница не найдена")

def home_page(request):
    """Главная страница"""
    try:
        # Ищем страницу с slug 'home' для главной страницы
        page = get_object_or_404(Page, slug='home', is_published=True)
        site_settings = SiteSettings.objects.first()
        
        context = {
            'page': page,
            'site_settings': site_settings,
            'menu_items': get_menu_items(),
        }
        
        return render(request, 'pages/page_detail.html', context)
        
    except Page.DoesNotExist:
        # Если страницы 'home' нет, показываем заглушку
        site_settings = SiteSettings.objects.first()
        context = {
            'page': {
                'title': site_settings.site_name if site_settings else 'Триал - Рекламное агентство',
                'meta_description': 'Рекламное агентство полного цикла'
            },
            'site_settings': site_settings,
            'menu_items': get_menu_items(),
        }
        return render(request, 'pages/home_placeholder.html', context)