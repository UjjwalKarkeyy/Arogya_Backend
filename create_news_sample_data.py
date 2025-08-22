#!/usr/bin/env python3
"""
Script to create sample news data for testing the news functionality.
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

from news.models import News, Category, Tag

def create_sample_news():
    """Create sample news data for testing"""
    
    # Create categories
    categories_data = [
        {'name': 'Health Updates'},
        {'name': 'Disease Prevention'},
        {'name': 'Medical Research'},
        {'name': 'Public Health'},
        {'name': 'Nutrition'},
        {'name': 'Mental Health'},
        {'name': 'Emergency Alerts'},
        {'name': 'Vaccination'},
    ]
    
    # Create tags
    tags_data = [
        'health', 'prevention', 'research', 'nutrition', 'mental-health',
        'vaccination', 'emergency', 'wellness', 'fitness', 'disease',
        'treatment', 'medicine', 'healthcare', 'public-health', 'safety'
    ]
    
    # Sample news articles
    news_data = [
        {
            'title': 'New Study Shows Benefits of Regular Exercise for Heart Health',
            'content': 'A comprehensive study involving 50,000 participants over 10 years has demonstrated that regular moderate exercise significantly reduces the risk of cardiovascular disease. The research, published in the Journal of Cardiology, shows that just 30 minutes of daily exercise can reduce heart disease risk by up to 35%. Key findings include improved blood pressure, better cholesterol levels, and enhanced overall cardiovascular function.',
            'categories': ['Health Updates', 'Medical Research'],
            'tags': ['health', 'research', 'fitness', 'prevention']
        },
        {
            'title': 'WHO Announces New Guidelines for Mental Health Support',
            'content': 'The World Health Organization has released updated guidelines for mental health support in communities worldwide. The new recommendations emphasize early intervention, community-based care, and integration of mental health services with primary healthcare. The guidelines aim to address the growing mental health crisis affecting millions globally.',
            'categories': ['Mental Health', 'Public Health'],
            'tags': ['mental-health', 'healthcare', 'wellness', 'public-health']
        },
        {
            'title': 'Breakthrough in Cancer Treatment Shows Promising Results',
            'content': 'Researchers at leading medical institutions have developed a new immunotherapy treatment that shows remarkable success in treating advanced-stage cancers. Clinical trials demonstrate a 60% improvement in patient outcomes compared to traditional treatments. The therapy works by enhancing the body\'s natural immune response to target cancer cells more effectively.',
            'categories': ['Medical Research', 'Health Updates'],
            'tags': ['research', 'treatment', 'medicine', 'health']
        },
        {
            'title': 'Seasonal Flu Vaccination Campaign Begins Nationwide',
            'content': 'Health authorities have launched the annual flu vaccination campaign, urging all eligible individuals to get vaccinated before the peak flu season. This year\'s vaccine has been updated to protect against the most prevalent strains. Free vaccination is available at healthcare centers, pharmacies, and mobile clinics across the country.',
            'categories': ['Vaccination', 'Public Health'],
            'tags': ['vaccination', 'prevention', 'public-health', 'safety']
        },
        {
            'title': 'Study Reveals Impact of Mediterranean Diet on Brain Health',
            'content': 'A long-term study has found that following a Mediterranean diet rich in olive oil, fish, nuts, and vegetables can significantly improve cognitive function and reduce the risk of dementia. Participants who adhered to the diet showed 40% slower cognitive decline compared to those following a standard diet.',
            'categories': ['Nutrition', 'Medical Research'],
            'tags': ['nutrition', 'research', 'wellness', 'prevention']
        },
        {
            'title': 'Emergency Alert: Heat Wave Safety Precautions',
            'content': 'Health officials have issued an emergency alert as temperatures are expected to reach dangerous levels this week. Citizens are advised to stay hydrated, avoid outdoor activities during peak hours, and check on elderly neighbors. Cooling centers have been opened in major cities to provide relief from extreme heat.',
            'categories': ['Emergency Alerts', 'Public Health'],
            'tags': ['emergency', 'safety', 'public-health', 'prevention']
        },
        {
            'title': 'Digital Health Apps Show Promise in Managing Chronic Diseases',
            'content': 'Recent studies indicate that mobile health applications are proving effective in helping patients manage chronic conditions like diabetes and hypertension. The apps provide medication reminders, track vital signs, and offer personalized health recommendations, leading to better patient outcomes and reduced hospital visits.',
            'categories': ['Health Updates', 'Medical Research'],
            'tags': ['healthcare', 'medicine', 'treatment', 'wellness']
        },
        {
            'title': 'Air Quality Improvement Linked to Reduced Respiratory Diseases',
            'content': 'Environmental health data shows a significant correlation between improved air quality measures and decreased rates of respiratory diseases in urban areas. Cities that implemented stricter emission controls have seen a 25% reduction in asthma and COPD cases over the past five years.',
            'categories': ['Public Health', 'Disease Prevention'],
            'tags': ['public-health', 'prevention', 'health', 'disease']
        },
        {
            'title': 'Telemedicine Adoption Continues to Transform Healthcare Access',
            'content': 'The widespread adoption of telemedicine has revolutionized healthcare delivery, particularly in rural and underserved areas. Patients can now access specialist consultations, mental health services, and routine check-ups remotely, improving healthcare accessibility and reducing costs.',
            'categories': ['Health Updates', 'Public Health'],
            'tags': ['healthcare', 'medicine', 'wellness', 'public-health']
        },
        {
            'title': 'Youth Mental Health Initiative Launches in Schools',
            'content': 'A comprehensive mental health program has been launched in schools nationwide to address the growing mental health concerns among young people. The initiative includes counseling services, peer support programs, and mental health education for students, teachers, and parents.',
            'categories': ['Mental Health', 'Public Health'],
            'tags': ['mental-health', 'wellness', 'healthcare', 'public-health']
        }
    ]
    
    print("Creating sample news data...")
    
    # Clear existing data (optional)
    News.objects.all().delete()
    Category.objects.all().delete()
    Tag.objects.all().delete()
    print("Cleared existing news data")
    
    # Create categories
    category_objects = {}
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(name=cat_data['name'])
        category_objects[cat_data['name']] = category
        if created:
            print(f"Created category: {category.name}")
    
    # Create tags
    tag_objects = {}
    for tag_name in tags_data:
        tag, created = Tag.objects.get_or_create(name=tag_name)
        tag_objects[tag_name] = tag
        if created:
            print(f"Created tag: {tag.name}")
    
    # Create news articles
    created_count = 0
    for news_item in news_data:
        news = News.objects.create(
            title=news_item['title'],
            content=news_item['content']
        )
        
        # Add categories
        for cat_name in news_item['categories']:
            if cat_name in category_objects:
                news.category.add(category_objects[cat_name])
        
        # Add tags
        for tag_name in news_item['tags']:
            if tag_name in tag_objects:
                news.tags.add(tag_objects[tag_name])
        
        news.save()
        created_count += 1
        print(f"Created news: {news.title}")
    
    print(f"\nSample news data creation completed!")
    print(f"Created {len(categories_data)} categories")
    print(f"Created {len(tags_data)} tags")
    print(f"Created {created_count} news articles")
    print(f"Total news in database: {News.objects.count()}")

if __name__ == '__main__':
    create_sample_news()
