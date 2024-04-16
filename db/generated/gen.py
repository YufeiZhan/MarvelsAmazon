from werkzeug.security import generate_password_hash
import csv
from faker import Faker

num_users = 100
num_products = 500
num_purchases = 2500
num_coupons = 50
num_inventories = 2000
possible_discounts = [0.95, 0.9, 0.85, 0.80, 0.75, 0.70, 0.65]
num_cart_items = 2000
num_order_items = 2000
num_reviews = 500

Faker.seed(0)
fake = Faker()


def get_csv_writer(f):
    return csv.writer(f, dialect='unix')


def gen_users(num_users):
    available_uids = []
    with open('Users.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Users...', end=' ', flush=True)
        for uid in range(num_users):
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            profile = fake.profile()
            email = profile['mail']
            plain_password = f'pass{uid}'
            password = generate_password_hash(plain_password)
            name_components = profile['name'].split(' ')
            firstname = name_components[0]
            lastname = name_components[-1]
            balance = f'{str(fake.random_int(max=1000))}.{fake.random_int(max=99):02}'
            role_indicator = fake.random_int(min=0, max=1)
            writer.writerow([uid, email, password, firstname, lastname,  balance, role_indicator])
            available_uids.append(uid)
        print(f'{num_users} generated')
    return available_uids


def gen_products(num_products, available_uids):
    available_uids2 = available_uids.copy()
    # available_uids2 += ['']
    available_pids = []
    categories = ["Electronics", "Book", "Food", "Weapon"]
    with open('Products.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Products...', end=' ', flush=True)

        used_names = set()
        for pid in range(num_products):
            if pid % 100 == 0:
                print(f'{pid}', end=' ', flush=True)
            name = fake.sentence(nb_words=2)[:-1]

            while name in used_names:  # Double-check to avoid any duplicates
                name = fake.sentence(nb_words=2)[:-1]
            used_names.add(name)
            description = fake.sentence(nb_words=10)[:-1]
            # price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            category = fake.random_element(elements=categories)
            creator = fake.random_element(elements=available_uids2)
            writer.writerow([pid, name, description, category, creator])
            available_pids.append(pid)
            
        print(f'{num_products} generated; {len(available_pids)} available')
    return available_pids


# def gen_purchases(num_purchases, available_pids):
#     with open('Purchases.csv', 'w') as f:
#         writer = get_csv_writer(f)
#         print('Purchases...', end=' ', flush=True)
#         for id in range(num_purchases):
#             if id % 100 == 0:
#                 print(f'{id}', end=' ', flush=True)
#             uid = fake.random_int(min=0, max=num_users-1)
#             pid = fake.random_element(elements=available_pids)
#             time_purchased = fake.date_time()
#             writer.writerow([id, uid, pid, time_purchased])
#         print(f'{num_purchases} generated')
#     return

def gen_orders(num_purchases, available_pids):
    orders_data = {}
    with open('Orders.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Orders...', end=' ', flush=True)
        for oid in range(num_purchases):
            if oid % 100 == 0:
                print(f'{oid}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)
            address = fake.address().replace('\n', ', ')
            time_purchased = fake.date_time()
            discount = fake.random_element(elements=possible_discounts)
            writer.writerow([oid, uid, address, time_purchased, discount])
            orders_data[oid] = uid
        print(f'{num_purchases} generated')
    return orders_data

def gen_coupons(num_coupons):
    with open('Coupon.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Coupons...', end=' ', flush=True)
        used_codes = set()  
        for _ in range(num_coupons):
            # Ensure unique coupon codes
            code = fake.unique.bothify(text='???-####')  # Placeholder pattern, e.g., ABC-1234
            while code in used_codes:  # Double-check to avoid any duplicates
                code = fake.unique.bothify(text='???-####')
            used_codes.add(code)
            discount = fake.random_element(elements=possible_discounts)  # Randomly select a discount
            writer.writerow([code, discount])
        print(f'\n{num_coupons} coupons generated.')
    return

def gen_inventories(num_inventories, available_pids, available_uids):
    inventory_data = {}
    with open('Inventory.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Inventories...', end=' ', flush=True)

        for iid in range(num_inventories):
            if iid % 200 == 0:
                print(f'{iid}', end=' ', flush=True)
            pid = fake.random_element(elements=available_pids) 
            seller_id = fake.random_element(elements=available_uids)  
            unit_price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            quantity_available = fake.random_int(max=100)
            inventory_data[iid] = (quantity_available, seller_id)
            writer.writerow([iid, pid, seller_id, unit_price, quantity_available])
        print(f'\n{num_inventories} inventory items generated.')
    return inventory_data

def gen_cart_items(num_cart_items, available_uids, inventory_data):
    with open('CartItems.csv', 'w') as f:
        writer = csv.writer(f, dialect='unix')  
        print('CartItems...', end=' ', flush=True)
        for _ in range(num_cart_items):
            uid = fake.random_element(elements=available_uids)
            iid, (available_quantity, seller_id) = fake.random_element(list(inventory_data.items()))  # Randomly select an inventory item
            if available_quantity > 1:
                quantity = fake.random_int(min=1, max=available_quantity - 1)
            elif available_quantity == 1:
                quantity = 1
            status = 1  # Default status
            writer.writerow([uid, iid, quantity, status])
        print(f'\n{num_cart_items} cart items generated.')
    return

def gen_order_items(num_order_items, inventory_data, orders_data):
    status = ["placed", "in delivery", "fulfilled", "cancelled"]
    seller_buyer_pairs = []
    buyer_product_pairs = []
    with open('OrderItems.csv', 'w') as f:
        writer = csv.writer(f, dialect='unix')
        print('OrderItems...', end=' ', flush=True)
        for oiid in range(num_order_items):
            oid, buyer_id = fake.random_element(list(orders_data.items())) 
            iid, (available_quantity, seller_id) = fake.random_element(list(inventory_data.items()))  # Randomly select an inventory item
            quantity_purchased = fake.random_int(max=100) 
            item_status = fake.random_element(elements=status) 
            
            buyer_product_pairs.append((buyer_id,iid))
            seller_buyer_pairs.append((seller_id,buyer_id))
            writer.writerow([oiid, oid, iid, quantity_purchased, item_status])
        print(f'\n{num_order_items} order items generated.')
    return seller_buyer_pairs, buyer_product_pairs

def gen_seller_reviews(num_reviews, seller_buyer_pairs):
    with open('SellerReview.csv', 'w') as f:
        writer = csv.writer(f, dialect='unix')
        print('Seller reviews...', end=' ', flush=True)

        used_pairs = set()
        for _ in range(num_reviews):
            (seller_id, buyer_id) = fake.random_element(elements = seller_buyer_pairs)

            if (seller_id, buyer_id) not in used_pairs:
                content = fake.sentence(nb_words=20)[:-1]
                rating = fake.random_int(min=1.0, max=5.0)
                review_time = fake.date_time()
                upvotes = fake.random_int(max=500) 
                writer.writerow([seller_id, buyer_id, content, rating, review_time, upvotes])
                used_pairs.add((seller_id, buyer_id))
            if len(used_pairs) >= len(seller_buyer_pairs):  # Break if all possible unique pairs are used
                break
        print(f'\n{num_reviews} seller reviews generated.')
    return

def gen_product_reviews(num_reviews, buyer_product_pairs):
    with open('ProductReview.csv', 'w') as f:
        writer = csv.writer(f, dialect='unix')
        print('Product reviews...', end=' ', flush=True)

        used_pairs = set()
        for _ in range(num_reviews):
            (buyer_id, iid) = fake.random_element(elements = buyer_product_pairs)

            if (buyer_id, iid) not in used_pairs:
                content = fake.sentence(nb_words=20)[:-1]
                rating = fake.random_int(min=1.0, max=5.0)
                review_time = fake.date_time()
                upvotes = fake.random_int(max=500) 
                writer.writerow([buyer_id, iid, content, rating, review_time, upvotes])
                used_pairs.add((buyer_id, iid))
            if len(used_pairs) >= len(buyer_product_pairs):  # Break if all possible unique pairs are used
                break
        print(f'\n{num_reviews} product reviews generated.')
    return


available_uids = gen_users(num_users)
available_pids = gen_products(num_products, available_uids)
orders_data = gen_orders(num_purchases, available_pids)
gen_coupons(num_coupons)
inventory_data = gen_inventories(num_inventories, available_pids, available_uids)
gen_cart_items(num_cart_items, available_uids, inventory_data)
seller_buyer_pairs, buyer_product_pairs = gen_order_items(num_order_items, inventory_data, orders_data)
print(len(seller_buyer_pairs)) #Should be 2000
gen_seller_reviews(num_reviews, seller_buyer_pairs)
print(len(buyer_product_pairs)) #Should be 2000
gen_product_reviews(num_reviews, buyer_product_pairs)