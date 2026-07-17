import json

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from book.google_books import search_book
from book.models import Book

from .selectors import reading_list_get_for_user, reading_lists_for_user
from .services import book_add_to_reading_list, reading_list_create, reading_list_create_default, reading_list_update


@login_required
def overview(request):
    return render(request, "overview.html", {"readinglists": reading_lists_for_user(user=request.user)})


@login_required
@require_POST
def add_to_reading_list(request):
    try:
        data = json.loads(request.body)
    except (TypeError, json.JSONDecodeError):
        return JsonResponse({"error": "Datos JSON inválidos."}, status=400)
    title = (data.get("title") or "").strip()
    author = (data.get("author") or "").strip()
    if not title or not author:
        return JsonResponse({"error": "El título y el autor son obligatorios."}, status=400)
    reading_list = reading_list_create_default(user=request.user)
    book, _ = Book.objects.get_or_create(title=title, author=author, defaults={"description": data.get("description") or "Sin descripción disponible", "buy_link": data.get("buyLink") or "", "cover": data.get("cover") or Book._meta.get_field("cover").default})
    try:
        added = book_add_to_reading_list(reading_list=reading_list, book=book)
    except ValidationError as error:
        return JsonResponse({"error": error.messages[0]}, status=400)
    return JsonResponse({"message": "Libro agregado a Leer más tarde." if added else "El libro ya está en Leer más tarde."})


@login_required
def createlist(request):
    if request.method == "GET":
        return render(request, "createlist.html")
    title, description = request.POST.get("title", "").strip(), request.POST.get("description", "").strip()
    if not title or not description:
        return render(request, "createlist.html", {"error_message": "El título y la descripción son obligatorios."})
    try:
        reading_list = reading_list_create(user=request.user, title=title, description=description, cover=request.FILES.get("cover"))
    except ValidationError as error:
        return render(request, "overview.html", {"readinglists": reading_lists_for_user(user=request.user), "error_message": error.messages[0]})
    messages.success(request, "Lista de lectura creada exitosamente.")
    return redirect("detail", reading_list.id)


@login_required
def detail(request, reading_list_id):
    reading_list = reading_list_get_for_user(user=request.user, reading_list_id=reading_list_id)
    if request.method == "POST":
        title, author = request.POST.get("title", "").strip(), request.POST.get("author", "").strip()
        if not title or not author:
            return _detail_response(request, reading_list, "El título y el autor son obligatorios.")
        book_data = search_book(title=title, author=author)
        if not book_data:
            return _detail_response(request, reading_list, "No fue posible encontrar un libro con esos datos.")
        book, _ = Book.objects.get_or_create(title=book_data["title"], author=book_data["author"], defaults=book_data)
        try:
            book_add_to_reading_list(reading_list=reading_list, book=book)
        except ValidationError as error:
            return _detail_response(request, reading_list, error.messages[0])
        messages.success(request, "Libro agregado exitosamente.")
        return redirect("detail", reading_list.id)
    return _detail_response(request, reading_list)


def _detail_response(request, reading_list, error_message=None):
    context = {"reading_list": reading_list, "books": reading_list.books.all()}
    if error_message:
        context["error_message"] = error_message
    return render(request, "detail.html", context)


@login_required
def updatereadinglist(request, reading_list_id):
    reading_list = reading_list_get_for_user(user=request.user, reading_list_id=reading_list_id)
    if request.method == "GET":
        return render(request, "updatereadinglist.html", {"initial_data": {"title": reading_list.title, "description": reading_list.description}, "reading_list": reading_list})
    title, description = request.POST.get("title", "").strip(), request.POST.get("description", "").strip()
    if not title or not description:
        return render(request, "updatereadinglist.html", {"reading_list": reading_list, "error": "El título y la descripción son obligatorios."})
    reading_list_update(reading_list=reading_list, title=title, description=description, cover=request.FILES.get("cover"))
    return redirect("detail", reading_list.id)


@login_required
@require_POST
def deletelist(request, reading_list_id):
    reading_list = reading_list_get_for_user(user=request.user, reading_list_id=reading_list_id)
    if reading_list.is_default:
        messages.error(request, "La lista predeterminada no puede eliminarse.")
    else:
        reading_list.delete()
        messages.success(request, "Lista de lectura eliminada exitosamente.")
    return redirect("overview")


@login_required
@require_POST
def deletebook(request, reading_list_id, book_id):
    reading_list = reading_list_get_for_user(user=request.user, reading_list_id=reading_list_id)
    reading_list.books.remove(book_id)
    messages.success(request, "Libro eliminado exitosamente.")
    return redirect("detail", reading_list.id)
