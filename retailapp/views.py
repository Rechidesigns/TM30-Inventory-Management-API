# from django.shortcuts import render


from rest_framework.views import APIView
from rest_framework import status
from .models import Product, Cart
from retailapp.serializers import ProductSerializer
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.authentication import JWTAuthentication
from account.models import CustomUser 
from account.permissions import IsAdminOnly, IsUserAuthenticated, IsUserOrReadOnly
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, authentication_classes, permission_classes
from .serializers import CartSerializer, ProductSerializer, ProductUserSerializer, CartReqSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import NotFound, PermissionDenied



class ProductView(APIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsUserOrReadOnly]
    
    def get(self, request, format=None):
        """
        Allow logged in user and admin to get all products in the database.
        If item quantity is equal to zero it does not show in the retrieved data.
        It also returns the number of user that ordered the item.
        Allows only admin to post products.
        """
        obj = Product.objects.all()
        new_data = []
        for product in obj:
            if product.quantity > 0:
                new_data.append(product)

        serializer = ProductUserSerializer(new_data, many=True, )

        data = {
            'message': 'retrieve sucessful',
            'data': serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)

    @swagger_auto_schema(method='post', request_body=ProductSerializer())
    @action(methods=['POST'], detail=True)
    def post(self, request, format=None):
            
        serializer = ProductSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            
            data = {
                "message":"success"
            }

            return Response(data, status = status.HTTP_200_OK)

        else:
            data = {
                "message":"failed",
                "error":serializer.errors
            }
        
        return Response(data, status = status.HTTP_400_BAD_REQUEST)

class ProductEditView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOnly]

    def get_product(self, product_id):
        """
        Tries to retrieves a product from the database with the given id.
        If the product does not exist, it therefore returns an error message.
        """
        
        try:
            return Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise NotFound(detail={'message': 'product with id does not exist.'})

    def get(self, request, product_id, format=None):
        
        """
        Retrieve an product from the database with the given id
        Allows only 
           
        """
        obj = self.get_product(product_id=product_id)
        serializer = ProductSerializer(obj)

        data = {
            'message': 'Successful retrieve',
            'data': serializer.data
        }

        return Response(data, status=status.HTTP_200_OK)

    @swagger_auto_schema(method='put', request_body=ProductSerializer())
    @action(methods=['PUT'], detail=True)
    def put(self, request, product_id, format=None):
        """
        Updates the entire or partial data of an existing product in the database.
        Allows only admin users to update the given item.
        """

        obj = self.get_product(product_id=product_id)
        serializer = ProductSerializer(obj, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            data = {
                'message': 'update successful',
                'data': serializer.data
            }

            return Response(data, status=status.HTTP_202_ACCEPTED)

        else:

            data = {
                'message': 'update failed',
                'data': serializer.errors
            }

            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(method='delete')
    @action(methods=['DELETE'], detail=True)
    def delete(self, request, product_id, format=None):

        """Deletes an existing product from the database.
           Returns a message response to be sure it deleted and a status code of 204 NO_CONTENT.
           It is only accessible to admin users.
        """

        obj = self.get_product(product_id=product_id)
        obj.delete()
        data = {
            'message': 'Product deleted successfully.'
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)

class CartView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsUserAuthenticated]

    def get(self, request, format=None):
        """
        Retrieves a logged in user cart from the database, only pending product are shown.
        Anonymoususer are restricted from using this method.
        returns an error message if user is not logged in.
        """
        if request.user in CustomUser.objects.all():

            user_id = request.user.id
            object = CustomUser.objects.get(id=user_id)
            obj = object.user.filter(status='pending')

            serializer = CartSerializer(obj, many=True)

            data = {
                'message': 'cart retrieve successful',
                'total orders': obj.count(),
                'data': serializer.data
            }

            return Response(data, status=status.HTTP_200_OK)

        else:
            raise PermissionDenied(detail={'error': 'AnonymousUser not authorized and has no cart present in the database.'})

    @swagger_auto_schema(method='post', request_body=CartReqSerializer())
    @action(methods=['POST'], detail=True)
    def post(self, request, format=None):
        """
        Adds product to the cart of a user in the database to the cart model only if the  
        product quantity available in the database is greater than quantity demanded.
        Accessible only to logged in users.
        """  
        data = {}
        data['cart_product'] = request.data['cart_product']
        data['product_quantity'] = request.data['product_quantity']
        data['user'] = request.user.id
        try:
            cart_total = Product.objects.get(id=data['cart_product'])          
            cart_total_price = cart_total.price
            data['product_cost'] = data['product_quantity'] * cart_total_price
            data['status'] = 'pending'



            users = CustomUser.objects.all()
            if request.user in users:
                user_id = request.user.id
                object = CustomUser.objects.get(id=user_id)
                obj = object.user.all()
                objs = []
                for item in obj:
                    items = Product.objects.get(item_name=item)
                    it_name = items.item_name
                    objs.append(it_name) # to get the name of item of the cart order and append to a list

                if str(cart_total) not in objs: # to check whether the cart order is already in the user cart
                
                    if data['quantity'] > cart_total.quantity_available: #check whether quantity in the store is greater than quantity demanded
                        return Response(data={'message': 'Quantity ordered is higher than quantity available in store'}, status=status.HTTP_403_FORBIDDEN)


            if request.user in CustomUser.objects.all():
                
                if data['product_quantity'] > cart_total.product_quantity:
                    return Response(data={'message': 'Quantity ordered is higher than quantity available in store'}, status=status.HTTP_403_FORBIDDEN)

                else:
                    cart_total.product_quantity -= data['product_quantity'] 
                    cart_total.save()
                    serializer = CartSerializer(data=data)
                    
                    if serializer.is_valid():
                        serializer.save()
                        
                        data = {
                            "message":"product successfully added to cart",
                        }

                        return Response(data, status = status.HTTP_200_OK)

                    else:
                        data = {
                            "message":"failed",
                            "error":serializer.errors
                        }
                    
                    return Response(data, status = status.HTTP_400_BAD_REQUEST)

            else:
                raise PermissionDenied(detail={'message': 'AnonymousUser are forbidden to perform this action.'})

        except Product.DoesNotExist:
            raise NotFound(detail={'message': 'product with id does not exist'})

class CartEditView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsUserAuthenticated]

    def get_cart_products(self, cart_id):
        """
        Tries to retrieves a cart product from the database with the given id.
        If the cart does not exist, it returns an error message.
        """
        
        try:
            return Cart.objects.get(id=cart_id)
        except Cart.DoesNotExist:
            raise NotFound(detail={'message': 'cart-product with id does not exist.'})
   

    @swagger_auto_schema(method='delete')
    @action(methods=['DELETE'], detail=True)
    def delete(self, request, cart_id, format=None):
        """Delete a single cart product relating to a logged in user.
           Returns a reponse message 'success' if deleted successfully and status code of 204.
           when a pending cart product is deleted the quantity is added to the quantity of the product model.
        """
        try:
            user_id = request.user.id
            object = CustomUser.objects.get(id=user_id)

            
            if request.user == object and request.user in CustomUser.objects.all():
                obj = self.get_cart_product(cart_id=cart_id)
                try: 
                    p = Product.objects.get(product_name=obj.cart_products)
                    p.product_quantity+=obj.product_quantity
                    p.save()
                
                    obj.delete()
                    return Response(status=status.HTTP_204_NO_CONTENT)
                except Cart.DoesNotExist:
                    raise NotFound(detail={'message': 'Cart does not exist'})

            else:
                raise PermissionDenied(detail={'message': 'user is forbidden to acces another user data or user is anonymous.'})
            
        except CustomUser.DoesNotExist:
            raise NotFound(detail={'message': 'User is an anonyousUser.'})

@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminOnly])
def delivered_products(request, cart_id):
    """Allows admin user to change the status of a cart product to delivered if the product has been delivered to the user"""
    
    if request.method == 'GET':
        try:
            cart_product = Cart.objects.get(id=cart_id, status="pending")
            cart_product.status = "delivered"
            cart_product.save()
       
            return Response({"message":"success"}, status=status.HTTP_204_NO_CONTENT)
        
        except Cart.DoesNotExist:
            return Response({"error":"Cart not found","message":"failed"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminOnly])
def make_pending(request, cart_id):
    """Allows admin user to make a cart product status to 'pending' if the product wasnt successfully delievered"""
    
    if request.method == 'GET':
        try:
            cart_product = Cart.objects.get(id=cart_id, status="delivered")
            cart_product.status = "pending"
            cart_product.save()
       
            return Response({"message":"success"}, status=status.HTTP_204_NO_CONTENT)
        
        except Cart.DoesNotExist:
            return Response({"error":"not found","message":"failed"}, status=status.HTTP_404_NOT_FOUND)

