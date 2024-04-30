from datetime import date, datetime, time, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from django.forms import model_to_dict
from reserva.models import Reservation
from demo import settings

def workDay():
    try:
        today = date.today()
        reservas_del_dia = Reservation.objects.filter(reservation_date=today)
        for reserva in reservas_del_dia:
            createTask(reserva)
    except:
        print("NOT FOUND RESERVATIONS")

def createTask(reserva):
    hora_inicio = reserva.start_time
    now = datetime.now()
    fecha_hora_inicio = datetime.combine(now.date(), hora_inicio)
    scheduler = BackgroundScheduler()
    scheduler.add_job(taskReservation, 'date', run_date=fecha_hora_inicio, args=[reserva])
    scheduler.start()

def taskReservation(reserva):
    data = {str(reserva.id) : "1"}
    settings.FIREBASE_DB.child("parkingtime").push(data)

def startScheduler():
    scheduler = BackgroundScheduler()
    workDay()
    scheduler.add_job(workDay, 'cron', hour=0, minute=0)
    scheduler.start()