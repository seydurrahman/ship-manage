# finance/admin.py
from django.contrib import admin
from .models import Ship, MonthlyProfit, Partner, PartnerPayout, Project, DailyIncome, Expense

# Register your models here.
admin.site.register(Ship)
admin.site.register(MonthlyProfit)
admin.site.register(Partner)
admin.site.register(PartnerPayout)
admin.site.register(Project)
admin.site.register(DailyIncome)
admin.site.register(Expense)