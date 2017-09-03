from django.shortcuts import render, HttpResponse,redirect
from django.http import JsonResponse
from .models import mobiletask, mobileid, softid, QQFriends, QQFriendslog,QQGroup,QQGrouplog,QQGroupList,QQGroupListlog, UserPortrait,softid
import json
from datetime import datetime, timedelta
from django.core import serializers
# Create your views here.
#------- AUTOSERVER FLOW--------#
#1. mobiles method ='get' server  'task values'
#2. server auto1 make task
#3. mobile sort Deal With
#4. mysql 'mobiletask' is tasklist, other is  userid and SortMessage
# [ ] Add
#   [ ] friend
#        [ ] time在系统分发
#        [ ] number从当日列表计算
#        [ ] 列表是通过算法完成
#   [ ] Group.User
#   [ ]  Group
# [ ] Get.
#   [ ] Friend list.
#       [ ] 判断值是否和服务器一致
#       [ ] 如果不一致从新数据跑一次
#   [ ] Group user list.
#   [ ] Group. list.
# [ ] Change.ip
# [ ] Change name.
#   [ ] 在检测的时是否在数据有这个号如果没有就点击查看，并修改名字
# [ ] Send.
#   [ ] Space.
#   [ ] Message.
#   [ ] Say.
# [ ] interactivity
#   [ ] Like.
#   [ ] Get information.
#------- AUTOSERVER FLOW--------#


def index(request):
    if request.method=='GET':
        UserPortraitlist = UserPortrait.objects.all()
        return render(request, 'autoweb/autoweb.html', {"UserPortraitlist":UserPortraitlist})
    if request.method=='POST':
        UserPortrait_Id = int(request.POST['UserPortrait'])
        TaskSort = int(request.POST['TaskSort'])
        GetMobilelist = mobileid.objects.filter(UserPortraitId=UserPortrait_Id)
        UserPortraitid = request.POST['UserPortrait']
        getlist = request.POST['getlist'].split(',')
        sendcontains = request.POST['sendcontains']
        softname = 0
        try:
            wechat = int(request.POST['wechat'])
        except:
            wechat=0
        try:
            QQ = int(request.POST['QQ'])
        except:
            QQ = 0
        if QQ == 1:
            softname = 1
        elif wechat == 1:
            softname = 2

        ##1. add firends
        #2. add group
        #5. Send assign firends
        #6. Send assign Group
        if TaskSort == 1 or TaskSort == 2 or TaskSort == 5 or TaskSort == 6 or TaskSort == 9:
            for Qs in getlist:
                if Qs.__len__() < 5:
                    del getlist[getlist.index(Qs):]
                    continue
                if TaskSort == 1:
                    if QQFriends.objects.filter(QQfriends=int(Qs)).__len__() > 2:
                        del getlist[getlist.index(Qs):]
                        continue
                elif TaskSort == 2:
                    if QQGroup.objects.filter(QQfriends=int(Qs)).__len__() > 2:
                        del getlist[getlist.index(Qs):]
                        continue

                softobname = softid.objects.get(id=softname)
                userportraitIdget = UserPortrait.objects.get(id=int(UserPortrait_Id))
                createtask = mobiletask.objects.create(UserPortraitId=userportraitIdget, content=sendcontains,taskSort=TaskSort,
                                                       softid=softobname, AccountId=int(Qs))
                createtask.save()
                return redirect('/autoweb/')
        #3. sendALL firends
        #4. sendALL Group
        if TaskSort == 3 or TaskSort == 4 or TaskSort == 7 or TaskSort == 8:
                softobname = softid.objects.get(id=softname)

                userportraitIdget = UserPortrait.objects.get(id=int(UserPortrait_Id))
                getsendlist = mobileid.objects.filter(UserPortraitId=userportraitIdget)
                for getsendlistfor in getsendlist:
                    createtask = mobiletask.objects.create(UserPortraitId=userportraitIdget, content=sendcontains,taskSort=TaskSort,softid=softobname,mobileid=getsendlistfor)
                    createtask.save()
                return redirect('/autoweb/')


mobiletask_taskSort_choices = (
    (1, 'add_User'),
    (2, 'ADD_GROUP'),
    (3, 'send_message_to_friend_list'),
    (4, 'send_message_to_GROUP_list'),
    (5, 'send_message_to_user_Accoutid'),
    (6, 'send_message_to_GROUP_Accoutid'),
    (7, 'Get_Pople_list'),
    (8, 'Get_Group_list'),
    (9, 'Get_Group_QQ_list'),
)



def Task(request, mobile_ID = ''):
    if request.method=='POST':
        mobileID = mobileid.objects.get(id=int(mobile_ID))
        locktime = datetime.now() - timedelta(minutes=1)
        task = mobiletask.objects.filter(mobileid=mobileID, status=1).filter(startTime__lt=datetime.now())
        if not task.exists():
            task = mobiletask.objects.filter(UserPortraitId=mobileID.UserPortraitId, status=1).filter(startTime__lt=datetime.now())
            if not task.exists():
                return HttpResponse(0)
            else:
                task=task[0]
                task.mobileid=mobileID
                task.startTime=locktime
                task.save()
        task = mobiletask.objects.filter(mobileid=mobileID, status=1).filter(startTime__lt=datetime.now())
        task = task[0]
        taskdict ={
            'deviceName':task.mobileid.deviceName,
            'platformVersion':task.mobileid.platformVersion,
            'appActivity':task.softid.appActivity,
            'appPackage':task.softid.appPackage,
            'taskSort':task.taskSort,
            'AccountId': task.AccountId,
            'content': task.content,
            'startTime': task.startTime,
            'endTime': task.endTime,
            'statusTime': task.statusTime,
            'status': task.status,
            'webserverurl':task.mobileid.webserverurl,
            'udid':task.mobileid.udid,
            'mobileID':task.mobileid_id,
            'taskid':task.id,
            'QQ':task.mobileid.QQ,
        }
        return JsonResponse(taskdict, safe=False)

def TaskDone(request, task_id = ''):
    if request.method=='POST':
        task = mobiletask.objects.get(id=task_id, status=1)
        task.status=2
        task.endTime=datetime.now()
        task.save()
    return HttpResponse('1')
def TaskDone(request, task_id = '', task_sort=''):
    print(type(task_sort))
    if request.method=='POST':
        task = mobiletask.objects.get(id=task_id, status=1)
        #task.status=2
        #task.endTime=datetime.now()
        #task.save()
        if int(task_sort) == 3:
            QqFList_1 = QQFriends.objects.filter(QQ=task.mobileid.QQ)
            QqFList = []
            for QQFlistN in QqFList_1:
                QqFList.append(QQFlistN.QQFriends)
            json_data1 = json.loads(request.body)
            json_data = json_data1[task_sort]
            AddQqFList = set(QqFList) - set(json_data)
            delQqFList = set(json_data) - set(QqFList)
            if not len(AddQqFList) ==0:
                for AddQqFListN in AddQqFList:
                    QFListLog = QQFriendslog.objects.create(status=1, QQ=task.mobileid.QQ, QQFriends=AddQqFListN)
                    QFListLog.save()
                    QFListadd = QQFriends.objects.create(QQ=task.mobileid.QQ, QQFriends=AddQqFListN)
                    QFListadd.save()
            if not len(delQqFList) ==0:
                for delQqFListN in delQqFList:
                    QFListLog = QQFriendslog.objects.create(status=2, QQ=task.mobileid.QQ, QQFriends=AddQqFListN)
                    QFListLog.save()
                    QFListLog = QQFriends.objects.filter(QQ=task.mobileid.QQ, QQFriends=delQqFListN).delete()
                    QFListLog.save()
    if int(task_sort) == 4:
        QqFList_1 = QQGroup.objects.filter(QQ=task.mobileid.QQ)
        QqFList = []
        for QQFlistN in QqFList_1:
            QqFList.append(QQFlistN.QQFriends)
        json_data1 = json.loads(request.body)
        json_data = json_data1[task_sort]
        AddQqFList = set(QqFList) - set(json_data)
        delQqFList = set(json_data) - set(QqFList)
        if not len(AddQqFList) == 0:
            for AddQqFListN in AddQqFList:
                QFListLog = QQGrouplog.objects.create(status=1, QQ=task.mobileid.QQ, QQGroup=AddQqFListN)
                QFListLog.save()
                QFListadd = QQGroup.objects.create(QQ=task.mobileid.QQ, QQGroup=AddQqFListN)
                QFListadd.save()
        if not len(delQqFList) == 0:
            for delQqFListN in delQqFList:
                QFListLog = QQGrouplog.objects.create(status=2, QQ=task.mobileid.QQ, QQGroup=AddQqFListN)
                QFListLog.save()
                QFListLog = QQGroup.objects.filter(QQ=task.mobileid.QQ, QQGroup=delQqFListN).delete()
                QFListLog.save()

    if int(task_sort) == 9:
        QqFList_1 = QQGroupList.objects.filter(QQGroup=task.mobileid.QQ)
        QqFList = []
        for QQFlistN in QqFList_1:
            QqFList.append(QQFlistN.QQGroupList)
        json_data1 = json.loads(request.body)
        json_data = json_data1[task_sort]
        AddQqFList = set(QqFList) - set(json_data)
        delQqFList = set(json_data) - set(QqFList)
        if not len(AddQqFList) == 0:
            for AddQqFListN in AddQqFList:
                QFListLog = QQGrouplog.objects.create(status=1, QQ=task.mobileid.QQ, QQGroup=AddQqFListN)
                QFListLog.save()
                QFListadd = QQGroup.objects.create(QQ=task.mobileid.QQ, QQGroup=AddQqFListN)
                QFListadd.save()
        if not len(delQqFList) == 0:
            for delQqFListN in delQqFList:
                QFListLog = QQGrouplog.objects.create(status=2, QQ=task.mobileid.QQ, QQGroup=AddQqFListN)
                QFListLog.save()
                QFListLog = QQGroup.objects.filter(QQ=task.mobileid.QQ, QQGroup=delQqFListN).delete()
                QFListLog.save()
    return HttpResponse('1')

def QQID(request, QQ_ID=''):
    if request.method == 'GET':
        QQlist_temp = QQFriends.objects.filter(QQid=QQ_ID)
        QQlist = []
        for x in QQlist_temp:
            QQlist.append(x.QQFriends)
    return JsonResponse(QQlist, safe=False)
