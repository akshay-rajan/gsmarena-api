# GSMArena API

Fetch smartphone specifications from [gsmarena.com](https://www.gsmarena.com) using `BeautifulSoup`.

The project has two parts:
#### 1. [scrape.py](./README.md#scrapepy): A python file containing functions for scraping the website.
#### 2. [API](./README.md#django-rest-api): An API that fetch data from the website, built using the Django REST Framework.

> This project was done as part of the final project for the Harvard's CS50 Web Programming with Python and JavaScript course, to learn about web scraping and APIs.

## Usage

1. Clone the repository:

  ```bash
  git clone https://github.com/akshay-rajan/gsmarena-api.git
  ```

2. Install the requirements:

  ```bash
  pip install -r requirements.txt
  ```

3. Start the development server at http://127.0.0.1:8000/ :
  ```bash
  cd restapi
  python3 manage.py runserver
  ```
4. Now you can access the API by sending HTTP requests [like this](README.md#django-rest-api).


## [scrape.py](./scrape.py)

This file contains all the functions used for scraping *gsmarena.com*.


### `getDataFromUrl(url)`
- Description: Returns the source of a page.
- Parameters:
  - `url` (str): The URL of the page to retrieve data from.
- Returns:
  - str: The source of the page.

### `getBrands()`
- Description: Returns all brands as JSON objects in a list.
- Returns:
  - list: A list of JSON objects representing brands, each with keys `id`, `name`, and `devices`.

### `getNextPage(soup)`
- Description: If a 'next page' exists, returns it.
- Parameters:
  - `soup` (BeautifulSoup): The BeautifulSoup object representing the current page.
- Returns:
  - str: The URL of the next page if it exists, else False.

### `getDevices(soup, devices_list)`
- Description: Returns a refined list of devices as JSON objects.
- Parameters:
  - `soup` (BeautifulSoup): The BeautifulSoup object representing the current page.
  - `devices_list` (list): A list of devices to extract information from.
- Returns:
  - list: A list of JSON objects representing devices, each with keys `id`, `name`, `img`, and `description`.

### `getBrand(brand)`
- Description: Returns all devices of a particular brand.
- Parameters:
  - `brand` (str): The brand name.
- Returns:
  - list: A list of JSON objects representing devices of the brand.

### `getDevice(device)`
- Description: Scrapes a page of a particular device.
- Parameters:
  - `device` (str): The device name.
- Returns:
  - dict: A dictionary representing the device with keys `name`, `img`, `quick_spec`, `detail_spec`, `pricing`, and `popularity`.

## DJANGO REST API

A REST API A REST API built using the Django REST Framework that fetches data from *gsmarena.com*.

- http://localhost:8000/api/brands/: Get the list of brands.
  ```
  http://127.0.0.1:8000/api/brands/
  ```
- http://localhost:8000/api/brands/<brand_id>/devices/: Get devices of a particular brand.
  ```
  http://127.0.0.1:8000/api/brands/samsung-phones-9/devices/
  ```
- http://localhost:8000/api/devices/<device_id>/: Get details of a particular device.
  ```
  http://127.0.0.1:8000/api/devices/samsung_galaxy_z_fold6-13147/
  ```
