from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from unittest.mock import patch, MagicMock
from parqueo.models import Address, Parking
from reserva.models import Reservation, Price
from accounts.models import MobileToken, User
from reserva.tasks import DailyTaskScheduler, ReservationManager
from vehiculos.models import TypeVehicle
from .views import ReservationApiView

class ReservationManagementTestCase(TestCase):
    def setUp(self):
        # Crear un usuario
        self.user = User.objects.create_user(username='testuser', password='12345', email='test@example.com')
        MobileToken.objects.create(
             user = self.user,
             token = "fi_-BlUsS-eAMOtCio0hbx:APA91bHoJqCWowDP4qxVqdKS_i3I8dKMTs0AQov8wL0iviopldKxY2yjSRwBa9udmsz6V-TGuzMCjo_I-yNRR5G4ZFYiu5i1gks6T6eDsoliuOpoaTFOJ105W_0su2ZXsOSqj5jobgi6"
        )
        # Crear un tipo de vehículo
        self.type_vehicle = TypeVehicle.objects.create(name='Coche')
        
        # Crear un parking
        self.parking = Parking.objects.create(
            name='Parking Central',
            capacity=100,
            phone='123-456-7890',
            email='parking@example.com',
            user=self.user,
            spaces_available=50,
            url_image='https://example.com/parking.jpg',
            description='Parking céntrico con buena ubicación'
        )
        
        # Crear una dirección para el parking
        self.address = Address.objects.create(
            city='Ciudad Ejemplo',
            street='Calle Principal 123',
            longitude='-3.703790',
            latitude='40.416775',
            parking=self.parking
        )
               
        # Crear un price
        self.price = Price.objects.create(
            type_vehicle=self.type_vehicle,
            price=10.0,
            parking=self.parking,
            is_reservation=True,
            is_entry_fee=False,
            is_pricehour=True
        )
        
        # Crear un mobile token para el usuario
        MobileToken.objects.create(user=self.user, token='test_token')
        
        # Mock the Firebase DB
        self.mock_db = MagicMock()
        self.mock_db.child.return_value.child.return_value.set = MagicMock()
        self.mock_db.child.return_value.child.return_value.update = MagicMock()

    @patch('reserva.tasks.db', new_callable=MagicMock)
    @patch('reserva.tasks.messaging')
    def test_short_reservation_management(self, mock_messaging, mock_db):
        # Set up the request data
        now = timezone.now()
        start_time = (now + timedelta(minutes=10)).time()
        end_time = (now + timedelta(minutes=25)).time()  # 15 minutes duration
        reservation_date = now.date()
        
        request_data = {
            'reservation': {
                'start_time': start_time.strftime('%H:%M:%S'),
                'end_time': end_time.strftime('%H:%M:%S'),
                'total_amount': 5.0,
                'price': self.price.id,
                'reservation_date': reservation_date.isoformat(),
                'user': self.user.id,
            },
            'vehicle_entry': {
                'parking': self.parking.id,
                'user': self.user.id,
                'is_reserva': True,
                'phone': '987-654-3210',
                'is_userexternal': False,
            }
        }
        
        # Create a mock request
        mock_request = MagicMock()
        mock_request.data = request_data
        
        # Create the reservation
        view = ReservationApiView()
        response = view.post(mock_request)
        
        # Check if the reservation was created successfully
        self.assertEqual(response.status_code, 201)
        
        # Get the created reservation
        reservation = Reservation.objects.get(id=response.data['reservation']['id'])
        
        # Check if DailyTaskScheduler.create_task was called
        with patch.object(DailyTaskScheduler, 'create_task') as mock_create_task:
            scheduler = DailyTaskScheduler()
            scheduler.create_task(reservation)
            mock_create_task.assert_called_once_with(reservation)
        
        # Simulate time passing to just before the reservation starts
        with patch('reserva.views.datetime') as mock_datetime:
            mock_datetime.now.return_value = now + timedelta(minutes=9)
            mock_datetime.combine.return_value = now + timedelta(minutes=9)
            
            reservation_manager = ReservationManager(reservation)
            reservation_manager.send_pre_notification()
            
            # Check if the pre-notification was sent
            mock_messaging.send.assert_called_once()
        
        # Simulate saving initial duration
        with patch('reserva.views.datetime') as mock_datetime:
            mock_datetime.now.return_value = now + timedelta(minutes=10)
            mock_datetime.combine.return_value = now + timedelta(minutes=10)
            
            reservation_manager = ReservationManager(reservation)
            reservation_manager.save_initial_duration()
            
            # Check if the Firebase DB was updated with initial duration
            mock_db.child.assert_called_with('parkingtime')
            mock_db.child().child.assert_called_with(str(self.user.id))
            mock_db.child().child().set.assert_called_once()
        
        # Simulate time passing during the reservation
        with patch('reserva.views.datetime') as mock_datetime:
            for minute in range(1, 16):  # 15 minutes duration
                mock_datetime.now.return_value = now + timedelta(minutes=10+minute)
                mock_datetime.combine.return_value = now + timedelta(minutes=10+minute)
                
                reservation_manager = ReservationManager(reservation)
                reservation_manager.task_reservation()
                
                # Check if the Firebase DB was updated with the new remaining time
                mock_db.child().child().update.assert_called()
                mock_db.child().child().update.reset_mock()
                
                # Check for 15-minute warning
                if minute == 1:  # 14 minutes remaining
                    self.assertEqual(mock_messaging.send.call_count, 2)
        
        # Simulate the reservation ending
        with patch('reserva.views.datetime') as mock_datetime:
            mock_datetime.now.return_value = now + timedelta(minutes=26)  # 1 minute after end time
            mock_datetime.combine.return_value = now + timedelta(minutes=26)
            
            reservation_manager = ReservationManager(reservation)
            reservation_manager.task_reservation()
            
            # Check if the Firebase DB was updated with 00:00:00 remaining time
            mock_db.child().child().update.assert_called_with({"remaining_time": "00:00:00"})
        
        # Check if a final notification was sent
        self.assertEqual(mock_messaging.send.call_count, 3)
        # Set up the request data
        now = timezone.now()
        start_time = (now + timedelta(minutes=10)).time()
        end_time = (now + timedelta(minutes=25)).time()  # 15 minutes duration
        reservation_date = now.date()
        
        request_data = {
            'reservation': {
                'start_time': start_time.strftime('%H:%M:%S'),
                'end_time': end_time.strftime('%H:%M:%S'),
                'total_amount': 5.0,
                'price': self.price.id,
                'reservation_date': reservation_date.isoformat(),
                'user': self.user.id,
            },
            'vehicle_entry': {
                'parking': self.parking.id,
                'user': self.user.id,
                'is_reserva': True,
                'phone': '987-654-3210',
                'is_userexternal': False,
            }
        }
        # Create a mock request
        mock_request = MagicMock()
        mock_request.data = request_data
        
        # Create the reservation
        view = ReservationApiView()
        response = view.post(mock_request)
        
        # Check if the reservation was created successfully
        self.assertEqual(response.status_code, 201)
        
        # Get the created reservation
        reservation = Reservation.objects.get(id=response.data['reservation']['id'])
        
        # Check if DailyTaskScheduler.create_task was called
        with patch.object(DailyTaskScheduler, 'create_task') as mock_create_task:
            scheduler = DailyTaskScheduler()
            scheduler.create_task(reservation)
            mock_create_task.assert_called_once_with(reservation)
        
        # Simulate time passing to just before the reservation starts
        with patch('reserva.views.datetime') as mock_datetime:
            mock_datetime.now.return_value = now + timedelta(minutes=9)
            mock_datetime.combine.return_value = now + timedelta(minutes=9)
            
            reservation_manager = ReservationManager(reservation)
            reservation_manager.send_pre_notification()
            
            # Check if the pre-notification was sent
            mock_messaging.send.assert_called_once()
        
        # Check if the Firebase DB was updated with initial duration
        mock_db.child.assert_called_with('parkingtime')
        mock_db.child().child.assert_called_with(str(self.user.id))
        mock_db.child().child().set.assert_called_once()
        
        # Simulate time passing during the reservation
        with patch('reserva.views.datetime') as mock_datetime:
            for minute in range(1, 16):  # 15 minutes duration
                mock_datetime.now.return_value = now + timedelta(minutes=10+minute)
                mock_datetime.combine.return_value = now + timedelta(minutes=10+minute)
                
                reservation_manager = ReservationManager(reservation)
                reservation_manager.task_reservation()
                
                # Check if the Firebase DB was updated with the new remaining time
                mock_db.child().child().update.assert_called()
                mock_db.child().child().update.reset_mock()
                
                # Check for 15-minute warning
                if minute == 1:  # 14 minutes remaining
                    self.assertEqual(mock_messaging.send.call_count, 2)
        
        # Simulate the reservation ending
        with patch('reserva.views.datetime') as mock_datetime:
            mock_datetime.now.return_value = now + timedelta(minutes=26)  # 1 minute after end time
            mock_datetime.combine.return_value = now + timedelta(minutes=26)
            
            reservation_manager = ReservationManager(reservation)
            reservation_manager.task_reservation()
            
            # Check if the Firebase DB was updated with 00:00:00 remaining time
            mock_db.child().child().update.assert_called_with({"remaining_time": "00:00:00"})
        
        # Check if a final notification was sent
        self.assertEqual(mock_messaging.send.call_count, 3)