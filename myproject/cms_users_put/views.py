from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from models import Pages


# Create your views here.

def todo(request):
    salida = ""
    lista = Pages.objects.all()
    salida += "Las paginas que hay son:<ul>"
    for fila in lista:
        salida += "<li>" + fila.name + "--" + str(fila.page)
    salida += "</ul>"
    return HttpResponse(salida)


def handler(request, recurso):
    salida = ""

    if request.method == "PUT":
        if request.user.is_authenticated():
            fila = Pages(name=recurso, page=request.body)
            fila.save()
        else:
            salida += "No puedes crear una pagina sin estar registrado"
            return HttpResponse(salida)

    try:
        fila = Pages.objects.get(name=recurso)
        if request.user.is_authenticated():
            salida += "Estas registrado. Eres " + request.user.username + ""
            salida += " <br><a href='logout'>Logout</a><br><br>"
        else:
            salida += "No estas registrado -> "
            salida += "<a href='/admin/login/'>Autenticate</a><br><br>"
        salida += fila.page
        return HttpResponse(salida)
    except Pages.DoesNotExist:
        return HttpResponseNotFound('Pagina no encontrada: /%s.' % recurso)


def notfound(request, recurso):
    return HttpResponseNotFound("No tenemos " + recurso)
