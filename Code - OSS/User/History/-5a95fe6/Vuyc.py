#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

os.environ['GEMINI_API_KEY'] = 'AQ.Ab8RN6LL5syoUKoepINyx4u3q9tX_nuikIlw4r_U7fjkVa8_Ww'
os.environ['GOOGLE_API_KEY'] = 'AQ.Ab8RN6LL5syoUKoepINyx4u3q9tX_nuikIlw4r_U7fjkVa8_Ww'

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SOA.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()