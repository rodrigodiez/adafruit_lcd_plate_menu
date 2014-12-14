from distutils.core import setup

version_file = open(os.path.join(os.path.dirname(__file__), 'VERSION'))
version = version_file.read().strip()

setup(
    name="adafruit_lcd_plate_menu",
  	description='A simple yet powerful menu library for Adafruit\'s LCD plates',
  	version=version,
	author='Rodrigo Diez Villamuera',
	author_email='rodrigo@rodrigodiez.io',
	url='https://www.github.com/rodrigodiez/adafruit_lcd_plate_menu',
    download_url="https://github.com/rodrigodiez/adafruit_lcd_plate_menu/archive/%s.tar.gz" % (version),
    packages=[],
    install_requires=['Adafruit_CharLCD>=1.0.0'],
    classifiers=[
		'Development Status :: 3 - Alpha'
		'Environment :: Console',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Natural Language :: English',
		'Operating System :: OS Independent',
		'Programming Language :: Python :: 2.7',
		'Topic :: Software Development'
    ]
)