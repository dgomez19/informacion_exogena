from rest_framework.renderers import BaseRenderer

from uuid import UUID

from datetime import date

import json

from drf_excel.renderers import XLSXRenderer

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return f'{obj}'
        return json.JSONEncoder.default(self, obj)


class ErrorApiRenderer(BaseRenderer):
    media_type = 'aplication/json'
    format = 'json'

    def render(self, data, accepted_media_type=None, renderer_context=None):

        response_dict = {
            'detalle': data
        }

        if data.get('non_field_errors'):
            response_dict = {
                'detalle': data.get('non_field_errors')[0]
            }

        if data.get('detail'):
            response_dict = {
                'detalle': data.get('detail')
            }

        return json.dumps(response_dict, cls=CustomEncoder)


class ExcelRenderer(XLSXRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context.get('response')

        if response.status_code >= 400:
            response['Content-Type'] = 'application/json'
            return bytes(json.dumps(response.data).encode('utf-8'))

        view = renderer_context.get('view')

        filename = getattr(view, 'filename', 'reporte_{today}.xlsx')

        if filename:
            filename = filename.format(today=date.today().strftime('%d_%m_%Y'))
            renderer_context.get('response')['Access-Control-Expose-Headers'] = 'Content-Disposition'
            renderer_context.get('response')['Content-Disposition'] = f'attachment; filename="{filename}"'

        if hasattr(view, 'transform_data'):
            data = view.transform_data(data)

        return super().render(data, accepted_media_type, renderer_context)
