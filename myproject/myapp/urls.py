from django.urls import path
from .views import scrape_data

urlpatterns = [
    path('scrape/', scrape_data, name="scrape_data"),
]


# url = 'https://results.eci.gov.in/AcResultGenOct2024/partywisewinresult-834U08.htm'
