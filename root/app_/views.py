from django.shortcuts import render, redirect
from django.db import connections, transaction
from django.views import View

from app_.models import Item


def get_master_db():
    return Item.objects.using('default')


def get_replica_db():
    return Item.objects.using('replica')


def get_master_items():
    return get_master_db().all()


def get_replica_items():
    return get_replica_db().all()


class MainView(View):

    def get(self, request):
        master_items = get_master_items()
        replica_items = get_replica_items()
        subname = subid = 'None'

        with connections['replica'].cursor() as cursor:
            cursor.execute('SELECT * FROM pg_stat_subscription')
            if cursor.rowcount > 0:
                row = cursor.fetchone()
                subname = row[1]
                subid = row[0]

        context = {
            'master_items': master_items,
            'replica_items': replica_items,
            'subname': subname,
            'subid': subid
        }

        return render(request, 'main.html', context=context)

    def post(self, request):

        try:

            # определяем какая кнопка была нажата по атрибуту name (см. разметку)
            if 'clear_items' in request.POST:
                get_master_items().delete()
                get_replica_items().delete()

            if 'add_item' in request.POST:
                item_name = 'default item' if not request.POST['item_name'] else request.POST['item_name']
                item_obj = Item(name=item_name)
                item_obj.save(using='default')

            if 'rep_on' in request.POST:
                with connections['replica'].cursor() as cursor:
                    cursor.execute("CREATE SUBSCRIPTION master_subscription \
                        CONNECTION 'host=pg-master port=5432 password=pass user=postgres dbname=master_db' \
                        PUBLICATION publication")

            if 'rep_off' in request.POST:
                with connections['replica'].cursor() as cursor:
                    cursor.execute('DROP SUBSCRIPTION IF EXISTS master_subscription')

        finally:
            return redirect('main_page_route')
