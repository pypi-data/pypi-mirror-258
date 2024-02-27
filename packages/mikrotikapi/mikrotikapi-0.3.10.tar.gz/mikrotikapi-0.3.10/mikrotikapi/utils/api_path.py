def api_path(path, id_=None):
    path = path
    if id_:
        return f"{path}/{id_}"
    return path
