# views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Q
from django.utils import timezone
from datetime import datetime, timedelta
from .models import *
from .serializers import *
from .services import calculate_monthly_profit

class ShipViewSet(viewsets.ModelViewSet):
    queryset = Ship.objects.all()
    serializer_class = ShipSerializer

class PartnerViewSet(viewsets.ModelViewSet):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class DailyIncomeViewSet(viewsets.ModelViewSet):
    queryset = DailyIncome.objects.all()
    serializer_class = DailyIncomeSerializer
    
    @action(detail=False, methods=['get'])
    def daily_summary(self, request):
        date = request.GET.get('date', timezone.now().date())
        incomes = DailyIncome.objects.filter(date=date)
        serializer = self.get_serializer(incomes, many=True)
        return Response(serializer.data)

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

class MonthlyProfitViewSet(viewsets.ModelViewSet):
    queryset = MonthlyProfit.objects.all()
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
    queryset = PartnerPayout.objects.all()
    serializer_class = PartnerPayoutSerializer

