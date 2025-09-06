from typing import Dict, List, Optional

from models.models import Category, Product


CATALOG: Dict[str, Category] = {
    "tv": Category(
        slug="tv",
        title="TV",
        products=[
            Product(id="tv-1", title="Samsung 55\" QLED", price=8999000, description="55 dyuym, 4K QLED televizor"),
            Product(id="tv-2", title="LG 50\" UHD", price=6499000, description="50 dyuym, 4K UHD televizor"),
        ],
    ),
    "smartphones": Category(
        slug="smartphones",
        title="Smartfonlar",
        products=[
            Product(id="sp-1", title="iPhone 14", price=11999000, description="128GB, A15 Bionic"),
            Product(id="sp-2", title="Samsung Galaxy S23", price=9999000, description="256GB, Snapdragon 8 Gen 2"),
        ],
    ),
    "appliances": Category(
        slug="appliances",
        title="Maishiy texnikalar",
        products=[
            Product(id="ap-1", title="Artel kir yuvish mashinasi", price=3599000, description="7 kg, 1200 ayl/min"),
            Product(id="ap-2", title="Bosch kir yuvish mashinasi", price=4999000, description="8 kg, energiya tejamkor"),
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


