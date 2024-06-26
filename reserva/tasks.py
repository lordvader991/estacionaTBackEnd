from datetime import date, datetime,timedelta
import uuid
from apscheduler.schedulers.background import BackgroundScheduler
from accounts.models import MobileToken
from reserva.models import Reservation
from demo.settings import FIREBASE_DB as db
from firebase_admin import messaging

scheduler = None

def initialize_scheduler():
    global scheduler
    if not scheduler:
        scheduler = BackgroundScheduler()
        scheduler.start()
    return scheduler

class DailyTaskScheduler:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DailyTaskScheduler, cls).__new__(cls)
            cls._instance.initialize()
        return cls._instance
    
    def initialize(self):
        self.scheduler = initialize_scheduler()
        self.scheduler.add_job(self.start_daily_tasks, 'cron', hour=0, minute=0)
        self.start_daily_tasks(only_future=True)

    def start_daily_tasks(self,only_future = False):
        try:
            now = datetime.now()
            today = now.date()
            if only_future:
                reservas_del_dia = Reservation.objects.filter(
                    reservation_date=today,
                    start_time__gt=now.time(),
                    state__in=[ Reservation.StateChoices.CONFIRMED]
                )
                print(f"Iniciando tareas para reservas futuras del {today}")
            else:
                reservas_del_dia = Reservation.objects.filter(
                    reservation_date=today,
                    state__in=[Reservation.StateChoices.CONFIRMED]
                )
                print(f"Iniciando tareas para todas las reservas pendientes o confirmadas del {today}")

            if reservas_del_dia.exists():
                for reserva in reservas_del_dia:
                    print(reserva.__dict__)
                    self.create_task(reserva)
            
            print(f"Se procesaron {reservas_del_dia.count()} reservas")

        except Exception as e:
            print(f"ERROR al iniciar tareas diarias: {e}")

    def create_task(self, reserva):
        now = datetime.now()
        
        date_start = datetime.combine(now.date(), reserva.start_time)
        time_start = date_start - timedelta(minutes=1)
        
        manager = ReservationManager(reserva)
        self.scheduler.add_job(manager.send_pre_notification, 'date', run_date=time_start, id=f'pre_notification_{reserva.id}')
        self.scheduler.add_job(manager.save_initial_duration, 'date', run_date=time_start, id=f'reservation_{reserva.id}')
class ReservationManager:
    def __init__(self, reserva):
        self.scheduler = initialize_scheduler()
        today = date.today()
        self.reserva_id = str(reserva.id) if reserva.id else uuid.uuid4().hex
        self.user_id = reserva.user.id
        self.start_time = datetime.combine(today, reserva.start_time)
        self.end_time = datetime.combine(today, reserva.end_time)
        self.duration = self.calculate_duration()

    def send_pre_notification(self):
        body = "Tu reserva comenzará en 5 minutos."
        self.send_notification(body)    

    def calculate_duration(self):
        return self.end_time - self.start_time

    def save_initial_duration(self):
        data = {"remaining_time": str(self.duration), "reservation": self.reserva_id}
        db.child("parkingtime").child(str(self.user_id)).set(data)
        self.scheduler.add_job(self.task_reservation, 'interval', minutes=1, id=self.reserva_id, next_run_time=self.start_time)

    def task_reservation(self):
        new_remaining_time = self.duration - timedelta(minutes=1)
        print("TASK RESERVATION")
        print(f"Duración de la reserva: {str(self.duration)}")

        if new_remaining_time.total_seconds() > 0:
            db.child("parkingtime").child(str(self.user_id)).update({"remaining_time": str(new_remaining_time)})
            self.duration = new_remaining_time
            if timedelta(minutes=14) <= new_remaining_time <= timedelta(minutes=15):
                self.send_notification("Quedan 15 minutos para acabar la reserva")
                print("+ " + str(self.duration))
        else:
            db.child("parkingtime").child(str(self.user_id)).update({"remaining_time": "00:00:00"})
            self.send_notification("Tu reserva ha terminado.")
            self.scheduler.remove_job(self.reserva_id)

    def send_notification(self, body):
        token = self.get_device_token(self.user_id)
        notification = messaging.Notification(title='Reserva Notificación', body=body)
        message = messaging.Message(notification=notification, token=token)
        messaging.send(message)

    def get_device_token(self, user_id):
        mobile_token = MobileToken.objects.filter(user=user_id).first()
        print("mobile token")
        print(mobile_token.token)
        return mobile_token.token