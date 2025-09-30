#!/usr/bin/env python
"""
Create database migration for advance_taken field
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'labor_management.settings')
django.setup()

from django.core.management import execute_from_command_line

def create_migration():
    """Create migration for the new advance_taken field"""
    print("Creating migration for advance_taken field...")
    
    try:
        # Create migration
        execute_from_command_line(['manage.py', 'makemigrations', 'salary'])
        print("✓ Migration created successfully")
        
        # Apply migration
        execute_from_command_line(['manage.py', 'migrate'])
        print("✓ Migration applied successfully")
        
        print("\nAdvance field has been added to the salary system!")
        
    except Exception as e:
        print(f"Error creating migration: {e}")

if __name__ == "__main__":
    create_migration()
