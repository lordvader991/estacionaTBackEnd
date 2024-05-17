from datetime import date, datetime,timedelta
import uuid
from apscheduler.schedulers.background import BackgroundScheduler
from accounts.models import MobileToken
from reserva.models import Reservation
from demo.settings import FIREBASE_DB as db
from firebase_admin import messaging

class DailyTaskScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(self.start_daily_tasks, 'cron', hour=0, minute=0)

    def start_daily_tasks(self):
        try:
            today = datetime.today().date()
            reservas_del_dia = Reservation.objects.filter(reservation_date=today)
            for reserva in reservas_del_dia:
                self.create_task(reserva)
        except Exception as e:
            print("ERROR:", e)

    def create_task(self, reserva):
        now = datetime.now()
        
        date_start = datetime.combine(now.date(), reserva.start_time)
        time_start = date_start - timedelta(minutes=0)
        
        manager = ReservationManager(reserva)
        self.scheduler.add_job(manager.save_initial_duration, 'date', run_date=time_start)
        self.scheduler.start()

    def start(self):  
        self.scheduler.start()

class ReservationManager:
    def __init__(self, reserva):
        today = date.today()
        self.reserva_id = str(reserva.id) if reserva.id else uuid.uuid4().hex
        self.user_id = reserva.user.id
        self.start_time = datetime.combine(today, reserva.start_time)
        self.end_time = datetime.combine(today, reserva.end_time)
        self.duration = self.calculate_duration()
        self.scheduler = BackgroundScheduler()
    
    def calculate_duration(self):
        return self.end_time - self.start_time
    
    def save_initial_duration(self):
        data = {"remaining_time": str(self.duration),"reservation":self.reserva_id}
        db.child("parkingtime").child(str(self.user_id)).set(data)
        self.scheduler.add_job(self.start_reservation_task, 'interval', minutes=15,id=self.reserva_id)
        self.scheduler.start()

    def start_reservation_task(self):
        self.send_notification("Your reservation has started.")
        first_run_time = datetime.now() + timedelta(minutes=15)
        self.scheduler.add_job(self.task_reservation, 'interval', minutes=1, id=self.reserva_id, next_run_time=first_run_time, replace_existing=True)

    def task_reservation(self):
        new_remaining_time = self.duration - timedelta(minutes=1)
        if new_remaining_time.total_seconds() > 0:
            db.child("parkingtime").child(str(self.reserva_id)).update({"remaining_time": str(new_remaining_time)})
            self.duration = new_remaining_time
            if new_remaining_time == timedelta(minutes=15): 
                self.send_notification("Quedan 15 minutos para acabar la reserva")
            print("+ " + str(self.duration))
        else:
            db.child("parkingtime").child(str(self.reserva_id)).update({"remaining_time": "00:00:00"})
            self.send_notification("Your reservation has ended.")
            self.scheduler.remove_job(self.reserva_id)
    def send_notification(self, message):
        token = self.get_device_token(self.user_id)
        notification = messaging.Notification(title='Reserva Notificacion', body=message)
        message = messaging.Message(notification=notification, token=token)
        messaging.send(message)

    def get_device_token(self, user_id):
        return MobileToken.objects.filter(user=user_id).first().token
    
