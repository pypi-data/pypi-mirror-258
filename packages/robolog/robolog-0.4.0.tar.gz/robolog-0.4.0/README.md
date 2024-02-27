# Robolog

![Image Alt Text](robolog/img/_idea_robolog.drawio.png)

These are a set of predefined configurations optimized for RPA usage (but not limited to!). The project aims to predict the most suitable default logging configurations for your needs. This fully capable logger can be created with just a single line of code. It is highly configurable and can seamlessly coexist with other loggers.

If you are familiar with Python's `logging` library, you can leverage this tool to save time on tedious configurations or copying code from one project to another. However, if you've recently embarked on your Python journey, you can employ basic syntax without being encumbered by handlers, formatters, and other components necessary for proper logging setup. Simply follow these instructions to utilize a fully functional logger within minutes.


## Prerequisites
This package was developed and tested on Windows, but it should function on other systems as long as their console is capable of handling the `colorlog` library, the sole dependency.

While some tests are planned, they are not implemented at this stage of the project.



## Installation

In order to install the `robolog` package just make sure that you have access to the PyPI and type in your shell: 

```powershell
pip install robolog 
```

Now you can import the `robolog` library into your project files.

## Test default settings:
After installation, import the `robolog` library at the top of your script and run the following:

```python
from robolog import robolog

log = robolog.get_logger()

log.debug("Testing logger. This is level DEBUG")
log.info("Testing logger. This is level INFO")
log.warning("Testing logger. This is level WARNING")
log.error("Testing logger. This is level ERROR")
```

You shuld see all available logs in your console:

![Image Alt Text](robolog/img/md01.png)

Also check if default directory `log` was created. Yhere should be a log file with slightly different (more detailed) format.

## Logging customization possibilities


If you don't like certain aspects of this formatting you can easly personalize most of the important aspects such as:

- **Logged fields:** You can provide your own formatting string understandable by the python's logging library. Aplicible for file/screen logs independently. 
- **Colors:** You can switch them of entirely or pick your own (limited only to the colorlog library color palette). 
- **Line compacteness:** If you prefer shorter screen messages, try predefined compact version before writing your own formatting string. 
- **Logging levels:** You can filter certain logging levels for screen logging and for the file logs independently.
- **Turn off/on handlers independently:** You can switch off logging to file and use this logger as a colored print statement or contrary -- collect only file logs without displaying them in the standard output.
- **Customizable date/time format:** There is a possibility to provide custom date and time formatting.
- **Log file name:** The robolog by default will create a new log file each year/month(default)/day or even hourly, depending on your need. If you want a static single file for your logs -- it is also customizable. You can store logs in the `.csv`-like format or plain `.txt`.
- **Log file directory:** By default robolog will store file logs in the `logs/` dolder but you can provide your own directory name. 
- **Using with another loggers:** This logger is called `'robolog'` and after initial creation you can retreive it from anywhere in your code using python's standard library. It can coexist with other loggers. 


## How to customize:

Depending on your preference, you can provide certain arguments into the `get_logger()` function one by one or jus unpack python dictionary in order to set all your configurations at once. Let's see an example:

```python
    from robolog import robolog
    import logging
    
    # Example of your configuration file
    CONFIG = {
        "logger_name": "MY_CUSTOM_NAME",                # custom logger name
        "colors": {                                     # custom color palette
            "INFO": "blue",                             # defined by colorlog library
            "WARNING": "green", 
            "ERROR": "purple"
            },
        "file_ext": "txt",                              # change file extension
        "stdo_fmt": "[{levelname:^7s}] :: {message:s}", # custom format string
        "stdo_lvl": logging.WARNING,                    # filter out DEBUG and INFO 
        "file_lvl": logging.ERROR,                      # Store only ERROR in file
    }

    log = get_logger(**CONFIG)                          # Unpack config  

    # Test:
    log.debug("TEST DEBUG")
    log.info("TEST INFO")
    log.warning("TEST WARNING")
    log.error("TEST ERROR")

```

## Default settings

Here is the list of all possible arguments and its default values:
  - **logger_name** (`str`): Name of the logger (*default is "robolog"*).
  - **file_dir** (`str`): Directory to store log files (*default is "logs"*).
  - **stdo_lvl** (`int`): Logging level in standard output (*default is logging.DEBUG*).
  - **file_lvl** (`int`): Logging level in file (*default is logging.DEBUG*).
  - **use_file** (`bool`): Flag to enable or disable file logging (*default is True*).
  - **use_stdo** (`bool`): Flag to enable or disable standard output logging (*default is True*).
  - **use_colors** (`bool`): Flag to enable or disable colored output (*default is True*).
  - **file_name** (`str`): Static file name for log files, if not provided, it is generated using **file_stamp** format (see below), By defult this is `None` as logger will create date-stamped log files in each month.
  - **file_stamp** (`str`): Timestamp format for log file names (default is "%Y%m") This will determine how often a new log file will be created. If you want a static name -- set your own name to the **file_name** argument.
  - **colors** (`Dict[str, str]`): Mapping of log level to color codes (default is None, using predefined colors). This mapping is consistent with the `colorlog` library.
  - **stdo_fmt** (`str`): Log format for standard output logs (default is detailed format containing log level, time, logging mofule name, line in that module, and your mesage) .
  - **file_fmt** (`str`): Log format for file logs (default is CSV-like format). It is more detailed than screen logs by default: especially date. Each field is `;`-separated.
  - **use_compact** (`bool`): Predefined shorter standard output line (default is False).
  - **file_ext** (`str`): File extension for log files (default is "csv").
  - **date_fmt** (`str`): Timestamp format for standard output logs as the file log dates are as detailed as possible (default is "%H:%M:%S").