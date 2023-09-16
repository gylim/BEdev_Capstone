from django.test import TestCase
from django.contrib.auth.models import User, AnonymousUser
from rest_framework.test import force_authenticate, APIRequestFactory
from restaurant.views import MenuItemsView, SingleMenuItemView, BookingViewSet
from restaurant.models import Menu, Booking
from datetime import datetime
from zoneinfo import ZoneInfo

class MenuViewTest(TestCase):

  def setUp(self) -> None:
    # instantiate request factory and set-up admin user
    self.factory = APIRequestFactory()
    self.user = User.objects.create(username='test', password='testing123', is_staff=True)
    # populate test database
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
    request = self.factory.post('menu/', {'Title': 'Cheese', 'Price': 3.8, 'Inventory': 15}, format='json')

    # test that anonymous user cannot add menu item
    force_authenticate(request, user=AnonymousUser())
    response = MenuItemsView.as_view()(request)
    self.assertEqual(response.status_code, 403)
    self.assertEqual(Menu.objects.count(), 2)

    # test that admin user can add menu item
    force_authenticate(request, user=self.user)
    response = MenuItemsView.as_view()(request)
    self.assertEqual(response.status_code, 201)
    self.assertEqual(Menu.objects.count(), 3)
    self.assertEqual(Menu.objects.get(Title='Cheese').Inventory, 15)

  def test_del_one(self):
    pk = Menu.objects.get(Title="Ice Cream").id
    request = self.factory.delete('menu/')

    # test that anonymous user cannot delete menu item
    force_authenticate(request, user=AnonymousUser())
    response = SingleMenuItemView.as_view()(request, pk=pk)
    self.assertEqual(response.status_code, 403)
    self.assertEqual(Menu.objects.count(), 2)

    # test that admin user can delete menu item
    force_authenticate(request, user=self.user)
    response = SingleMenuItemView.as_view()(request, pk=pk)
    self.assertEqual(response.status_code, 204)
    self.assertEqual(Menu.objects.count(), 1)

  def test_put_one(self):
    pk = Menu.objects.get(Title="Ice Cream").id
    request = self.factory.put('/menu', {'Title': 'Fries', 'Price': 4.4, 'Inventory': 21})

    # test that anonymous user cannot put menu item
    force_authenticate(request, user=AnonymousUser())
    response = SingleMenuItemView.as_view()(request, pk=pk)
    self.assertEqual(response.status_code, 403)
    self.assertEqual(Menu.objects.get(id=pk).Title, 'Ice Cream')

    # test that admin user can change menu item
    force_authenticate(request, user=self.user)
    response = SingleMenuItemView.as_view()(request, pk=pk)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(Menu.objects.get(id=pk).Title, 'Fries')

  def test_patch_one(self):
    pk = Menu.objects.get(Title="Ice Cream").id
    request = self.factory.patch('/menu', {'Inventory': 21})

    # test that anonymous user cannot patch menu item
    force_authenticate(request, user=AnonymousUser())
    response = SingleMenuItemView.as_view()(request, pk=pk)
    self.assertEqual(response.status_code, 403)
    self.assertEqual(Menu.objects.get(id=pk).Title, 'Ice Cream')
    self.assertEqual(Menu.objects.get(id=pk).Inventory, 27)

    # test that admin user can change menu item
    force_authenticate(request, user=self.user)
    response = SingleMenuItemView.as_view()(request, pk=pk)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(Menu.objects.get(id=pk).Title, 'Ice Cream')
    self.assertEqual(Menu.objects.get(id=pk).Inventory, 21)


class BookingViewTest(TestCase):

  def setUp(self) -> None:
    # instantiate request factory and user
    self.factory = APIRequestFactory()
    self.user = User.objects.create(username='test2', password='testing234')

    # populate test database
    Booking.objects.create(Name="Luffy", No_of_guests=5, BookingDate=datetime(2023, 9, 20, 13, tzinfo=ZoneInfo('Asia/Singapore')))
    Booking.objects.create(Name="Chopper", No_of_guests=2, BookingDate=datetime(2023, 9, 21, 17, tzinfo=ZoneInfo('Asia/Bangkok')))

  def test_get_all(self):
    request = self.factory.get('restaurant/booking/tables')
    response = BookingViewSet.as_view({'get': 'list'})(request)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(len(response.data), 2)
    self.assertEqual(response.data[0]['Name'], "Luffy")
    self.assertEqual(response.data[1]['No_of_guests'], 2)

  def test_add_one(self):
    request = self.factory.post('restaurant/booking/tables', {'Name': 'Zorro', 'No_of_guests': 3, 'BookingDate': datetime(2023, 9, 22, 19, tzinfo=ZoneInfo('Asia/Singapore'))})

    # test that unauthenticated user cannot add booking
    response = BookingViewSet.as_view({'post': 'create'})(request)
    self.assertEqual(response.status_code, 401)
    self.assertEqual(Booking.objects.count(), 2)

    # test that normal user can add booking
    force_authenticate(request, user=self.user)
    response = BookingViewSet.as_view({'post': 'create'})(request)
    self.assertEqual(response.status_code, 201)
    self.assertEqual(Booking.objects.get(Name='Zorro').No_of_guests, 3)
    self.assertEqual(Booking.objects.count(), 3)

  def test_del_one(self):
    pk = Booking.objects.get(Name="Luffy").id
    request = self.factory.delete('restaurant/booking/tables')

    # test that unauthenticated user cannot delete booking
    response = BookingViewSet.as_view({'delete': 'destroy'})(request, pk=pk)
    self.assertEqual(response.status_code, 401)
    self.assertEqual(Booking.objects.count(), 2)

    # test that normal user can delete booking
    force_authenticate(request, user=self.user)
    response = BookingViewSet.as_view({'delete': 'destroy'})(request, pk=pk)
    self.assertEqual(response.status_code, 204)
    self.assertEqual(Booking.objects.get().Name, 'Chopper')
    self.assertEqual(Booking.objects.count(), 1)

  def test_patch_one(self):
    pk = Booking.objects.get(Name='Luffy').id
    request = self.factory.patch('/restaurant/booking/tables', {'Name': "Franky", 'No_of_guests': 100})

    # test that unauthenticated user cannot patch booking
    response = BookingViewSet.as_view({'patch': 'partial_update'})(request, pk=pk)
    self.assertEqual(response.status_code, 401)
    self.assertEqual(Booking.objects.get(id=pk).Name, 'Luffy')
    self.assertEqual(Booking.objects.get(id=pk).No_of_guests, 5)

    # test that normal user can patch booking
    force_authenticate(request, user=self.user)
    response = BookingViewSet.as_view({'patch': 'partial_update'})(request, pk=pk)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(Booking.objects.get(id=pk).Name, 'Franky')
    self.assertEqual(Booking.objects.get(id=pk).No_of_guests, 100)

  def test_put_one(self):
    pk = Booking.objects.get(Name='Chopper').id
    request = self.factory.put('/restaurant/booking/tables', {'Name': "Sanji", 'No_of_guests': 10, 'BookingDate': datetime(2023, 9, 22, 19, tzinfo=ZoneInfo('Asia/Singapore'))})

    # test that unauthenticated user cannot put booking
    response = BookingViewSet.as_view({'put': 'update'})(request, pk=pk)
    self.assertEqual(response.status_code, 401)
    self.assertEqual(Booking.objects.get(id=pk).Name, 'Chopper')
    self.assertEqual(Booking.objects.get(id=pk).No_of_guests, 2)

    # test that normal user can put booking
    force_authenticate(request, user=self.user)
    response = BookingViewSet.as_view({'put': 'update'})(request, pk=pk)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(Booking.objects.get(id=pk).Name, 'Sanji')
    self.assertEqual(Booking.objects.get(id=pk).No_of_guests, 10)
