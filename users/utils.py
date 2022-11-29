# per funkcione ndihmese
from django.db.models import Q 
from django.core.paginator import Paginator ,PageNotAnInteger , EmptyPage


from .models import Profile , Skill

def searchProfiles(request):
    search_query = ''

    if request.GET.get('search_query'): # 'search_query' emri i inputit name
        search_query = request.GET.get('search_query')

    # PER SKILLS
    skills = Skill.objects.filter(name__icontains=search_query)

    #distinct() - e kthen veq ni instance tqdo user-i
    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) | Q(short_intro__icontains = search_query) |
        Q(skill__in=skills) , #childmodel__in per child models
        )
         # Q edhe | kshyrin edhe te name edhe te short_intro edhe na japin rezultatet

    return profiles , search_query

def paginateProfiles(request , profiles , results):

    # pagination
    page = request.GET.get('page')
    paginator = Paginator(profiles , results)
    """
    varName = Paginator(queryset , sa postime per qdo faqe)
    """
    try:
        profiles = paginator.page(page) # na jep faqen e par prej 3(results)
    except PageNotAnInteger: # kur thyje useri heren e par
        page = 1
        profiles = paginator.page(page)
    except EmptyPage: # kur tmundohet me shku ma shum se qka kena faqe
        page = paginator.num_pages
        profiles = paginator.page(page)

    left_index = (int(page) - 4) # per faqet qe shfaqen nmajt
    if left_index < 1:
        left_index =1 

    right_index = (int(page) + 5) # per faqet qe shfaqen ndjath
    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1

    custom_range = range(left_index , right_index)


    return custom_range , profiles 
