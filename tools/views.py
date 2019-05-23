from django.db.models import Manager
from django.http import StreamingHttpResponse, HttpResponse
from django.shortcuts import render, render_to_response
import os,csv
from tools.models import Gexpress, Results


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


def icgcgene(request):
    emseble=request.POST.get('gene')
    url='https://dcc.icgc.org/genes/'+emseble
    return (request, url)


def searchgexp(request):
    gid=request.POST.get('geneid').split(',')
    item=['Gene','baseMean','log2FoldChange','lfcSE','pvalue','padj','symbol','entrez']
    sqlquery = "select * from rsdb.results where Gene in("
    for r in gid:
        sqlquery+="'"+r+"',"
    sqlquery = sqlquery.strip(',')+")"
    genes=[]
    for g in Results.objects.raw(sqlquery):
        one = []
        for ge in item:
            string = 'one.append(g.' + str(ge).lower() + ')'
            exec(string)
        genes.append(one)
    content={
        'genes': genes,
        'item': item
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
        myFile2 = request.FILES.get("genefile", None)  # 获取上传的文件，如果没有文件，则默认为None
        if not myFile2:
            return HttpResponse("no files for upload!")
        destination = open(os.path.join(UP_DIR, myFile2.name), 'wb+')  # 打开特定的文件进行二进制的写操作
        for chunk in myFile2.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()
        genes = []
        gfile = open(os.path.join(UP_DIR, myFile2.name), 'r')
        sqlquery = "select * from rsdb.results where Gene in("
        for g in gfile:
            g=g.strip()
            sqlquery += "'" + g + "',"
        sqlquery = sqlquery.strip(',') + ")"
        item=['Gene','baseMean','log2FoldChange','lfcSE','pvalue','padj','symbol','entrez']
        for gene in Results.objects.raw(sqlquery):
            one = []
            for g in item:
                string = 'one.append(gene.' + str(g).lower() + ')'
                exec(string)
            genes.append(one)
        genes.insert(0, item)
        searchresult = csv.writer(open(os.path.join(BASE_DIR, "download/result.csv"),'w',newline=''))
        searchresult.writerows(genes)
        searchresult = open(os.path.join(BASE_DIR, "download/result.csv"),'r')
        response = HttpResponse(searchresult)
        response['Content-Disposition'] = 'attachment; filename=result.csv'
        return response