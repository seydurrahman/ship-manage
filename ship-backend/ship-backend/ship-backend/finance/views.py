# views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime
from .models import *
from .serializers import *
from .services import calculate_monthly_profit


class ShipViewSet(viewsets.ModelViewSet):
    queryset = Ship.objects.all().order_by("id")
    serializer_class = ShipSerializer


class PartnerViewSet(viewsets.ModelViewSet):
    queryset = Partner.objects.all().order_by("id")
    serializer_class = PartnerSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by("id")
    serializer_class = ProjectSerializer


class DailyIncomeViewSet(viewsets.ModelViewSet):
    queryset = DailyIncome.objects.all().order_by("id")
    serializer_class = DailyIncomeSerializer

    @action(detail=False, methods=['get'])
    def daily_summary(self, request):
        date = request.GET.get('date', timezone.now().date())
        incomes = DailyIncome.objects.filter(date=date).order_by("id")
        serializer = self.get_serializer(incomes, many=True)
        return Response(serializer.data)


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all().order_by("id")
    serializer_class = ExpenseSerializer


class MonthlyProfitViewSet(viewsets.ModelViewSet):
    queryset = MonthlyProfit.objects.all().order_by("id")
    serializer_class = MonthlyProfitSerializer

    @action(detail=False, methods=['post'])
    def calculate_profit(self, request):
        month_str = request.data.get('month')
        ship_id = request.data.get('ship_id')

        try:
            month = datetime.strptime(month_str, '%Y-%m').date()
            profit_data = calculate_monthly_profit(ship_id, month)
            return Response(profit_data)
        except Exception as e:
            return Response({'error': str(e)}, status=400)


class PartnerPayoutViewSet(viewsets.ModelViewSet):
    queryset = PartnerPayout.objects.all().order_by("id")
    serializer_class = PartnerPayoutSerializer
