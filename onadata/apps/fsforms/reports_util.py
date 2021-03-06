import json
from bson import json_util
from django.conf import settings
from django.utils.translation import ugettext_lazy, ugettext as _

from onadata.apps.logger.models import Attachment
from onadata.libs.utils.decorators import apply_form_field_names
from formpack import FormPack
from .models import FieldSightXF
from onadata.apps.viewer.models.parsed_instance import dict_for_mongo, _encode_for_mongo, xform_instances
from django.contrib.sites.models import Site as DjangoSite

DEFAULT_LIMIT = 30000

def get_images_for_sites_count(site_id):
    try:
        return settings.MONGO_DB.instances.aggregate(
            [{"$match": {"fs_site":{'$in' : [str(site_id), int(site_id)]}}},
                {"$unwind": "$_attachments"},{"$match":{"_attachments.mimetype": {'$in': ['image/png', 'image/jpeg']}}},
                {"$group": {"_id":  "null", "count":{"$sum": 1} }}], cursor={})
    except:
        return []


def get_recent_images(site_id):
    urls = Attachment.objects.filter(instance__fieldsight_instance__is_deleted=False,
                              instance__fieldsight_instance__site=site_id).values_list('media_file', 'instance')[:6]
    BASEURL = DjangoSite.objects.get_current().domain
    recent_pictures = []

    for url in urls:
        download_url = 'https://' + BASEURL + '/attachment/medium?media_file=' + url[0]
        attachment = {"_id": url[1],
                      "_attachments": {"download_url": download_url}}
        recent_pictures.append(attachment)
    return recent_pictures


def get_images_for_site(site_id):
    return settings.MONGO_DB.instances.aggregate(
        [{"$match": {
            "fs_site": {'$in': [str(site_id), int(site_id)]},
            '_deleted_at': {'$exists': False}}},
            {"$unwind": "$_attachments"},
            {"$match": {"_attachments.mimetype": {'$in': ['image/png', 'image/jpeg']}}},
            {"$sort": {"_id": -1}}, {"$limit": 6}], cursor={})


def get_images_for_site_all(site_id):
    images_list = settings.MONGO_DB.instances.aggregate(
        [{"$match": {
            "fs_site": {'$in': [str(site_id), int(site_id)]},
            '_deleted_at': {'$exists': False}}},
            {"$unwind": "$_attachments"},
            {"$match": {"_attachments.mimetype": {'$in': ['image/png', 'image/jpeg']}}},
            {"$sort": {"_id": -1}}], cursor={})

    images_list = list(images_list)
    return images_list


def get_site_responses_coords(site_id):
    coords = settings.MONGO_DB.instances.aggregate(
        [{"$match": {"fs_site": {'$in': [str(site_id), int(site_id)]}, '_deleted_at': None,
                    "_geolocation":{"$not": { "$elemMatch": {"$eq": None }}}}},
                                  {"$project" : {"_id":0, "type": {"$literal": "Feature"}, "geometry":
                                      { "type": {"$literal": "Point"}, "coordinates": "$_geolocation" },
                                                 "properties": {"id":"$_id", "fs_uuid":
                                                     "$fs_uuid", "submitted_by":"$_submitted_by"}}}], cursor={})
    return list(coords)

def get_instaces_for_site_individual_form(fieldsightxf_id):
    query = {"fs_uuid":str(fieldsightxf_id)}
    return settings.MONGO_DB.instances.find(query)
    
def get_instances_for_field_sight_form(fieldsight_form_id, submission=None):
    query = {"$or":[{"_uuid":fieldsight_form_id}, {"fs_uuid":fieldsight_form_id}, {"_uuid":str(fieldsight_form_id)}, {"fs_uuid":str(fieldsight_form_id)}]}
    return settings.MONGO_DB.instances.find(query)

def delete_form_instance(instance_id):
    return settings.MONGO_DB.instances.update({'_id': instance_id}, { '$set': {'_deleted_at':True}})


def get_instances_for_project_field_sight_form(project_fieldsight_form_id, submission=None):
    query = {'fs_project_uuid': { '$in': [project_fieldsight_form_id, str(project_fieldsight_form_id)]}}
    return settings.MONGO_DB.instances.find(query)


def get_instance_form_data(fieldsight_form_id, instance_id):

    query = {'_id': instance_id, '_deleted_at': {'$exists': False}}
    return settings.MONGO_DB.instances.find(query)


def get_instance(instance_id):
    query = {'_id': int(instance_id)}
    return settings.MONGO_DB.instances.find(query)


def update_status(instance_id, status):
    settings.MONGO_DB.instances.update({'_id': int(instance_id)}, {'$set': {'fs_status': status}}, upsert=False, multi=False)


def build_formpack(id_string, xform):
    schema = {
        "id_string": id_string,
        "version": 'v1',
        "content": xform.to_kpi_content_schema(),
    }
    return  xform, FormPack([schema], xform.title)


def build_export_context(request,xform, id_string):

    hierarchy_in_labels = request.GET.get('hierarchy_in_labels', None)
    group_sep = request.GET.get('group_sep', '/')

    xform, formpack = build_formpack(id_string, xform)

    translations = formpack.available_translations
    lang = request.GET.get('lang', None) or next(iter(translations), None)

    options = {'versions': 'v1',
               'group_sep': group_sep,
               'lang': lang,
               'hierarchy_in_labels': hierarchy_in_labels,
               # 'copy_fields': ('_id', '_uuid', '_submission_time''),
               'copy_fields': ('_id','_submission_time', '_submitted_by', 'fs_site'),
               # 'force_index': True
               'force_index': False
               }

    return {
        'id_string': id_string,
        'languages': translations,
        'headers_lang': lang,
        'formpack': formpack,
        'xform': xform,
        'group_sep': group_sep,
        'lang': lang,
        'hierarchy_in_labels': hierarchy_in_labels,
        'export': formpack.export(**options)
    }



def get_xform_and_perms(fsxf_id, request):
    fs_xform = FieldSightXF.objects.get(pk=fsxf_id)
    xform = fs_xform.xf
    is_owner = xform.user == request.user
    can_edit = True
    can_view = can_edit or\
        request.user.has_perm('logger.view_xform', xform)
    return [xform, is_owner, can_edit, can_view, fs_xform]


@apply_form_field_names
def query_mongo(username, id_string, query, fields, sort, start=0,
                    limit=DEFAULT_LIMIT, count=False, hide_deleted=True, fs_uuid=None, fs_project_uuid=None, site_id=None):
    USERFORM_ID = u'_userform_id'
    STATUS = u'_status'
    DEFAULT_BATCHSIZE = 1000

    fields_to_select = {USERFORM_ID: 0}
    # TODO: give more detailed error messages to 3rd parties
    # using the API when json.loads fails
    if isinstance(query, basestring):
        query = json.loads(query, object_hook=json_util.object_hook)
    query = query if query else {}
    query = dict_for_mongo(query)
    query[USERFORM_ID] = u'%s_%s' % (username, id_string)

    # check if query contains and _id and if its a valid ObjectID
    # if '_uuid' in query and ObjectId.is_valid(query['_uuid']):
    #     query['_uuid'] = ObjectId(query['_uuid'])

    query.pop('_userform_id')
    if fs_uuid is not None:
        query = {"$and": [query, {"$or":[ {"_uuid":fs_uuid}, {"fs_uuid":fs_uuid}, {"_uuid":str(fs_uuid)}, {"fs_uuid":str(fs_uuid)}]}]}
        # query['_uuid'] = { '$in': [fs_uuid, str(fs_uuid)] } #fs_uuid
    if fs_project_uuid is not None:
        if site_id is None:
            query['fs_project_uuid'] = { '$in': [fs_project_uuid, str(fs_project_uuid)] } #fs_project_uuid
        elif site_id and count:
            query['fs_project_uuid'] = {'$in': [fs_project_uuid, str(fs_project_uuid)]}
            #query = query.update({'fs_project_uuid': {'$in': [fs_project_uuid, str(fs_project_uuid)] }, 'fs_site': { '$in': [site_id, str(site_id)] }})
        elif site_id:
            query['fs_project_uuid'] = {'$in': [fs_project_uuid, str(fs_project_uuid)]}

    # if hide_deleted:
    #     # display only active elements
    #     # join existing query with deleted_at_query on an $and
    #     query = {"$and": [query, {"_deleted_at": None}]}

    # fields must be a string array i.e. '["name", "age"]'
    if isinstance(fields, basestring):
        fields = json.loads(fields, object_hook=json_util.object_hook)
    fields = fields if fields else []

    # TODO: current mongo (2.0.4 of this writing)
    # cant mix including and excluding fields in a single query
    if type(fields) == list and len(fields) > 0:
        fields_to_select = dict(
            [(_encode_for_mongo(field), 1) for field in fields])
    if isinstance(sort, basestring):
        sort = json.loads(sort, object_hook=json_util.object_hook)
    sort = sort if sort else {}
    # if fs_uuid is not None:
    #     cursor = xform_instances.find({"$or":[ {"_uuid":fs_uuid}, {"fs_uuid":fs_uuid}, {"_uuid":str(fs_uuid)}, {"fs_uuid":str(fs_uuid)}]}, fields_to_select)
    # else:
    #     cursor = xform_instances.find({"$or":[ {"fs_project_uuid":fs_project_uuid}, {"fs_project_uuid": str(fs_project_uuid)}]}, fields_to_select)

    cursor = xform_instances.find(query, fields_to_select)
    if count:
        return [{"count": cursor.count()}]

    if start < 0 or limit < 0:
        raise ValueError(_("Invalid start/limit params"))

    cursor.skip(start).limit(limit)
    if type(sort) == dict and len(sort) == 1:
        sort_key = sort.keys()[0]
        # TODO: encode sort key if it has dots
        sort_dir = int(sort[sort_key])  # -1 for desc, 1 for asc
        cursor.sort(_encode_for_mongo(sort_key), sort_dir)
    # set batch size
    cursor.batch_size = DEFAULT_BATCHSIZE
    return cursor
