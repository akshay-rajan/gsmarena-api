from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import BrandSerializer, DeviceSerializer, DeviceDetailSerializer
from bs4 import BeautifulSoup
import httpx
import asyncio

async def getDataFromUrl(url):
    headers = {
        "Referer": "https://www.google.com/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Chrome/W.X.Y.Z Safari/537.36"
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(f'https://www.gsmarena.com{url}', headers=headers, timeout=(None, None))
        return response.text

async def getBrands():
    response = await getDataFromUrl('/makers.php3')
    soup = BeautifulSoup(response, 'html.parser')
    brands_data = []
    brands = soup.find_all('table')[0].find_all('td')
    for element in brands:
        links = element.find('a')
        spans = element.find('span')
        brands_data.append({
            'id': links['href'].replace('.php', ''),
            'name': links.get_text(strip=True).replace(' devices', '').replace('[0-9]', ''),
            'devices': int(spans.get_text(strip=True).replace(' devices', ''), 10),
        })
    return brands_data

def getNextPage(soup):
    nextPageUrl = soup.select_one('a.pages-next')
    if nextPageUrl:
        nextPage = nextPageUrl['href']
        if '#' in nextPage:
            return False
        return "/" + nextPage
    return False

def getDevices(soup, devices_list):
    devices = []
    for device in devices_list:
        img = device.find('img')
        name = device.find('span').contents
        fullname = f"{name[0]} {name[-1]}"
        devices.append({
            'id': device.find('a')['href'].replace('.php', ''),
            'name': fullname,
            'img': img['src'],
            'description': img['title'],
        })
    return devices

async def getBrand(brand):
    response = await getDataFromUrl(f"/{brand}.php")
    soup = BeautifulSoup(response, 'html.parser')
    brand_data = []

    devices = getDevices(soup, soup.select('.makers li'))
    brand_data.extend(devices)
    while getNextPage(soup):
        nextPageUrl = getNextPage(soup)
        nextPage = await getDataFromUrl(nextPageUrl)
        soup = BeautifulSoup(nextPage, 'html.parser')
        devices = getDevices(soup, soup.select('.makers li'))
        brand_data.extend(devices)

    return brand_data

async def getDevice(device):
    url = f'/{device}.php'
    html = await getDataFromUrl(url)
    soup = BeautifulSoup(html, 'html.parser')

    try:
        display_size = soup.find('span', {'data-spec': 'displaysize-hl'}).text
        display_res = soup.find('div', {'data-spec': 'displayres-hl'}).text
        camera_pixels = soup.find('span', {'data-spec': 'camerapixels-hl'}).text
        video_pixels = soup.find('div', {'data-spec': 'videopixels-hl'}).text
        ram_size = soup.find('span', {'data-spec': 'ramsize-hl'}).text
        chipset = soup.find('div', {'data-spec': 'chipset-hl'}).text
        battery_size = soup.find('span', {'data-spec': 'batsize-hl'}).text
        battery_type = soup.find('div', {'data-spec': 'battype-hl'}).text
        popularity_percentage = soup.find('li', class_='light pattern help help-popularity').find('strong').get_text(strip=True)
    except:
        return {
            'name': '',
            'img': '',
            'quick_spec': '',
            'detail_spec': '',
            'pricing': '',
            'popularity': '' 
        }
    try:
        popularity = float(popularity_percentage.rstrip("%"))
    except ValueError:
        popularity = 0.0

    quick_spec = [
        {'name': 'Display size', 'value': display_size},
        {'name': 'Display resolution', 'value': display_res},
        {'name': 'Camera pixels', 'value': camera_pixels},
        {'name': 'Video pixels', 'value': video_pixels},
        {'name': 'RAM size', 'value': ram_size},
        {'name': 'Chipset', 'value': chipset},
        {'name': 'Battery size', 'value': battery_size},
        {'name': 'Battery type', 'value': battery_type},
    ]

    name = soup.find('h1', {'class': 'specs-phone-name-title'}).text
    img = soup.find('div', {'class': 'specs-photo-main'}).find('img').get('src')

    detail_spec = []
    spec_nodes = soup.find_all('table', class_='pricing')

    pricing = []
    for spec_node in spec_nodes:
        spec_list = []
        category = spec_node.find('th')
        if category is not None:
            category = category.text
            spec_items = spec_node.find_all('tr')

            for spec_item in spec_items:
                spec_list.append({
                    'name': spec_item.find('td', {'class': 'ttl'}).text,
                    'value': spec_item.find('td', {'class': 'nfo'}).text,
                })

            if category:
                detail_spec.append({
                    'category': category,
                    'specifications': spec_list,
                })
        else:
            variants = spec_node.find_all('tr')
            for variant in variants:
                price = [
                    {'variant': variant.find('td').text},
                    {'price': variant.find('a').text},
                    {'site_img_url': variant.find('img')['src']},
                ]
                pricing.append(price)

    return {
        'name': name,
        'img': img,
        'quick_spec': quick_spec,
        'detail_spec': detail_spec,
        'pricing': pricing,
        'popularity': popularity        
    }

# @api_view(['GET'])
# async def brands_list(request):
#     brands = await getBrands()
#     serializer = BrandSerializer(brands, many=True)
#     return Response(serializer.data)

# @api_view(['GET'])
# async def brand_devices(request, brand_id):
#     devices = await getBrand(brand_id)
#     serializer = DeviceSerializer(devices, many=True)
#     return Response(serializer.data)

# @api_view(['GET'])
# async def device_detail(request, device_id):
#     device = await getDevice(device_id)
#     serializer = DeviceDetailSerializer(device)
#     return Response(serializer.data)

@api_view(['GET'])
def brands_list(request):
    brands = asyncio.run(getBrands())  # Await the coroutine in a synchronous context
    serializer = BrandSerializer(brands, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def brand_devices(request, brand_id):
    devices = asyncio.run(getBrand(brand_id))
    serializer = DeviceSerializer(devices, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def device_detail(request, device_id):
    device = asyncio.run(getDevice(device_id))
    serializer = DeviceDetailSerializer(device)
    return Response(serializer.data)
