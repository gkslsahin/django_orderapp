from django.http import response
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
import json


class TetstorderAPI(APITestCase):
    def test_create_order(self):
        order_data = {"user": 3, "food": 4, "order_status": 0}
        # order_data = json.dumps(order_data)
        response = self.client.post(reverse("order"), order_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_complete_order(self):

        # first add data
        order_data = {"user": 3, "food": 4, "order_status": 0}
        response = self.client.post(reverse("order"), order_data, format="json")

        response = self.client.put(reverse("complete_order", args=[1]), format="")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_complete_order(self):
        response = self.client.put(reverse("complete_order", args=[7333]), format="")
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_order_list(self):
        response = self.client.get(reverse("order_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
