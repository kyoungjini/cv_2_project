from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from .models import OutfitInfo
from .serializers import OutfitSerializer

from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpResponse
from django.http import JsonResponse

# Create your views here.

@api_view(['GET', 'POST'])
def process_image(request):
    print("넘어왔당")
    img_file = request.FILES.get('image')
    if img_file:
        try:
            image = Image.open(img_file)
            print("요기부터")
            # 이미지 처리 작업을 수행
            processed_image = image
            output_io = BytesIO()
            processed_image.save(output_io, format='JPEG')
            print("요기까지 오류 처리")
            
            # 이미지를 HttpResponse에 삽입
            response = HttpResponse(content_type='image/jpeg')  # 이미지 타입에 따라 변경 가능
            processed_image.save(response, format='JPEG')  # 이미지를 HttpResponse에 저장
            
            response = HttpResponse(content_type='image/jpeg')
            response.write(output_io.getvalue())

            return response
        except Exception as e:
            # 이미지 처리 중 예외가 발생한 경우 오류 응답 반환
            response_data = {'message': f'이미지 처리 오류: {str(e)}'}
            return JsonResponse(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        # 이미지가 전송되지 않았을 경우 오류 응답 반환
        response_data = {'message': '이미지를 찾을 수 없습니다.'}
        return JsonResponse(response_data, status=status.HTTP_400_BAD_REQUEST)
    
    # image = Image.open(img_file)
    # # 여기서 Pillow를 사용하여 원하는 작업 수행 (크기 조절, 필터 적용 등)
    # print("이상해")
    # # 처리된 이미지를 다시 InMemoryUploadedFile 객체로 변환
    # output_io = BytesIO()
    # image.save(output_io, format='JPEG')  # 원하는 포맷으로 저장
    # processed_image = InMemoryUploadedFile(
    #     output_io, None, img_file.name, 'image/jpeg',
    #     output_io.tell, None
    # )
    # return

class OutfitsAPI(APIView):
    def get(self, request):
        request.body
        outfits = OutfitInfo.objects.all()
        serializer = OutfitSerializer(outfits, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request):
        # 데이터 처리하고 image_url, shopping_url 가져오기
        count = 3
        response_data = {
            'count': count,
            'upper': [{'image_url': 'abc', 'shopping_url': 'Abc'}] * count,
            'lower': [{'image_url': 'abc', 'shopping_url': 'Abc'}] * count,
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    

class OutfitAPI(APIView):    
    def get(self, request, oid):
        outfit = get_object_or_404(OutfitInfo, oid=oid)
        serializer = OutfitSerializer(outfit)
        return Response(serializer.data, status=status.HTTP_200_OK)