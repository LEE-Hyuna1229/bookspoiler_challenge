from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import NotFound

from .models import ChallengeInfo, ChallengeSpoiler, DoItComment
from .serializers import ChallengeInfoSerializer, ChallengeSpoilerSerializer, DoItCommentSerializer
from books.serializers import BookSerializer
from users.models import User
from books.models import Book
#from permissions import IsOwnerOrStaff, IsPaidUserOrStaff, IsStaff

# http method  정의    
class CreateChallenge(APIView):  # 신규챌린지 생성하기 (관리자만 가능)
    #permission_classes=[IsStaff]

    def post(self, request, book_id): 
        book = get_object_or_404(Book, pk=book_id)  # 주어진 book_id에 해당하는 Book 객체 가져오기
        request_data = request.data
        request_data['book'] = book.id

        serializer = ChallengeInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class UpdateChallenge(APIView):  # 챌린지 정보 업데이트 하기 (관리자만 가능) - ChallengeSpoiler를 불러와야하나 ?
    #permission_classes=[IsStaff]

    def post(self, request, challengeinfo_id): 
        try:
            challenge_info = ChallengeInfo.objects.get(pk=challengeinfo_id)
        except ChallengeInfo.DoesNotExist:
            return Response({"message": "Challenge not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ChallengeInfoSerializer(instance=challenge_info, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ChallengeList(APIView): # 전체 챌린지 리스트 가져오기 (관리자, 로그인유저만 가능)
    #permission_classes=[IsOwnerOrStaff]#권한부여

    def get(self, request): 
        challenges = ChallengeInfo.objects.all()
        serializer = ChallengeInfoSerializer(challenges, many = True) # object -> json
        return Response(serializer.data) # serialized된 데이터를 return
        


class  UserChallengeList(APIView): # 사용자가 신청한 챌린지 리스트 가져오기 (관리자, 결제유저만 가능)
    #permission_classes=[IsPaidUserOrStaff]

    def get(self, request, user_id):
        try:
            user_challenges = ChallengeInfo.objects.filter(user_id=user_id)
            serializer = ChallengeInfoSerializer(user_challenges, many=True)
            return Response(serializer.data)
        except ChallengeInfo.DoesNotExist:
            return Response({"error": "User challenges not found"}, status=status.HTTP_404_NOT_FOUND)
    
class UserChallengeDetail(APIView): # 신청한 챌린지 상세사항 보기(관리자, 결제유저만 가능) - 책정보,일차별스포일러 나와야함  *여기 질문
    #permission_classes=[IsPaidUserOrStaff] # 백에서 하는 기능이 맞나?,serializer 어떻게?
    def get(self, request, challengeinfo_id, user_id):
        try:
            challenge_info = ChallengeInfo.objects.get(pk=challengeinfo_id)
        except ChallengeInfo.DoesNotExist:
            return Response({"error": "Challenge not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # 챌린지 정보에 연결된 책 정보 가져오기
        #book_serializer = BookSerializer(challenge_info.book)

        # 챌린지 정보에 연결된 challengespoiler들 가져오기
        #challenge_spoilers = ChallengeSpoiler.objects.filter(challenge_info=challenge_info)
        #spoiler_serializer = ChallengeSpoilerSerializer(challenge_spoilers, many=True)

        # 챌린지에 대한 댓글들 가져오기
        #doitcomments = DoItComment.objects.filter(challengespoiler_info__challenge_info=challenge_info)
        #comment_serializer = DoItCommentSerializer(doitcomments, many=True)

        # 모든 정보를 조합하여 응답 데이터 구성
        response_data = {
            "challenge_info" : ChallengeInfoSerializer(challenge_info).data,
            #"book_info": book_serializer.data,
            #"challenge_spoilers": spoiler_serializer.data,
            #"doitcomments": comment_serializer.data
        }

        return Response(response_data)


class UserChallengeDo(APIView):  # 챌린지 참여현황 가져오기 - 몇 % 진행됬는지 - 구현 순서 중

    def get(self, request, user_id):
        # 해당 사용자가 신청한 모든 챌린지 가져오기
        user_challenges = ChallengeInfo.objects.filter(user_id=user_id)
        user_doing = []

        for challenge_info in user_challenges:
            total_days = 5  # 도전 챌린지 총 day 수
            challenge_spoilers = ChallengeSpoiler.objects.filter(challenge_info=challenge_info)
            completed_days = 0

            for day in range(1, total_days + 1):
                # 해당 챌린지의 특정 일차별 스포일러 가져오기
                try:
                    spoiler = challenge_spoilers.get(day=str(day))
                except ChallengeSpoiler.DoesNotExist:
                    continue
                
                # 해당 일차별 스포일러에 달린 사용자의 댓글 수 계산
                comment_days = DoItComment.objects.filter(challengespoiler_info=spoiler, user_id=user_id).count()
                if comment_days > 0:
                    completed_days += 1

            # 챌린지의 완료 일수를 기반으로 사용자의 수행 백분율 계산
            doing_percentage = (completed_days / total_days) * 100
            user_doing.append({
                'user_id': user_id,
                'challengeinfo_id': challenge_info.id,
                'user_doing': int(doing_percentage)  # 소수점 이하 버림
            })

        return Response(user_doing)

# ChallengeSpoiler 댓글 관련 기능
class ChallengeSpoilerComment(APIView): #챌린지 스포일러에 전체 댓글 가져오기 (관리자, 결제유저만 가능)
    #permission_classes = [IsPaidUserOrStaff]

    def get(self, request, challengespoiler_id):
        try:
            challengespoiler = ChallengeSpoiler.objects.get(pk=challengespoiler_id)
        except ChallengeSpoiler.DoesNotExist:
            return Response({"error": "ChallengeSpoiler not found"}, status=status.HTTP_404_NOT_FOUND)

        # challengespoiler_id에 연결된 DoItComment 댓글들을 가져옵니다.
        doit_comments = DoItComment.objects.filter(challengespoiler_info=challengespoiler)
        serializer = DoItCommentSerializer(doit_comments, many=True)
        return Response(serializer.data)
    
class CreateDIComment(APIView):  #챌린지 스포일러에 댓글 생성하기 (관리자, 결제유저만 가능)
    #permission_classes = [IsPaidUserOrStaff]

    def post(self, request, challengespoiler_id):
        try:
            challengespoiler = ChallengeSpoiler.objects.get(pk=challengespoiler_id)
        except ChallengeSpoiler.DoesNotExist:
            return Response({"error": "ChallengeSpoiler not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # 요청 데이터에 spoiler_id와 user 정보 추가하여 DoItCommentSerializer 생성
        data_with_challengespoiler_id = request.data.copy()
        data_with_challengespoiler_id['challengespoiler_info'] = challengespoiler_id
        data_with_challengespoiler_id['user'] = request.user.id  # 현재 사용자 정보를 추가
        
        serializer = DoItCommentSerializer(data=data_with_challengespoiler_id)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UpdateDIComment(APIView): # 챌린지용 스포일러에 댓글 업데이트 하기 (관리자, 결제유저만 가능)
    #permission_classes = [IsPaidUserOrStaff]

    def put(self, request, doitcomment_id): 
        try:
            doit_comment = DoItComment.objects.get(pk=doitcomment_id)
        except DoItComment.DoesNotExist:
            return Response({"message": "DoItComment not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = DoItCommentSerializer(doit_comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DeleteDIComment(APIView): # 챌린지용 스포일러에 댓글 삭제학기 (관리자, 결제유저만 가능)
    #permission_classes = [IsPaidUserOrStaff]
    
    def post(self, request, doitcomment_id): 
        doitcomment_id = request.data.get('doitcomment_id')

        if not doitcomment_id:
            return Response({"error":"사용자가 아닙니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            doitcomment = DoItComment.objects.get(id=doitcomment_id)
        except DoItComment.DoesNotExist:
            return Response({"message": "DoItComment not found"}, status=status.HTTP_404_NOT_FOUND)
        
        doitcomment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# class TotalChallenge(APIView): # 총 진행중인 챌린지 개수 가져오기 - 구현 순서 하
#     def get(self, request):
#         # 총 챌린지 개수, pay_id 에서 challenge_id 중복빼고 개수?

