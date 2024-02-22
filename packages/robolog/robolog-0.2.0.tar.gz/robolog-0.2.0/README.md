# Robolog
This is a set of predefined configurations optimized for RPA usage. The aim of this project is to anticipate which logging configurations would best suit your needs and set them as defaults. This fully capable logger can be created with just a single line of code. It is highly configurable and can seamlessly coexist with other loggers.

If you are acquainted with Python's `logging` library, you can leverage this tool to save time on intricate configurations. Conversely, if you've recently embarked on your Python journey, you can employ basic syntax without being encumbered by handlers, formatters, and other components necessary for proper logging setup. Simply follow these instructions to utilize a fully functional logger within minutes.

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

## Logging customization

Comming soon...