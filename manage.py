#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    if os.environ.get("STAGE") == "prod":
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoDo.prod_settings")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoDo.dev_settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
