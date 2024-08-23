import datetime
import json

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from django.template.response import TemplateResponse

from wagtail.models import Page
from wagtail.search.models import Query

from events.models import EventPostPage


def search(request):
    search_query = request.GET.get('query', None)
    page = request.GET.get('page', 1)

    # Search
    if search_query:
        search_results = Page.objects.live().search(search_query)
        query = Query.get(search_query)

        # Record hit
        query.add_hit()
    else:
        search_results = Page.objects.none()

    # Pagination
    paginator = Paginator(search_results, 10)
    try:
        search_results = paginator.page(page)
    except PageNotAnInteger:
        search_results = paginator.page(1)
    except EmptyPage:
        search_results = paginator.page(paginator.num_pages)

    return TemplateResponse(request, 'search/search.html', {
        'search_query': search_query,
        'search_results': search_results,
    })


def search_autocomplete(request):
    try:
        q = request.GET.get('term', '').capitalize()
        search_qs = EventPostPage.objects.filter(post_title__icontains=q).order_by("-start_date")
        results = []
        category = ""
        recently = datetime.datetime.now().date() - datetime.timedelta(days=183)
        present = datetime.datetime.now().date()

        for item in search_qs:
            if item.start_date.date() >= present:
                category = "Upcoming"
            elif item.start_date.date() < present and item.start_date.date() > recently:
                category = "Recent"
            else:
                category = "Archive"

            result = {
                "label": item.post_title,
                "value": item.slug,
                "category": category
            }
            results.append(result)

        data = json.dumps(results)
    except Exception as e:
        data = f'Fail: {e}'

    mimetype = 'application/json'

    return HttpResponse(data, mimetype)
