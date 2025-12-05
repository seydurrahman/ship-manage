# serializers.py
from rest_framework import serializers
from .models import *

class ShipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ship
        fields = '__all__'

class PartnerSerializer(serializers.ModelSerializer):
    ship_name = serializers.CharField(source='ship.name', read_only=True)
    
    class Meta:
        model = Partner
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    ship_name = serializers.CharField(source='ship.name', read_only=True)
    
    class Meta:
        model = Project
        fields = '__all__'

class DailyIncomeSerializer(serializers.ModelSerializer):
    ship_name = serializers.CharField(source='ship.name', read_only=True)
    project_name = serializers.CharField(source='project.name', read_only=True)
    
    class Meta:
        model = DailyIncome
        fields = '__all__'

class ExpenseSerializer(serializers.ModelSerializer):
    ship_name = serializers.CharField(source='ship.name', read_only=True)
    
    class Meta:
        model = Expense
        fields = '__all__'

class MonthlyProfitSerializer(serializers.ModelSerializer):
    ship_name = serializers.CharField(source='ship.name', read_only=True)
    
    class Meta:
        model = MonthlyProfit
        fields = '__all__'

class PartnerPayoutSerializer(serializers.ModelSerializer):
    partner_name = serializers.CharField(source='partner.name', read_only=True)
    ship_name = serializers.CharField(source='partner.ship.name', read_only=True)
    month = serializers.DateField(source='monthly_profit.month', read_only=True)
    
    class Meta:
        model = PartnerPayout
        fields = '__all__'