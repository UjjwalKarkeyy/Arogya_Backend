#!/usr/bin/env python3
"""
Script to create sample health content data for testing the educational content functionality.
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

from healthContent.models import HealthCategory, MediaContent

def create_sample_health_content():
    """Create sample health content data for testing"""
    
    # Create health categories
    categories_data = [
        {
            'name': 'Nutrition',
            'description': 'Learn about healthy eating, balanced diets, and nutritional guidelines',
            'icon': 'nutrition',
            'color': '#4CAF50',
            'order': 1
        },
        {
            'name': 'Hygiene',
            'description': 'Personal hygiene practices and cleanliness habits for better health',
            'icon': 'hygiene',
            'color': '#2196F3',
            'order': 2
        },
        {
            'name': 'Exercise & Fitness',
            'description': 'Physical activity, workout routines, and fitness tips',
            'icon': 'fitness',
            'color': '#FF9800',
            'order': 3
        },
        {
            'name': 'Mental Health',
            'description': 'Mental wellness, stress management, and emotional health',
            'icon': 'mental-health',
            'color': '#9C27B0',
            'order': 4
        },
        {
            'name': 'Disease Prevention',
            'description': 'Preventive care and disease prevention strategies',
            'icon': 'prevention',
            'color': '#F44336',
            'order': 5
        },
        {
            'name': 'Child Health',
            'description': 'Health information specifically for children and parents',
            'icon': 'child-health',
            'color': '#E91E63',
            'order': 6
        },
        {
            'name': 'Women\'s Health',
            'description': 'Health topics specific to women\'s health needs',
            'icon': 'womens-health',
            'color': '#673AB7',
            'order': 7
        },
        {
            'name': 'Senior Health',
            'description': 'Health guidance for older adults and seniors',
            'icon': 'senior-health',
            'color': '#607D8B',
            'order': 8
        }
    ]
    
    # Sample media content
    content_data = [
        # Nutrition Content
        {
            'category': 'Nutrition',
            'title': 'Understanding Balanced Diet Basics',
            'description': 'Learn the fundamentals of creating a balanced diet with proper portions of proteins, carbohydrates, fats, vitamins, and minerals.',
            'content_type': 'video',
            'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            'author': 'Dr. Sarah Johnson',
            'source': 'Health Education Network',
            'duration': '12:30',
            'difficulty_level': 'beginner',
            'target_age_group': 'all_ages',
            'is_featured': True,
            'is_verified': True,
            'tags': 'nutrition, diet, balanced eating, healthy food, wellness',
            'meta_description': 'Complete guide to understanding balanced diet fundamentals'
        },
        {
            'category': 'Nutrition',
            'title': 'Meal Planning for Busy Families',
            'description': 'Practical tips and strategies for planning nutritious meals for busy families on a budget.',
            'content_type': 'article',
            'url': 'https://example.com/meal-planning-guide',
            'author': 'Nutritionist Maria Garcia',
            'source': 'Family Health Magazine',
            'difficulty_level': 'intermediate',
            'target_age_group': 'adults',
            'is_featured': True,
            'tags': 'meal planning, family nutrition, budget meals, healthy cooking',
            'meta_description': 'Learn effective meal planning strategies for busy families'
        },
        
        # Hygiene Content
        {
            'category': 'Hygiene',
            'title': 'Proper Hand Washing Technique',
            'description': 'Step-by-step guide to proper hand washing technique to prevent infections and diseases.',
            'content_type': 'video',
            'url': 'https://www.youtube.com/watch?v=hygiene123',
            'author': 'WHO Health Team',
            'source': 'World Health Organization',
            'duration': '3:45',
            'difficulty_level': 'beginner',
            'target_age_group': 'all_ages',
            'is_featured': True,
            'is_verified': True,
            'tags': 'hand washing, hygiene, infection prevention, health safety',
            'meta_description': 'Learn the correct way to wash your hands effectively'
        },
        {
            'category': 'Hygiene',
            'title': 'Dental Care for Children',
            'description': 'Complete guide to maintaining good dental hygiene in children, including brushing techniques and cavity prevention.',
            'content_type': 'infographic',
            'url': 'https://example.com/dental-care-infographic',
            'author': 'Dr. Michael Chen',
            'source': 'Pediatric Dental Association',
            'difficulty_level': 'beginner',
            'target_age_group': 'children',
            'is_verified': True,
            'tags': 'dental care, children health, oral hygiene, teeth brushing',
            'meta_description': 'Essential dental care tips for children and parents'
        },
        
        # Exercise & Fitness Content
        {
            'category': 'Exercise & Fitness',
            'title': '30-Minute Home Workout for Beginners',
            'description': 'No-equipment workout routine that can be done at home, perfect for fitness beginners.',
            'content_type': 'video',
            'url': 'https://www.youtube.com/watch?v=fitness123',
            'author': 'Fitness Coach Alex Thompson',
            'source': 'Home Fitness Channel',
            'duration': '32:15',
            'difficulty_level': 'beginner',
            'target_age_group': 'adults',
            'is_featured': True,
            'tags': 'home workout, beginner fitness, exercise routine, no equipment',
            'meta_description': 'Easy 30-minute workout routine for beginners at home'
        },
        {
            'category': 'Exercise & Fitness',
            'title': 'Benefits of Regular Physical Activity',
            'description': 'Comprehensive overview of how regular exercise benefits physical and mental health.',
            'content_type': 'article',
            'url': 'https://example.com/exercise-benefits',
            'author': 'Dr. Lisa Park',
            'source': 'Sports Medicine Journal',
            'difficulty_level': 'all',
            'target_age_group': 'all_ages',
            'is_verified': True,
            'tags': 'exercise benefits, physical activity, health, fitness, wellness',
            'meta_description': 'Discover the many benefits of regular physical activity'
        },
        
        # Mental Health Content
        {
            'category': 'Mental Health',
            'title': 'Stress Management Techniques',
            'description': 'Learn effective techniques for managing stress and anxiety in daily life.',
            'content_type': 'video',
            'url': 'https://www.youtube.com/watch?v=stress123',
            'author': 'Dr. Emma Wilson',
            'source': 'Mental Health Institute',
            'duration': '18:20',
            'difficulty_level': 'beginner',
            'target_age_group': 'adults',
            'is_featured': True,
            'is_verified': True,
            'tags': 'stress management, anxiety, mental health, relaxation, mindfulness',
            'meta_description': 'Effective stress management techniques for better mental health'
        },
        {
            'category': 'Mental Health',
            'title': 'Meditation Guide for Beginners',
            'description': 'Simple meditation practices to improve mental clarity and emotional well-being.',
            'content_type': 'audio',
            'url': 'https://example.com/meditation-guide',
            'author': 'Mindfulness Expert John Davis',
            'source': 'Meditation Center',
            'duration': '25:00',
            'difficulty_level': 'beginner',
            'target_age_group': 'adults',
            'tags': 'meditation, mindfulness, mental wellness, relaxation',
            'meta_description': 'Learn basic meditation techniques for beginners'
        },
        
        # Disease Prevention Content
        {
            'category': 'Disease Prevention',
            'title': 'Vaccination Schedule for Children',
            'description': 'Complete vaccination schedule and importance of immunizations for children.',
            'content_type': 'pdf',
            'url': 'https://example.com/vaccination-schedule.pdf',
            'author': 'Centers for Disease Control',
            'source': 'CDC',
            'difficulty_level': 'all',
            'target_age_group': 'children',
            'is_verified': True,
            'tags': 'vaccination, immunization, children health, disease prevention',
            'meta_description': 'Official vaccination schedule for children and infants'
        },
        {
            'category': 'Disease Prevention',
            'title': 'Heart Disease Prevention Tips',
            'description': 'Lifestyle changes and habits that can help prevent heart disease and maintain cardiovascular health.',
            'content_type': 'article',
            'url': 'https://example.com/heart-disease-prevention',
            'author': 'Dr. Robert Martinez',
            'source': 'Cardiology Today',
            'difficulty_level': 'intermediate',
            'target_age_group': 'adults',
            'is_featured': True,
            'is_verified': True,
            'tags': 'heart disease, cardiovascular health, prevention, lifestyle',
            'meta_description': 'Learn how to prevent heart disease through lifestyle changes'
        }
    ]
    
    print("Creating sample health content data...")
    
    # Clear existing data (optional)
    MediaContent.objects.all().delete()
    HealthCategory.objects.all().delete()
    print("Cleared existing health content data")
    
    # Create categories
    category_objects = {}
    for cat_data in categories_data:
        category, created = HealthCategory.objects.get_or_create(
            name=cat_data['name'],
            defaults={
                'description': cat_data['description'],
                'icon': cat_data['icon'],
                'color': cat_data['color'],
                'order': cat_data['order'],
                'is_active': True
            }
        )
        category_objects[cat_data['name']] = category
        if created:
            print(f"Created category: {category.name}")
    
    # Create media content
    created_count = 0
    for content_item in content_data:
        category = category_objects[content_item['category']]
        
        content = MediaContent.objects.create(
            category=category,
            title=content_item['title'],
            description=content_item['description'],
            content_type=content_item['content_type'],
            url=content_item['url'],
            author=content_item.get('author', ''),
            source=content_item.get('source', ''),
            duration=content_item.get('duration', ''),
            difficulty_level=content_item['difficulty_level'],
            target_age_group=content_item['target_age_group'],
            is_featured=content_item.get('is_featured', False),
            is_active=True,
            is_verified=content_item.get('is_verified', False),
            tags=content_item['tags'],
            meta_description=content_item['meta_description'],
            view_count=0,
            like_count=0,
            share_count=0
        )
        
        created_count += 1
        print(f"Created content: {content.title}")
    
    print(f"\nSample health content data creation completed!")
    print(f"Created {len(categories_data)} categories")
    print(f"Created {created_count} media content items")
    print(f"Total categories in database: {HealthCategory.objects.count()}")
    print(f"Total content in database: {MediaContent.objects.count()}")
    print(f"Active content: {MediaContent.objects.filter(is_active=True).count()}")

if __name__ == '__main__':
    create_sample_health_content()
