# GSMArena API

Fetches smartphone specifications from [gsmarena](https://www.gsmarena.com) website and returns the result as JSON objects.


## Usage

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
