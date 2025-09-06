from typing import Dict, List, Optional

from models.models import Category, Product


CATALOG: Dict[str, Category] = {
    "tv": Category(
        slug="tv",
        title="TV",
        products=[
            Product(id="tv-1", title="Samsung 55\" QLED 4K", price=8999000, description="55 dyuym, 4K QLED televizor, Smart TV"),
            Product(id="tv-2", title="LG 50\" UHD Smart TV", price=6499000, description="50 dyuym, 4K UHD televizor, WebOS"),
            Product(id="tv-3", title="Sony 65\" OLED 4K", price=12999000, description="65 dyuym, OLED 4K, Android TV"),
            Product(id="tv-4", title="TCL 43\" Android TV", price=3999000, description="43 dyuym, Android TV, 4K"),
        ],
    ),
    "smartphones": Category(
        slug="smartphones",
        title="Smartfonlar",
        products=[
            Product(id="sp-1", title="iPhone 15 Pro", price=15999000, description="128GB, A17 Pro chip, Titanium"),
            Product(id="sp-2", title="iPhone 15", price=12999000, description="128GB, A16 Bionic, Dynamic Island"),
            Product(id="sp-3", title="Samsung Galaxy S24 Ultra", price=13999000, description="256GB, Snapdragon 8 Gen 3, S Pen"),
            Product(id="sp-4", title="Samsung Galaxy S24", price=9999000, description="128GB, Snapdragon 8 Gen 3"),
            Product(id="sp-5", title="Xiaomi 14 Pro", price=7999000, description="256GB, Snapdragon 8 Gen 3, Leica camera"),
            Product(id="sp-6", title="OnePlus 12", price=6999000, description="256GB, Snapdragon 8 Gen 3, 100W charging"),
        ],
    ),
    "appliances": Category(
        slug="appliances",
        title="Maishiy texnikalar",
        products=[
            Product(id="ap-1", title="Artel kir yuvish mashinasi", price=3599000, description="7 kg, 1200 ayl/min, inverter motor"),
            Product(id="ap-2", title="Bosch kir yuvish mashinasi", price=4999000, description="8 kg, energiya tejamkor, ActiveWater"),
            Product(id="ap-3", title="Samsung muzlatgich", price=6999000, description="300L, No Frost, Digital Inverter"),
            Product(id="ap-4", title="LG konditsioner", price=3999000, description="1.5 ton, inverter, WiFi"),
            Product(id="ap-5", title="Artel mikroto'lqinli pech", price=899000, description="25L, grill, convection"),
            Product(id="ap-6", title="Philips blender", price=599000, description="1000W, 6 tezlik, stainless steel"),
        ],
    ),
}


def get_categories() -> List[Category]:
    return list(CATALOG.values())


def get_products_by_category(slug: str) -> List[Product]:
    category: Optional[Category] = CATALOG.get(slug)
    return category.products if category else []


def get_product_by_id(product_id: str) -> Optional[Product]:
    for category in CATALOG.values():
        for product in category.products:
            if product.id == product_id:
                return product
    return None


