from django.http import HttpResponse
from common.common import (make_json_response,
                           request_body_to_json)
from .models import Backlog, OfferedSp, Project
from django.utils import timezone
from django.db.models import Count, CASCADE
from django.db.models.options import Options
from django.db.models.fields.related import ForeignObject
import time

def view_all(request, project_id):
    db_list = list(Backlog.objects.filter(
        delete_flag="False").filter(project_id=project_id).all())
    response_data = []
    for db_data in db_list:
        response_data.append({"id": db_data.id, "pbl_id": db_data.pbl_id, "pbl_name": db_data.pbl_name, "pbl_sp": db_data.pbl_sp, "register_date": db_data.register_date,
                             "update_date": db_data.update_date, "pbl_priority": db_data.pbl_priority, "project_id": db_data.project_id, "pbl_sprint": db_data.pbl_sprint})
    return make_json_response(list(response_data))


def register_offered_sp(request):
    try:
        request_data = request_body_to_json(request.body)
        OfferedSp.objects.create(
            user_name=request_data.get('user_name'),
            user_sp=request_data.get('user_sp'),
            backlog_id=request_data.get('backlog_id'),
            sp_count=0
        )
    except Exception as e:
        return HttpResponse(status=400)
    return HttpResponse()


def read_pbl(request):
    try:
        request_data = request_body_to_json(request.body)
        db_data = Backlog.objects.get(id=request_data.get("id"))
    except Exception as e:
        return HttpResponse(status=400)
    response_data = {"id": db_data.id, "pbl_id": db_data.pbl_id, "pbl_name": db_data.pbl_name,
                     "project_id": db_data.project_id, "pbl_priority": db_data.pbl_priority, "pbl_sprint": db_data.pbl_sprint}
    return make_json_response(response_data, status=200)


def register_backlog(request):
    try:
        request_data = request_body_to_json(request.body)
        # データ最大値の取得
        record_length = Backlog.objects.all().count()
        Backlog.objects.create(
            pbl_id=request_data['pbl_id'],
            pbl_name=request_data['pbl_name'],
            pbl_priority=record_length + 1,
            project_id=request_data['project_id'],
            pbl_sprint=request_data['pbl_sprint']
        )
    except Exception as e:
        return HttpResponse(status=400)
    return HttpResponse()


def view_offered_sp(request, selected_backlog_id):
    offered_all_list = sorted(list(OfferedSp.objects.filter(
        backlog_id=selected_backlog_id).values()), key=lambda x: (float(x['id'])))
    return make_json_response(offered_all_list)


def register_pbl_sp(request):
    try:
        request_data = request_body_to_json(request.body)
        pbl_data = Backlog.objects.get(id=request_data.get("id"))
        pbl_data.pbl_sp = request_data.get("pbl_sp")
    except Exception as e:
        return HttpResponse(status=400)
    pbl_data.update_date = timezone.datetime.now()
    pbl_data.save()

    return HttpResponse()


def update_backlog(request):
    request_data = request_body_to_json(request.body)
    try:
        backlog = Backlog.objects.get(id=request_data.get('id'))
    # 暫定でException
    except Exception as e:
        return HttpResponse(status=400)
    backlog.pbl_id = request_data.get('pbl_id')
    backlog.pbl_name = request_data.get('pbl_name')
    backlog.pbl_sp = request_data.get('pbl_sp')
    backlog.update_date = timezone.localtime(timezone.now())
    backlog.pbl_sprint = request_data.get('pbl_sprint')
    backlog.save()
    return HttpResponse()

def update_offered_sp(request):
    request_data = request_body_to_json(request.body)
    try:
        offered_sp = OfferedSp.objects.get(id=request_data.get('id'))
    except OfferedSp.DoesNotExist:
        return HttpResponse(status=404)
    except Exception as e:
        return HttpResponse(status=400)

    offered_sp.user_sp = request_data.get('user_sp', offered_sp.user_sp)
    offered_sp.sp_count += 1
    offered_sp.save()

    return HttpResponse()



def delete_backlog(request):
    request_data = request_body_to_json(request.body)
    try:
        backlog = Backlog.objects.get(id=request_data.get('id'))
    except Exception as e:
        return HttpResponse(status=400)
    backlog.delete_flag = True
    backlog.update_date = timezone.localtime(timezone.now())
    backlog.save()
    return HttpResponse()


def update_priority(request):
    def get_unique_id():
        # ミリ秒単位のタイムスタンプを生成
        timestamp = int(time.time() * 1000)
        # IntegerFieldの最大値
        max_int = 2147483647
        return timestamp % max_int
    request_data = request_body_to_json(request.body)
    backlog_num = Backlog.objects.filter(project=request_data.get(
        'project_id')).filter(delete_flag=0).count()
    try:
        target_backlog = Backlog.objects.get(
            pbl_priority=request_data.get('priority'))
        origin_backlog = Backlog.objects.get(
            pbl_priority=request_data.get('target_priority'))
        origin_backlog.pbl_priority = get_unique_id()
        origin_backlog.save()
        target_backlog.pbl_priority = request_data.get('target_priority')
        target_backlog.update_date = timezone.localtime(timezone.now())
        target_backlog.save()
        origin_backlog.pbl_priority = request_data.get('priority')
        origin_backlog.update_date = timezone.localtime(timezone.now())
        origin_backlog.save()
    except Exception as e:
        return HttpResponse(status=400)
    return HttpResponse()


def read_transferred_pbl(request):
    try:
        request_data = request_body_to_json(request.body)
        max_backlog_num = Backlog.objects.filter(delete_flag="False").filter(
            project_id=request_data.get('project_id')).all().count()
        backlog_list = Backlog.objects.filter(delete_flag="False").filter(
            project_id=request_data.get('project_id')).all().order_by('pbl_priority').values()
        for index, backlog in enumerate(backlog_list):
            if (backlog['pbl_priority'] == request_data.get('pbl_priority')):
                if (max_backlog_num == 1):
                    prev_id = -1
                    prev_title = ""
                    next_id = -1
                    next_title = ""
                elif ((index != 0) & (index != max_backlog_num - 1)):
                    prev_id = backlog_list[index - 1].get('id')
                    prev_title = backlog_list[index - 1].get('pbl_name')
                    next_id = backlog_list[index + 1].get('id')
                    next_title = backlog_list[index + 1].get('pbl_name')
                elif (index == 0):
                    prev_id = -1
                    prev_title = ""
                    next_id = backlog_list[index + 1].get('id')
                    next_title = backlog_list[index + 1].get('pbl_name')
                elif (index == max_backlog_num - 1):
                    prev_id = backlog_list[index - 1].get('id')
                    prev_title = backlog_list[index - 1].get('pbl_name')
                    next_id = -1
                    next_title = ""
        response_data = {"prev_id": prev_id, "prev_title": prev_title,
                         "next_id": next_id, "next_title": next_title}
    except Exception as e:
        return HttpResponse(status=400)
    return make_json_response(response_data, status=200)


def view_project_all(request):
    db_list = list(Project.objects.filter(delete_flag="False").all())
    response_data = []
    for db_data in db_list:
        response_data.append({"id": db_data.id, "project_name": db_data.project_name,
                             "register_date": db_data.register_date, "update_date": db_data.update_date})
    return make_json_response(list(response_data))


def register_project(request):
    try:
        request_data = request_body_to_json(request.body)
        Project.objects.create(
            project_name=request_data['project_name'],
            register_date=timezone.localtime(timezone.now()),
            update_date=timezone.localtime(timezone.now())
        )
    except Exception as e:
        return HttpResponse(status=400)
    return HttpResponse(status=200)


def delete_project(request):
    request_data = request_body_to_json(request.body)
    try:
        project = Project.objects.get(id=request_data.get('id'))
    except Exception as e:
        return HttpResponse(status=400)
    project.delete_flag = True
    project.update_date = timezone.localtime(timezone.now())
    project.save()
    return HttpResponse()


def delete_user_sp(request):
    request_data = request_body_to_json(request.body)
    offeredSp = OfferedSp.objects.filter(user_name=request_data.get(
        'user_name')).filter(backlog_id=request_data.get('backlog_id'))
    offeredSp.delete()
    return HttpResponse()
