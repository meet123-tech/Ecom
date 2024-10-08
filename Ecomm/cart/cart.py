from shop.models import Product,Profile

class Cart():
    
    def __init__(self,request):
        self.session = request.session

        self.request = request

        cart = self.session.get('session_key')

        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        self.cart = cart

    def add(self,product,quantity):
        product_id = str(product.id)
        product_qunt = str(quantity)

        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qunt)
            # print(self.cart)
        
        self.session.modified = True

       
        if self.request.user.is_authenticated:
            
            current_user = Profile.objects.filter(user__id = self.request.user.id)
            cart_memory = str(self.cart)
            cart_memory = cart_memory.replace("\'","\"")
            current_user.update(old_cart = str(cart_memory))
            
    def db_add(self, product, quantity):
        product_id = str(product)
        product_qunt = str(quantity)

        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qunt)
            # print(self.cart)

        self.session.modified = True

        if self.request.user.is_authenticated:

            current_user = Profile.objects.filter(
                user__id=self.request.user.id)
            cart_memory = str(self.cart)
            cart_memory = cart_memory.replace("\'", "\"")
            current_user.update(old_cart=str(cart_memory))

    def get_products(self):

        product_ids = self.cart.keys()
        cart_products = Product.objects.filter(id__in = product_ids)

        return cart_products
    
    def get_quants(self):
        quantities = self.cart
        return quantities
    

    def update(self,product,quantity):
        product = str(product)
        quantity = int(quantity)

        main_cart  = self.cart
        main_cart[product] = quantity

        self.session.modified = True

        final_cart = self.cart

        if self.request.user.is_authenticated:

            current_user = Profile.objects.filter(
                user__id=self.request.user.id)
            cart_memory = str(self.cart)
            cart_memory = cart_memory.replace("\'", "\"")
            current_user.update(old_cart=str(cart_memory))
            
        return final_cart
    
    
    def delete(self,product):
        product_id = str(product)

        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

        if self.request.user.is_authenticated:

            current_user = Profile.objects.filter(
                user__id=self.request.user.id)
            cart_memory = str(self.cart)
            cart_memory = cart_memory.replace("\'", "\"")
            current_user.update(old_cart=str(cart_memory))

    def cart_total(self):

        product_ids = self.cart.keys()
        cart_products = Product.objects.filter(id__in = product_ids)
        quantities = self.cart
        total = 0


        for key,val in quantities.items():

            key = int(key)

            for product in cart_products:
                if product.id == key:
                    if product.is_sale:
                        total = total + (product.sale_price * val)
                    else:
                        total = total + (product.price * val)

        return total

    

    def __len__(self):
        return len(self.cart)