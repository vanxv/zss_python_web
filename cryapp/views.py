from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CryOrder
from financial.models import deposit, orderBill
from goods.models import Shop, Goods
from users.models import AuthUser, pcGuidLog, jdUsername, tbUsername
import re
import requests
from django.db.models import Q, F
from django.views.generic.base import View  # View是一个get和post的一个系统，可以直接def post和get，
from django.contrib.auth import authenticate, login
from datetime import datetime, timedelta
#from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

#url切出数字和切出店铺分类
def platformUrl(self):
    if 'tmall' in self:
        platform = 'tmall'
        tempid = re.findall(r'id=(\d+)',self)
        id = tempid[0]
        res = requests.get(self)
        res.encoding="gbk"
        print(res.text)
        #next get image#
        imagetemp1 = re.findall(r'J_ImgBooth"(.*?)>', res.text) #正则切到J_ImgBooth字段
        imagetemp2 = re.findall(r'src="(.*?).jpg', imagetemp1[0]) #正则切到J_ImgBooth字段
        GoodsImage = imagetemp2[0] + '.jpg'
        if 'http' in GoodsImage:
            pass
        else:
            GoodsImage = 'https:' + GoodsImage
        #next get GoodsName
        tempGoodsname = re.findall(r'<title>(.*?)-', res.text)#获取产品名
        Goodsname = tempGoodsname[0]
        tempname = re.findall(r'<strong>(.*?)</strong>', res.text) #正则获取用户名
        shopname = tempname[0]
        shopusername = tempname[0]
    elif 'taobao' in self:
        platform = 'taobao'
        id = re.findall(r'id=(\d+)',self)[0]
        res = requests.get(self)
        res.encoding="gbk"
        print(res.text)
        #next get image#
        imagetemp1 = re.findall(r'J_ImgBooth"(.*?)>', res.text) #正则切到J_ImgBooth字段
        imagetemp2 = re.findall(r'src="(.*?).jpg', imagetemp1[0]) #正则切到J_ImgBooth字段
        GoodsImage = imagetemp2[0] + '.jpg'
        if 'http' in GoodsImage:
            pass
        else:
            GoodsImage = 'https:' + GoodsImage
        #next get GoodsName
        tempGoodsname = re.findall(r'<title>(.*?)-', res.text)#获取产品名
        Goodsname = tempGoodsname[0]
        tempusername = re.findall(r'data-nick="(.*?)"', res.text) #正则获取用户名
        tempshopname = re.findall(r'title="掌柜:(.*?)"', res.text) #正则获取用户名
        shopname = tempshopname[0]
        shopusername = tempusername[0]
    elif 'jd' in self:
        platform = 'jd'
        jd = re.findall(r'(\d+)',self)
        id = jd[0]
        GoodsImage = ''
    elif '1688' in self:
        platform = '1688'
    else:
        pass
    return id, platform, shopname ,shopusername, GoodsImage, Goodsname

def crycost(x):
    x = float(x)
    c = 10
    sellercost = round((x/100) + 10,2)
    buyercost = round(((x/100)*0.5) + 5,2)
    return sellercost, buyercost

def ordermoney(request):
    ordermoneytotal = 0
    orderMoneyFilter = CryOrder.objects.filter(Userid=request.user.id).filter(Q(Status=1),Q(Status=2),Q(Status=3),Q(Status=4))
    #orderMoneyFilter = CryOrder.objects.filter(Userid=x)
    for money in orderMoneyFilter:
        ordermoneytotal += (float(money.Money) + float(money.Express) + float(money.sellerMoney))
    return ordermoneytotal

def lockOrderAuthentication(request):
    # lock_Authentication_orders
    lockdaynumber = 33
    lockday = datetime.now() - timedelta(days=lockdaynumber)
    lockOrderSelect = CryOrder.objects.filter(buyerid=request.user.id).filter(AddTime__gt=lockday).filter(~Q(Status=0))
    lockOrderlist = []
    for CLOS in lockOrderSelect:
        if CLOS.ShopId in lockOrderlist:
            break
        else:
            lockOrderlist.append(CLOS.ShopId)

    return lockOrderlist


#save task
##Home_page_add_product
class sellerIndex(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        mymoney = deposit.objects.get(user=request.user.id)
        return render(request, 'material/seller/dashboard.html', {'mymoney':mymoney})

class seller_orders(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        pagenumber=1
        pagearray =[]
        productnumber=30
        orderslists = {}
        ordersfilter = CryOrder.objects.filter(Userid_id=request.user.id).order_by()
        pagetotal = len(ordersfilter)
        try:
            pagearray = int(productnumber/pagetotal)+1
        except:
            pagearray = 0
        orderlistid = 1
        for orderslist in ordersfilter:
            orderslists[orderlistid] = {
                'id':orderslist.id,
                'images':orderslist.GoodId.image1,
                'goodid':orderslist.GoodId,
                'shopname':orderslist.ShopId.shopname,
                'shopkeepname':orderslist.ShopId.shopkeepername,
                'Keywords':orderslist.Keywords,
                'platform':orderslist.ShopId.platform,
                'OrderSort':orderslist.OrderSort,
                'Status':orderslist.Status,
                'StartTime':orderslist.StartTime,
                'EndTime':orderslist.EndTime,
                'Note':orderslist.Note,
                'Money':orderslist.Money,
            }
            orderlistid += 1

        print(len(ordersfilter))
        return render(request, 'material/seller/table.html',{'orderslists':orderslists})

class buyerIndex(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            orderdict = {}
            select_cryorder = CryOrder.objects.filter()
            lockOrderlist = lockOrderAuthentication(request)
            for corder in select_cryorder:
                if corder.ShopId in lockOrderlist:
                    continue
                if corder.GoodId.id in orderdict:
                    orderdict[corder.GoodId.id][0] += 1
                else:
                    orderdict[corder.GoodId.id] = [1,corder.GoodId.image1,corder.GoodId.name, corder.GoodId.platform,corder.Money]
            # ------ old index
            # return render(request, 'index/index.html', {'orderdict':orderdict})
            # ------ old index
            return render(request, 'material/index.html', {'orderdict':orderdict})
        else:
            orderdict = {}
            order = CryOrder.objects.filter()
            for corder in order:
                if corder.GoodId.id in orderdict:
                    orderdict[corder.GoodId.id][0] += 1
                else:
                    orderdict[corder.GoodId.id] = [1,corder.GoodId.image1,corder.GoodId.name, corder.GoodId.platform,corder.Money]
            return render(request, 'material/index.html', {'orderdict':orderdict})


def GetGoods(request, goodid):
    if request.user.is_authenticated:
        if request.method=="GET":
            goodsview = Goods.objects.get(id=goodid)
            money = CryOrder.objects.filter(GoodId=goodid)
            # --- old product list
            #return render(request, 'product/goods.html', {'goodsview':goodsview,'money':money})
            # --- old product list
            return render(request, 'material/product.html', {'goodsview':goodsview,'money':money})

        elif request.method == "POST":
            #---Authentication blacklist
            UserBlackList = AuthUser.objects.filter(id=request.user.id, is_blacklist=1)
            if UserBlackList:
                return redirect('/')
            #---Authentication blacklist

            #-- hard authentiaction
            yesterday = datetime.now() - timedelta(hours=1)
            pcguid = pcGuidLog.objects.filter(user=request.user.id).filter(addtime__gt=yesterday)
            if pcguid.count() == 0:
                return redirect('/webbrowser/')
            #-- hard authentiaction


            #-- authentication account --#
            # platform = request.POST['platform']
            # tb = []
            # tb = ["tmall","taobao","1688"]
            # if platform in tb:
            #     platformusername = tbUsername.objects.filter(user=request.user.id)
            #     return redirect('/cryapp/buyer/orders/')
            # elif platform == 'jd':
            #     platformusername = jdUsername.objects.filter(user=request.user.id)
            #     return HttpResponseRedirect(reverse('buyerusers'))
            # -- authentication account --#
            LockOrderList = lockOrderAuthentication(request)
            goodsviews = CryOrder.objects.get(id=request.POST['cryorderid'])
            if goodsviews.ShopId in LockOrderList:
                return redirect('/')
            if pcguid:
                goodsviews = CryOrder.objects.filter(id=request.POST['cryorderid']).update(buyerid_id=request.user.id, Status=2)
                return redirect('/cryapp/buyer/orders/')
            else:
                return redirect('/')


    else:
        return render(request, 'login.html')

class Good_Index_Add(LoginRequiredMixin, View):
    ##############首页增加产品#######################
    def post(self, request, *args, **kwargs):

        # ----- get values-----#
        self.ordernumber_index_add = int(request.POST['number']) #获取数量
        global ordeordernumber_index_addrnumber
        money = float(request.POST['money'])
        sellercost, buyercost = crycost(money)
        sellercosttotal = (sellercost * self.ordernumber_index_add)
        total = float((self.ordernumber_index_add*money)+sellercosttotal)
        geteposit = deposit.objects.get(user=request.user.id)
        deposit_index_add = float(geteposit.deposit)
        cryordermoney = ordermoney(request)
        txtIndexAddUrl = request.POST['txtIndexAddUrl'] #获取链接
        keywords = request.POST['keywords'] #获取关键词
        note = request.POST['note'] #获取备注
        startdatetime = request.POST['startDate'] #获取启动时间
        endDateTime = request.POST['endDate'] #获取结束时间
        # ----- get values-----#
        def saveorder():
            while self.ordernumber_index_add > 0:
                savecryorder = CryOrder.objects.create(Userid=request.user, OrderSort=1, ShopId=saveshop, Status=1, GoodId=getGoods, StartTime=startdatetime, EndTime=endDateTime,  platform=platform, Keywords=keywords,Note=note, Money=request.POST['money'], Express=0, buyerMoney=buyercost, sellerMoney=sellercost)
                savecryorder.save()
                self.ordernumber_index_add -= 1

        def savegoods():
            saveGoods = Goods.objects.create(user=request.user, shop=saveshop, name=Goodsname, pgoods_id=id, sendaddress='', platform=platform,image1=GoodsImage,keyword1=keywords,price1=request.POST['money'],remark1=note)
            saveGoods.save()

        #deposit 
        trytotal = (total > (deposit_index_add - cryordermoney - 200))
        if trytotal == True:
            text = '余额不足请充值,'
            return render(request, 'material/seller/dashboard.html', {'test': text, 'money':deposit})
        #deposit

        #get urls values
        id,platform,shopname,shopusername,GoodsImage,Goodsname = platformUrl(txtIndexAddUrl) #用正则读取数据

        #判断产品是否存在
        tempGoodsTrue = Goods.objects.filter(pgoods_id=id, platform=platform, shop__shopname__contains=shopname)
        tempGoodsUserTrue = Goods.objects.filter(pgoods_id=id, platform=platform, shop__shopname__contains=shopname, user_id=request.user.id)
        tempShopFlase = Shop.objects.filter(shopname=shopname, platform=platform).filter(~Q(user_id=request.user.id))
        tempShopUserFlase = Shop.objects.filter(shopname=shopname, platform=platform).filter(~Q(user_id=request.user.id))
        tempShopUserTrue = Shop.objects.filter(shopname=shopname, platform=platform).filter(Q(user_id=request.user.id))

        if len(tempGoodsUserTrue) >0: #判断产品是否存在
            print('发布任务')
            saveshop = Shop.objects.get(user=request.user, shopname=shopname) #店铺名称
            saveGoods = Goods.objects.get(user=request.user, pgoods_id=id)#shop=saveshop, name=Goodsname,
            getGoods = Goods.objects.get(user=request.user, pgoods_id=id, platform=platform)
            saveorder()
        elif len(tempShopUserFlase) >0: #判断产品是否在其他账户上
            return render(request, 'material/seller/dashboard.html', {'test': '产品已存在'})
        elif len(tempShopUserTrue) >0: #判断产品是否在其他账户上
            print('发布任务，发布产品')
            saveshop = Shop.objects.get(user=request.user, shopname=shopname, shopkeepername=shopusername,platform=platform) #增加店铺
            saveshop.save()
            savegoods()
            getGoods = Goods.objects.get(user=request.user, pgoods_id=id, platform=platform)
            saveorder()
        elif len(tempShopFlase) >0: #判断产品是否在其他账户上
            return render(request, 'material/seller/dashboard.html', {'test': '店铺已存在其他人账户上'})
        else:
            print('发布店铺、发布产品、发布任务')
            saveshop = Shop.objects.create(user=request.user, shopname=shopname, shopkeepername=shopusername,platform=platform) #增加店铺
            saveshop.save()
            savegoods()
            saveorder()
        return render(request, 'material/seller/dashboard.html',{'test':'已经发布任务'})



#-------seller CRUD -----#
def cryapp_delete(request, cryorders_id = 0):
    cryorders = int(cryorders_id)
    deletecryappdate = CryOrder.objects.filter(id=cryorders).update(Status=0)
    print(cryorders)
    return render(request, 'material/seller/dashboard.html',{})


def ordersnotdone(request, cryorders_id = 0):
    cryorders = int(cryorders_id)
    notthrough = CryOrder.objects.filter(id=cryorders).update(Status=4)
    return render(request, 'material/seller/dashboard.html',{})

def ordersdone(request, cryorders_id = 0):
    cryorders = int(cryorders_id)
    # - create money
    cryordersGet = CryOrder.objects.get(id=cryorders)
    # - create money
    Createsellermoney = orderBill.objects.create(CryOrderid=cryordersGet, total_amount=(-cryordersGet.Express-cryordersGet.sellerMoney), orderBillSort=1)
    Createsellermoney.save()
    Createbuyermoney = orderBill.objects.create(CryOrderid=cryordersGet, total_amount=(cryordersGet.Express+cryordersGet.buyerMoney), orderBillSort=1)
    Createbuyermoney.save()
    CreatesellerCost = orderBill.objects.create(CryOrderid=cryordersGet, total_amount=(-cryordersGet.Money), orderBillSort=2)
    CreatesellerCost.save()
    CreatebuyerCost = orderBill.objects.create(CryOrderid=cryordersGet, total_amount=(cryordersGet.Money), orderBillSort=2)
    CreatebuyerCost.save()
    depositSeller = deposit.objects.get(user=cryordersGet.Userid)
    depositSeller.deposit = F('deposit') - (cryordersGet.Money+cryordersGet.Express+cryordersGet.sellerMoney)
    depositSeller.save()
    depositbuyer = deposit.objects.get(user=cryordersGet.buyerid_id)
    depositbuyer.deposit = F('deposit') + (cryordersGet.Money+cryordersGet.Express+cryordersGet.buyerMoney)
    depositbuyer.save()
    through = CryOrder.objects.filter(id=cryorders).update(Status=5)
    return redirect('/cryapp/seller/orders/')


def cryapp_edit(request, cryorders_id = 0):
    if request.method=="GET":
        cryorders = int(cryorders_id)
        editcryappdata = CryOrder.objects.get(id=cryorders)
        return render(request, 'material/seller/project_edit.html', {'editcryappdata':editcryappdata})
    if request.method=="POST":
        cryorders = int(cryorders_id)
        editcryappdata = CryOrder.objects.filter(id=cryorders).update(Keywords=request.POST['keywords'])
        return render(request, 'material/seller/table.html')
#-------seller CRUD -----#
def cryapp_buyer_delete(request, cryorders_id = 0):
    cryorders = int(cryorders_id)
    deletecryappdate = CryOrder.objects.filter(id=cryorders).update(Status=1, buyerid=None)
    print(cryorders)
    return redirect('/cryapp/buyer/orders/')
#----- buyer CRUD ----#

#----- buyer CRUD ----#


#———————buyer admin------#
def buyeradmin(request):
    if request.user.is_authenticated:
        return render(request, 'material/buyer/dashboard.html')
    else:
        return render(request, 'login.html')

def buyer_user(request):
    if request.user.is_authenticated:
        return render(request, 'material/buyer/user.html')
    else:
        return render(request, 'login.html')


class buyer_orders(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        pagenumber=1
        pagearray =[]
        productnumber=30
        orderslists = {}
        ordersfilter = CryOrder.objects.filter(buyerid=request.user.id).order_by()
        pagetotal = len(ordersfilter)
        try:
            pagearray = int(productnumber/pagetotal)+1
        except:
            pagearray = 0
        orderlistid = 1
        for orderslist in ordersfilter:
            orderslists[orderlistid] = {
                'id':orderslist.id,
                'images':orderslist.GoodId.image1,
                'goodid':orderslist.GoodId,
                'shopname':orderslist.ShopId.shopname,
                'shopkeepname':orderslist.ShopId.shopkeepername,
                'Keywords':orderslist.Keywords,
                'platform':orderslist.ShopId.platform,
                'OrderSort':orderslist.OrderSort,
                'Status':orderslist.Status,
                'StartTime':orderslist.StartTime,
                'EndTime':orderslist.EndTime,
                'Note':orderslist.Note,
                'Money':orderslist.Money,
            }
            orderlistid += 1

        print(len(ordersfilter))
        return render(request, 'material/buyer/table.html',{'orderslists':orderslists})


def buyer_commit_orders(request, cryorders_id = 0):
    cryorderid=cryorders_id
    print(request.POST['paltfromorders'])
    print(int(request.POST['paltfromorders']))
    commitorders = CryOrder.objects.filter(id=cryorderid).update(PlatformOrdersid=int(request.POST['paltfromorders']), Status=3)
    return redirect('/cryapp/buyer/orders/')
#———————buyer admin------#
