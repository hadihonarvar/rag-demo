from app.config import settings
from app.utils.logger import log
import shopify

shopify.ShopifyResource.set_site(f"https://{settings.SHOP_NAME}.myshopify.com/admin/api/{settings.SHOP_API_VERSION}")

async def get_shopify_products():
    log.info("Getting Shopify products")
    products = shopify.Product.find()
    return products

async def get_shopify_product(product_id: int):
    log.info(f"Getting Shopify product {product_id}")
    product = shopify.Product.find(product_id)
    return product

async def create_shopify_product(product):
    log.info(f"Creating Shopify product {product.title}")
    product.save()
    return product

async def update_shopify_product(product):
    log.info(f"Updating Shopify product {product.title}")
    product.save()
    return product

async def delete_shopify_product(product_id: int):
    log.info(f"Deleting Shopify product {product_id}")
    product = shopify.Product.find(product_id)
    product.destroy()
    return {"message": "Product deleted successfully"}

async def get_shopify_orders():
    log.info("Getting Shopify orders")
    orders = shopify.Order.find()
    return orders

async def get_shopify_order(order_id: int):
    log.info(f"Getting Shopify order {order_id}")
    order = shopify.Order.find(order_id)
    return order

async def create_shopify_order(order):
    log.info(f"Creating Shopify order {order.name}")
    order.save()
    return order

async def update_shopify_order(order):
    log.info(f"Updating Shopify order {order.name}")
    order.save()
    return order

async def delete_shopify_order(order_id: int):
    log.info(f"Deleting Shopify order {order_id}")
    order = shopify.Order.find(order_id)
    order.destroy()
    return {"message": "Order deleted successfully"}

async def get_shopify_customers():
    log.info("Getting Shopify customers")
    customers = shopify.Customer.find()
    return customers

async def get_shopify_customer(customer_id: int):
    log.info(f"Getting Shopify customer {customer_id}")
    customer = shopify.Customer.find(customer_id)
    return customer

async def create_shopify_customer(customer):
    log.info(f"Creating Shopify customer {customer.email}")
    customer.save()
    return customer

async def update_shopify_customer(customer):
    log.info(f"Updating Shopify customer {customer.email}")
    customer.save()
    return customer

async def delete_shopify_customer(customer_id: int):
    log.info(f"Deleting Shopify customer {customer_id}")
    customer = shopify.Customer.find(customer_id)
    customer.destroy()
    return {"message": "Customer deleted successfully"}

async def get_shopify_collections():
    log.info("Getting Shopify collections")
    collections = shopify.CustomCollection.find()
    return collections

async def get_shopify_collection(collection_id: int):
    log.info(f"Getting Shopify collection {collection_id}")
    collection = shopify.CustomCollection.find(collection_id)
    return collection

async def create_shopify_collection(collection):
    log.info(f"Creating Shopify collection {collection.title}")
    collection.save()
    return collection

async def update_shopify_collection(collection):
    log.info(f"Updating Shopify collection {collection.title}")
    collection.save()
    return collection

async def delete_shopify_collection(collection_id: int):
    log.info(f"Deleting Shopify collection {collection_id}")
    collection = shopify.CustomCollection.find(collection_id)
    collection.destroy()
    return {"message": "Collection deleted successfully"}

async def get_shopify_smart_collections():
    log.info("Getting Shopify smart collections")
    smart_collections = shopify.SmartCollection.find()
    return smart_collections

async def get_shopify_smart_collection(smart_collection_id: int):
    log.info(f"Getting Shopify smart collection {smart_collection_id}")
    smart_collection = shopify.SmartCollection.find(smart_collection_id)
    return smart_collection

async def create_shopify_smart_collection(smart_collection):
    log.info(f"Creating Shopify smart collection {smart_collection.title}")
    smart_collection.save()
    return smart_collection

async def update_shopify_smart_collection(smart_collection):
    log.info(f"Updating Shopify smart collection {smart_collection.title}")
    smart_collection.save()
    return smart_collection

async def delete_shopify_smart_collection(smart_collection_id: int):
    log.info(f"Deleting Shopify smart collection {smart_collection_id}")
    smart_collection = shopify.SmartCollection.find(smart_collection_id)
    smart_collection.destroy()
    return {"message": "Smart Collection deleted successfully"}

async def get_shopify_custom_collections():
    log.info("Getting Shopify custom collections")
    custom_collections = shopify.CustomCollection.find()
    return custom_collections

async def get_shopify_custom_collection(custom_collection_id: int):
    log.info(f"Getting Shopify custom collection {custom_collection_id}")
    custom_collection = shopify.CustomCollection.find(custom_collection_id)
    return custom_collection

async def create_shopify_custom_collection(custom_collection):
    log.info(f"Creating Shopify custom collection {custom_collection.title}")
    custom_collection.save()
    return custom_collection

async def update_shopify_custom_collection(custom_collection):
    log.info(f"Updating Shopify custom collection {custom_collection.title}")
    custom_collection.save()
    return custom_collection

async def delete_shopify_custom_collection(custom_collection_id: int):
    log.info(f"Deleting Shopify custom collection {custom_collection_id}")
    custom_collection = shopify.CustomCollection.find(custom_collection_id)
    custom_collection.destroy()
    return {"message": "Custom Collection deleted successfully"}

async def get_shopify_collects():
    log.info("Getting Shopify collects")
    collects = shopify.Collect.find()
    return collects

async def get_shopify_collect(collect_id: int):
    log.info(f"Getting Shopify collect {collect_id}")
    collect = shopify.Collect.find(collect_id)
    return collect

async def create_shopify_collect(collect):
    log.info(f"Creating Shopify collect {collect.title}")
    collect.save()
    return collect

async def update_shopify_collect(collect):
    log.info(f"Updating Shopify collect {collect.title}")
    collect.save()
    return collect

async def delete_shopify_collect(collect_id: int):
    log.info(f"Deleting Shopify collect {collect_id}")
    collect = shopify.Collect.find(collect_id)
    collect.destroy()
    return {"message": "Collect deleted successfully"}

