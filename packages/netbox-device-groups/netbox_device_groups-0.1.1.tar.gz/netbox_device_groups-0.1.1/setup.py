# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['netbox_device_groups',
 'netbox_device_groups.api',
 'netbox_device_groups.core',
 'netbox_device_groups.core.models',
 'netbox_device_groups.forms',
 'netbox_device_groups.graphql',
 'netbox_device_groups.migrations',
 'netbox_device_groups.models',
 'netbox_device_groups.tests']

package_data = \
{'': ['*'],
 'netbox_device_groups': ['templates/netbox_device_groups/*',
                          'templates/netbox_device_groups/physical_cluster/*']}

install_requires = \
['bleach==6.1.0',
 'django-cors-headers==4.3.1',
 'django-debug-toolbar==4.2.0',
 'django-filter==23.5',
 'django-graphiql-debug-toolbar==0.2.0',
 'django-mptt==0.14.0',
 'django-pglocks==1.0.4',
 'django-prometheus==2.3.1',
 'django-redis==5.4.0',
 'django-rich==1.8.0',
 'django-rq==2.10.1',
 'django-tables2==2.7.0',
 'django-taggit==5.0.1',
 'django-timezone-field==6.1.0',
 'django==4.2.8',
 'djangorestframework==3.14.0',
 'drf-spectacular-sidecar==2023.12.1',
 'drf-spectacular==0.27.0',
 'feedparser==6.0.11',
 'graphene-django==3.0.0',
 'gunicorn==21.2.0',
 'jinja2==3.1.2',
 'markdown==3.5.1',
 'mkdocs-material==9.5.3',
 'mkdocstrings[python-legacy]==0.24.0',
 'netaddr==0.9.0',
 'pillow==10.1.0',
 'psycopg[binary,pool]==3.1.16',
 'pyyaml==6.0.1',
 'requests==2.31.0',
 'social-auth-app-django==5.4.0',
 'social-auth-core[openidconnect]==4.5.1',
 'svgwrite==1.4.3',
 'tablib==3.5.0',
 'tzdata==2023.3']

setup_kwargs = {
    'name': 'netbox-device-groups',
    'version': '0.1.1',
    'description': 'A netbox plugin for managing multiple device group types',
    'long_description': '\nA netbox plugin for managing multiple device group types by site\n\n<a href="https://github.com/sapcc/netbox-device-groups/forks"><img src="https://img.shields.io/github/forks/sapcc/netbox-device-groups" alt="Forks Badge"/></a>\n<a href="https://github.com/sapcc/netbox-device-groups/pulls"><img src="https://img.shields.io/github/issues-pr/sapcc/netbox-device-groups" alt="Pull Requests Badge"/></a>\n<a href="https://github.com/sapcc/netbox-device-groups/issues"><img src="https://img.shields.io/github/issues/sapcc/netbox-device-groups" alt="Issues Badge"/></a>\n<a href="https://github.com/sapcc/netbox-device-groups/graphs/contributors"><img alt="GitHub contributors" src="https://img.shields.io/github/contributors/sapcc/netbox-device-groups?color=2b9348"></a>\n<a href="https://github.com/sapcc/netbox-device-groups/blob/master/LICENSE"><img src="https://img.shields.io/github/license/sapcc/netbox-device-groups?color=2b9348" alt="License Badge"/></a>\n\n## Installing the Plugin in Netbox\n\n### Prerequisites\n\n- The plugin is compatible with Netbox 3.5.0 and higher.\n- Databases supported: PostgreSQL\n- Python supported : Python3 >= 3.10\n\n### Install Guide\n\n> NOTE: Plugins can be installed manually or using Python\'s `pip`. See the [netbox documentation](https://docs.netbox.dev/en/stable/plugins/) for more details. The pip package name for this plugin is [`netbox-device-groups`](https://pypi.org/project/netbox-device-groups/).\n\nThe plugin is available as a Python package via PyPI and can be installed with `pip`:\n\n```shell\npip install netbox-device-groups\n```\n\nTo ensure the device cluster plugin is automatically re-installed during future upgrades, create a file named `local_requirements.txt` (if not already existing) in the Netbox root directory (alongside `requirements.txt`) and list the `netbox_device_groups` package:\n\n```shell\necho netbox-device-groups >> local_requirements.txt\n```\n\nOnce installed, the plugin needs to be enabled in your Netbox configuration. The following block of code below shows the additional configuration required to be added to your `$NETBOX_ROOT/netbox/configuration.py` file:\n\n- Append `"netbox_device_groups"` to the `PLUGINS` list.\n- Append the `"netbox_device_groups"` dictionary to the `PLUGINS_CONFIG` dictionary and override any defaults.\n\n```python\nPLUGINS = [\n    "netbox_device_groups",\n]\n```\n\n## Post Install Steps\n\nOnce the Netbox configuration is updated, run the post install steps from the _Netbox Home_ to run migrations and clear any cache:\n\n```shell\n# Apply any database migrations\npython3 netbox/manage.py migrate\n# Trace any missing cable paths (not typically needed)\npython3 netbox/manage.py trace_paths --no-input\n# Collect static files\npython3 netbox/manage.py collectstatic --no-input\n# Delete any stale content types\npython3 netbox/manage.py remove_stale_contenttypes --no-input\n# Rebuild the search cache (lazily)\npython3 netbox/manage.py reindex --lazy\n# Delete any expired user sessions\npython3 netbox/manage.py clearsessions\n# Clear the cache\npython3 netbox/manage.py clearcache\n```\n\nThen restart the Netbox services:\n\n```shell\nsudo systemctl restart netbox netbox-rq\n```\n',
    'author': 'Pat McLean',
    'author_email': 'patrick.mclean@sap.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/sapcc/netbox-device-groups',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
