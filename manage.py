import os
import sys
import webbrowser
import time
import threading

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'labor_management.settings')

    try:
        # Auto-open browser only when running the dev server
        if len(sys.argv) >= 2 and sys.argv[1] == "runserver":
            def open_browser():
                time.sleep(2)
                webbrowser.open("http://127.0.0.1:8000")

            threading.Thread(target=open_browser).start()

        from django.core.management import execute_from_command_line
        execute_from_command_line(sys.argv)

    except Exception as e:
        print("🚨 EMS failed to start!")
        print(str(e))
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
