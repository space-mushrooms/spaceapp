import uuid


def get_random_filename(filename):
    filename = filename.split('/')[-1]
    ext = ''
    if '.' in filename:
        ext = filename.split('.')[-1]
    if ext:
        filename = '{}.{}'.format(uuid.uuid4(), ext)

    return filename
