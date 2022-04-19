from django import template

register = template.Library()


@register.filter(name='zeroadd')
def zeroadd(value, arg):
    return str(value).zfill(arg)


@register.filter(name='phone')
def phone(value):
    phonenumber = ''
    inputnumber = str(value)

    phonenumber += inputnumber[0:3]
    phonenumber += '-'
    phonenumber += inputnumber[3:7]
    phonenumber += '-'
    phonenumber += inputnumber[7:]
    return phonenumber


@register.filter(name='cafe')
def cafe(value):
    if value is None:
        value = ''
    return value


@register.filter(name='time')
def time(value):
    value = str(value)
    result = ''
    result += value[0:5]
    return result
