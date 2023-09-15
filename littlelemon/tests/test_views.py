from django.test import TestCase, RequestFactory
from restaurant.views import MenuItemsView, BookingViewSet
from restaurant.models import Menu, Booking
from datetime import datetime
from zoneinfo import ZoneInfo

class MenuViewTest(TestCase):

  def setUp(self) -> None:
    self.factory = RequestFactory()
    Menu.objects.create(Title="Ice Cream", Price=5.70, Inventory=27)
    Menu.objects.create(Title="Pie", Price=4.60, Inventory=34)

  def test_get_all(self):
    request = self.factory.get('menu/')
    response = MenuItemsView.as_view()(request)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(len(response.data), 2)
    self.assertEqual(response.data[0]['Title'], "Ice Cream")
    self.assertEqual(response.data[1]['Title'], "Pie")

  def test_add_one(self):
    request = self.factory.post('menu/', {'Title': 'Cheese', 'Price': 3.8, 'Inventory': 15}, content_type='application/json')
    response = MenuItemsView.as_view()(request)
    self.assertEqual(response.status_code, 201)
    self.assertEqual(Menu.objects.count(), 3)
    self.assertEqual(Menu.objects.get(Title='Cheese').Inventory, 15)

class BookingViewTest(TestCase):

  def setUp(self) -> None:
    self.factory = RequestFactory()
    Booking.objects.create(Name="Luffy", No_of_guests=5, BookingDate=datetime(2023, 9, 20, 13, tzinfo=ZoneInfo('Asia/Singapore')))
    Booking.objects.create(Name="Chopper", No_of_guests=2, BookingDate=datetime(2023, 9, 21, 17, tzinfo=ZoneInfo('Asia/Bangkok')))

  def test_get_all(self):
    request = self.factory.get('restaurant/booking/tables')
    response = BookingViewSet.as_view({'get': 'list'})(request)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(len(response.data), 2)
    self.assertEqual(response.data[0]['Name'], "Luffy")
    self.assertEqual(response.data[1]['No_of_guests'], 2)
