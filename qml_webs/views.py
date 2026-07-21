from django.shortcuts import render, redirect
from .models import Person, PersonDetail, Product, ProductDetail, Topic, Entry
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required
from django.http import Http404

# Create your views here.
def index(request):
    '''qml_webs index main page'''
    return render(request, 'qml_webs/index.html')

def persons(request):
    '''display all the persons'''
    persons = Person.objects.order_by('date_joined')
    context = {'persons': persons}
    return render(request, 'qml_webs/persons.html', context)

def person_details(request, person_id):
    '''display the person detail'''
    person = Person.objects.get(id=person_id)
    details = person.persondetail_set.order_by('-date_added')
    honorskills = person.personhonorskill_set.order_by('-date_added')
    context = {'person': person, 'details': details, 'honorskills': honorskills}
    return render(request, 'qml_webs/person_details.html', context)

def products(request):
    '''display all the products'''
    products = Product.objects.order_by('-date_added')
    context = {'products': products}
    return render(request, 'qml_webs/products.html', context)

def product_details(request, product_id):
    '''display the product detail'''
    product = Product.objects.get(id=product_id)
    details = product.productdetail_set.order_by('-date_added')
    context = {'product': product, 'details': details}
    return render(request, 'qml_webs/product_details.html', context)

def contacts(request):
    '''display the contact page'''
    return render(request, 'qml_webs/contacts.html')

@login_required
def topics(request):
    """display all the topics"""
    topics = Topic.objects.order_by('-date_added')
    context = {'topics': topics}
    return render(request, 'qml_webs/topics.html', context)

@login_required
def topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'qml_webs/topic.html', context)

@login_required
def new_topic(request):
    """add a new topic"""
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('qml_webs:topics')

    context = {'form': form}
    return render(request, 'qml_webs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """add a new entry"""
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.owner = request.user
            new_entry.save()
            return redirect('qml_webs:topic', topic_id=topic_id)

    context = {'topic': topic, 'form': form}
    return render(request, 'qml_webs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """edit an entry"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if entry.owner != request.user:
        raise Http404("你没有权限修改这条内容")
        #return redirect('qml_webs:topic', topic_id=topic.id)

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(data=request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect('qml_webs:topic', topic_id=topic.id)

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'qml_webs/edit_entry.html', context)