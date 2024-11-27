from celery import shared_task

from apps.core.models import (
    FileDetail,
    File
)

from openpyxl import load_workbook

from django.conf import settings

import csv

import pydash

# @shared_task
def upload_file():
    pendings = File.objects.filter(
        status=File.PENDING
    )

    for pending in pendings:
        try:
            with open(f'{settings.MEDIA_ROOT}/{pending.file_route}', newline='', encoding='utf-8') as csvfile:
                pending.status = File.IN_PROGRESS
                pending.save()

                reader = csv.reader(csvfile)

                count = 0

                position_type_document = None
                position_numero_documento = None
                position_nombre_razon_social = None
                position_apellidos = None
                position_dir_tipo = None
                position_dir_numero = None
                position_dir_apendice = None
                position_dir_orientacion = None
                position_dir_numero2 = None
                position_dir_apendice2 = None
                position_dir_orientacion2 = None
                position_dir_placa = None
                position_dir_interior = None
                position_dir_bloque = None
                position_direccion_especial = None
                position_correo_electronico = None
                position_departamento = None
                position_municipio = None
                position_pais = None
                position_tel_fijo = None
                position_tel_celular = None
                position_direccion = None
                position_direccion_notificacion = None
                file_detail = None
                is_error = False

                for row in reader:

                    new_data = [item for item in row]

                    if 'numero_documento' not in new_data:
                        new_data = [item.strip('"') for item in row[0].split(',')]

                    if count == 0:
                        if 'tipo_documento' in new_data:
                            position_type_document = new_data.index('tipo_documento')

                        if 'numero_documento' in new_data:
                            position_numero_documento = new_data.index('numero_documento')
                        else:
                            is_error = True
                            break

                        if 'nombre_razon_social' in new_data:
                            position_nombre_razon_social = new_data.index('nombre_razon_social')

                        if 'apellidos' in new_data:
                            position_apellidos = new_data.index('apellidos')

                        if 'dir_tipo' in new_data:
                            position_dir_tipo = new_data.index('dir_tipo')

                        if 'dir_numero' in new_data:
                            position_dir_numero = new_data.index('dir_numero')

                        if 'dir_apendice' in new_data:
                            position_dir_apendice = new_data.index('dir_apendice')

                        if 'dir_orientacion' in new_data:
                            position_dir_orientacion = new_data.index('dir_orientacion')

                        if 'dir_numero2' in new_data:
                            position_dir_numero2 = new_data.index('dir_numero2')

                        if 'dir_apendice2' in new_data:
                            position_dir_apendice2 = new_data.index('dir_apendice2')

                        if 'dir_orientacion2' in new_data:
                            position_dir_orientacion2 = new_data.index('dir_orientacion2')

                        if 'dir_placa' in new_data:
                            position_dir_placa = new_data.index('dir_placa')

                        if 'dir_interior' in new_data:
                            position_dir_interior = new_data.index('dir_interior')

                        if 'dir_bloque' in new_data:
                            position_dir_bloque = new_data.index('dir_bloque')

                        if 'direccion_especial' in new_data:
                            position_direccion_especial = new_data.index('direccion_especial')

                        if 'correo_electronico' in new_data:
                            position_correo_electronico = new_data.index('correo_electronico')

                        if 'departamento' in new_data:
                            position_departamento = new_data.index('departamento')

                        if 'municipio' in new_data:
                            position_municipio = new_data.index('municipio')

                        if 'pais' in new_data:
                            position_pais = new_data.index('pais')

                        if 'tel_fijo' in new_data:
                            position_tel_fijo = new_data.index('tel_fijo')

                        if 'tel_celular' in new_data:
                            position_tel_celular = new_data.index('tel_celular')

                        if 'direccion' in new_data:
                            position_direccion = new_data.index('direccion')

                        if 'direccion_notificacion' in new_data:
                            position_direccion_notificacion = new_data.index('direccion_notificacion')

                    elif count > 0:
                        address = build_address(
                            new_data[position_dir_tipo] if position_dir_tipo is not None else '',
                            new_data[position_dir_numero] if position_dir_numero is not None else '',
                            new_data[position_dir_apendice] if position_dir_apendice is not None else '',
                            new_data[position_dir_orientacion] if position_dir_orientacion is not None else '',
                            new_data[position_dir_numero2] if position_dir_numero2 is not None else '',
                            new_data[position_dir_apendice2] if position_dir_apendice2 is not None else '',
                            new_data[position_dir_orientacion2] if position_dir_orientacion2 is not None else '',
                            new_data[position_dir_placa] if position_dir_placa is not None else '',
                            new_data[position_dir_interior] if position_dir_interior is not None else '',
                            new_data[position_dir_bloque] if position_dir_bloque is not None else '',
                            new_data[position_direccion_especial] if position_direccion_especial is not None else ''
                        )

                        file_detail = [
                            FileDetail(
                                file=pending,
                                type_document=new_data[position_type_document] if position_type_document is not None else 0,
                                number_document=new_data[position_numero_documento] if position_numero_documento is not None else '',
                                social_reason=new_data[position_nombre_razon_social] if position_nombre_razon_social is not None else '',
                                surnames=new_data[position_apellidos] if position_apellidos is not None else '',
                                email=new_data[position_correo_electronico] if position_correo_electronico is not None else '',
                                department=new_data[position_departamento] if position_departamento is not None else '',
                                municipality=new_data[position_municipio] if position_municipio is not None else '',
                                country=new_data[position_pais] if position_pais is not None else '',
                                phone=new_data[position_tel_fijo] if position_tel_fijo is not None else '',
                                cell_phone=new_data[position_tel_celular] if position_tel_celular is not None else '',
                                address=new_data[position_direccion] if position_direccion is not None else '',
                                compound_address=address,
                                notification_address=new_data[position_direccion_notificacion] if position_direccion_notificacion is not None else ''
                            )
                        ]

                    count += 1
                    FileDetail.objects.bulk_create(file_detail)

            if is_error:
                pending.status = File.FINISHED_ERRORS
            else:
                pending.status = File.SUCCESSFULLY_COMPLETED

            pending.save()

        except Exception as error:
            pending.status = File.FINISHED_ERRORS
            pending.save()

def build_address(
    dir_tipo,
    dir_numero,
    dir_apendice,
    dir_orientacion,
    dir_numero2,
    dir_apendice2,
    dir_orientacion2,
    dir_placa,
    dir_interior,
    dir_bloque,
    direccion_especial
):
    return f'{dir_tipo} {dir_numero} {dir_apendice} {dir_orientacion} {dir_numero2} {dir_apendice2} {dir_orientacion2} {dir_placa} {dir_interior} {dir_bloque} {direccion_especial}'
