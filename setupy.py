from setuptools import setup, find_packages

config = {
    'include_package_data': True,
    'description': 'math bot for SAT',
    'version': '0.0.1',
    'packages': ['database'],
    'zip_safe': False,
    'setup_requires': [],
    'install_requires': [
        'nose',
        'xmltodict',
        'mock'
    ],
    'name': 'math_bot'
}

if __name__ == '__main__':
    setup(**config)