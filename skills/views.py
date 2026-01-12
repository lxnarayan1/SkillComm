from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Skill

@login_required
def browse_users(request):
    users = User.objects.exclude(id=request.user.id).select_related('profile')
    
    # Get filter parameters
    skill_teach = request.GET.get('skill_teach')
    skill_learn = request.GET.get('skill_learn')
    search = request.GET.get('search')
    
    # Apply filters
    if skill_teach:
        users = users.filter(profile__skills_to_teach__id=skill_teach)
    
    if skill_learn:
        users = users.filter(profile__skills_to_learn__id=skill_learn)
    
    if search:
        users = users.filter(
            Q(username__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(profile__location__icontains=search)
        )
    
    # Get all skills for filter dropdowns
    all_skills = Skill.objects.all()
    
    context = {
        'users': users.distinct(),
        'all_skills': all_skills,
        'selected_skill_teach': skill_teach,
        'selected_skill_learn': skill_learn,
        'search_query': search,
    }
    return render(request, 'skills/browse_users.html', context)

@login_required
def skill_list(request):
    skills = Skill.objects.all()
    category = request.GET.get('category')
    
    if category:
        skills = skills.filter(category=category)
    
    context = {
        'skills': skills,
        'categories': Skill.CATEGORY_CHOICES,
        'selected_category': category,
    }
    return render(request, 'skills/skill_list.html', context)
