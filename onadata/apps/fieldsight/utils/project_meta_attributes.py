import uuid


def create_id_in_project_metas(project):
    meta_list = project.site_meta_attributes
    for meta in meta_list:
        if 'id' not in meta:
            meta['id'] = str(uuid.uuid4())
    project.save()


