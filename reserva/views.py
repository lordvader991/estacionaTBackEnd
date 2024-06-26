from dataclasses import fields
from rest_framework.views import APIView
from rest_framework import generics
from django.db.models.functions import TruncMonth, TruncYear

from rest_framework.response import Response
from rest_framework import status
from parqueo.models import Details
from parqueo.serializers import VehicleEntrySerializer
from reserva.models import Reservation
from reserva.serializers import ReservationSerializer, ParkingEarningsSerializer
from datetime import date, datetime,timedelta
from .tasks import DailyTaskScheduler, initialize_scheduler
from django.db import transaction

class ReservationApiView(APIView):
    def get(self, request):
        serializer = ReservationSerializer(Reservation.objects.all(), many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
    def post(self, request, *args, **kwargs):
        return self.save_details(request, *args, **kwargs)

    def save_details(self, request, *args, **kwargs):
        with transaction.atomic():
            reservation_data = request.data.get('reservation')
            vehicle_entry_data = request.data.get('vehicle_entry')

            vehicle_entry_data['is_reserva'] = True

            vehicle_entry_serializer = VehicleEntrySerializer(data=vehicle_entry_data)
            vehicle_entry_serializer.is_valid(raise_exception=True)
            vehicle_entry = vehicle_entry_serializer.save()

            reservation_data['vehicle_entry'] = vehicle_entry.id  # Use the ID temporarily for validation

            reservation_serializer = ReservationSerializer(data=reservation_data)
            reservation_serializer.is_valid(raise_exception=True)

            # Here, replace the vehicle_entry ID with the actual instance
            reservation_serializer.validated_data['vehicle_entry'] = vehicle_entry
            reservation = reservation_serializer.save()

            if reservation_serializer.validated_data.get('reservation_date') == date.today():
                    scheduler = initialize_scheduler()
                    daily_task_scheduler = DailyTaskScheduler()
                    daily_task_scheduler.create_task(reservation)

            return Response(status=status.HTTP_201_CREATED, data={
                'reservation': reservation_serializer.data,
                'vehicle_entry': vehicle_entry_serializer.data,
            })

class ReservationDetailApiView(APIView):
    def get_object(self, pk):
        try:
            return Reservation.objects.get(pk=pk)
        except Reservation.DoesNotExist:
            return None

    def get(self, request, id):
        reservation = self.get_object(id)
        if reservation is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ReservationSerializer(reservation)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def put(self, request, id):
        reservation = self.get_object(id)
        if reservation is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ReservationSerializer(reservation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    def delete(self, request, id):
        reservation = self.get_object(id)
        if reservation is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        reservation.delete()
        response_data = {'deleted': True}
        return Response(status=status.HTTP_200_OK, data=response_data)

class ReservationUserDetailApiView(APIView):
    def get(self, request, userID):
        reservations = Reservation.objects.filter(user=userID)
        if not reservations:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ReservationSerializer(reservations, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

class ReservationPayment(APIView):
    def get_object(self, id):
        try:
            return Reservation.objects.get(id=id)
        except Reservation.DoesNotExist:
            return None

    def post(self, request, id):
        reservation = self.get_object(id)
        if reservation is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        reservation.state = Reservation.StateChoices.CONFIRMED
        reservation.save()
        return Response(status=status.HTTP_200_OK)

class ParkingEarningsView(APIView):
    def get(self, request, parking_id=None):
        if parking_id is None:
            return Response({"error": "parking_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        earnings = Reservation.calculate_total_earnings_and_vehicle_count_per_parking(parking_id)
        serializer = ParkingEarningsSerializer(earnings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

from django.db.models import Avg, Sum, Count, F, ExpressionWrapper, fields
from django.db.models.functions import ExtractMonth, ExtractYear
from datetime import datetime

class ParkingStatisticsView(APIView):
    def post(self, request, parking_id):
        # Obtener parámetros del body
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        month = request.data.get('month')
        year = request.data.get('year')
        # Crear el filtro base
        base_filter = {'vehicle_entry__parking_id': parking_id}
        # Añadir filtros adicionales según los parámetros recibidos
        if start_date and end_date:
            base_filter['reservation_date__range'] = [start_date, end_date]
        elif month and year:
            base_filter['reservation_date__month'] = month
            base_filter['reservation_date__year'] = year

        # Calcular la diferencia de tiempo en horas
        time_diff_expr = ExpressionWrapper(
            F('end_time') - F('start_time'),
            output_field=fields.DurationField()
        )

        # Tiempo promedio de reserva
        avg_reservation_time = Reservation.objects.filter(**base_filter).aggregate(
            avg_time=Avg(time_diff_expr)
        )['avg_time']

        # Tiempo total de reserva
        total_reservation_time = Reservation.objects.filter(**base_filter).aggregate(
            total_time=Sum(time_diff_expr)
        )['total_time']

        # Actualizar el filtro base para Details
        if 'reservation_date__range' in base_filter:
            base_filter['starttime__range'] = base_filter.pop('reservation_date__range')
        elif 'reservation_date__month' in base_filter:
            base_filter['starttime__month'] = base_filter.pop('reservation_date__month')
            base_filter['starttime__year'] = base_filter.pop('reservation_date__year')
        # Calcular la diferencia de tiempo en horas para Details
        details_time_diff_expr = ExpressionWrapper(
            F('endtime') - F('starttime'),
            output_field=fields.DurationField()
        )
        # Tiempo promedio de Details
        avg_details_time = Details.objects.filter(**base_filter).aggregate(
            avg_time=Avg(details_time_diff_expr)
        )['avg_time']
        # Tiempo total de Details
        total_details_time = Details.objects.filter(**base_filter).aggregate(
            total_time=Sum(details_time_diff_expr)
        )['total_time']

        # Convertir los resultados a horas
        def to_hours(duration):
            if duration:
                return duration.total_seconds() / 3600
            return 0

        return Response({
            'avg_reservation_time_hours': to_hours(avg_reservation_time),
            'avg_details_time_hours': to_hours(avg_details_time),
            'total_reservation_time_hours': to_hours(total_reservation_time),
            'total_details_time_hours': to_hours(total_details_time)
        })
class MonthlyEarningsView(APIView):
    def get(self, request, parking_id):
        year = request.GET.get('year', datetime.now().year)
        
        # Ganancias de reserva por mes
        reservation_earnings = Reservation.objects.filter(
            vehicle_entry__parking_id=parking_id,
            reservation_date__year=year
        ).annotate(
            month=ExtractMonth('reservation_date')
        ).values('month').annotate(
            total=Sum('total_amount')
        ).order_by('month')

        # Ganancias de Details por mes
        details_earnings = Details.objects.filter(
            vehicle_entry__parking_id=parking_id,
            starttime__year=year
        ).annotate(
            month=ExtractMonth('starttime')
        ).values('month').annotate(
            total=Sum('totalamount')
        ).order_by('month')

        return Response({
            'year': year,
            'reservation_earnings': reservation_earnings,
            'details_earnings': details_earnings
        })

class PopularPricesView(APIView):
    def post(self, request, parking_id):
        # Obtener parámetros del body
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        month = request.data.get('month')
        year = request.data.get('year')

        # Crear el filtro base
        base_filter = {'vehicle_entry__parking_id': parking_id}

        # Añadir filtros adicionales según los parámetros recibidos
        if start_date and end_date:
            base_filter['reservation_date__range'] = [start_date, end_date]
        elif month and year:
            base_filter['reservation_date__month'] = month
            base_filter['reservation_date__year'] = year
        elif year:
            base_filter['reservation_date__year'] = year
        else:
            # Si no se proporciona ningún filtro, usar el año y mes actual
            current_date = datetime.now()
            base_filter['reservation_date__year'] = current_date.year
            base_filter['reservation_date__month'] = current_date.month

        # Precios más usados en reservas
        popular_reservation_prices = Reservation.objects.filter(**base_filter).values(
            'price__id',
            'price__price',
            'price__type_vehicle__name'
        ).annotate(
            count=Count('id')
        ).order_by('-count')

        # Actualizar el filtro base para Details
        if 'reservation_date__range' in base_filter:
            base_filter['starttime__range'] = base_filter.pop('reservation_date__range')
        elif 'reservation_date__month' in base_filter:
            base_filter['starttime__month'] = base_filter.pop('reservation_date__month')
            base_filter['starttime__year'] = base_filter.pop('reservation_date__year')
        elif 'reservation_date__year' in base_filter:
            base_filter['starttime__year'] = base_filter.pop('reservation_date__year')

        # Precios más usados en Details
        popular_details_prices = Details.objects.filter(**base_filter).values(
            'price__id',
            'price__price',
            'price__type_vehicle__name'
        ).annotate(
            count=Count('id')
        ).order_by('-count')

        # Preparar la respuesta
        response_data = {
            'popular_reservation_prices': popular_reservation_prices,
            'popular_details_prices': popular_details_prices
        }

        # Añadir información sobre el filtro utilizado
        if start_date and end_date:
            response_data['filter'] = f"From {start_date} to {end_date}"
        elif month and year:
            response_data['filter'] = f"Month {month}, Year {year}"
        elif year:
            response_data['filter'] = f"Year {year}"
        else:
            response_data['filter'] = f"Current month and year"

        return Response(response_data)