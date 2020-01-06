
def separate_metrices(attributes):
    default_metrics = []
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
                elif value['selectedIndividualForm']['form']['category'] == "individual_form":
                    individual_form_metrics.append(a)
                else:
                    raise ValueError
            elif value.get('category') == "site_information":
                site_info_metrics.append(a)

            else:
                raise ValueError
        else:
            raise ValueError
    return default_metrics, individual_form_metrics, form_information_metrics, user_metrics, site_info_metrics
