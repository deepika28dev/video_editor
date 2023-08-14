from rest_framework import generics
from rest_framework.response import Response
from .models import *
from .serializer import *
from moviepy.video.io.VideoFileClip import VideoFileClip
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import os 
from django.conf import settings
from moviepy.video.tools.drawing import circle
from PIL import Image
from moviepy.video.io.VideoFileClip import VideoFileClip





class ThumbnailView(generics.CreateAPIView):
      @csrf_exempt 
      @action(detail=False, methods=['post'])
      def post(self, request, format=None):
            video= request.data.get('video')
            title=request.data.get('title')
            start= int(request.data.get('startTime'))
            end= int(request.data.get('endTime'))
            if not video:
                 return Response({"message":"video is required","status":"400"})
            
            if not title:
                 return Response({"message":"title is required","status":"400"})
            
            video_data=Clips.objects.create(video=video,title=title)
            serializer = VideoClipSerializer(data=video_data)
            video_data.save() 
            video_id=video_data.id

            k= Clips.objects.filter(id=video_data.id).values('id','video')
            video1=k[0]['video']
            video_path = os.path.join(settings.BASE_DIR, 'static','media',str(video1))
            clip2 = VideoFileClip(video_path)
            thumbnail = clip2.get_frame(5)
            clip2.close()
            image = Image.fromarray(thumbnail)
            thumbnail_size = (300, 200) # Width, height
            image.thumbnail(thumbnail_size)
            thumbnail_path = "static/media/thumbnail/"+str(video_id)+".jpg"
            image.save(thumbnail_path)
            image.save(thumbnail_path)
            Clips.objects.filter(id=video_data.id).update(thumbnail_url=settings.BASE_URL+thumbnail_path)
            return Response({"message":"thumbnail successfully created","status":"200","thumbnail_url":settings.BASE_URL+thumbnail_path,"video":settings.BASE_URL+video1,"title":title,"video_id":str(video_id)})

class RenameTitleThumbnail(generics.CreateAPIView):
      @csrf_exempt 
      @action(detail=False, methods=['post'])
      def post(self, request, format=None):
            title= request.data.get('title')
            video_id=request.data.get('video_id')
            if not title:
                 return Response({"message":"title is required","status":"400"})
            if not video_id:
                 return Response({"message":"title is required","status":"400"})
            if not Clips.objects.filter(id=video_id).exists():
              return Response({"message":"invalid video detail","status":"400"})
            else:
                 if title:
                   data=Clips.objects.filter(id=video_id).update(title=title)
                   video_data=Clips.objects.filter(id=video_id).values('thumbnail_url')
                   thumbnail_url=video_data[0]['thumbnail_url']
                   return Response({"message":"thumbnail rename successfully","status":"200","title":title,"thumbnail_url":thumbnail_url})

# create subclip and thumbnail
class VideoView(generics.CreateAPIView):
     @csrf_exempt 
     @action(detail=False, methods=['post'])
     def post(self, request, format=None):
          viideo= request.data.get('video')
          start= int(request.data.get('startTime'))
          end= int(request.data.get('endTime'))
          title= request.data.get('title')
          if not viideo:
                 return Response({"message":"video is required","status":"400"})
            
          if not title:
                 return Response({"message":"title is required","status":"400"})
            
          video_data=Clips.objects.create(video=viideo,title=title)
          serializer = VideoClipSerializer(data=video_data)
          video_data.save() 
          print(video_data.video)
          video_id=video_data.id
          video_path = os.path.join(settings.BASE_DIR, 'static','media',str(video_data.video))
          print("video path",video_path)
          output_video_path="static/media/subclips/"+str(video_id)+".mp4"
          
          with VideoFileClip(video_path) as video:
               new = video.subclip(start, end)
               new.write_videofile(output_video_path, codec='libx264')
          Clips.objects.filter(id=video_id).update(subclips=settings.BASE_URL+output_video_path)
          clip2 = VideoFileClip(output_video_path)
          thumbnail = clip2.get_frame(1)
          clip2.close()
          image = Image.fromarray(thumbnail)
          thumbnail_size = (300, 300) # Width, height
          image.thumbnail(thumbnail_size)
          thumbnail_path = "static/media/thumbnail/thumbnail"+str(video_id)+".jpg"
          image.save(thumbnail_path)
          image.save(thumbnail_path)
          return Response({"subclip_url":settings.BASE_URL+output_video_path,"thumnail_url":settings.BASE_URL+thumbnail_path})



# Session authentication used with when we use  login and logout which is imported from from django.contrib.auth import login,logout
# views.py
from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializer import UserSerializer
from django.contrib.auth import login,logout
from django.contrib.auth import authenticate

class RegisterView(views.APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(views.APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return Response({'detail': 'Logged in successfully.'})
        return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

from django.utils.crypto import get_random_string
from rest_framework.views import APIView   

class SendOtpEmail(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):

     email=request.data.get('email')
     if not email:
        return Response({"message":"email id is required"})
     if not User.objects.filter(email=email).exists():
         return Response({"message":" please Enter valid email address"})
     else:
        otp = get_random_string(length=6, allowed_chars='0123456789')
        print(otp)
        message = f"Your OTP is {otp}"
        send_mail(
            'your otp',
            message,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        User.objects.filter(email=email).update(changepw_otp=otp)
        return Response({"message":"email successfully send to your email id","otp":otp})

class VerifyEmailView(APIView):
    permission_classes = [IsAuthenticated,]
    def post(self, request, format=None):
       email=request.data.get('email')
       otp= request.data.get('otp')
       if not email:
           return Response({"message":"please provide email"},status=status.HTTP_400_BAD_REQUEST)
       if not User.objects.filter(email=email).exists():
            return Response({"message":"invalid email"},status=status.HTTP_400_BAD_REQUEST)
       if not otp:
           return Response({"message":"please provide otp"},status=status.HTTP_400_BAD_REQUEST)
       
       if not User.objects.filter(changepw_otp=otp).exists():
            return Response({"message":"invalid email"},status=status.HTTP_400_BAD_REQUEST)
       
       else:

        updated=User.objects.filter(email=email).update(changepw_otp=None,is_verfied=True)
           
        return Response({"message":"email verified"})



class ChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):

     return Response(123)

#X-CSRFToken pass in headers which is generated in login headers when logout 
class LogoutView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        logout(request)
        return Response({'detail': 'Logged out successfully.'})



#video to audio convert
from rest_framework.views import APIView
from rest_framework.response import Response
import moviepy.editor as mp

class VideoToAudioView(APIView):
    
   def post(self, request,format=None):
        video_file = request.FILES['video_file'] 
        title=request.data.get('title')
        video_data=VideoToAudio.objects.create(video=video_file, title=title)
        serializer=VideoToAudioSerializer(data=video_data)
        video_data.save()
        video_path = os.path.join(settings.BASE_DIR, 'static','media',str(video_data.video))
        clip = VideoFileClip(video_path)
        audio_path="static/media/audio_data/"+str(video_data.id)+".mp3"
        audio_file = clip.audio.to_audiofile(audio_path)
        VideoToAudio.objects.filter(id=video_data.id).update(audio_url=settings.BASE_URL+audio_path)
     
        return Response({"message":"success","audio_url":settings.BASE_URL+audio_path})

from django.core.mail import send_mail
class EmailView(APIView):
    def post(self, request,format=None):
        email_from = settings.EMAIL_HOST_USER
        email_to = 'deepika@codenomad.net'

        send_mail(
    'Success mail',
    'success message',
    email_from,
    [email_to],
)

        return Response({"message":"success"})
        
# get table value in json form 
from django.http import JsonResponse
class ConvertJson(APIView):
    def get(self, request,format=None):
        Products_d=list(VideoToAudio.objects.values())
        return JsonResponse({"products":Products_d},safe=False)



from django.shortcuts import get_object_or_404  
class PersonDetailView(APIView):
    def get(self, request, pk):
        person = get_object_or_404(Person, pk=pk)
        serializer = PersonSerializer(person)
        return Response(serializer.data)

from django.shortcuts import render  
from .forms import EmpForm
  
def index(request):
  if request.method == "POST":
    form = EmpForm(request.POST)
    
    if form.is_valid():
      form.save()
     
  else:
      form = EmpForm()
  return render(request, 'index.html', {'form': form})

def product_list(request):
    student = Student.objects.all()
    context = {'students': student}
    return render(request, 'students_list.html', context)

