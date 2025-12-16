# services.py
from django.db.models import Sum, Q
from datetime import datetime, timedelta,timezone
from .models import *

def calculate_monthly_profit(ship_id, month):
    """
    Calculate monthly profit for a ship and create partner payouts
    """
    try:
        ship = Ship.objects.get(id=ship_id)
        
        # Calculate date range
        start_date = month.replace(day=1)
        if month.month == 12:
            end_date = month.replace(year=month.year + 1, month=1, day=1)
        else:
            end_date = month.replace(month=month.month + 1, day=1)
        
        # Calculate total income
        total_income = DailyIncome.objects.filter(
            ship=ship,
            date__gte=start_date,
            date__lt=end_date
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        # Calculate total expenses
        total_expenses = Expense.objects.filter(
            ship=ship,
            date__gte=start_date,
            date__lt=end_date
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        # Calculate net profit
        net_profit = total_income - total_expenses
        
        # Create or update MonthlyProfit
        monthly_profit, created = MonthlyProfit.objects.get_or_create(
            ship=ship,
            month=start_date,
            defaults={
                'total_income': total_income,
                'total_expenses': total_expenses,
                'net_profit': net_profit
            }
        )
        
        if not created:
            monthly_profit.total_income = total_income
            monthly_profit.total_expenses = total_expenses
            monthly_profit.net_profit = net_profit
            monthly_profit.save()
        
        # Create partner payouts
        partners = Partner.objects.filter(ship=ship, is_active=True)
        total_share_percentage = sum(partner.share_percentage for partner in partners)
        
        # Clear existing payouts
        PartnerPayout.objects.filter(monthly_profit=monthly_profit).delete()
        
        payouts = []
        for partner in partners:
            if total_share_percentage > 0:
                share_amount = (net_profit * partner.share_percentage) / total_share_percentage
            else:
                share_amount = 0
                
            payout = PartnerPayout.objects.create(
                partner=partner,
                monthly_profit=monthly_profit,
                share_amount=share_amount
            )
            payouts.append(payout)
        
        return {
            'monthly_profit_id': monthly_profit.id,
            'ship': ship.name,
            'month': start_date.strftime('%B %Y'),
            'total_income': float(total_income),
            'total_expenses': float(total_expenses),
            'net_profit': float(net_profit),
            'payouts_created': len(payouts)
        }
        
    except Ship.DoesNotExist:
        raise Exception("Ship not found")
    except Exception as e:
        raise Exception(f"Error calculating profit: {str(e)}")

def get_daily_income_report(date=None):
    """Get daily income summary for all ships"""
    if not date:
        date = timezone.now().date()
    
    ships = Ship.objects.filter(is_active=True)
    report = []
    
    for ship in ships:
        daily_income = DailyIncome.objects.filter(
            ship=ship,
            date=date
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        report.append({
            'ship_name': ship.name,
            'date': date,
            'total_income': float(daily_income)
        })
    
    return report