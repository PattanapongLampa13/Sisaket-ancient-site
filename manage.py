<div id="register-form-section" style="display:none;">
    <h1>สร้างบัญชีใหม่</h1>
    <form method="post" action="{% url 'auth' %}" id="register-form">
        {% csrf_token %}
        {{ register_form.as_p }}
        <button type="submit" class="btn-submit">สมัครสมาชิก</button>
    </form>
    <p class="form-link">มีบัญชีอยู่แล้ว? <a href="#" onclick="showTab('login');return false;">เข้าสู่ระบบ</a></p>
</div>
#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sisaket.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
