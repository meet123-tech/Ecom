from shop.models import Product

class Cart():
    
    def __init__(self,request):
        self.session = request.session

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
        return final_cart
    
    
    def __len__(self):
        return len(self.cart)