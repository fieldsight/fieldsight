def check_file_extension(file_url):
    type = 'others'

    if file_url.endswith(('.jpg', '.png', '.jpeg')):
        type = 'image'

    elif file_url.endswith(('.xls', '.xlsx')):
        type = 'excel'

    elif file_url.endswith('.pdf'):
        type = 'pdf'

    elif file_url.endswith(('.doc', '.docm', 'docx', '.dot', '.dotm', '.dot', '.txt', '.odt')):
        type = 'word'

    return type


def readable_date(date):

    if date is not None:
        date = date.strftime('%d, %b %Y')
    return date