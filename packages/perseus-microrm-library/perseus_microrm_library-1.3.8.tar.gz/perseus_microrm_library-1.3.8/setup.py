# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['majormode',
 'majormode.perseus',
 'majormode.perseus.model',
 'majormode.perseus.utils']

package_data = \
{'': ['*']}

install_requires = \
['perseus-core-library>=1.19,<2.0', 'psycopg2-binary>=2.9,<3.0']

setup_kwargs = {
    'name': 'perseus-microrm-library',
    'version': '1.3.8',
    'description': 'Python small, little, mini, tiny, micro Object-Relational Mapping (ORM)',
    'long_description': '# Perseus MicrORM\n\nMajormode Perseus MicrORM Python Library is a small, little, mini, tiny, micro Object-Relational Mapping (ORM).\n\nMicrORM is not a object-relational mapping in the sense it maps Pyth objects to a Relational DataBase Management System (RDBMS), but in the sense it maps results of SQL queries, executed on a RDBMS, to Python objects.\n\n## Installation\n\nTo install [Perseus MicrORM Python Library](https://github.com/dcaune/perseus-microrm-python-library), simply enter the follow command line:\n\n``` shell\npip install perseus-microrm-library\n```\n\n## Usage\n\n``` python\nimport uuid\n\nfrom majormode.perseus.utils import cast\nfrom majormode.perseus.utils.rdbms import RdbmsConnection\n\n\nRDBMS_CONNECTION_PROPERTIES = {\n    None: {\n        \'rdbms_hostname\': \'localhost\',\n        \'rdbms_port\': 5432,\n        \'rdbms_database_name\': \'foo\',\n        \'rdbms_account_username\': \'dbo\',\n        \'rdbms_account_password\': \'\'\n    }\n}\n\nPLACE_IDS = [\n    uuid.UUID(\'54879ffc-a1ec-11e8-85bd-0008a20c190f\'),\n    uuid.UUID(\'9025d1c8-a1ec-11e8-9e29-0007cb040bcc\')\n]\n\nwith RdbmsConnection.acquire_connection(\n        RDBMS_CONNECTION_PROPERTIES,\n        auto_commit=False,\n        connection=None) as connection:\n    cursor = connection.execute(\n        """\n        SELECT place_id,\n               ST_X(location) AS longitude,\n               ST_Y(location) AS latitude,\n               ST_Z(location) AS altitude,\n               accuracy,\n               creation_time\n          FROM place\n          WHERE place_id IN %[place_ids]s\n        """,\n        {\n            \'place_ids\': PLACE_IDS \n        })\n    rows = cursor.fetch_all()\n\n    places = [\n        row.get_object({\n            \'place_id\': cast.string_to_uuid,\n            \'creation_time\': cast.string_to_timestamp})\n        for row in cursor.fetch_all()]\n\n    for place in places:\n        print(place.place_id, place.longitude, place.latitude)\n```\n',
    'author': 'Daniel CAUNE',
    'author_email': 'daniel.caune@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/majormode/perseus-microrm-python-library',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
