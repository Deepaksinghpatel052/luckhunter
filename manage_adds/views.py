from django.shortcuts import render,get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import LsAdds,LsAddsCategory
from .serializear import LsAddserializers
from django.http import HttpResponse, JsonResponse
from django.db.models import Q,Subquery,Count
# Create your views here.
@csrf_exempt
def index(request):
    data = {}
    status = "0"
    if LsAddsCategory.objects.filter(Status=True).filter(Category_keyword="home_page_header").exists():
        category = get_object_or_404(LsAddsCategory , Status=True,Category_keyword="home_page_header")
        if LsAdds.objects.filter(Pogition=category).filter(Status=True).exists():
            project_info =  get_object_or_404(LsAdds , Pogition=category,Status=True)
            project_info_sri = LsAddserializers(project_info)
            data = project_info_sri.data
            status = "1"
    return JsonResponse({"status": status,"data":data})