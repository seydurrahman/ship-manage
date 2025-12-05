from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'ships', views.ShipViewSet)
router.register(r'partners', views.PartnerViewSet)
router.register(r'projects', views.ProjectViewSet)
router.register(r'incomes', views.DailyIncomeViewSet)
router.register(r'expenses', views.ExpenseViewSet)
router.register(r'profits', views.MonthlyProfitViewSet)
router.register(r'payouts', views.PartnerPayoutViewSet)

urlpatterns = [
    path('', include(router.urls)),    # ✅ FIXED — remove "api/"
]
