from django.shortcuts import render

def group(request, group_id):
    return render(request, "timetable/rasp.html", {"group_id": group_id})
