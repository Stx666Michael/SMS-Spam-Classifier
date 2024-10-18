# classifier/views.py
from rest_framework.views import APIView
from django.shortcuts import render
from .serializers import SMSSerializer
from .utils import preprocess_data, classify_sms

class SMSClassificationView(APIView):
    def get(self, request):
        return render(request, 'index.html')

    def post(self, request):
        serializer = SMSSerializer(data=request.data)
        if serializer.is_valid():
            sms = serializer.validated_data['sms']
            clean_sms = preprocess_data(sms)
            classification, probability = classify_sms(clean_sms)
            return render(request, 'index.html', {
                'sms': sms,
                'classification': classification,
                'probability': int(probability * 100)
            })
        return render(request, 'index.html', {'errors': serializer.errors})
