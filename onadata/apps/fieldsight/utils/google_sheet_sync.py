from onadata.apps.fieldsight.models import Project, Site


def site_information(project_id):
    values = []
    header_row = ['identifier', 'name', 'type','region_identifier', 'phone',
                  'address',
                  'public_desc', 'additional_desc', 'latitude', 'longitude',
                  'progress', 'root_site_identifier']
    meta_ques = Project.objects.get(pk=project_id).site_meta_attributes
    for question in meta_ques:
        if not question['question_type'] == 'Link':
            header_row.append(question['question_name'])
    values.append(header_row)
    sites = Site.objects.filter(project=project_id)
    for site in sites.select_related('region').iterator():
        l = [site.identifier,
             site.name,
             site.type.identifier if site.type else "",
             site.phone,
             site.address,
             site.public_desc, site.additional_desc, site.latitude,
             site.longitude, site.current_progress,
             site.site.identifier if site.site else ""]
        meta_ans = site.all_ma_ans
        for question in meta_ques:
            if not question['question_type'] == 'Link':
                # question is not draw from another project
                question_name = question['question_name']
                l.append(meta_ans.get(question_name, ""))
        values.append(l)

    return values