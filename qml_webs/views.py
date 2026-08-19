from django.shortcuts import render, redirect
from .models import Person, Product, Topic, Entry, Order
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse, HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .utils.wechat_pay import create_native_order, generate_qrcode_data, wx_query_order, wx_aes_gcm_decrypt
import uuid, json



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

def create_order(request, product_id):
    product = Product.objects.get(id=product_id)
    context = {'product': product}
    return render(request, 'qml_webs/product_pay.html', context)

def create_order_view(request):
    """create order, return scan to pay qr code"""
    product_id = request.GET.get("pid")
    product = Product.objects.get(id=product_id)
    order_no = str(uuid.uuid4()).replace("-", "")
    order = Order.objects.create(
        order_no=order_no,
        product=product,
        total_fee=product.price,
    )
    #use wechat native to order
    res = create_native_order(order_no, float(product.price), product.name)
    print("create_order_view:" + order_no + " " + res["code_url"])
    if res.get("code_url"):
        order.code_url = res["code_url"]
        order.save()
        qr_b64 = generate_qrcode_data(res["code_url"])
        return JsonResponse({
            "ok": True,
            "order_no": order_no,
            "qr_img": qr_b64
        })
    else:
        return JsonResponse({"ok":False,"msg":res.get("message","Use wechat failure")})

def query_order_status(request):
    """query order status from frontend"""
    order_no = request.GET.get("order_no")
    order = Order.objects.filter(order_no=order_no).first()
    print("query_order_status:" + order_no + " " + str(order.status))
    if not order:
        return JsonResponse({"ok":False,"msg":"Order does not exist"})

    if order.status == Order.STATUS_PAID:
        return JsonResponse({"status":Order.STATUS_PAID})

    wx_result = wx_query_order(order_no)
    if wx_result is None:
        return JsonResponse({"status":Order.STATUS_PENDING})

    trade_state = wx_result.get("trade_state")
    print("query_order_status: " + trade_state)
    if trade_state == "SUCCESS":
        order.status = Order.STATUS_PAID
        order.transaction_id = wx_result.get("transaction_id")
        order.pay_time = wx_result.get("success_time")
        order.save()
        return JsonResponse({"status":Order.STATUS_PAID})
    else:
        return JsonResponse({"status":Order.STATUS_PENDING})


@csrf_exempt
def wechat_pay_notify(request):
    """wechat pay notify response, public https"""
    print("wechat_pay_notify method:" + request.method)
    if request.method != 'POST':
        return JsonResponse({"code": "FAIL", "message": "method error"}, status=405)

    try:
        body = request.body
        print(f"wechat raw body: {body.decode('utf-8')}")

        #import xml.etree.ElementTree as ET
        #root = ET.fromstring(body)
        #resource_node = root.find("./resource")
        #nonce = resource_node.find("nonce").text
        #ciphertext = resource_node.find("ciphertext").text
        #associated_data = resource_node.find("associated_data").text

        data = json.loads(body)
        resource = data["resource"]
        nonce = resource["nonce"]
        ciphertext = resource["ciphertext"]
        associated_data = resource["associated_data"]
        pay_info = wx_aes_gcm_decrypt(ciphertext, nonce, associated_data)
        print(f"decrypt pay_info: {pay_info}")

        order_no = pay_info["out_trade_no"]
        transaction_id = pay_info["transaction_id"]
        trade_state = pay_info["trade_state"]
        print("wechat_pay_notify:" + order_no + " " + transaction_id + " " + trade_state)

        order = Order.objects.filter(order_no=order_no).first()
        if order and trade_state == "SUCCESS":
            order.status = Order.STATUS_PAID
            order.transaction_id = transaction_id
            order.pay_time = timezone.now()
            order.save()

        return JsonResponse({"code":"SUCCESS","message":"OK"})

    except Exception as e:
        import traceback
        stack = traceback.format_exc()
        print(f"=====WECHAT_NOTIFY_ERROR=====\n{stack}")
        return JsonResponse({"code":"FAIL","message": "error"}, status=500)