# EVE
Eve is a cli tool to bring together all my utilities into a centralised place.

## Tutorials
Follow my YouTube tutorial series to follow along making this program.

[![Youtube video series](/media/Thumbnail.jpg)](https://www.youtube.com/channel/UCQCjA6qUutAtWqkCA4Z36CQ)

## How to Install
1. `git clone https://github.com/IVIURRAY/yt-eve.git`
2. `cd eve`
3. `pip install .`
4. `eve [cmd]` See [API](#API) section for commands to run.

## Configuration
There is a [`config.py`](/eve/config.py) that can be customised to support different use cases.

Override the relevant variables to fit your usecase.

**DO NOT COMMIT SENSITIVE ANY INFORMATION!**
 
# API
Below is a list of the currently support API command you can run.

* [`eve weather`](#weather) - Weather information.

## Weather
The weather API uses [OpenWeatherMap](https://openweathermap.org/) under the hood.
It is intended to be used for querying and viewing weather information. 
Below, is a list of currently supported endpoints.

___options___
* `-l` `--location` - override the default location. `eve weather -l <mytown> current`



```commandline
Usage: eve weather [OPTIONS] COMMAND [ARGS]...

  Weather Information

Options:
  -l, --location TEXT  Weather at this location.
  --help               Show this message and exit.

Commands:
  current   Current weather at a location
  forecast  Forecast for a location
```

***`current`***

The current endpoint gives you information for weather at a location right now.

```commandline
$ eve weather current
========= London GB - BROKEN CLOUDS =========
🔥 Temp: 22.84 - 21.67/23.89 (min/max)
🌪 Wind: 12.8
💧 Rain: {}
🌕 Sunrise: 05:08 - Sunset: 20:08 🌑
```

***`forecast`***

The forecast endpoint displays weather for the upcoming days.

```commandline
$ eve weather  forecast
================================= London GB =================================
📅 Date:  Sat 1 Aug     Sun 2 Aug     Mon 3 Aug     Tue 4 Aug     Wed 5 Aug   
🔥 Temp:    23.49         21.57          21.1         15.81         21.98     
🌪 Wind:     9.24          9.64          7.96          8.77          12.8     
💧 Rain:      {}            {}            {}            {}            {}   
```
