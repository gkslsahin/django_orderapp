import re
from django.db.models import manager
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from OrderApp.KafkaService import KafkaService
import json

from OrderApp.models import *
from OrderApp.serializers import *

# initialzie kafka_service
kafka_service = KafkaService(topic="channel")

@csrf_exempt
def add_order(request):
    if request.method == "POST":
        order_data = JSONParser().parse(request)
        try:
            kafka_service.send_to_topic(order_data)
        except Exception as err:
            print(str(err))
            return JsonResponse('{"msg:""error"}', safe=False, status=500)
        else:
            data = {"data": order_data}
            return JsonResponse(data, safe=False, status=200)


@csrf_exempt
def complate_order(request, id):
    if request.method == "PUT":
        # order_data = JSONParser().parse(request)
        order = None
        try:
            print("id:" + str(id))
            order = Order.objects.get(order_id=id)
            order.order_status = 1
            order = order.save()
        except Exception as err:
            return JsonResponse(
                '{"msg":"The order could not be completed"}', safe=False, status=500
            )
        else:
            return JsonResponse('{"msg":"order complated"}', safe=False, status=200)


@csrf_exempt
def orders_list(request):
    if request.method == "GET":
        orders = Order.objects.all()
        waiting_orders, complated_orders = [], []
        try:
            for order in orders:
                order_data = OrderSerializer(order).data
                if order.order_status:
                    complated_orders.append(order_data)
                else:
                    waiting_orders.append(order_data)
        except Exception as err:
            print(str(err))
            return JsonResponse(
                '{"msg":"The orders could not be returned"}', safe=False, status=500
            )

        return JsonResponse(
            {"waiting_orders": waiting_orders, "complated_orders": complated_orders},
            safe=False,
            status=200,
        )
