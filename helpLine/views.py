from rest_framework import status, viewsets
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Conversation, Message, FAQ
from .serializers import MessageSerializer
from google.generativeai import GenerativeModel, configure
from rest_framework.decorators import action
import os
import random

configure(api_key="AIzaSyBtTzE_ACdf4pUYE2uOnWB0299ZCaT_Z58")

model = GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="""You are Aura, a supportive and compassionate mental health companion chatbot. Your purpose is to provide a safe, non-judgmental space for users to express their feelings.    **Your Core Rules:**
    1.  **Always be empathetic, patient, and encouraging.** Use a calm and reassuring tone.
    2.  **Encourage users to seek professional help** for serious issues.
    3.  **CRITICAL SAFETY RULE:** If a user expresses thoughts of self-harm, suicide, or harming others, immediately and calmly provide the following crisis resource and then stop the conversation on that topic: "It sounds like you are going through a difficult time. Please consider reaching out for immediate support. You can connect with people who can support you by calling or texting 988 anytime in the US and Canada. In the UK, you can call 111."
    4.  Do not engage in debates or arguments. Your role is to listen and support.
    5. You are to give nepali numbers"""
)

class ChatViewSet(viewsets.ViewSet):
    """
    create: Send a message to Aura and receive a reply.
    POST body: {"username": "<user>", "message": "<text>"}
    Response: serialized bot Message (same as before)
    """
    def create(self, request, *args, **kwargs):
        user_id = request.data.get('username')
        user_message_text = request.data.get('message')

        if not user_id or not user_message_text:
            return Response(
                {'error': 'User ID and message are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(username=user_id)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        conversation, _ = Conversation.objects.get_or_create(user=user)

        user_message = Message.objects.create(
            conversation=conversation,
            text=user_message_text,
            is_user=True
        )

        try:
            history_messages = conversation.messages.order_by('timestamp')
            history = [
                {
                    'role': 'user' if m.is_user else 'model',
                    'parts': [{'text': m.text}]
                }
                for m in history_messages
            ]

            chat = model.start_chat(history=history)
            response = chat.send_message(user_message_text)
            bot_response_text = response.text

        except Exception as e:
            print(f"Gemini API Error: {e}")
            bot_response_text = "Sorry, I'm having trouble connecting right now. Please try again later."

        bot_message = Message.objects.create(
            conversation=conversation,
            text=bot_response_text,
            is_user=False
        )

        serializer = MessageSerializer(bot_message)
        return Response(serializer.data, status=status.HTTP_200_OK)

class FAQViewSet(viewsets.ViewSet):
    """
    list (GET /faqs/): List FAQs. Optional ?category=<name> filter.
    create (POST /faqs/): Return categories with a random emoji (preserves your current POST behavior).
    """
    def list(self, request, *args, **kwargs):
        print("Fetching FAQs")
        category = request.query_params.get('category')
        faqs = FAQ.objects.all()
        if category:
            faqs = faqs.filter(category=category)

        response_data = {
            'faqs': [{'question': faq.question, 'answer': faq.answer} for faq in faqs]
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        list_emoji = ['🧠', '💊', '🏃', '🛑', '💉']
        faqs = FAQ.objects.all()
        response_data = {
            'faqs': [{'category': faq.category, 'icon': random.choice(list_emoji)} for faq in faqs]
        }
        return Response(response_data, status=status.HTTP_200_OK)
