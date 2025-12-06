# models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Ship(models.Model):
    name = models.CharField(max_length=100)
    purchase_cost = models.DecimalField(max_digits=10, decimal_places=2, default=30000000.00)  # 3 crores
    purchase_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Partner(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    share_percentage = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])
    ship = models.ForeignKey(Ship, on_delete=models.CASCADE, related_name='partners')
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['name', 'ship']
    
    def __str__(self):
        return f"{self.name} - {self.ship.name}"

class Project(models.Model):
    name = models.CharField(max_length=200)
    ship = models.ForeignKey(Ship, on_delete=models.CASCADE, related_name='projects')
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} - {self.ship.name}"

class DailyIncome(models.Model):
    ship = models.ForeignKey(Ship, on_delete=models.CASCADE, related_name='daily_incomes')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='daily_incomes')
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['ship', 'project', 'date']
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.ship.name} - {self.project.name} - {self.date}"

class Expense(models.Model):
    EXPENSE_CATEGORIES = [
        ('FUEL', 'Fuel'),
        ('MAINTENANCE', 'Maintenance'),
        ('CREW', 'Crew Salary'),
        ('REPAIR', 'Repairs'),
        ('INSURANCE', 'Insurance'),
        ('OTHER', 'Other'),
    ]
    
    ship = models.ForeignKey(Ship, on_delete=models.CASCADE, related_name='expenses')
    category = models.CharField(max_length=20, choices=EXPENSE_CATEGORIES)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    date = models.DateField()
    description = models.TextField()
    receipt_number = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.ship.name} - {self.category} - {self.date}"

class MonthlyProfit(models.Model):
    ship = models.ForeignKey(Ship, on_delete=models.CASCADE, related_name='monthly_profits')
    month = models.DateField()  # First day of the month
    total_income = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_expenses = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    net_profit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    calculated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['ship', 'month']
        ordering = ['-month']
    
    def __str__(self):
        return f"{self.ship.name} - {self.month.strftime('%B %Y')}"

class PartnerPayout(models.Model):
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='payouts')
    monthly_profit = models.ForeignKey(MonthlyProfit, on_delete=models.CASCADE, related_name='payouts')
    share_amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    paid = models.BooleanField(default=False)
    paid_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['partner', 'monthly_profit']
    
    def __str__(self):
        return f"{self.partner.name} - {self.monthly_profit.month.strftime('%B %Y')}"