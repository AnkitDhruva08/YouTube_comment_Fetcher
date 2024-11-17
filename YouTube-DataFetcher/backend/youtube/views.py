from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from rest_framework import authentication, permissions
from rest_framework.decorators import permission_classes
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer 
from rest_framework_simplejwt.views import TokenObtainPairView # for login page
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from .serializers import (
    UserSerializer, 
    UserRegisterTokenSerializer, 

)
import openpyxl
from openpyxl.styles import Font
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Video, Comment, Reply
from googleapiclient.discovery import build
import pandas as pd
import datetime
from io import BytesIO
from django.http import HttpResponse
import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

import google.auth  
from googleapiclient.discovery import build  

from .utils import extract_video_id

import os
from dotenv import load_dotenv

# register user
class UserRegisterView(APIView):
    """To Register the User"""

    def post(self, request, format=None):
        data = request.data # holds username and password (in dictionary)
        username = data["username"]
        email = data["email"]

        if username == "" or email == "":
            return Response({"detial": "username or email cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)

        else:
            check_username = User.objects.filter(username=username).count()
            check_email =  User.objects.filter(email=email).count()

            if check_username:
                message = "A user with that username already exist!"
                return Response({"detail": message}, status=status.HTTP_403_FORBIDDEN)
            if check_email:
                message = "A user with that email address already exist!"
                return Response({"detail": message}, status=status.HTTP_403_FORBIDDEN)
            else:
                user = User.objects.create(
                    username=username,
                    email=email,
                    password=make_password(data["password"]),
                )
                serializer = UserRegisterTokenSerializer(user, many=False)
                return Response(serializer.data)

# login user (customizing it so that we can see fields like username, email etc as a response 
# from server, otherwise it will only provide access and refresh token)
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserRegisterTokenSerializer(self.user).data

        for k, v in serializer.items():
            data[k] = v
        
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer




# get user details
class UserAccountDetailsView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            user = User.objects.get(id=pk)
            serializer = UserSerializer(user, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except:
            return Response({"details": "User not found"}, status=status.HTTP_404_NOT_FOUND)


# update user account
class UserAccountUpdateView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk):
        user = User.objects.get(id=pk)
        data = request.data

        if user:
            if request.user.id == user.id:
                user.username = data["username"]
                user.email = data["email"]

                if data["password"] != "":
                    user.password = make_password(data["password"])

                user.save()
                serializer = UserSerializer(user, many=False)
                message = {"details": "User Successfully Updated.", "user": serializer.data}
                return Response(message, status=status.HTTP_200_OK)
            else:
                return Response({"details": "Permission Denied."}, status.status.HTTP_403_FORBIDDEN)
        else:
            return Response({"details": "User not found."}, status=status.HTTP_404_NOT_FOUND)


# delete user account
class UserAccountDeleteView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):

        try:
            user = User.objects.get(id=pk)
            data = request.data

            if request.user.id == user.id:
                if check_password(data["password"], user.password):
                    user.delete()
                    return Response({"details": "User successfully deleted."}, status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response({"details": "Incorrect password."}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({"details": "Permission Denied."}, status=status.HTTP_403_FORBIDDEN)
        except:
            return Response({"details": "User not found."}, status=status.HTTP_404_NOT_FOUND)


# get billing address (details of user address, all addresses)
class UserAddressesListView(APIView):

    def get(self, request):
        user = request.user
        user_address = BillingAddress.objects.filter(user=user)
        serializer = BillingAddressSerializer(user_address, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)


# get specific address only
class UserAddressDetailsView(APIView):

    def get(self, request, pk):
        user_address = BillingAddress.objects.get(id=pk)
        serializer = BillingAddressSerializer(user_address, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


# create billing address
class CreateUserAddressView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = request.data
        
        new_address = {
            "name": request.data["name"],
            "user": request.user.id,
            "phone_number": request.data["phone_number"],
            "pin_code": request.data["pin_code"],
            "house_no": request.data["house_no"],
            "landmark": request.data["landmark"],
            "city": request.data["city"],
            "state": request.data["state"],
        }

        serializer = BillingAddressSerializer(data=new_address, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# edit billing address
class UpdateUserAddressView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk):
        data = request.data

        try:
            user_address = BillingAddress.objects.get(id=pk)

            if request.user.id == user_address.user.id:

                updated_address = {
                    "name": data["name"] if data["name"] else user_address.name,
                    "user": request.user.id,
                    "phone_number": data["phone_number"] if data["phone_number"] else user_address.phone_number,
                    "pin_code": data["pin_code"] if data["pin_code"] else user_address.pin_code,
                    "house_no": data["house_no"] if data["house_no"] else user_address.house_no,
                    "landmark": data["landmark"] if data["landmark"] else user_address.landmark,
                    "city": data["city"] if data["city"] else user_address.city,
                    "state": data["state"] if data["state"] else user_address.state,
                }

                serializer = BillingAddressSerializer(user_address, data=updated_address)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"details": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
        except:
            return Response({"details": "Not found."}, status=status.HTTP_404_NOT_FOUND)


# delete address
class DeleteUserAddressView(APIView):

    def delete(self, request, pk):
        
        try:
            user_address = BillingAddress.objects.get(id=pk)

            if request.user.id == user_address.user.id:
                user_address.delete()
                return Response({"details": "Address successfully deleted."}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"details": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
        except:
            return Response({"details": "Not found."}, status=status.HTTP_404_NOT_FOUND)









# Load environment variables from .env file
load_dotenv()

# Fetch the API Key from the environment variables
API_KEY = os.getenv('API_KEY')













def get_comments(request):
    comments = Comment.objects.all().values()
    print('comments ===<<<>>>', comments)
    return JsonResponse(list(comments), safe=False)


#  insert comment and replay into database 
class FetchDataView(APIView):
    def post(self, request):
        # Get the channel URL
        channel_url = request.data.get('channel_url')
        print('channel_url ==<<<>>>>', channel_url)

        if not channel_url:
            return Response({'error': 'Channel URL is required.'}, status=400)

        comments_and_replies = []

        try:
            # Extract video ID from the channel URL
            video_id = extract_video_id(channel_url)
            print('video_id ===<<>>>', video_id)

            if not video_id:
                return Response({'error': 'Invalid YouTube URL.'}, status=400)

            # Initialize YouTube API client
            youtube = build('youtube', 'v3', developerKey=API_KEY)
            print('YouTube client initialized')

            # Retrieve video details (e.g., title) from the video ID
            video_response = youtube.videos().list(
                part='snippet',
                id=video_id
            ).execute()

            if not video_response['items']:
                return Response({'error': 'Video not found.'}, status=404)

            # Get video title and description (if available)
            video_title = video_response['items'][0]['snippet']['title']

            # Create or get the Video object in the database
            video, created = Video.objects.get_or_create(
                video_id=video_id,
                defaults={'title': video_title}
            )
            print(f'Video: {video.title} (ID: {video.video_id})')

            # Retrieve video comments (limit to 10)
            video_response = youtube.commentThreads().list(
                part='snippet,replies',
                videoId=video_id,
                maxResults=10  # Limit to 10 comments
            ).execute()

            # Iterate through the comments and store them
            for item in video_response['items']:
                comment_data = item['snippet']['topLevelComment']['snippet']
                comment_id = item['id']
                text = comment_data['textDisplay']

                # Create the Comment object
                comment = Comment.objects.create(
                    video=video,
                    comment_id=comment_id,
                    text=text                )
                print(f'Comment  {text} saved')

                # If there are replies to this comment, store them as well
                if 'replies' in item:
                    for reply_item in item['replies']['comments']:
                        reply_data = reply_item['snippet']
                        reply_id = reply_item['id']
                        reply_author = reply_data['authorDisplayName']
                        reply_text = reply_data['textDisplay']

                        # Create the Reply object
                        Reply.objects.create(
                            comment=comment,
                            reply_id=reply_id,
                            author=reply_author,
                            text=reply_text,
                        )
                        print(f'Reply by {reply_author} saved')

            return Response({'message': 'Data is inserted successfully.'})

        except Exception as e:
            print(f"Error: {e}")
            return Response({'error': str(e)}, status=500)









def export_comments_to_excel(request):
    try:
        # Fetch all comments from the database
        comments = Comment.objects.all().values('id', 'video_id', 'comment_id', 'text')
        print('comments for download excel ===<<<>>>', comments)

        if not comments:
            return HttpResponse("No comments available to export.", status=404)

        # Create a workbook and worksheet
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Comments"

        # Add headers to the worksheet
        headers = ['ID', 'Vidoe Id','Comment ID', 'Comment Text']
        print('headers ===<<<>>>>', headers)
        for col_num, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col_num, value=header)
            cell.font = Font(bold=True)

        print('headers ===<<<>>>>', headers)
        # Write data to the worksheet
        for row_num, comment in enumerate(comments, start=2):
            ws.cell(row=row_num, column=1, value=comment['id'])
            ws.cell(row=row_num, column=2, value=comment['video_id'])
            ws.cell(row=row_num, column=3, value=comment['comment_id'])
            ws.cell(row=row_num, column=4, value=comment['text'])

        # Save the workbook to an in-memory buffer
        output = BytesIO()
        print('output ===<<<<>>>', output)
        wb.save(output)
        output.seek(0)  # Move the cursor to the beginning of the buffer

        # Create HTTP response for the Excel file
        response = HttpResponse(
            output,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="comments.xlsx"'
        return response

    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)