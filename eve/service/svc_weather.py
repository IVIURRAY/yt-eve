from pyowm import OWM

from eve.config import WX_API_KEY, WX_LOCATION, WX_METRIC_TEMP, WX_METRIC_WIND


class Weather:
    def __init__(self, api_key=None, metric_temp=None, metric_wind=None):
        self.manager = OWM(api_key or WX_API_KEY).weather_manager()
        self.default_location = WX_LOCATION
        self.metric_temp = metric_temp or WX_METRIC_TEMP
        self.metric_wind = metric_wind or WX_METRIC_WIND

    def get_weather_data(self, weather):
        return {
            "max": weather.temperature(self.metric_temp)["temp_max"],
            "min": weather.temperature(self.metric_temp)["temp_min"],
            "temp": weather.temperature(self.metric_temp)["temp"],
            "wind": weather.wind(self.metric_wind)["speed"],
            "status": weather.detailed_status,
            "sun_rise": weather.srise_time,
            "sun_set": weather.sset_time,
            "rain": weather.rain,
            "time": weather.ref_time,
        }

    def current(self, location=None):
        observation = self.manager.weather_at_place(location or self.default_location)
        weather = observation.weather

        result = self.get_weather_data(weather)
        result["location"] = f"{observation.location.name} {observation.location.country}"

        return result

    def forecast(self, location=None, interval="3h"):
        forecaster = self.manager.forecast_at_place(location or self.default_location, interval)
        location = f"{forecaster.forecast.location.name} {forecaster.forecast.location.country}"
        return [
            {**self.get_weather_data(weather), **{"location": location}} for weather in forecaster.forecast.weathers
        ]
