# from .epc.clarite import analyze, describe, load, modify, plot, survey  # noqa E402

# # from .ge.modules import etl  # noqa E402

# __all__ = [
#     "load",
#     "describe",
#     "modify",
#     "plot",
#     "analyze",
#     "survey",
#     # "etl",
# ]


# try:
#     import os

#     import django

#     os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings")
#     django.setup()
# except Exception as e:
#     print(e)  # add if to handle
#     import sys
#     sys.path.append("/users/andrerico/dev/project_igem/igem")
#     import os

#     import django
#     os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings")
#     django.setup()


import os
import sys

import django

import igem_lite

try:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings")
    django.setup()
except Exception as e:  # noqa F841
    # print(e)  # add if to handle
    sys.path.append(os.path.dirname(igem_lite.__file__))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings")
    django.setup()

from .epc import analyze, describe, load, modify, plot, survey
from .ge import db, filter

__all__ = [
    "db",
    "filter",
    "analyze",
    "describe",
    "load",
    "modify",
    "plot",
    "survey",
]
