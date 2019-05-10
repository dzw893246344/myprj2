from django.db.models import Manager
from django.http import StreamingHttpResponse, HttpResponse
from django.shortcuts import render, render_to_response
import os,csv
from tools.models import Gexpress
# Create your views here.


def index(request):
    return render(request, 'tools/index.html')


def contact(request):
    return render(request, 'tools/contact.html')


def dbs(request):
    return render(request, 'tools/dbs.html')


def alldt(request):
    return render(request, 'tools/alldt.html')


def partdt(request):
    return render(request, 'tools/partdt.html')


def searchgexp(request):
    gid=request.POST.get('geneid').split(',')
    runs=[]
    sqlquery = "select Run,"+request.POST.get('geneid')+" from rsdb.gexpress where Run in("
    for r in request.POST.get('run').split(','):
        sqlquery+="'"+r+"',"
    sqlquery = sqlquery.strip(',')+")"
    for run in Gexpress.objects.raw(sqlquery):
        one = [run.run]
        for g in gid:
            string = 'one.append(run.'+str(g).lower()+')'
            exec(string)
        runs.append(one)
    content={
        'geneid': gid,
        'runs': runs
    }
    return render(request, 'tools/searchgexp.html', content)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def down_runlist(request):
    result = open(os.path.join(BASE_DIR, "download/runlist.txt"),'r')
    response = HttpResponse(result)
    response['Content-Disposition'] = 'attachment; filename=runlist.txt'
    return response


def down_genelist(request):
    result = open(os.path.join(BASE_DIR, "download/genelist.txt"),'r')
    response = HttpResponse(result)
    response['Content-Disposition'] = 'attachment; filename=genelist.txt'
    return response


def searchgexp2(request):
    UP_DIR=os.path.join(BASE_DIR,"upload")
    if request.method == "POST":    # 请求方法为POST时，进行处理
        myFile1 =request.FILES.get("runfile", None)    # 获取上传的文件，如果没有文件，则默认为None
        if not myFile1:
            return HttpResponse("no files for upload!")
        destination = open(os.path.join(UP_DIR,myFile1.name),'wb+')    # 打开特定的文件进行二进制的写操作
        for chunk in myFile1.chunks():      # 分块写入文件
            destination.write(chunk)
        destination.close()
        myFile2 = request.FILES.get("genefile", None)  # 获取上传的文件，如果没有文件，则默认为None
        if not myFile2:
            return HttpResponse("no files for upload!")
        destination = open(os.path.join(UP_DIR, myFile2.name), 'wb+')  # 打开特定的文件进行二进制的写操作
        for chunk in myFile2.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()
        runs = []
        genes = []
        rfile = open(os.path.join(UP_DIR, myFile1.name), 'r')
        for r in rfile:
            runs.append(r.strip('\n'))
        gfile = open(os.path.join(UP_DIR, myFile2.name), 'r')
        for g in gfile:
            genes.append(g.strip('\n'))
        sqlquery = "select *" + " from rsdb.gexpress where Run in("
        for r in runs:
            sqlquery += "'" + r + "',"
        sqlquery = sqlquery.strip(',') + ")"
        runs=[]
        for run in Gexpress.objects.raw(sqlquery):
            one = [run.run]
            for g in genes:
                string = 'one.append(run.' + str(g).lower() + ')'
                exec(string)
            runs.append(one)
        genes.insert(0, "Run")
        runs.insert(0, genes)
        searchresult = csv.writer(open(os.path.join(BASE_DIR, "download/result.csv"),'w',newline=''))
        searchresult.writerows(runs)
        searchresult = open(os.path.join(BASE_DIR, "download/result.csv"),'r')
        response = HttpResponse(searchresult)
        response['Content-Disposition'] = 'attachment; filename=result.csv'
        return response