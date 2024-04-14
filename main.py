from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.utils import platform

from plyer import gps
import requests
import json

class LocationTrackerApp(App):

    def build(self):
        self.label = Label(text="Esperando ubicación...")
        Clock.schedule_interval(self.get_location, 10)  # Llama a get_location cada 10 segundos
        return self.label

    def get_location(self, dt):
        if platform == 'android':
            gps.configure(on_location=self.on_location)
            gps.start(minTime=1000, minDistance=0)
        else:
            self.label.text = "La aplicación solo funciona en Android"

    def on_location(self, **kwargs):
        latitude = kwargs['lat']
        longitude = kwargs['lon']
        self.label.text = f"Latitud: {latitude}\nLongitud: {longitude}"
        
        # Guardar la ubicación en la base de datos
        self.save_location(latitude, longitude)

    def save_location(self, latitude, longitude):
        payload = {
            "dispositivo": "moto x (2013)",
            "latitud": str(latitude),
            "longitud": str(longitude)
        }
        url = "https://g9d479bf6d1f16a-wqyj6jbtcf3qgx2m.adb.sa-santiago-1.oraclecloudapps.com/ords/campo/ubi/cargar"
        
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                print("Datos enviados correctamente")
            else:
                print(f"Error al enviar datos. Código de estado: {response.status_code}")
        except Exception as e:
            print(f"Error al enviar datos: {e}")

if __name__ == '__main__':
    LocationTrackerApp().run()
