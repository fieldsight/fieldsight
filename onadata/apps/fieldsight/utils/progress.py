from django.db.models import Sum

from onadata.apps.fieldsight.models import SiteProgressHistory
from onadata.apps.fsforms.models import FieldSightXF

def advance_stage_approved(site):
    from onadata.apps.fsforms.models import FieldSightXF, Stage
    """
    Algorithm:
        Find maximum stage  order from site level form

        find maxmium stage order of project

        maximum order is maximum of one of this.

        appproved weight is total weight of substages less than  equal to maximum order

        if not weight
        approved weight is count of substages which have order less than or equal maximum order


    """
    project = site.project
    main_stage = None
    project_main_stage = None

    advance_stage_site = site.site_instances.filter(
        form_status=3,
        site_fxf__is_staged=True).order_by(
        '-site_fxf__stage__stage__order',
        '-site_fxf__stage__order').values('site_fxf__stage').first()
    if advance_stage_site:
        stage_id = advance_stage_site.get('site_fxf__stage')
        stage = Stage.objects.get(pk=stage_id)
        main_stage = stage.stage

    advance_stage_project = site.site_instances.filter(
        form_status=3,
        project_fxf__is_staged=True).order_by(
        '-project_fxf__stage__stage__order',
        '-project_fxf__stage__order').values('project_fxf__stage').first()

    if advance_stage_project:
        stage_id = advance_stage_project.get('project_fxf__stage')
        project_stage = Stage.objects.get(pk=stage_id)
        project_main_stage = project_stage.stage


    if advance_stage_site and advance_stage_project:
        max_stage_order = max(main_stage.order, project_main_stage.order)
    elif advance_stage_site:
        max_stage_order = main_stage.order
    elif advance_stage_project:
        max_stage_order = project_main_stage.order
    else:
        return 0


    approved_site_forms_weight = FieldSightXF.objects.filter(
        stage__stage__order__lte=max_stage_order,site=site).values_list('stage__weight', flat=True)
    approved_site_weight_total = sum([w for w in approved_site_forms_weight if w is not None])
    approved_project_forms_weight = FieldSightXF.objects.filter(
        stage__stage__order__lte=max_stage_order,project=site.project).values_list('stage__weight', flat=True)
    approved_projects_weight_total = sum([w for w in approved_project_forms_weight if w is not None])
    approved_weight = approved_site_weight_total + approved_projects_weight_total
    if approved_weight:
        from onadata.apps.fsforms.models import Stage
        site_stages_weight = Stage.objects.filter(stage__site=self).aggregate(Sum('weight'))['weight__sum']
        project_stages_weight = Stage.objects.filter(stage__project=project).aggregate(Sum('weight'))[
            'weight__sum']
        site_stages_weight = site_stages_weight if site_stages_weight else 0
        project_stages_weight = project_stages_weight if project_stages_weight else 0
        total_weight = site_stages_weight + project_stages_weight
        p = ("%.0f" % (approved_weight / (total_weight * 0.01)))
        p = int(p)
        if p > 99:
            return 100
        return p
    # weight not set
    approved_forms_site = Stage.objects.filter(stage__order__lte=max_stage_order, site=site).count()
    approved_forms_project = Stage.objects.filter(stage__order__lte=max_stage_order, project=project).count()
    approved = approved_forms_site + approved_forms_project
    if not approved:
        return 0
    from onadata.apps.fsforms.models import Stage
    stages = Stage.objects.filter(stage__project=project).count() + Stage.objects.filter(stage__site=site).count()
    if not stages:
        return 0
    p = ("%.0f" % (approved / (stages * 0.01)))
    p = int(p)
    if p > 99:
        return 100
    return p


def pull_integer_answer(form, xform_question, site):
    return 0


def set_site_progress(site, project_settings=None):
    progress = 0
    if not project_settings:
        project_settings = site.project.progress_settings.filter(deployed=True, active=True)
        if project_settings:
            project_settings = project_settings[0]
    if not project_settings or project_settings.source == 0:
        # default progress (stages approved/stages total) weight
        progress = site.progress()
    elif project_settings.source == 1:
        progress = advance_stage_approved(site)
    if project_settings.source == 2:
        form = FieldSightXF.objects.get(pk=project_settings.pull_integer_form)
        xform_question = project_settings.pull_integer_form_question
        progress = pull_integer_answer(form, xform_question, site)
        progress = progress
    if project_settings.source == 3:
        p = ("%.0f" % (site.site_instances.count() / (project_settings.no_submissions_total_count * 0.01)))
        p = int(p)
        if p > 99:
            p = 100
        progress = p

    if project_settings.source == 4:
        p = ("%.0f" % (site.site_instances.filter(
            project_fxf_id=project_settings.no_submissions_form).count() / (
                project_settings.no_submissions_total_count * 0.01)))
        p = int(p)
        if p > 99:
            p = 100
        progress = p

    site.current_progress = progress
    site.save()

    history, _created = SiteProgressHistory.objects.get_or_create(site=site, progress=progress, settings=project_settings)
    if not _created:
        history.save()


