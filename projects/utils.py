from django.db.models import Q
from django.core.paginator import Paginator ,PageNotAnInteger , EmptyPage

from .models import Project , Tag

def searchProjects(request):
    search_query = ''

    if request.GET.get('search_query'): # 'search_query' emri i inputit name
        search_query = request.GET.get('search_query')
    
    # many to many field 
    tags = Tag.objects.filter(
        name__icontains=search_query
    )
    
    projects = Project.objects.distinct().filter(
        Q(title__icontains=search_query) |
        Q(description__icontains = search_query) |
        #Parentmodel__field__icontains=
        Q(owner__name__icontains=search_query) |
        Q(tags__in=tags)
    )

    return projects , search_query

def paginateProjects(request , projects , results):

    # pagination
    page = request.GET.get('page')
    paginator = Paginator(projects , results)
    """
    varName = Paginator(queryset , sa postime per qdo faqe)
    """
    try:
        projects = paginator.page(page) # na jep faqen e par prej 3(results)
    except PageNotAnInteger: # kur thyje useri heren e par
        page = 1
        projects = paginator.page(page)
    except EmptyPage: # kur tmundohet me shku ma shum se qka kena faqe
        page = paginator.num_pages
        projects = paginator.page(page)

    left_index = (int(page) - 4) # per faqet qe shfaqen nmajt
    if left_index < 1:
        left_index =1 

    right_index = (int(page) + 5) # per faqet qe shfaqen ndjath
    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1

    custom_range = range(left_index , right_index)


    return custom_range , projects 
