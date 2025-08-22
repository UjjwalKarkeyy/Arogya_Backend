#!/usr/bin/env python
"""
Script to create sample FAQ data for Helpline functionality
Run this after starting the Django server to populate test data
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Arogya_Backend.settings')
django.setup()

from helpLine.models import FAQ
from django.contrib.auth.models import User

def create_sample_data():
    print("Creating sample helpline FAQ data...")
    
    # Create sample FAQs for different categories
    faqs_data = [
        # Mental Health Category
        {
            "question": "What is anxiety and how can I recognize it?",
            "answer": "Anxiety is a natural response to stress that can become overwhelming. Common symptoms include excessive worry, restlessness, difficulty concentrating, muscle tension, and sleep problems. If these symptoms persist and interfere with daily life, consider seeking professional help.",
            "category": "Mental Health"
        },
        {
            "question": "How can I manage stress effectively?",
            "answer": "Effective stress management includes regular exercise, adequate sleep, healthy eating, deep breathing exercises, meditation, and maintaining social connections. Setting realistic goals and learning to say no can also help reduce stress levels.",
            "category": "Mental Health"
        },
        {
            "question": "When should I seek professional mental health support?",
            "answer": "Seek professional help if you experience persistent sadness, anxiety, or mood changes that last more than two weeks, thoughts of self-harm, substance abuse, or if mental health issues interfere with work, relationships, or daily activities.",
            "category": "Mental Health"
        },
        
        # Physical Health Category
        {
            "question": "How much exercise do I need for good health?",
            "answer": "Adults should aim for at least 150 minutes of moderate-intensity aerobic activity or 75 minutes of vigorous-intensity activity per week, plus muscle-strengthening activities on 2 or more days per week.",
            "category": "Physical Health"
        },
        {
            "question": "What constitutes a balanced diet?",
            "answer": "A balanced diet includes fruits, vegetables, whole grains, lean proteins, and healthy fats. Limit processed foods, added sugars, and excessive sodium. Stay hydrated by drinking plenty of water throughout the day.",
            "category": "Physical Health"
        },
        {
            "question": "How many hours of sleep do I need?",
            "answer": "Most adults need 7-9 hours of quality sleep per night. Maintain a consistent sleep schedule, create a relaxing bedtime routine, and avoid screens before bedtime for better sleep quality.",
            "category": "Physical Health"
        },
        
        # Emergency Category
        {
            "question": "What should I do in a medical emergency?",
            "answer": "Call emergency services immediately (dial 102 in Nepal). Stay calm, provide clear information about the situation and location. If trained, provide first aid while waiting for help. Do not move someone with potential spinal injuries unless they're in immediate danger.",
            "category": "Emergency"
        },
        {
            "question": "How do I recognize signs of a heart attack?",
            "answer": "Common signs include chest pain or discomfort, shortness of breath, nausea, lightheadedness, and pain in arms, back, neck, or jaw. Women may experience different symptoms. Call emergency services immediately if you suspect a heart attack.",
            "category": "Emergency"
        },
        {
            "question": "What are the signs of a stroke?",
            "answer": "Remember FAST: Face drooping, Arm weakness, Speech difficulty, Time to call emergency services. Other signs include sudden confusion, trouble seeing, severe headache, or loss of balance. Act quickly - time is critical in stroke treatment.",
            "category": "Emergency"
        },
        
        # Nutrition Category
        {
            "question": "How much water should I drink daily?",
            "answer": "Most adults should drink about 8 glasses (64 ounces) of water daily, but needs vary based on activity level, climate, and individual factors. Monitor your urine color - pale yellow indicates good hydration.",
            "category": "Nutrition"
        },
        {
            "question": "Are supplements necessary for good health?",
            "answer": "Most people can get necessary nutrients from a balanced diet. However, some may benefit from specific supplements like vitamin D, B12 (especially vegetarians), or folic acid (pregnant women). Consult a healthcare provider before starting supplements.",
            "category": "Nutrition"
        },
        {
            "question": "How can I reduce my sugar intake?",
            "answer": "Read food labels carefully, choose whole fruits over fruit juices, limit processed foods, use natural sweeteners in moderation, and gradually reduce added sugars to allow your taste buds to adjust.",
            "category": "Nutrition"
        },
        
        # General Health Category
        {
            "question": "How often should I have health checkups?",
            "answer": "Generally, annual checkups are recommended for adults. However, frequency may vary based on age, health conditions, and risk factors. Your healthcare provider can recommend an appropriate schedule for your specific needs.",
            "category": "General"
        },
        {
            "question": "What vaccines do adults need?",
            "answer": "Adults typically need annual flu vaccines, tetanus boosters every 10 years, and may need others based on age, health conditions, travel, or occupation. Consult your healthcare provider for personalized vaccine recommendations.",
            "category": "General"
        },
        {
            "question": "How can I boost my immune system naturally?",
            "answer": "Maintain a healthy diet rich in fruits and vegetables, exercise regularly, get adequate sleep, manage stress, avoid smoking, limit alcohol, wash hands frequently, and stay up to date with vaccinations.",
            "category": "General"
        }
    ]
    
    # Create or update FAQs
    for faq_data in faqs_data:
        faq, created = FAQ.objects.get_or_create(
            question=faq_data["question"],
            defaults={
                "answer": faq_data["answer"],
                "category": faq_data["category"]
            }
        )
        if created:
            print(f"Created FAQ: {faq_data['question'][:50]}...")
        else:
            # Update existing FAQ if needed
            faq.answer = faq_data["answer"]
            faq.category = faq_data["category"]
            faq.save()
            print(f"Updated FAQ: {faq_data['question'][:50]}...")
    
    # Create a default user for chat functionality if it doesn't exist
    default_user, created = User.objects.get_or_create(
        username='default_user',
        defaults={
            'email': 'default@example.com',
            'first_name': 'Default',
            'last_name': 'User'
        }
    )
    if created:
        print("Created default user for chat functionality")
    
    print(f"\nSample data creation completed!")
    print(f"Total FAQs: {FAQ.objects.count()}")
    print(f"Categories: {FAQ.objects.values_list('category', flat=True).distinct().count()}")
    
    # Print category breakdown
    categories = FAQ.objects.values_list('category', flat=True).distinct()
    for category in categories:
        count = FAQ.objects.filter(category=category).count()
        print(f"  - {category}: {count} FAQs")

if __name__ == "__main__":
    create_sample_data()
