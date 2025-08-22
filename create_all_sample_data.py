#!/usr/bin/env python3
"""
Master script to create all sample data for the Arogya health app.
Run this script from the Django project root directory to populate all features with test data.
"""

import os
import django
import sys
import subprocess

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Arogya_Backend.settings')
django.setup()

def run_script(script_name):
    """Run a sample data script and handle errors"""
    try:
        print(f"\n{'='*60}")
        print(f"Running {script_name}...")
        print(f"{'='*60}")
        
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True, cwd=os.getcwd())
        
        if result.returncode == 0:
            print(result.stdout)
            print(f"✅ {script_name} completed successfully!")
        else:
            print(f"❌ Error running {script_name}:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Exception running {script_name}: {e}")
        return False
    
    return True

def main():
    """Run all sample data creation scripts"""
    print("🚀 Starting comprehensive sample data creation for Arogya Health App")
    print("This will populate all features with test data...")
    
    # List of all sample data scripts
    scripts = [
        'create_lab_sample_data.py',
        'create_helpline_sample_data.py', 
        'create_tips_sample_data.py',
        'create_news_sample_data.py',
        'create_health_content_sample_data.py'
    ]
    
    successful_scripts = []
    failed_scripts = []
    
    for script in scripts:
        if os.path.exists(script):
            if run_script(script):
                successful_scripts.append(script)
            else:
                failed_scripts.append(script)
        else:
            print(f"⚠️  Warning: {script} not found, skipping...")
            failed_scripts.append(script)
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 SAMPLE DATA CREATION SUMMARY")
    print(f"{'='*60}")
    print(f"✅ Successful: {len(successful_scripts)} scripts")
    for script in successful_scripts:
        print(f"   - {script}")
    
    if failed_scripts:
        print(f"\n❌ Failed: {len(failed_scripts)} scripts")
        for script in failed_scripts:
            print(f"   - {script}")
    
    print(f"\n🎉 Sample data creation completed!")
    print(f"Your Arogya Health App is now populated with test data for:")
    print(f"   • Lab Results (tests, hospitals, reports)")
    print(f"   • Helpline (FAQ categories and questions)")
    print(f"   • Health Tips (daily wellness tips)")
    print(f"   • News Updates (health news articles)")
    print(f"   • Educational Content (health categories and media)")
    
    print(f"\n🚀 Next steps:")
    print(f"   1. Start your backend server: python manage.py runserver 0.0.0.0:8000")
    print(f"   2. Start your frontend: npm start (in the React Native project)")
    print(f"   3. Test all features on your mobile device via Expo")

if __name__ == '__main__':
    main()
