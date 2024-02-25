# PythonConfigIniGUI
A Python Web GUI for any projects Config Ini File.
So you can easily edit your config ini file from a web interface.

## About this repository

This repository is a Python Web GUI for any projects Config Ini File.
So you can easily edit your config ini file from a web interface.

## How to use it

Import the `ConfigIniGUI` class from the `configinigui` module and create an instance of it with the path of your config ini file as parameter.

```python
from configinigui import ConfigIniGUI

configinigui = ConfigIniGUI('path/to/your/config.ini')
configinigui.run()
```

Then, open your web browser and go to `http://localhost:5000`.

You can also specify the port of the web server by passing the `port` parameter to the `run` method.

```python
configinigui.run(port=8000)
```

## How to install it

You can install this package from the Python Package Index (PyPI) using pip.

```bash
pip install configinigui
```

## How to contribute

If you want to contribute to this project, you can fork this repository and create a pull request with your changes.

## How to report a bug

If you find a bug in this project, you can open an issue in this repository.
Please provide a detailed description of the bug and the steps to reproduce it.

## How to request a feature

If you want to request a feature, you can open an issue in this repository.
Please provide a detailed description of the feature you want and why you need it.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

