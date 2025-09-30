import os
import django
from django.core.management import execute_from_command_line

def setup_database():
    """Setup Django database with migrations"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'labor_management.settings')
    django.setup()
    
    print("🔄 Creating database migrations...")
    execute_from_command_line(['manage.py', 'makemigrations'])
    
    print("🔄 Applying database migrations...")
    execute_from_command_line(['manage.py', 'migrate'])
    
    print("✅ Database setup completed!")
    print("👤 Default admin credentials: admin / admin")
    print("🌐 Run 'python manage.py runserver' to start the application")

if __name__ == "__main__":
    setup_database()
