import json
import datetime
from rest_framework import serializers
from phonenumber_field.modelfields import PhoneNumberField
from accounts.serializers import AccountCreationSerializer

from carts.models import CartItem
from .models import Payment, Order, OrderProduct

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'user', 'payment_id', 'payment_method', 'amount_paid', 'status')

    def create(self, validated_data):
      body = self.context.get('request').data

      validated_data['payment_id'] = body['transID'],
      validated_data['payment_method'] = body['payment_method'],
      # validated_data['amount_paid'] = order.order_total,
      validated_data['status'] = body['status'],

      payment = Payment.objects.create(**validated_data)
      return payment

      

    
class OrderSerializer(serializers.ModelSerializer):
      status = serializers.CharField(default='New', read_only=True)
      full_name = serializers.SerializerMethodField(read_only=True)
      user = AccountCreationSerializer(read_only=True)
      payment = serializers.CharField(default='Awaiting Payment', read_only=True)
      order_number = serializers.CharField(max_length=20, read_only=True)
      first_name = serializers.CharField(max_length=50, read_only=True)
      last_name = serializers.CharField(max_length=50, read_only=True)
      phone = PhoneNumberField()
      email = serializers.EmailField(max_length=50, read_only=True)
      address_line_1 = serializers.CharField(max_length=50)
      address_line_2 = serializers.CharField(max_length=50, allow_null=True)
      country = serializers.CharField(max_length=50)
      state = serializers.CharField(max_length=50)
      city = serializers.CharField(max_length=50)
      order_note = serializers.CharField(max_length=100, allow_null=True)
      order_total = serializers.FloatField(read_only=True)
      tax = serializers.FloatField(read_only=True)
      ip = serializers.IPAddressField(allow_null=True, read_only=True)
      is_ordered = serializers.BooleanField(default=False)
      created_at = serializers.DateTimeField(read_only=True)
      updated_at = serializers.DateTimeField(read_only=True)

      class Meta:
          model = Order
          fields = '__all__'

          read_only_fields = ['user', 'payment', 'order_number', 'order_total', 'tax', 'status', 'ip', 'is_ordered', 'created_at', 'updated_at', 'full_name', 'email', 'phone', 'first_name', 'last_name',]

      def get_full_name(self, obj):
          return obj.first_name + ' ' + obj.last_name

      def create(self, validated_data, total=0, quantity=0):
          current_user = self.context.get('request').user
          cart_items = CartItem.objects.filter(user=current_user)

          print(cart_items)


          grand_total = 0
          tax = 0
          for cart_item in cart_items:
              total += (cart_item.product.price * cart_item.quantity)
              quantity += cart_item.quantity
          tax = (2 * total)/100
          grand_total = total + tax

          yr = int(datetime.date.today().strftime('%Y'))
          dt = int(datetime.date.today().strftime('%d'))
          mt = int(datetime.date.today().strftime('%m'))
          d = datetime.date(yr,mt,dt)
          current_date = d.strftime("%Y%m%d") 

          validated_data['order_number'] = current_date + str(current_user.id)
          validated_data['order_total'] = grand_total
          validated_data['tax'] = tax
          validated_data['user'] = current_user
          validated_data['first_name'] = current_user.first_name
          validated_data['last_name'] = current_user.last_name
          validated_data['phone'] = current_user.phone_number
          validated_data['email'] = current_user.email
          validated_data['payment'] = 'Awaiting Payment'
          validated_data['status'] = 'New'
          validated_data['ip'] = self.context.get('request').META.get("REMOTE_ADDR")
          validated_data['is_ordered'] = True
          validated_data['created_at'] = datetime.datetime.now()
          validated_data['updated_at'] = datetime.datetime.now()


          
          order = Order.objects.create(**validated_data)
          return order

class OrderProductSerializer(serializers.ModelSerializer):
      class Meta:
          model = OrderProduct
          fields = '__all__'

      def create(self, validated_data):
          body = json.loads(self.request.body)
          validated_data['order'] = body['order']
          validated_data['payment'] = body['payment']
          validated_data['user'] = body['user']
          order_product = OrderProduct.objects.create(**validated_data)
          return order_product


class UpdateOrderStatusSerializer(serializers.ModelSerializer):
    status = serializers.CharField(default='New')
    class Meta:
        model = Order
        fields = ['status']

    def update(self, instance, validated_data):
        instance.status = validated_data['status']
        instance.save()
        return instance
    
    