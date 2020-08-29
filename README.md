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

## Configuration
There is a [`config.py`](/eve/config.py) that can be customised to support different use cases.

Override the relevant variables to fit your use case.

**DO NOT COMMIT ANY SENSITIVE INFORMATION!**
 
# API
Below is a list of the currently support API commands.

* [`eve github`](#github) - Github utilities.
* [`eve tidy`](#tidy) - Directory tidy.
* [`eve weather`](#weather) - Weather information.

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

  Weather Information

Options:
  -l, --location TEXT  Weather at this location.
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
$ eve weather  forecast

================================= London GB =================================
📅 Date:  Sat 1 Aug     Sun 2 Aug     Mon 3 Aug     Tue 4 Aug     Wed 5 Aug   
🔥 Temp:    23.49         21.57          21.1         15.81         21.98     
🌪 Wind:     9.24          9.64          7.96          8.77          12.8     
💧 Rain:      {}            {}            {}            {}            {}   
```
