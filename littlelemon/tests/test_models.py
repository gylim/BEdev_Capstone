from django.test import TestCase
from restaurant.models import Menu, Booking
from datetime import datetime
from decimal import Decimal
from zoneinfo import ZoneInfo

class MenuTest(TestCase):
  def setUp(self) -> None:
    Menu.objects.create(Title="Ice Cream", Price=5.70, Inventory=27)

  def test_get_item(self):
    item = Menu.objects.get(Title="Ice Cream")
    self.assertEqual(item.Price, Decimal('5.70'))
    self.assertEqual(item.Inventory, 27)

  def test_change_item(self):
    item = Menu.objects.get(Title="Ice Cream")
    item.Price = 4.6
    item.save(update_fields=['Price'])
    updated = Menu.objects.get(Title='Ice Cream')
    self.assertEqual(updated.Price, Decimal('4.60'))

  def test_delete_item(self):
    first = Menu.objects.get()
    first.delete()
    self.assertEqual(Menu.objects.count(), 0)

class BookingTest(TestCase):
  def setUp(self) -> None:
    Booking.objects.create(Name="Luffy", No_of_guests=5, BookingDate=datetime(2023, 9, 20, 13, tzinfo=ZoneInfo('Asia/Singapore')))

  def test_get_item(self):
    item = Booking.objects.get(Name="Luffy")
    self.assertEqual(item.No_of_guests, 5)
    self.assertEqual(item.BookingDate, datetime(2023, 9, 20, 13, tzinfo=ZoneInfo('Asia/Singapore')))

  def test_change_item(self):
    item = Booking.objects.get(Name="Luffy")
    item.No_of_guests = 3
    item.save(update_fields=['No_of_guests'])
    updated = Booking.objects.get(Name='Luffy')
    self.assertEqual(updated.No_of_guests, 3)

  def test_delete_item(self):
    first = Booking.objects.get()
    first.delete()
    self.assertEqual(Booking.objects.count(), 0)
