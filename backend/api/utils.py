from django.http import HttpResponse


def make_file(data, filename, http_status):
    product_list = []
    for ingredient in data:
        product_list.append(
            '{name} ({unit}) - {amount}'.format(
                name=ingredient['ingredient__name'],
                unit=ingredient['ingredient__measurement_unit'],
                amount=ingredient['amount']
            )
        )
    response = HttpResponse(
        content='\n'.join(product_list),
        content_type='text/plain',
        status=http_status
    )
    response['Content-Disposition'] = (
        f'attachment; filename={filename}')
    return response
