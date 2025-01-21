from django.shortcuts import render
from .tasks import sendEmail
from django.http import HttpResponse, JsonResponse
from django.core.cache import cache
from django.views.decorators.cache import cache_page


# Create your views here.
def send_email(request):
    sendEmail.delay()
    return HttpResponse("<h1>Done Sending</h1>")


"""@cache_page(60)
def test(request):
    response = requests.get(
        "https://b0334311-3948-4555-af18-17d55a318926.mock.pstmn.io/test/delay/5"
    )
    return JsonResponse(response.json())"""