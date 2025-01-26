from pyexpat.errors import messages
import paho.mqtt.client as mqtt
import threading
from django.core.mail import send_mail
from django.utils.timezone import now as timezone_now
from time import localtime
import paho.mqtt.client as mqtt
import json
from django.http import JsonResponse
from django.utils import timezone
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from myapp.models import *
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .models import User



def login_p(request):
    return render(request,'login_p.html')

def index(request):
    return render(request,'index.html')

def index_d(request):
    return render(request,'index_d.html')



def medical_history_d(request):

    return render(request,'medical_history_d.html')


def sign_up(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        gender = request.POST['gender']
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('login_p')
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('login_p')
       
        # Create and save the user
        user = User(name=name, email=email, gender=gender, username=username, password=password)
        user.save()

        return HttpResponse('<script>alert("signup sucessfull! now you can login"); window.location.href="/login_p/";</script>')



    return render(request, 'login_p.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        print(username)
        password = request.POST['password']
        print(password)

        # Check if the username is 'Doctor' and the password is 'Doctor@098'
        if username == "Doctor" and password == "Doctor@098":
            request.session['username'] = username
            return render(request, 'index_d.html')

        try:
            # Try to fetch the user by username
            user = User.objects.get(username=username)
            
            if user.password == password:  # Compare plain-text password
                request.session['username'] = username
                initialize_mqtt(request)
                
                return HttpResponse('<script>alert("Login successful"); window.location.href="/index/";</script>')
            else:
                # Invalid password
                return HttpResponse('<script>alert("Invalid credentials"); window.location.href="/login_p/";</script>')
        
        except User.DoesNotExist:
            # User not found
            return HttpResponse('<script>alert("User not found"); window.location.href="/login_p/";</script>')

    return render(request, 'login_p.html')


def request_send(request):
    if request.method == "POST":
        # Get the username from the session
        username = request.session.get('username')
        
        if not username:
            return HttpResponse('<script>alert("Session expired. Please log in again."); window.location.href="/login/";</script>')

        current_time = localtime(now()).replace(microsecond=0)  # Use full datetime here

        # Check for duplicate time
        if VideoConsultationRequest.objects.filter(request_time=current_time).exists():
            return HttpResponse('<script>alert("Request with the current time already exists!"); window.history.back();</script>')

        # Save the request in the database
        VideoConsultationRequest.objects.create(username=username, request_time=current_time)

        return HttpResponse('<script>alert("Request submitted successfully!"); window.location.href="/video_consultation_user";</script>')

    return HttpResponse('<script>alert("Invalid request method."); window.history.back();</script>')



def video_consultation_requests(request):
    consultation_requests = VideoConsultationRequest.objects.all()
    print(consultation_requests)

    # Pass the consultation requests to the template
    return render(request, 'video_consultation_doctor.html', {
        'consultation_requests': consultation_requests
    })


def send_link(request, request_id):
    consultation_request = get_object_or_404(VideoConsultationRequest, id=request_id)
    
    if request.method == "POST":
        # Default Google Meet URL
        gmeet_url = "https://meet.google.com/iyp-sbtj-gyu"  # Your default URL

        VideoConsultation.objects.create(
            request=consultation_request,
            gmeet_url=gmeet_url,
            username=consultation_request.username,
            request_time=consultation_request.request_time
        )


        return redirect(gmeet_url)
        
 
    return render(request, 'video_consultation_doctor.html', {'consultation_request': consultation_request})

def reject_request(request, request_id):
    # Fetch the consultation request by ID
    consultation_request = get_object_or_404(VideoConsultationRequest, id=request_id)
    
    if request.method == "POST":
        # Delete the consultation request
        consultation_request.delete()
        return HttpResponse('<script>alert("Request Rejected Successfully!"); window.location.href="/video_consultation_requests/";</script>')

    # If GET request (not really needed in this case, but you can add logic for it if needed)
    return HttpResponse('<script>alert("Invalid Request Method!"); window.location.href="/video_consultation_requests/";</script>')

def video_consultation_user(request):
    username = request.session.get('username')
    print(username)
    
    video_consultation = VideoConsultation.objects.filter(username=username).first()
    
    print(video_consultation)  # Debugging line to check if data is fetched correctly.
    
    return render(request, 'video_consultation_user.html', {
        'video_consultation': video_consultation,
    })


def signout(request):

    request.session.flush()  
    return redirect('login_p')


def prescription_d(request):
    users = User.objects.all()
    print(users)
    return render(request,'prescription_d.html', {'users': users})


def upload_prescription(request):
    if request.method == 'POST':
        patient_username = request.POST.get('username')  # Patient's username
        disease_name = request.POST.get('disease_name')
        medicine = request.POST.get('medicine')
        description = request.POST.get('description')

        # Find the user's email based on the username
        try:
            patient = User.objects.get(username=patient_username)
        except User.DoesNotExist:
            return HttpResponse('<script>alert("Patient not found!"); window.location.href="/prescription_d/";</script>')

        # Save prescription to the database
        Prescription.objects.create(
            patient_name=patient_username,
            disease_name=disease_name,
            medicine=medicine,
            description=description
        )

        # Send an email to the patient
        subject = "Your Prescription Details"
        message = f"""
        Hello {patient.name},

        Your prescription details have been uploaded:

        Disease: {disease_name}
        Medicine: {medicine}
        Description: {description}

        Please follow up as advised.

        Regards,
        Medireach Team
        """
        from_email = 'medireachog@gmail.com'  
        recipient_list = [patient.email]

        try:
            send_mail(subject, message, from_email, recipient_list)
            alert_message = "Prescription uploaded successfully and email sent to the patient!"
        except Exception as e:
            alert_message = f"Prescription uploaded, but email could not be sent: {str(e)}"

        return HttpResponse(f'<script>alert("{alert_message}"); window.location.href="/prescription_d/";</script>')
    
    return render(request, 'prescription_d.html')


def prescription_view(request):
  
    username = request.session.get('username')

    # Retrieve the latest prescription for the user
    latest_prescription = None
    if username:
        latest_prescription = Prescription.objects.filter(patient_name=username).order_by('-created_at').first()
        print(latest_prescription)

    return render(request, 'prescription.html', {
        'latest_prescription': latest_prescription,
        'username': username,
    })

def profile_view(request):
    user = request.session.get('username')
    user = User.objects.get(username=user)  # Fetch the user data
    
    if request.method == 'POST':
        # If the form is submitted, update the user's details
        name = request.POST.get('name')
        email = request.POST.get('email')
        gender = request.POST.get('gender')

        # Update the user's details
        user.name = name
        user.email = email
        user.gender = gender
        user.save()  

        return redirect('profile_view')  

    context = {
        'username': user.username,
        'name': user.name,
        'email': user.email,
        'gender': user.gender,
    }

    return render(request, 'profile.html', context)



# Global variables
received_data = {}
session_username = None  

# MQTT Configuration
MQTT_HOST = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_CLIENT_NAME = "Test"
MQTT_CLIENT_ID = "86bc7458-060f-4d7b-bfe0-ff8b2018d0f9"
MQTT_TOPIC = "remote001"

# The callback function when the message is received
def on_message(client, userdata, message):
    global received_data, session_username
    print("Message received")
    
    # Decode the message payload
    payload = message.payload.decode("utf-8")
    print(f"Decoded payload: {payload}")

    # Parse payload manually for non-JSON messages
    try:
        key, value = payload.split(":", 1)
        key = key.strip()
        value = value.strip()
        # Handle units if present
        if "deg. farenheit" in value:
            value = value.replace("deg. farenheit", "").strip()
        received_data[key] = value
        print(f"Updated received_data: {received_data}")
    except ValueError:
        print(f"Failed to parse payload: {payload}")
        return


    required_keys = {"SPO2", "Temperature", "Heart rate", "Systolic pressure", "Diastolic pressure"}
    if required_keys.issubset(received_data.keys()):
       
        received_data["timestamp"] = timezone.now()


        sensor_data = sensordata.objects.create(
            username=session_username,
            temperature=received_data.get("Temperature"),
            spo2=received_data.get("SPO2"),
            heart_rate=received_data.get("Heart rate"),
            systolic_pressure=received_data.get("Systolic pressure"),
            diastolic_pressure=received_data.get("Diastolic pressure"),
            timestamp=received_data["timestamp"],
        )
        print(f"Sensor data saved: {sensor_data}")
        
        received_data.clear()
    else:
        print("Not all required data received yet. Waiting for more messages.")


def initialize_mqtt(request):
    global session_username

    # Fetch username from the session
    session_username = request.session.get('username')
    print(f"Session username set: {session_username}")

    # Create and configure the MQTT client
    client = mqtt.Client()
    client.username_pw_set(username=None, password=None)

    # Define the callbacks
    client.on_message = on_message

    # Connect to the broker
    client.connect(MQTT_HOST, MQTT_PORT, 60)
    print(f"Connected to MQTT broker at {MQTT_HOST}:{MQTT_PORT}")

    # Subscribe to the topic
    client.subscribe(MQTT_TOPIC)
    print(f"Subscribed to topic {MQTT_TOPIC}")

    # Start the MQTT loop
    client.loop_start()
    print("Started MQTT loop in background")

    return JsonResponse({"message": "MQTT initialized and listening to messages."})

# Django view function
def get_sensor_data(request):
    global received_data
    print(f"get_sensor_data called. Current received_data: {received_data}")

    if not received_data:
        print("No data available to send.")
        return JsonResponse({"error": "No sensor data available"}, status=404)

    response = JsonResponse(received_data)
    print(f"Response sent: {response.content}")
    return response



def medical_history(request):
    
    return render(request,'medical_history.html')


def live_sensor_data(request):
    
    username = request.session.get('username')
    print(username)
    sensor_data = sensordata.objects.filter(username=username).latest('timestamp') 
    
    # Prepare the data to be sent back as JSON
    data = {
        'Temperature': sensor_data.temperature,
        'Heart rate': sensor_data.heart_rate,
        'SPO2': sensor_data.spo2,
        'Systolic pressure': sensor_data.systolic_pressure,
        'Diastolic pressure': sensor_data.diastolic_pressure,
    }
    print(data)
    return JsonResponse(data)


def get_history_data(request):
  
    username = request.session.get('username')

    print(username)
    
    history_data =  sensordata.objects.filter(username=username).order_by('-timestamp')[:10] 
    
    # Prepare the data for the chart
    data = {
        'Temperature': [entry.temperature for entry in history_data],
        'Systolic pressure': [entry.systolic_pressure for entry in history_data],
        'Diastolic pressure': [entry.diastolic_pressure for entry in history_data],
        'Heart rate': [entry.heart_rate for entry in history_data],
        'SPO2': [entry.spo2 for entry in history_data],
    }
    print(data)
    
    return JsonResponse(data)



def live_sensor_data_d(request, username):
   
        # Fetch the latest sensor data for the specified username
        sensor_data = sensordata.objects.filter(username=username).latest('timestamp')
        
        
        # Prepare the data to be sent back as JSON
        data = {
            'Temperature': sensor_data.temperature,
            'Heart rate': sensor_data.heart_rate,
            'SPO2': sensor_data.spo2,
            'Systolic pressure': sensor_data.systolic_pressure,
            'Diastolic pressure': sensor_data.diastolic_pressure,
        }
        print(data)
        return JsonResponse(data)


def get_history_data_d(request, username):

        history_data = sensordata.objects.filter(username=username).order_by('-timestamp')[:10]
        print(history_data)

        data = {
            'Dates': [entry.timestamp for entry in history_data],
            'Temperature': [entry.temperature for entry in history_data],
            'Systolic pressure': [entry.systolic_pressure for entry in history_data],
            'Diastolic pressure': [entry.diastolic_pressure for entry in history_data],
            'Heart rate': [entry.heart_rate for entry in history_data],
            'SPO2': [entry.spo2 for entry in history_data],
        }
        print(data)
        return JsonResponse(data)


def get_users(request):
   
    usernames = sensordata.objects.values_list('username', flat=True).distinct()
    print(usernames)
    return JsonResponse(list(usernames), safe=False)
  



########################################################


# Forgot password form handler
def forgot_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = User.objects.get(username=username)
            # Pass username to the template and indicate that modal should be shown
            return render(request, 'login_p.html', {'username': username, 'show_update_password_modal': True})
        except User.DoesNotExist:
            messages.error(request, "Username not found.")
            return redirect('login_p')
    return render(request, 'login_p.html')  


def update_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            return HttpResponse(f'<script>alert("Password does not match!"); window.location.href="/login_p/";</script>')

        try:
            user = User.objects.get(username=username)
            user.password = new_password 
            user.save()
            return HttpResponse(f'<script>alert("Password reset successfully!"); window.location.href="/login_p/";</script>')
        except User.DoesNotExist:
            messages.error(request, "Username not found.")
            return redirect('login_view')
    return redirect('login_view')

