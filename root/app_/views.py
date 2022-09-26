from django.shortcuts import render, redirect

from app_.models import Item


def get_db_items(db):
    return Item.objects.all().using(db)


def main_view(request):

    # определяем какая кнопка была нажата по атрибуту name (см. разметку)
    if 'clear_items' in request.POST:
        Item.objects.all().delete()

    if 'add_item' in request.POST:
        item_name = request.POST.get('item_name', 'empty name')
        item_obj = Item(name=item_name)
        item_obj.save(using='default')

    master_items = get_db_items('default')
    replica_items = get_db_items('replica')

    context = {
        'master_items': master_items,
        'replica_items': replica_items
    }

    return render(request, 'main.html', context=context)
