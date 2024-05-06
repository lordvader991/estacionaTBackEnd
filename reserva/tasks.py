from datetime import date, datetime,timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from reserva.models import Reservation
from demo import settings
class DailyTaskScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(self.start_daily_tasks, 'cron', hour=0, minute=0)
    
    def start_daily_tasks(self):
        try:
            today = date.today()
            reservas_del_dia = Reservation.objects.filter(reservation_date=today)
            for reserva in reservas_del_dia:
                self.create_task(reserva)
        except:
            print("NOT FOUND RESERVATIONS")

    def create_task(self, reserva):
        now = datetime.now()
        
        fecha_hora_inicio = datetime.combine(now.date(), reserva.start_time)
        manager = ReservationManager(reserva.id, reserva.start_time, reserva.end_time)
        self.scheduler.add_job(manager.save_initial_duration, 'date', run_date=fecha_hora_inicio)
        self.scheduler.start()

    def start(self):
        self.scheduler.start()

class ReservationManager:
    def __init__(self, reserva_id, start_time, end_time):
        self.reserva_id = reserva_id
        self.start_time = datetime.strptime(start_time, '%H:%M')
        self.end_time = datetime.strptime(end_time, '%H:%M')
        self.duration = self.calculate_duration()
        self.scheduler = BackgroundScheduler()
    
    def calculate_duration(self):
        return self.end_time - self.start_time
    
    def save_initial_duration(self):
        data = {"remaining_time": str(self.duration)}
        settings.FIREBASE_DB.child("parkingtime").child(str(self.reserva_id)).set(data)
        self.scheduler.add_job(self.task_reservation, 'interval', minutes=1)
        self.scheduler.start()

    def task_reservation(self):
        print(str(self.duration))
        new_remaining_time = self.duration - timedelta(minutes=1)
        if new_remaining_time.total_seconds() > 0:
            settings.FIREBASE_DB.child("parkingtime").child(str(self.reserva_id)).update({"remaining_time": str(new_remaining_time)})
            self.duration = new_remaining_time
            print("+ " + str(self.duration))
        else:
            settings.FIREBASE_DB.child("parkingtime").child(str(self.reserva_id)).update({"remaining_time": "00:00:00"})
            self.scheduler.shutdown()