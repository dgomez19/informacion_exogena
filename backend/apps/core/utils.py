def file_path(instance, filename):
    """
    Devuelve la ruta en la que se guardaran los archivos cargados en excel

    :param instance: Instancia del proyecto (modelo proyecto).
    :param filename: Nombre del archivo.
    :return: Ruta para guardar el archivo.
    """
    return f"files/{instance.uuid}/{filename}"
