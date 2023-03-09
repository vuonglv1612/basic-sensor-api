# Basic Sensor API

## Introduction
This is a basic sensor API that allows you to update a sensor and then read the sensor data. The sensor data is stored in redis and can be read by the API.

## Installation
To install the API, you need to have redis installed and running. You can install redis by following the instructions on the [redis website](http://redis.io/download).

Once you have redis installed, you can install the API by running the following commands:

```bash
git clone https://github.com/vuonglv1612/basic-sensor-api.git
cd basic-sensor-api
python3.9 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

## Usage
### Update a sensor metric
To update a sensor metric, you need to send a POST request to the `/api/metrics` endpoint with the following JSON body:

```json
{
    "sensor": "sensor1",
    "humidity": 70,
    "temperature_c": 24
}
```

Example cURL request:

```bash
curl --location --request POST 'http://localhost:8000/api/metrics?sensor=sensor1&humidity=70&temperature_c=24'
```

### Read a sensor metric
To read a sensor metric, you need to send a GET request to the `/api/metrics` endpoint with the following query parameters:

```json
{
    "sensor": "sensor1"
}
```

Example cURL request:

```bash
curl --location 'http://localhost:8000/api/metrics?sensor=sensor1'
```

