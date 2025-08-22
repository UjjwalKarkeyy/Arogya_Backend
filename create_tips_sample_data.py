#!/usr/bin/env python3
"""
Script to create sample tips data for testing the tips functionality.
Run this script from the Django project root directory.
"""

import os
import django
import sys

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Arogya_Backend.settings')
django.setup()

from tips.models import Tip

def create_sample_tips():
    """Create sample health tips for testing"""
    
    sample_tips = [
        {
            'title': 'Stay Hydrated',
            'content': 'Drink at least 8 glasses of water daily to maintain proper hydration and support overall health.',
            'is_active': True
        },
        {
            'title': 'Regular Exercise',
            'content': 'Aim for at least 30 minutes of moderate exercise daily to improve cardiovascular health and maintain fitness.',
            'is_active': True
        },
        {
            'title': 'Balanced Diet',
            'content': 'Include fruits, vegetables, whole grains, and lean proteins in your daily meals for optimal nutrition.',
            'is_active': True
        },
        {
            'title': 'Quality Sleep',
            'content': 'Get 7-9 hours of quality sleep each night to support mental health and physical recovery.',
            'is_active': True
        },
        {
            'title': 'Hand Hygiene',
            'content': 'Wash your hands frequently with soap and water for at least 20 seconds to prevent infections.',
            'is_active': True
        },
        {
            'title': 'Mental Health',
            'content': 'Practice mindfulness, meditation, or deep breathing exercises to manage stress and anxiety.',
            'is_active': True
        },
        {
            'title': 'Regular Checkups',
            'content': 'Schedule regular health checkups and screenings to detect and prevent health issues early.',
            'is_active': True
        },
        {
            'title': 'Sun Protection',
            'content': 'Use sunscreen with SPF 30+ and wear protective clothing when exposed to direct sunlight.',
            'is_active': True
        },
        {
            'title': 'Limit Screen Time',
            'content': 'Take regular breaks from screens and practice the 20-20-20 rule to protect your eyes.',
            'is_active': True
        },
        {
            'title': 'Social Connections',
            'content': 'Maintain healthy relationships and social connections to support emotional well-being.',
            'is_active': True
        },
        {
            'title': 'Avoid Smoking',
            'content': 'Quit smoking and avoid secondhand smoke to reduce risk of cancer and heart disease.',
            'is_active': True
        },
        {
            'title': 'Limit Alcohol',
            'content': 'Consume alcohol in moderation or avoid it completely for better liver and overall health.',
            'is_active': True
        }
    ]
    
    print("Creating sample tips data...")
    
    # Clear existing tips (optional - remove if you want to keep existing data)
    Tip.objects.all().delete()
    print("Cleared existing tips data")
    
    # Create new tips
    created_count = 0
    for tip_data in sample_tips:
        tip, created = Tip.objects.get_or_create(
            title=tip_data['title'],
            defaults={
                'content': tip_data['content'],
                'is_active': tip_data['is_active']
            }
        )
        if created:
            created_count += 1
            print(f"Created tip: {tip.title}")
        else:
            print(f"Tip already exists: {tip.title}")
    
    print(f"\nSample tips data creation completed!")
    print(f"Created {created_count} new tips")
    print(f"Total tips in database: {Tip.objects.count()}")
    print(f"Active tips: {Tip.objects.filter(is_active=True).count()}")

if __name__ == '__main__':
    create_sample_tips()
