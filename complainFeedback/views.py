from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from .models import Complains, ComplaintComment, ComplaintStatusHistory
from .serializers import ComplainsSerializer, ComplaintCommentSerializer, ComplaintStatusHistorySerializer

# Create your views here.
class ComplainViewSet(viewsets.ModelViewSet):
    queryset = Complains.objects.all()
    serializer_class = ComplainsSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)  # Added JSONParser for comments
    
    @action(detail=True, methods=['post'])
    def add_comment(self, request, pk=None):
        """Add a comment to a complaint"""
        complaint = self.get_object()
        serializer = ComplaintCommentSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(complaint=complaint)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        """Get all comments for a complaint"""
        complaint = self.get_object()
        top_level_comments = complaint.comments.filter(parent=None)
        serializer = ComplaintCommentSerializer(top_level_comments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """Update complaint status and add to history"""
        complaint = self.get_object()
        new_status = request.data.get('status')
        changed_by = request.data.get('changed_by', 'System')
        notes = request.data.get('notes', '')
        
        if new_status and new_status in dict(Complains.STATUS_CHOICES):
            # Update complaint status
            old_status = complaint.status
            complaint.status = new_status
            complaint.save()
            
            # Add to status history
            ComplaintStatusHistory.objects.create(
                complaint=complaint,
                status=new_status,
                changed_by=changed_by,
                notes=notes
            )
            
            return Response({
                'message': f'Status updated from {old_status} to {new_status}',
                'status': new_status
            })
        
        return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
    
    def create(self, request, *args, **kwargs):
        """Override create to provide better response for form submission"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            complaint = serializer.save()
            return Response({
                'success': True,
                'message': 'Complaint submitted successfully!',
                'complaint_id': complaint.id,
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'message': 'Failed to submit complaint',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def form_options(self, request):
        """Provide form options for frontend"""
        # Nepal municipalities by districts (sample data - you can expand this)
        municipalities = {
            'Kathmandu': ['Kathmandu Metropolitan City', 'Kirtipur Municipality', 'Budhanilkantha Municipality', 'Gokarneshwor Municipality', 'Kageshwori Manohara Municipality'],
            'Lalitpur': ['Lalitpur Metropolitan City', 'Godawari Municipality', 'Mahalaxmi Municipality'],
            'Bhaktapur': ['Bhaktapur Municipality', 'Changunarayan Municipality', 'Madhyapur Thimi Municipality', 'Suryabinayak Municipality'],
            'Pokhara': ['Pokhara Metropolitan City'],
            'Chitwan': ['Bharatpur Metropolitan City', 'Kalika Municipality', 'Khairahani Municipality', 'Madi Municipality'],
            'Morang': ['Biratnagar Metropolitan City', 'Sundar Haraicha Municipality', 'Rangeli Municipality'],
            'Jhapa': ['Mechinagar Municipality', 'Damak Municipality', 'Kankai Municipality', 'Birtamod Municipality'],
            'Rupandehi': ['Butwal Sub-Metropolitan City', 'Devdaha Municipality', 'Lumbini Sanskritik Municipality'],
            'Kailali': ['Dhangadhi Sub-Metropolitan City', 'Tikapur Municipality', 'Ghodaghodi Municipality'],
            'Kanchanpur': ['Bhimdatta Municipality', 'Bedkot Municipality', 'Krishnapur Municipality']
        }
        
        categories = [
            'Health Services',
            'Education',
            'Infrastructure',
            'Water Supply',
            'Electricity',
            'Transportation',
            'Sanitation',
            'Public Safety',
            'Administrative Services',
            'Other'
        ]
        
        return Response({
            'municipalities': municipalities,
            'categories': categories,
            'status_choices': dict(Complains.STATUS_CHOICES)
        })

class ComplaintCommentViewSet(viewsets.ModelViewSet):
    queryset = ComplaintComment.objects.all()
    serializer_class = ComplaintCommentSerializer
