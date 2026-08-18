'''define qml_webs URL patterns'''

from django.urls import path
from . import views

app_name = 'qml_webs'
urlpatterns = [
    # main page
    path('',views.index,name='index'),
    path('persons/', views.persons, name='persons'),
    path('persons/<int:person_id>/', views.person_details, name='person_details'),
    path('products/', views.products, name='products'),
    path('products/<int:product_id>/', views.product_details, name='product_details'),
    path('contacts/', views.contacts, name='contacts'),
    path('topics/', views.topics, name='topics'),
    path('topics/<int:topic_id>/', views.topic, name='topic'),
    path('new_topic/', views.new_topic, name='new_topic'),
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
    path('pay/order/<int:product_id>/', views.create_order, name='create_order'),
    path('pay/order_view/', views.create_order_view, name='create_order_view'),
    path('pay/query_order/', views.query_order_status, name='query_order'),
    path('pay/wechat_notify/', views.wechat_pay_notify, name='wechat_notify'),
    path('pay/order_success/<int:product_id>', views.product_details, name='order_success'),
]