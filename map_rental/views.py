from django.shortcuts import render
from .models import AdBoard
from constructor.models import SiteSettings, Page
import json

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

def rental_map(request):
    """Страница с картой аренды рекламных носителей"""
    adboards = AdBoard.objects.filter(is_active=True)
    site_settings = SiteSettings.objects.first()
    
    # Создаем JSON с данными для правильной передачи координат
    adboards_data = []
    for adboard in adboards:
        adboards_data.append({
            'id': adboard.id,
            'title': adboard.title,
            'ad_type': adboard.ad_type,
            'address': adboard.address,
            'description': adboard.description,
            'rental_terms': adboard.rental_terms,
            'price': float(adboard.price) if adboard.price else None,
            'contact_info': adboard.contact_info,
            'photo': adboard.photo.url if adboard.photo else '',
            'lat': float(adboard.lat),
            'lon': float(adboard.lon),
            'get_ad_type_display': adboard.get_ad_type_display(),
        })
    
    context = {
        'adboards': adboards,
        'adboards_json': json.dumps(adboards_data, ensure_ascii=False),
        'map_center': {
            'lat': 53.00,
            'lon': 78.65
        },
        'page_title': 'Аренда рекламных носителей в Славгороде',
        'site_settings': site_settings,
        'menu_items': get_menu_items(),
    }
    
    return render(request, 'map_rental/rental_map.html', context)