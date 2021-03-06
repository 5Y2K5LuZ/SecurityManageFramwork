#coding:utf-8
'''
Created on 2018年5月17日

@author: yuguanc
'''

from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from .. import models
from django.http import JsonResponse
from SeMFSetting.views import paging
from VulnManage.views.views import VULN_LEAVE,VULN_STATUS
from django.db.models import Count


ASSET_STATUS={
    '0':'使用中',
    '1':'闲置中',
    '2':'已销毁',
    }

@login_required
def assetdetailsview(request,asset_id):
    user = request.user
    if user.is_superuser:
        asset = get_object_or_404(models.Asset,asset_id=asset_id)
    else:
        asset = get_object_or_404(models.Asset,asset_user = user,asset_id=asset_id)
        
    vuln_all = asset.vuln_for_asset.all()
    vuln_count = vuln_all.count()
    vuln_ign = vuln_all.filter(fix_status = 0).count()
    vuln_fixed = vuln_all.filter(fix_status = 1).count()
    vuln_fix = vuln_all.exclude(fix_status__in=[0,1]).count()
        
    vuln_status = {
            'vuln_count':vuln_count,
            'vuln_ign':vuln_ign,
            'vuln_fixed':vuln_fixed,
            'vuln_fix':vuln_fix
            }
    
    assettypeinfo = asset.asset_type.parent.typeinfo_assettype.all() | asset.asset_type.typeinfo_assettype.all()
    
    info = []
    
    for typeinfo in assettypeinfo:
        info.append(typeinfo.key)
    
    if 'os' in info:
        try:
            os_info = asset.os_for_asset
        except:
            models.OS_Info.objects.get_or_create(asset=asset)
            os_info = asset.os_for_asset
    else:
        os_info = ''
            
    if 'internet' in info:
        try:
            internet_info = asset.internet_for_asset
        except:
            internet_info = models.Internet_Info.objects.get_or_create(asset=asset)
            internet_info=internet_info[0]
    else:
        internet_info=''
    
    return render(request,'AssetManage/assetdetails.html',{'asset':asset,'info':info,'os_info':os_info,'internet_info':internet_info,'vuln_status':vuln_status})


@login_required
def asset_ports(request,asset_id):
    user  = request.user
    resultdict={}
    
    #page = request.GET.get('page')
    #rows = request.GET.get('limit')
    
    if user.is_superuser:
        asset = get_object_or_404(models.Asset,asset_id=asset_id)
    else:
        asset = get_object_or_404(models.Asset,asset_user = user,asset_id=asset_id)
    port_list = asset.port_for_asset.all().order_by('-updatetime')
    total = port_list.count()
    #port_list = paging(port_list,rows,page)
    data = []
    for port in port_list:
        dic={}
        dic['id']=port.id
        dic['port']=port.port
        dic['product']=port.product
        dic['version']=port.version
        dic['port_info']=port.port_info
        dic['updatetime']=port.updatetime
        data.append(dic)
    resultdict['code']=0
    resultdict['msg']="端口列表"
    resultdict['count']=total
    resultdict['data']=data
    return JsonResponse(resultdict)


@login_required
def asset_vuln(request,asset_id):
    user  = request.user
    resultdict={}
    
    page = request.GET.get('page')
    rows = request.GET.get('limit')
    
    if user.is_superuser:
        asset = get_object_or_404(models.Asset,asset_id=asset_id)
    else:
        asset = get_object_or_404(models.Asset,asset_user = user,asset_id=asset_id)
    vuln_list = asset.vuln_for_asset.all().order_by('-fix_status','-leave')
    total = vuln_list.count()
    vuln_list = paging(vuln_list,rows,page)
    data = []
    for vuln in vuln_list:
        dic={}
        dic['vuln_id'] = vuln.vuln_id
        dic['cve_name'] = vuln.cve_name
        dic['vuln_name'] = vuln.vuln_name
        dic['vuln_type'] = vuln.vuln_type
        dic['leave'] = VULN_LEAVE[vuln.leave]
        dic['fix_status'] = VULN_STATUS[vuln.fix_status]
        dic['update_data'] = vuln.update_data
        dic['asset'] = vuln.vuln_asset.asset_key
        dic['asset_id'] = vuln.vuln_asset.asset_id
        data.append(dic)
    resultdict['code']=0
    resultdict['msg']="端口列表"
    resultdict['count']=total
    resultdict['data']=data
    return JsonResponse(resultdict)

        
        
@login_required
def asset_plugin(request,asset_id):
    user  = request.user
    resultdict={}
    
    #page = request.GET.get('page')
    #rows = request.GET.get('limit')
    
    if user.is_superuser:
        asset = get_object_or_404(models.Asset,asset_id=asset_id)
    else:
        asset = get_object_or_404(models.Asset,asset_user = user,asset_id=asset_id)
    plugin_list = asset.plugin_for_asset.all().order_by('-updatetime')
    total = plugin_list.count()
    #plugin_list = paging(plugin_list,rows,page)
    data = []
    for plugin in plugin_list:
        dic={}
        dic['id']=plugin.id
        dic['name']=plugin.name
        dic['version']=plugin.version
        dic['plugin_info']=plugin.plugin_info
        dic['updatetime']=plugin.updatetime
        data.append(dic)
    resultdict['code']=0
    resultdict['msg']="端口列表"
    resultdict['count']=total
    resultdict['data']=data
    return JsonResponse(resultdict)        


@login_required
def asset_file(request,asset_id):
    user  = request.user
    resultdict={}
    
    #page = request.GET.get('page')
    #rows = request.GET.get('limit')
    
    if user.is_superuser:
        asset = get_object_or_404(models.Asset,asset_id=asset_id)
    else:
        asset = get_object_or_404(models.Asset,asset_user = user,asset_id=asset_id)
    file_list = asset.file_for_asset.all().order_by('-updatetime')
    total = file_list.count()
    #file_list = paging(file_list,rows,page)
    data = []
    for file in file_list:
        dic={}
        dic['id']=file.id
        dic['name']=file.name
        dic['file']= '/uploads/'+str(file.file)
        dic['file_info']=file.file_info
        dic['updatetime']=file.updatetime
        data.append(dic)
    resultdict['code']=0
    resultdict['msg']="端口列表"
    resultdict['count']=total
    resultdict['data']=data
    return JsonResponse(resultdict) 


@login_required
def asset_asset(request,asset_id):
    user  = request.user
    resultdict={}
    
    #page = request.GET.get('page')
    #rows = request.GET.get('limit')
    
    if user.is_superuser:
        asset = get_object_or_404(models.Asset,asset_id=asset_id)
    else:
        asset = get_object_or_404(models.Asset,asset_user = user,asset_id=asset_id)
    assetconnect_list = asset.asset_connect.all().order_by('-asset_updatetime')
    total = assetconnect_list.count()
    #assetconnect_list = paging(assetconnect_list,rows,page)
    data = []
    for assetconnect in assetconnect_list:
        dic={}
        dic['asset_id'] = assetconnect.asset_id
        dic['asset_name'] = assetconnect.asset_name
        dic['asset_key'] = assetconnect.asset_key
        dic['asset_status'] = ASSET_STATUS[assetconnect.asset_status]
        if assetconnect.asset_inuse:
            dic['asset_inuse'] = '已认领'
        else:
            dic['asset_inuse'] = '待认领'
        if assetconnect.asset_type:
            dic['asset_type'] = assetconnect.asset_type.name
        else:
            dic['asset_type'] = '未分类'
        dic['user_email'] = assetconnect.user_email
        dic['asset_score'] = assetconnect.asset_score
        dic['asset_updatetime'] = assetconnect.asset_updatetime
        data.append(dic)
    resultdict['code']=0
    resultdict['msg']="端口列表"
    resultdict['count']=total
    resultdict['data']=data
    return JsonResponse(resultdict)     



