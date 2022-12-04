from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from .models import ToDoItems
from mysite.models import get_query_set_or_404, get_query_object_or_404, create_object
from django.http import Http404


class Home(View):

    def get(self, request):
        try:
            todo_list = get_query_set_or_404(request, ToDoItems)
        except Http404:
            todo_list = ToDoItems.objects.none()
        return render(request, 'todo/home.html', {'todo_list': todo_list})

    def post(self, request):
        todo_item = request.POST['todo_item']
        create_object(request, ToDoItems, item_name=todo_item)
        return redirect('todo:home')


class EditItem(View):

    def get(self, request, item_id):
        item = get_query_object_or_404(request, ToDoItems, pk=item_id)
        return render(request, 'todo/edit_item.html', {'item': item})

    def post(self, request, item_id):
        item = get_query_object_or_404(request, ToDoItems, pk=item_id)
        new_name = request.POST['new_name']
        item.item_name = new_name
        item.save()
        messages.success(request, 'Item edited successfully')
        return redirect('todo:home')


def delete_item(request, item_id):
    item = get_query_object_or_404(request, ToDoItems, pk=item_id)
    item.delete()
    messages.success(request, 'Item removed successfully')
    return redirect('todo:home')


def mark_item(request, item_id):
    item = get_query_object_or_404(request, ToDoItems, pk=item_id)
    item.is_completed = not item.is_completed
    item.save()
    return redirect('todo:home')








