# EVE
Eve is a cli tool to bring together all my utilities into a centralised place.

## Tutorials
Follow my YouTube tutorial series to follow along making this program.

[![Youtube video series](/media/Thumbnail.jpg)](https://www.youtube.com/watch?v=Jr4QDJwwj60)

## How to Install
1. `git clone https://github.com/IVIURRAY/yt-eve.git`
2. `cd eve`
3. `pip install .`
4. `eve [cmd]` See [API](#API) section for commands to run.

### Testing
Run tests with `pytest` command

## How to Contribute
The EVE project welcomes all contributions!

1. Fork this repo.
2. Make a branch to put your changes on.
3. Add a file called `/eve/commands/cmd_<you_change>.py` and `/eve/service/svc_<your_change>.py`.
    * Plenty of examples to take from already in those directories.
    * Splitting CLI logic under `/cmd_<you_change>.py` and api logic under `/svc_<your_change>.py`.
3. Submit a PR explaining your change and what it does, with examples!
4. Thank you in advance :thumbsup: !!

## Configuration
In order to use all supported commands, you would need to provide your personal preferences/credentials.
There are two ways it can be done, see below.

1. Override default parameters in [`~/eve/config.py`](/eve/config.py) (**Do not commit these changes**)
`os.environ.get("ENV", "default")` reads the env var `"ENV"` and takes `"default"` if this variable is not set.

 config.py example
```
import os

# Weather API
WX_API_KEY = os.environ.get("WX_API_KEY", "e5209303a83828u2eako7c849302d2j2")
WX_LOCATION = os.environ.get("WX_LOCATION", "London")
WX_METRIC_TEMP = os.environ.get("WX_METRIC_TEMP", "celsius")
WX_METRIC_WIND = os.environ.get("WX_METRIC_WIND", "km_hour")

# Github API
GITHUB_USER = os.environ.get("GITHUB_USER", "johndoe")
GITHUB_PASS = os.environ.get("GITHUB_PASS", "superSecretPass")

# Tidy
TIDY_ROOT = os.environ.get("TIDY_ROOT", "/User/johndoe/Downloads")  # "</path/to/root>"

# Crypto
COIN_MARKET_CAP_API_KEY = os.environ.get("COIN_MARKET_CAP_API_KEY", "5i3qe43d-2de2-2eid-63b3-9403920395d2")
DEFAULT_COIN = os.environ.get("DEFAULT_COIN", "BTC")
CURRENCY = os.environ.get("CURRENCY", "GBP")

# Calendar
DEFAULT_EVENTS_NUMBER = os.environ.get("DEFAULT_EVENTS_NUMBER", "10")
PATH_TO_CRED = os.environ.get("PATH_TO_CALENDAR_API_CRED", "/Users/john/cred/credentials.json")
```
2. Set env variables in your shell.
For convenience, create `~/.eve_config` file with the following content, examples in the comments
```
# Weather API
export WX_API_KEY=you_personal_open_weather_api_key # e5209303a83828u2eako7c849302d2j2
export WX_LOCATION=your_preferred_default_location # London
export WX_METRIC_TEMP=your_preferred_temperature_units # celsius ( <celsius|fahrenheit|kelvin> )
export WX_METRIC_WIND=your_preferred_wind_units # km_hour ( <miles_hour|km_hour|knots> )

#Github API
export GITHUB_USER=your_github_username # johndoe
export GITHUB_PASS=your_github_password # supersecretpassword

# Tidy
export TIDY_ROOT="</path/to/root>" # /User/johndoe/Downloads

#Crypto
export COIN_MARKET_CAP_API_KEY=your_personal_coinmarket_cap_api_key # 5i3qe43d-2de2-2eid-63b3-9403920395d2
export DEFAULT_COIN=your_preferred_default_crypto_currency_symbol # BTC
export CURRENCY=your_preferred_default_currency_to_convert_to # EUR

#Calendar
export DEFAULT_EVENTS_NUMBER=10
export PATH_TO_CALENDAR_API_CRED="/Users/john/creds/credentials.json"
```

export env variables in this file on the startup of the shell.
Depending on what shell you use, add this line to `~/.zshrc`; `~/.bash_profile`, `etc`
```
source ~/.eve_config
```
restart your shell

# API
Below is a list of the currently support API commands.

* [`eve football`](#football) - Football results.
* [`eve github`](#github) - Github utilities.
* [`eve tidy`](#tidy) - Directory tidy.
* [`eve weather`](#weather) - Weather information.
* [`eve crypto`](#crypto) - Crypto currency information.
* [`eve cal`](#calendar) - Google calendar utility.
* [`eve quote`](#quote) - Generate random book-quotes.

## Football
The `football` command uses [openfootball](https://github.com/openfootball/football.json) under the hood.

It is intended to be used for viewing football result and table information.

Below, is a list of currently support commands.

```commandline
Usage: eve football [OPTIONS] COMMAND [ARGS]...

  Football results

Options:
  --help  Show this message and exit.

Commands:
  table  View a table
```

***`table`***

The table command can be used to view the current standing of a given league.
(Defaults to English Premier league).

```commandline
Usage: eve football table [OPTIONS]

  View a table

Options:
  -l, --league TEXT  The league to view - See codes at
                     https://github.com/openfootball/football.json

  --help             Show this message and exit.
```

___options___
* `-l` `--league` - a league code to view the table for. Defautls to `en.1`.

```commandline
$ eve football table -l en.1
Running Premier League 2020/21 table generator
 1st:            Everton FC           13 pts  7 gd
 2nd:           Liverpool FC          10 pts  0 gd
 3rd:          Aston Villa FC         9 pts   9 gd
 4th:        Leicester City FC        9 pts   5 gd
 5th:            Arsenal FC           9 pts   2 gd
 6th:            Chelsea FC           8 pts   4 gd
 7th:       Tottenham Hotspur FC      7 pts   7 gd
 8th:         Leeds United FC         7 pts   1 gd
 9th:        Manchester City FC       7 pts   0 gd
10th:          Southampton FC         7 pts  -1 gd
11th:        Crystal Palace FC        7 pts  -2 gd
12th:       Newcastle United FC       7 pts  -2 gd
13th:        West Ham United FC       6 pts   4 gd
14th:    Wolverhampton Wanderers FC   6 pts  -3 gd
15th:       Manchester United FC      6 pts  -3 gd
16th:    Brighton & Hove Albion FC    4 pts  -2 gd
17th:       Sheffield United FC       1 pts  -5 gd
18th:            Fulham FC            1 pts  -8 gd
19th:     West Bromwich Albion FC     1 pts  -8 gd
20th:            Burnley FC           0 pts  -5 gd
```

## Github
The `github` command uses [PyGithub](https://github.com/PyGithub/PyGithub) under the hood.

It is intended to be used for automating repetitive tasks around repository management.

Below, is a list of currently support commands.

```commandline
Usage: eve github [OPTIONS] COMMAND [ARGS]...

  Github utilities

Options:
  --help  Show this message and exit.

Commands:
  create  Create a github repo
  delete  Delete a github repo

```


***`create`***

The `create` command allows you to create a repository on Github.

```commandline
Usage: eve github create [OPTIONS] NAME

  Create a github repo

Options:
  -p, --private BOOLEAN  Is the repo private?
  -i, --gitignore TEXT   The .gitignore file to add to the repo
  --help                 Show this message and exit.
```

___options___
* `-p` `--private` - set the repository to private or not. `eve github create <name> -p <True|False>`. Default to `False`.
* `-i` `--gitignore` - initialise with a [`.gitignore`](https://github.com/github/gitignore) file. `eve github create <name> -i Python`

```commandline
$ eve github create test-repo -i Python

Created: test-repo at https://github.com/IVIURRAY/test-repo
Run the below command to add the repo as a remote...
git remote add origin https://github.com/IVIURRAY/test-repo.git
```

***`delete`***

The `delete` command allows you to delete a repository on Github.

```commandline
Usage: eve github delete [OPTIONS] NAME

  Delete a github repo

Options:
  --help  Show this message and exit.
```

```commandline
$ eve github delete test-repo

Are you sure you want to delete https://github.com/IVIURRAY/test-repo? [y/N]: y
Deleted: test-repo
```

## Tidy
The `tidy` command is used to tidy a driectory into sub-folders based on the file's extension.

A detail explaniation can be found [here](https://www.youtube.com/watch?v=cmVt-ggdVz0).

```commandline
Usage: eve tidy [OPTIONS]

  Tidy a directory

Options:
  -v, --verbose    Enable verbose logging
  -p, --path TEXT  Directory path to tidy
  --help           Show this message and exit.
```

___options___
* '-v' '--verbose' - flag to enable verbose logging
* '-p' '--path' - the path to tidy. This can be set by default in [`config.py`](/eve/config.py)

***`tidy`***
Tidy a given directory, defaults to what is set in [`config.py`](/eve/config.py)

```commandline
$ eve tidy -v
============= Tidying 5 files in: /Users/SWEHaydn/Downloads =============
'some_pdf.pdf' --> '/pdf/some_pdf.pdf'
'some_txt.txt' --> '/txt/some_txt.txt'
'some_jpg.jpg' --> '/jpg/some_jpg.jpg'
'some_mp4.mp4' --> '/mp4/some_mp4.mp4'
'some_py.py'   --> '/py/some_py.py'
```


## Weather
The `weather` commands use [OpenWeatherMap](https://openweathermap.org/) under the hood.

It is intended to be used for querying and viewing weather information.

Below, is a list of currently supported commands.


```commandline
Usage: eve weather [OPTIONS] COMMAND [ARGS]...

  Weather information

Options:
  -l, --location TEXT  Weather at this location.  [default: London]
  --help               Show this message and exit.

Commands:
  current   Current weather at a location
  forecast  Forecast for a location
```

___options___
* `-l` `--location` - override the default location. `eve weather -l <mytown> current`


***`current`***

The `current` command gives you information for weather at a location right now.

```commandline
Usage: eve weather current [OPTIONS]

  Current weather at a location

Options:
  --help  Show this message and exit.
```

```commandline
$ eve weather current

========= London GB - BROKEN CLOUDS =========
🔥 Temp: 22.84 - 21.67/23.89 (min/max)
🌪 Wind: 12.8
💧 Rain: {}
🌕 Sunrise: 05:08 - Sunset: 20:08 🌑
```

***`forecast`***

The `forecast` command displays weather for the upcoming days.

```commandline
Usage: eve weather forecast [OPTIONS]

  Forecast for a location

Options:
  --help  Show this message and exit.
```

```commandline
$ eve weather forecast
  ================================== Paris FR =================================
  📅 Date:  Mon 15 Mar    Tue 16 Mar    Wed 17 Mar    Thu 18 Mar    Fri 19 Mar
  🔥 Temp:    11.79         10.88         10.56          9.27          7.56
  🌪 Wind:    23.62          8.24         22.03         29.02         24.12
  💧 Rain: {'3h': 0.36}       No            No       {'3h': 0.4}        No
```


## Crypto
The `crypto` commands use [CoinMarketCapApi](https://coinmarketcap.com/api/documentation/v1/) or 
[Gecko](https://github.com/man-c/pycoingecko) under the hood.

It is intended to be used for querying current price for given crypto currency.

Below, is a list of currently supported commands.


```commandline
Usage: eve crypto [OPTIONS] COMMAND [ARGS]...

  Coin price for a given coin

Options:
  -c, --coin TEXT                 Coin  [default: BTC]
  -ccy, --currency TEXT
                                  destination  [default: EUR]
  --help                          Show this message and exit.

Commands:
  price
```

***`price`***

The `price` command gives you information about the price of the coin.

```commandline
$ eve crypto price
  ============= BTC (BITCOIN) PRICE ============
  💱 Price:         50,413.6830 EUR
  💰 Market cap:    940,417,447,517.0726 EUR
  🏦 TTL supply:    18,654,012
  📈 24H change:    -1.7 %
```

___options___
* `-c` `--coin` - override the default coin. `eve crypto -c <mycoin> price`
* `-ccy` `--currency` - overrides the default destination `eve cripto -ccy <mycurrency> price`

___example___
```commandline
$ eve crypto -c "ADA" -ccy "RUB" price
  ============= ADA (CARDANO) PRICE ============
  💱 Price:         78.6613 RUB
  💰 Market cap:    2,513,096,409,058.2915 RUB
  🏦 TTL supply:    45,000,000,000
  📈 24H change:    -3.4 %
```

it is also possible to set another crypto currency as destination currency

```commandline
$ eve crypto -c "BTC" -ccy "ADA" price
============= BTC (BITCOIN) PRICE ============
💱 Price:         56,273.0083 ADA
💰 Market cap:    1,049,717,372,134.1301 ADA
🏦 TTL supply:    18,654,012
📈 24H change:    1.8 %
```

## Calendar

The `cal` command uses [Google Calendar Api](https://developers.google.com/calendar)
 
Intended to be used for getting info about upcoming events in the given calendar

```commandline
$ eve cal --help
Usage: eve cal [OPTIONS] COMMAND [ARGS]...

  Google calendar interaction

Options:
  --help  Show this message and exit.

Commands:
  events  Display number of upcoming events in google calendar
```

___example___
```commandline
$ eve cal events
 ========= Retrospective team Avengers =========
 👨 Organizer:     tony.stark@gmail.com
 ⏱ Starts in:     In Progress
 ⏳ Duration:      60 min
 ✅ Status:        Confirmed
 ==================== FriYay ===================
 👨 Organizer:     jane.doe@gmail.com
 ⏱ Starts in:     33
 ⏳ Duration:      60 min
 ✅ Status:        Confirmed
```

#### Accessing google calendar API

In order to access api you'd need to go to the [quickstart](https://developers.google.com/calendar/quickstart/python)
and click `Enable the Google Calendar API`

After that, move the downloaded file to the desired directory.
Once that is done, either change `config.py` specifying the directory as a second parameter in `os.environ.get()` for 
`PATH_TO_CRED` variable or export `PATH_TO_CALENDAR_API_CRED` in `.eve_config` file.

## Quote
The `quote` command uses the [quote module](https://github.com/maxhumber/quote) which is a python wrapper for the Goodreads Quote API.

Below is a list of currently supported options:

```commandline
Usage: eve quote [OPTIONS]

  Output quotes.
   
Options:
  -s, --search TEXT Searchstring for random quotes.
  -- help           Show this message and exit.
```

The default searchsting ('Tolkien') can be overridden by using the `search` option. For excample: `eve quote -s 'Harry Potter'`
