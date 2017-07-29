from setuptools import setup

config = {
    'include_package_data': True,
    'description': 'math bot for SAT',
    'version': '0.0.1',
    'packages': ['database', 'helper_scripts'],
    'zip_safe': False,
    'setup_requires': [],
    'install_requires': [
        'nose',
        'xmltodict',
        'mock',
        'pymysql',
        'Flask==0.11.1',
        'Jinja2==2.8',
        'MarkupSafe==0.23',
        'Werkzeug==0.11.10',
        'click==6.6',
        'gunicorn==19.6.0',
        'itsdangerous==0.24',
        'requests==2.10.0',
    ],
    'name': 'math_bot'
}

if __name__ == '__main__':
    setup(**config)
