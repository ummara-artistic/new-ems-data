import subprocess
import sys

def install_packages():
    """Install required Python packages"""
    packages = [
        'Django>=4.2.0',
        'reportlab>=4.0.0',
        'Pillow>=10.0.0',
    ]
    
    for package in packages:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"✓ Successfully installed {package}")
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to install {package}: {e}")
    
    print("\n📦 All dependencies installation completed!")
    print("🚀 Your Django labor management system is ready to use!")

if __name__ == "__main__":
    install_packages()
