from django.http import HttpResponse
import csv
import plotly.graph_objs as go
from django.shortcuts import render, redirect
from tuya_connector import TuyaOpenAPI
import datetime
from .models import data
from django.http import JsonResponse
import json
from power_consumption_app.models import data

ACCESS_ID = "xxxx"
ACCESS_KEY = "xxxx"
API_ENDPOINT = "https://openapi.tuyaeu.com"

file_path = 'C:/Users/Naf_Second/Downloads/407/monday/cur_power_data.csv'


def power(request):
    x_data = []
    y_data = []
    hover_text = []
    total_power = 0
    datas = data.objects.all()
    for m in datas:
         x_data.append(m.timestamp)
         y_data.append(float(m.power))
         hover_text.append(f"Current: {m.power}")
            
    for y in y_data:
        total_power += y
    x_data_json = json.dumps(x_data)
    y_data_json = json.dumps(y_data)
    return render(request, 'power.html', {'x_data_json': x_data_json, 'y_data': y_data, 'hover_text': hover_text})

def voltage(request):
    x_data = []
    y_data = []
    hover_text = []
    total_voltage = 0
    datas = data.objects.all()
    for m in datas:
         x_data.append(m.timestamp)
         y_data.append(float(m.voltage))
         hover_text.append(f"Current: {m.voltage}")
            
    for y in y_data:
        total_voltage += y
    x_data_json = json.dumps(x_data)
    y_data_json = json.dumps(y_data)
    return render(request, 'voltage.html', {'x_data': x_data, 'y_data': y_data, 'hover_text': hover_text})


def elec_con(request):
    x_data = []
    y_data = []
    hover_text = []
    total_con = 0
    cost = 0
    datas = data.objects.all()
    for m in datas:
         x_data.append(m.timestamp)
         y_data.append(float(m.electricity))
         hover_text.append(f"Current: {m.electricity}")
            
    for y in y_data:
        total_con += y
    cost = 6.5*(total_con/1000)
    x_data_json = json.dumps(x_data)
    y_data_json = json.dumps(y_data)
    return render(request, 'electricity.html', {'x_data_json': x_data_json, 'y_data': y_data, 'hover_text': hover_text,'total_con':total_con,'cost':cost})


def home(request):
    x_data = []
    y_data = []
    a_data = []
    b_data = []
    hover_text = []
    hover_text2 = []
    hover_text3 = []
    total_voltage = 0
    total_current = 0
    energy = 0
    
    datas = data.objects.all()
    
    for m in datas:
            x_data.append(m.timestamp)
            fx = float(m.voltage)
            y_data.append(fx/10)
            fy = float(m.electricity)
            a_data.append(float(m.current))
            b_data.append(fy/100)
            hover_text.append(f"Voltage: {fx/10}")
            hover_text2.append(f"Power: {fy/100}")
            hover_text3.append(f"Current: {m.current}")

    for y in y_data:
        total_voltage += y
    for a in a_data:
        total_current += a
    for b in b_data:
        energy += b
    total_voltage = total_voltage / 10
    total_cost = 7*(energy/1000)
    energy = energy/1000
    total_current = total_current/1000
    context = {
        'x_data': x_data,
        'y_data': y_data,
        'a_data': a_data,
        'b_data': b_data,
        'hover_text': hover_text,
        'total_voltage': total_voltage,
        'total_current': total_current,
        'energy': energy,
        'hover_text2': hover_text2,
        'hover_text3': hover_text3,
        'total_cost' : total_cost,
    }
    
    return render(request, 'homepage.html', context)



def database(request):
    rows_to_delete = []

    datas = data.objects.all()

    for m in datas:
        if m.power == '0':
            rows_to_delete.append(m)

    for row in rows_to_delete:
        row.delete()

    return HttpResponse("Complete")

def query(request):
     datas = data.objects.all()  # Retrieve all Album objects from the database

     return render(request, 'database.html', {'datas': datas})



def get_power_data2(request):
    openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
    openapi.connect()
    
    try:
        response = openapi.get('/v1.0/iot-03/devices/status?device_ids=xxxxx')
        
        currentconsumption = response['result'][0]['status'][2]
        currentcurrent = response['result'][0]['status'][3]
        currentpower = response['result'][0]['status'][4]
        currentvoltage = response['result'][0]['status'][5]
        current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        power = currentpower['value']
        current = currentcurrent['value']
        voltage = currentvoltage['value']
        consumption = currentconsumption['value']

        # Constructing the absolute path to the CSV file
        # Replace with the absolute path

        # Save data to database
        datas = data(
            power=power,
            voltage=voltage,
            current=current,
            electricity=consumption,
            timestamp=current_time
        )
        datas.save()

        # Prepare data for sending back to the client
        x_data = current_time  # Change this based on what you want to use for X-axis (time, timestamp, etc.)
        y_data = float(power)
        hover_text = f"Voltage: {power}"

        # Return the data as JSON response
        return JsonResponse({'x_data': x_data, 'y_data': y_data, 'hover_text': hover_text})
    
    except Exception as e:
        return JsonResponse({'status': 'error'})
