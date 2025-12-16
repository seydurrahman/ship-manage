from django.http import JsonResponse

def home(request):
    return JsonResponse({
        "status": "success",
        "message": "Ship Finance API Running",
        "endpoints": {
            "admin": "/admin/",
            "api": "/api/"
        }
    })
