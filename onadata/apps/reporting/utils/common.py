
def separate_metrics(attributes):
    default_metrics = []
    user_metrics_code = []
    default_metrics_code = []
    individual_form_metrics = []
    form_information_metrics = []
    user_metrics = []
    site_info_metrics = []
    for a in attributes:
        category = a.get('category')
        if category:
            if a['category'] == 'default':
                default_metrics.append(a)
            elif a['category'] == 'users':
                user_metrics.append(a)
        elif a.get('value'):
            value = a['value']
            if value.get('selectedQuestion'):
                if value['selectedQuestion']['form']['category'] == "form_information":
                    form_information_metrics.append(a)
                else:
                    raise ValueError
            elif value.get('selectedIndividualForm'):
                if value['selectedIndividualForm']['category'] == "individual_form":
                    individual_form_metrics.append(a)
                else:
                    raise ValueError
            elif value.get('category') == "site_information":
                site_info_metrics.append(a)

            else:
                raise ValueError
        else:
            raise ValueError
    for d in default_metrics:
        default_metrics_code.append(d['code'])
    for d in user_metrics:
        user_metrics_code.append(d['code'])
    return default_metrics_code, individual_form_metrics, form_information_metrics, user_metrics_code, site_info_metrics
