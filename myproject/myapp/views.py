from rest_framework.decorators import api_view
from rest_framework.response import Response
from bs4 import BeautifulSoup
import requests
from typing import Optional
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@api_view(["GET"])
def scrape_data(request):
    # Extract the URL parameter
    scrape_url = request.query_params.get("scrape_url")
    if not scrape_url:
        return JsonResponse({"error": "scrape_url parameter is required"}, status=400)
    
    head = []
    rows = []

    def scrape_page(soup):
        rows_ele = soup.find_all('tr')
        for row in rows_ele:
            td = row.find_all('td')  # Find all <td> elements in the current row
            th = row.find_all('th')  # Find all <th> elements in the current row

            arr = []
            for cell in td:
                cell_text = cell.get_text(strip=True)
                arr.append(cell_text)
            rows.append(arr)

            for cell in th:
                head.append(cell.get_text(strip=True))

    # Request the URL
    headers = {
        'User-Agent': 'curl/7.68.0'
    }

    try:
        response = requests.get(scrape_url, headers=headers, verify=False)
        response.raise_for_status()
    except requests.RequestException as e:
        return JsonResponse({"error": str(e)}, status=400)

    soup = BeautifulSoup(response.text, 'html.parser')
    scrape_page(soup)

    # Return the scraped data
    return Response({"columns": head, "rows": rows})

# url = 'https://results.eci.gov.in/AcResultGenOct2024/partywisewinresult-834U08.htm'


