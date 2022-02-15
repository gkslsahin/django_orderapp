from django.urls import re_path
from OrderApp import views

urlpatterns = [
    re_path(r"order$", views.add_order,name="order"),
    re_path(r"complate/order/([0-9]+)$", views.complate_order,name="complete_order"),
    re_path(r"order/list$", views.orders_list,name="order_list"),
]
