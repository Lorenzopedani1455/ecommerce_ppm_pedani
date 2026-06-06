from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404

from .models import Category, Product, Cart, CartItem, Order, OrderItem
from .serializers import CategorySerializer, ProductSerializer, CartSerializer, OrderSerializer
from users.permissions import IsStoreManager

# --- VISTE PER LE CATEGORIE ---
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated(), IsStoreManager()]

# --- VISTE PER I PRODOTTI ---
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated(), IsStoreManager()]

# --- VISTE PER IL CARRELLO ---
class CartViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def me(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_item(self, request, pk=None):
        cart = get_object_or_404(Cart, pk=pk, user=request.user)
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        product = get_object_or_404(Product, id=product_id)
        
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()

        return Response({'status': 'Oggetto aggiunto al carrello'})

    @action(detail=True, methods=['delete'])
    def remove_item(self, request, pk=None):
        cart = get_object_or_404(Cart, pk=pk, user=request.user)
        cart_item_id = request.data.get('cart_item_id')
        cart_item = get_object_or_404(CartItem, id=cart_item_id, cart=cart)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# --- VISTE PER GLI ORDINI ---
class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_store_manager:
            return Order.objects.all().order_by('-created_at')
        return Order.objects.filter(user=self.request.user).order_by('-created_at')

    def create(self, request, *args, **kwargs):
        cart = get_object_or_404(Cart, user=request.user)
        if not cart.items.exists():
            return Response({'detail': 'Il carrello è vuoto'}, status=status.HTTP_400_BAD_REQUEST)

        shipping_address = request.data.get('shipping_address')
        if not shipping_address:
            return Response({'detail': 'Indirizzo di spedizione richiesto'}, status=status.HTTP_400_BAD_REQUEST)

        for item in cart.items.all():
            if item.product.quantity_available < item.quantity:
                return Response({'detail': f'Stock insufficiente per {item.product.name}'}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(user=request.user, shipping_address=shipping_address)

        for item in cart.items.all():
            final_price = item.product.price
            if item.product.is_discounted and item.product.discount:
                final_price = final_price * (1 - (item.product.discount / 100))

            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=final_price
            )
            item.product.quantity_available -= item.quantity
            item.product.save()

        cart.items.all().delete()
        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        if not request.user.is_store_manager:
            return Response({'detail': 'Non hai i permessi'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def user(self, request):
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def admin(self, request):
        if not request.user.is_store_manager:
            return Response(status=status.HTTP_403_FORBIDDEN)
        orders = Order.objects.all().order_by('-created_at')
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)