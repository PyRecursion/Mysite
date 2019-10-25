from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseBadRequest
from .models import *
import json
import datetime
import decimal
from django.core import serializers
from .functions.musicspider import musicget
from .functions.sportspider import sportget
from django.views.decorators.csrf import csrf_protect,csrf_exempt
# Create your views here.

#主页
def index(request):
    imgtypes = ImageType.objects.values()  # 图片页面显示
    #验证登陆
    uid=request.session.get("uid")
    uname=request.session.get("uname")
    #读取帖子
    topic_img=[]
    topics=Topic.objects.all()
    for topic in topics:
        images=topic.userimages_set.all()
        topic_img.append((topic,images))

    return render(request,"index.html",locals())


#登陆
def login(request):
    if request.method == "GET":
        #选择记住密码
        if "user_id" in request.COOKIES:
            userobj = User.objects.filter(id=request.COOKIES["user_id"]).all()
            if userobj:
                loginname=userobj[0].loginname
                pwd=userobj[0].password
                return render(request, "login.html",locals())
        return render(request, "login.html")
    else:
        loginname=request.POST.get("loginname")
        pwd=request.POST.get('pwd')
        rmbpwd=request.POST.get('rmbpwd') #on or None
        userobj=User.objects.filter(loginname=loginname,password=pwd).all()
        if userobj:
            request.session["uid"]=userobj[0].id
            request.session["uname"]=userobj[0].name
            if rmbpwd:
                resp = redirect('/index')
                resp.set_cookie("user_id",userobj[0].id, 60*60*24*7)
                return resp
            return redirect("/index")
        else:
            err={"error":"用户名密码错误"}
            return render(request, "login.html",err)


#注册
def reg(request):
    if request.method=="GET":
        ck1 = request.GET.get("ck1")# 用户名验证
        ck2=request.GET.get("ck2") #昵称验证
        if ck1:
            ckloginname = User.objects.filter(loginname=ck1).all()  #对象列表
            if ckloginname:
                res={"flag":0}
            else:
                res={"flag":1}
            return HttpResponse(json.dumps(res))
        if ck2:
            ckname = User.objects.filter(name=ck2).all()  #对象列表
            if ckname:
                res={"flag":0}
            else:
                res={"flag":1}
            return HttpResponse(json.dumps(res))

        return render(request,"reg.html")
    else:
        loginname=request.POST.get("loginname")
        name=request.POST.get("name")
        pwd = request.POST.get("pwd")
        user=User()
        user.loginname=loginname
        user.name=name
        user.password=pwd
        print(user.password)
        user.save()
        user=User.objects.get(loginname=loginname)
        request.session["uid"] = user.id
        request.session["uname"] =name
        return redirect("/index/")

#退出登陆
def logout(request):
    if request.session['uid'] and request.session["uname"]:
        del request.session['uid']
        del request.session["uname"]
    return redirect("/index")


#发布帖子
@csrf_exempt
def publish(request):
    uid = request.session.get("uid")
    uname = request.session.get("uname")
    if request.method=="GET":
        if uid and uname:
            return render(request,"publish.html",locals())
        else:
            return redirect("/login/")
    else:
        title=request.POST.get("title")
        print(title)
        content=request.POST.get("content")
        print(content)
        image= request.FILES.get("image")
        filename=datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")+(image.name[-8:])

        topic=Topic()
        topic.title=title
        topic.content=content
        topic.publishtime=datetime.datetime.now()
        topic.user_id=uid
        topic.save()
        # with open("D:\PyProjects\Django\Mysite\static\\upload\\{}".format(filename),"wb") as f:
        # for i in image.chunks():
        userimg=UserImages()
        userimg.images.save(filename,image,save=False)
        userimg.topic=topic
        userimg.save()
        return HttpResponse(json.dumps({"flag":1}))

#帖子页

def content(request):
    #获取页数
    id=request.GET.get("id")
    #登录用户信息
    uid = request.session.get("uid")
    uname = request.session.get("uname")
    #帖子内容
    topic=Topic.objects.filter(id=id).all()[0]
    images=topic.userimages_set.all()
    comments=topic.comment_set.all()
    comment_replys=[]
    for comment in comments:
        replys=Reply.objects.filter(comment_id=comment.id).all()
        comment_replys.append((comment,replys))
    return render(request,"content.html",locals())


#帖子评论页
@csrf_exempt
def comment(request):
    uid = request.session.get("uid")
    uname = request.session.get("uname")
    time=datetime.datetime.now()
    content=request.POST.get("comment")
    topic_id=request.POST.get("topic_id")
    comment=Comment()
    comment.topic_id=topic_id
    comment.comment_userid_id=uid
    comment.comment_text=content
    comment.comment_time=time
    comment.save()
    timestr=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return HttpResponse(json.dumps({"uid":uid,"uname":uname,"time":timestr}))


@csrf_exempt
def cmt_reply(request):
    #做一下用户是否还在登录状态验证
    uid = request.session.get("uid")
    uname = request.session.get("uname")
    if uid and uname:
        comment_id=request.POST.get("comment_id")
        commentrpl=Reply()
        commentrpl.reply_type=0  #0代表回复评论
        commentrpl.comment_id=comment_id
        commentrpl.reply_id=comment_id
        commentrpl.reply_content=request.POST.get("commentrpl")
        commentrpl.from_uid_id=uid
        commentobj=Comment.objects.get(id=comment_id) #通过comment找用户
        touser=commentobj.comment_userid
        to_uid=touser.id
        to_name=touser.name
        commentrpl.to_uid=to_uid
        time = datetime.datetime.now()
        commentrpl.reply_datetime = time
        commentrpl.save()
        timestr=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return HttpResponse(json.dumps({"to_uid":to_uid,"to_name":to_name,"from_name":uname,"time":timestr}))
    else:
        return HttpResponseBadRequest()


@csrf_exempt
def rpl_reply(request):
    #做一下用户是否还在登录状态验证
    uid = request.session.get("uid")
    uname = request.session.get("uname")
    if uid and uname:
        reply_id=request.POST.get("reply_id")
        replyobj = Reply.objects.get(id=reply_id)
        comment_id = replyobj.comment_id
        replyrpl=Reply()
        replyrpl.comment_id=comment_id
        replyrpl.reply_type=1  #1代表回复回复
        replyrpl.reply_id=reply_id
        replyrpl.reply_content=request.POST.get("replyrpl")
        replyrpl.from_uid_id=uid
        to_uid=replyobj.from_uid_id
        replyrpl.to_uid=to_uid
        to_name=replyobj.from_uid.name
        time=datetime.datetime.now()
        replyrpl.reply_datetime=time
        replyrpl.save()
        timestr = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return HttpResponse(json.dumps({"to_uid":to_uid,"to_name":to_name,"from_name":uname,"time":timestr}))
    else:
        return HttpResponseBadRequest()




#音乐
def music(request):
    uid = request.session.get("uid")
    uname = request.session.get("uname")
    imgtypes = ImageType.objects.values()  # 图片页面显示
    hotmusic=musicget('https://music.163.com/discover/toplist?id=3778678')
    douyingmusic=musicget('https://music.163.com/discover/toplist?id=2250011882')
    newmusic=musicget('https://music.163.com/discover/toplist?id=3779629')
    return render(request,"music.html",locals())

#赛事直播
def sport(request):
    uid = request.session.get("uid")
    uname = request.session.get("uname")
    imgtypes = ImageType.objects.values()  # 图片页面显示
    sportgames=sportget()
    return render(request,"sport.html",locals())


#小说
def story(request):
    uid = request.session.get("uid")
    uname = request.session.get("uname")
    imgtypes = ImageType.objects.values()  # 图片页面显示
    dic=Story.objects.values()
    return render(request,"story.html",locals())


#目录
def story_dir(request):
    uid = request.session.get("uid")
    uname = request.session.get("uname")
    imgtypes = ImageType.objects.values()  # 图片页面显示
    id=request.GET["id"]
    story=Story.objects.get(id=id)
    dirs=story.story_text_set.all()
    lenth=len(dirs)
    dirs=dirs[0:200]
    pages=range((lenth//200)+1)
    return  render(request,"story_dir.html",locals())

#分页目录
def story_dirp(request,num):
    uid = request.session.get("uid")
    uname = request.session.get("uname")
    imgtypes = ImageType.objects.values()  # 图片页面显示
    id = request.GET["id"]
    story = Story.objects.get(id=id)
    dirs = story.story_text_set.all()
    lenth = len(dirs)
    dirs=dirs[(int(num)-1)*200:int(num)*200]
    pages = range((lenth // 200) + 1)
    return render(request,"story_dir.html",locals())

#小说文本响应
def story_text(request):
    uid = request.session.get("uid")
    uname = request.session.get("uname")
    imgtypes = ImageType.objects.values()  # 图片页面显示
    # 上一章处理
    callback_path = request.GET.get("path")
    flag = request.GET.get("flag")
    dir_id = request.GET.get("id")
    textobj = Story_text.objects.get(id=dir_id)
    path = textobj.content_path
    if callback_path:
        s = callback_path.partition("_")
        if flag=="pre":
            p = int(s[2]) - 1
            path = s[0] + s[1] + str(p)
        if flag=="next":
            p = int(s[2]) + 1
            path = s[0] + s[1] + str(p)
    story=textobj.story
    storyname=story.name
    text=[]
    try:
        with open("D:/爬虫数据2/{}/{}".format(story.name,path+".txt"),encoding="utf-8") as f:
            for line in f:
               text.append(line)
        return render(request,"story_text.html",locals())
    except FileNotFoundError as e:
        return HttpResponse("页面未找到")


#图片页
def photo(request):
    uid = request.session.get("uid")
    uname = request.session.get("uname")
    imgtypes=ImageType.objects.values()#图片页面显示
    type_id=request.GET.get("id")
    print(type_id)
    typeobj=ImageType.objects.get(id=type_id)
    typename=typeobj.type
    images=typeobj.images_set.all()[0:100]
    print(images)
    return render(request,"photo.html",locals())