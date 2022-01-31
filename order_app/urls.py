from django.urls import path
from . import views

urlpatterns = [


    path('my-orders/', views.my_orders_view, name='my_orders'),

    path('cancel-order/<str:pk>/', views.cancel_order_view, name='cancel'),

    path('detail-ordered-service/<str:pk>/', views.selected_order_service_info_view, name='orderd_item_det'),

    path('detail-ordered-custum-service/<str:pk>/', views.selected_custom_service_info_view,
         name='orderd_custom_item_det'),

    path('delete-from-order/<str:pk>/<str:order_pk>/', views.delete_orderd_service_view, name='delFromOrder'),

    path('order-offer/<str:pk>/', views.order_offer_view, name="order_offer"),

    path('cancel-order-offer/<str:pk>/', views.cancel_order_offer_view, name="cancel_order_offer"),

    path('edite-order-offer/<str:pk>/', views.edite_order_offer_view, name="edite_order_offer"),

    path('conter-order-offer/<str:pk>/', views.conter_order_offer_view, name="conter_order_offer"),

    path('orderd-service-offer/<str:pk>/', views.order_service_offer_view, name="orderd_service_offer"),

    path('cancel-orderd-service-offer/<str:pk>/', views.cancel_order_service_offer_view,
         name="cancel_order_service_offer"),

    path('edite-orderd-service-offer/<str:pk>/', views.edite_order_service_offer_view,
         name="edite_order_service_offer"),

    path('conter-orderd-service-offer/<str:pk>/', views.conter_order_service_offer_view,
         name="conter_order_service_offer"),

    path('orderd-custom-service-offer/<str:pk>/', views.order_custom_service_offer_view,
         name="orderd_custom_service_offer"),

    path('cancel-custom-service-offer/<str:pk>/', views.cancel_custom_service_offer_view,
         name="cancel_custom_service_offer"),

    path('edite-custom-service-offer/<str:pk>/', views.edite_custom_service_offer_view,
         name="edite_custom_service_offer"),

    path('conter-custom-service-offer/<str:pk>/', views.conter_custom_service_offer_view,
         name="conter_custom_service_offer"),

    path('location-offer/<str:pk>/<str:item>/<str:f_type>/', views.location_offer_view, name="location_offer"),

    path('cancel-location-offer/<str:pk>/<str:item>/<str:f_type>/', views.cancel_location_offer_view,
         name="cancel_location_offer"),

    path('accepte-location-offer/<str:pk>/<str:item>/<str:f_type>/', views.accept_location_offer_view,
         name="accept_location_offer"),

    path('add-task/<str:pk>/<str:item>/<str:f_type>/', views.add_extra_tasks_view, name="add_task"),

    path('edite-task/<str:pk>/<str:item>/<str:f_type>/', views.edite_extra_tasks_view, name="edite_task"),

    path('delete-task/<str:pk>/<str:item>/<str:f_type>/', views.delete_extra_tasks_view, name="delete_task"),

    path('accepte-offer/<str:pk>/', views.accept_offer_view, name="accept_offer"),

    path('delivery-book/<str:pk>/', views.delivery_book_view, name="deli_book"),

    path('edite-location-offer/<str:pk>/<str:item>/<str:f_type>/', views.edite_location_offer_view,
         name="edite_location_offer"),

    path('conter-location-offer/<str:pk>/<str:item>/<str:f_type>/', views.conter_location_offer_view,
         name="conter_location_offer"),

    path('del-orderd-locationl/<str:pk>/<str:service_pk>/<str:the_type>/', views.delete_orderd_location_view,
         name="del_orderd_location"),

    path('edit-orderd-locationl/<str:pk>/<str:item>/<str:the_type>/', views.edit_orderd_location_view,
         name="edit_ordered_location"),
]
