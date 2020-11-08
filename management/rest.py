from rest_framework import routers, viewsets, serializers

from shop.models import Product, ProductCategory, ProductAttributeType, ProductAttributeTypeInstance, ProductSubItem
from shop.rest import AddressViewSet, GuestViewSet, ContactViewSet, DeliveryViewSet, OrderViewSet, OrderItemViewSet, \
    CheckboxOrderItemViewSet, NumberOrderItemViewSet, SelectOrderItemViewSet, FileOrderItemViewSet


class ProductAttributeTypeSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = ProductAttributeType
        fields = '__all__'


class ProductAttributeTypeInstanceSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = ProductAttributeTypeInstance
        fields = '__all__'


class ProductCategorySerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = ProductCategory
        fields = '__all__'


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = '__all__'


class ProductSubItemSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = ProductSubItem
        fields = '__all__'


###############################################################


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer


class ProductAttributeTypeViewSet(viewsets.ModelViewSet):
    queryset = ProductAttributeType.objects.all()
    serializer_class = ProductAttributeTypeSerializer


class ProductAttributeTypeInstanceViewSet(viewsets.ModelViewSet):
    queryset = ProductAttributeTypeInstance.objects.all()
    serializer_class = ProductAttributeTypeInstanceSerializer


class ProductSubItemViewSet(viewsets.ModelViewSet):
    queryset = ProductSubItem.objects.all()
    serializer_class = ProductSubItemSerializer


router = routers.DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'categories', ProductCategoryViewSet)
router.register(r'productattributetypes', ProductAttributeTypeViewSet)
router.register(r'productattributetypeinstances', ProductAttributeTypeInstanceViewSet)
router.register(r'productsubitem', ProductSubItemViewSet)
router.register(r'accounts', GuestViewSet)
router.register(r'addresses', AddressViewSet)
router.register(r'contacts', ContactViewSet)
router.register(r'deliveries', DeliveryViewSet)
router.register(r'order', OrderViewSet)
router.register(r'orderitem',OrderItemViewSet)
router.register(r'fileorderitem',FileOrderItemViewSet)
router.register(r'selectorderitem',SelectOrderItemViewSet)
router.register(r'numberorderitem',NumberOrderItemViewSet)
router.register(r'checkboxorderitem',CheckboxOrderItemViewSet)