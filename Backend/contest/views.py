# -*- coding: utf-8 -*-
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.throttling import ScopedRateThrottle
from rest_framework import viewsets, mixins, filters
from rest_framework.permissions import IsAuthenticated
from .permission import ManagerOnly, UserRatingOnly, UserRatingOnly2, UserOnly, UserOnly1
from .models import ContestBoardTotal, ContestComingInfo,ContestTutorial, ContestAnnouncement, ContestRatingChange, ContestBoard, ContestComment, ContestInfo, ContestProblem, ContestRegister, StudentChoiceAnswer, ContestChoiceProblem
from problem.models import ChoiceProblem
from .serializers import ContestBoardTotalSerializer, ContestComingInfoSerializer,ContestTutorialSerializer, ContestRatingChangeSerializer, ContestAnnouncementSerializer, ContestBoardSerializer, ContestCommentSerializer, ContestInfoSerializer, ContestProblemSerializer, ContestRegisterSerializer, StudentChoiceAnswerSerializer, ContestChoiceProblemSerializer
import datetime

from user.models import User


class ContestAnnouncementView(viewsets.ModelViewSet):
    queryset = ContestAnnouncement.objects.all()
    serializer_class = ContestAnnouncementSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (ManagerOnly,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("contestid",)
    throttle_scope = "post"
    throttle_classes = [ScopedRateThrottle, ]

class ContestTutorialView(viewsets.ModelViewSet):
    queryset = ContestTutorial.objects.all()
    serializer_class = ContestTutorialSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (ManagerOnly,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("contestid",)
    throttle_scope = "post"
    throttle_classes = [ScopedRateThrottle, ]


class ContestBoardView(viewsets.ModelViewSet):
    queryset = ContestBoard.objects.all()
    serializer_class = ContestBoardSerializer
    permission_classes = (UserRatingOnly,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("contestid","username","problemrank","type",)
    throttle_scope = "post"
    throttle_classes = [ScopedRateThrottle, ]


class ContestCommentView(viewsets.ModelViewSet):
    queryset = ContestComment.objects.all()
    serializer_class = ContestCommentSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (UserRatingOnly2,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("contestid","problem",)
    throttle_scope = "post"
    throttle_classes = [ScopedRateThrottle, ]


class ContestInfoView(viewsets.ModelViewSet):
    queryset = ContestInfo.objects.all().order_by('-id')
    serializer_class = ContestInfoSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (ManagerOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filter_fields = ("begintime", "level", "type","title","classes")
    search_fields = ('title',)
    throttle_scope = "post"
    throttle_classes = [ScopedRateThrottle, ]


class ContestComingInfoView(viewsets.ModelViewSet):
    queryset = ContestComingInfo.objects.all().order_by('startTime')
    serializer_class = ContestComingInfoSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (ManagerOnly,)
    throttle_scope = "post"
    throttle_classes = [ScopedRateThrottle, ]


class ContestProblemView(viewsets.ModelViewSet):
    queryset = ContestProblem.objects.all().order_by('rank')
    serializer_class = ContestProblemSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (ManagerOnly,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('contestid',)
    throttle_scope = "post"
    throttle_classes = [ScopedRateThrottle, ]


class ContestRegisterView(viewsets.ModelViewSet):
    queryset = ContestRegister.objects.all()
    serializer_class = ContestRegisterSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (UserRatingOnly2,)
    filter_fields = ('user', "contestid")
    throttle_scope = "post"
    throttle_classes = [ScopedRateThrottle, ]


class ContestRatingChangeView(viewsets.ModelViewSet):
    queryset = ContestRatingChange.objects.extra(
        select={'t': 'contesttime+0'}).extra(order_by=["t"])
    serializer_class = ContestRatingChangeSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (ManagerOnly,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('user', "contestid")
    throttle_scope = "post"
    throttle_classes = [ScopedRateThrottle, ]


class CurrentTimeView(APIView):
    def get(self, request):
        return Response(datetime.datetime.now(), HTTP_200_OK)


class ContestBoardTotalView(viewsets.ModelViewSet):
    queryset = ContestBoardTotal.objects.all()
    serializer_class = ContestBoardTotalSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (ManagerOnly,)
    filter_fields = ('user','nickname', "contestid")
    throttle_scope = "post"
    throttle_classes = [ScopedRateThrottle, ]


class ContestBoardFilterAPIView(APIView):

    throttle_scope = "post"
    throttle_classes = [ScopedRateThrottle, ]

    def post(self, request, format=None):
        # if request.session.get("type") != 3:
        #     return Response("nopermission", status=HTTP_400_BAD_REQUEST)

        data = request.data

        contestid = data.get("contestid")
        schoolname = data.get("school","")
        coursename = data.get("course","")
        classname = data.get("class","")
        reslist = []
        boards = ContestBoard.objects.filter(contestid=contestid)

        usermap = {}

        for b in boards:
            username = b.username
            if usermap.get(username,None)!=None:
                if usermap.get(username) == True:
                    reslist.append(b)
                continue

            user = User.objects.get(username=username)
            flag = True

            if schoolname != "":
                if str(user.school) != str(schoolname):
                    flag = False

            if coursename != "":
                if str(user.course) != str(coursename):
                    flag = False

            if classname != "":
                if str(user.classes) != str(classname):
                    flag = False

            if flag == True:
                reslist.append(b)

            usermap[username] = flag

       # res = ContestBoard.objects.filter(pk__in=reslist)
        return Response(ContestBoardSerializer(reslist,many=True).data, HTTP_200_OK)


class StudentChoiceAnswerView(viewsets.ModelViewSet):
    queryset = StudentChoiceAnswer.objects.all()
    serializer_class = StudentChoiceAnswerSerializer
    permission_classes = (UserOnly,UserOnly1)
    filter_fields = ('username','contestid')



class ContestChoiceProblemView(viewsets.ModelViewSet):
    queryset = ContestChoiceProblem.objects.all().order_by('rank')
    serializer_class = ContestChoiceProblemSerializer
    permission_classes = (ManagerOnly,)
    filter_fields = ('ContestId','ChoiceProblemId', "rank")
    throttle_scope = "post"

class GetContestChoiceProblems(APIView):
    throttle_scope = "post"
    throttle_classes = [ScopedRateThrottle, ]
    permission_classes = (UserOnly,UserOnly1)
    def post(self, request, format=None):
        try:
            #获取比赛id
            data = request.data
            if type(data) != dict:
                data = data.dict()
            contestid = int(data['ContestId'])
            #此次比赛的选择题
            all_contest_choice_problem=[]
            #获取此次比赛的选择题的id,根据rank排序
            contest_choice_problem = ContestChoiceProblem.objects.filter(ContestId = contestid).order_by('rank')
            contest_choice_problem_id=[]
            #储存此次比赛的选择题的id
            for pro in contest_choice_problem:
                contest_choice_problem_id.append(int(pro.ChoiceProblemId))
            #获取具体的选择题
            for pro_id in contest_choice_problem_id:
                cproblem = ChoiceProblem.objects.filter(ChoiceProblemId=pro_id)
                single_pro = {}
                for cpro in cproblem:
                    #这个循环应该只会执行一遍
                    single_pro['des']=cpro.des
                    single_pro['A']=cpro.choiceA
                    single_pro['B']=cpro.choiceB
                    single_pro['C']=cpro.choiceC
                    single_pro['D']=cpro.choiceD
                    single_pro['cpro_id']=cpro.ChoiceProblemId
                all_contest_choice_problem.append(single_pro)

            return Response(all_contest_choice_problem, HTTP_200_OK)
        except Exception as e:
            print (e)

class ScoreContestChoiceProblems(APIView):
    throttle_scope = "post"
    throttle_classes = [ScopedRateThrottle, ]
    permission_classes = (ManagerOnly,UserOnly1)
    def post(self, request, format=None):
        try:
            #获取比赛id
            data = request.data
            if type(data) != dict:
                data = data.dict()
            #比赛ID
            contestid = int(data['ContestId'])
            #选择题标答
            cpro_answer = data['ChoiceProblemAnswer'].upper()
            #一道选择题的分值
            one_pro_score = int(data['one_pro_score'])

            #此次比赛学生选择题答案
            stu_cpro_info = StudentChoiceAnswer.objects.filter(contestid = contestid)
            stu_score = 0
            for stu_info in stu_cpro_info:
                stu_ans = stu_info.answer
                stu_score = 0
                for i in range(len(cpro_answer)):
                    if(str(cpro_answer[i]) == str(stu_ans[i])):
                        stu_score += one_pro_score
                StudentChoiceAnswer.objects.filter(contestid = contestid, username = stu_info.username).update(score = stu_score)
            return Response('评阅完成，刷新页面查看最新数据',HTTP_200_OK)
        except Exception as e:
            print (e)
        