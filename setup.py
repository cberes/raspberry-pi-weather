from distutils.core import setup

readme = open('README.md').read()

setup(
    name = "WeatherStation",
    version = "0.1",
    packages = ['station'],
    author = "Corey Beres",
    author_email = "corey.beres@gmail.com",
    description = "Weather station powered by a Raspberry Pi",
    long_description = readme,
    license = "GNU GPL v3",
    keywords = "raspberry, raspberry pi, weather, weather station, embedded",
    url = "https://github.com/cberes/raspberry-pi-weather",
)
