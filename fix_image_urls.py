"""
Fix corrupted image_url values in the products table.
Run once: python fix_image_urls.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from Core.database import SessionLocal
from Models.Product import Product

BAD_PREFIX = "http://localhost:8000"

def fix():
    db = SessionLocal()
    try:
        products = db.query(Product).filter(
            Product.image_url.like(f"{BAD_PREFIX}%")
        ).all()

        if not products:
            print("No corrupted URLs found.")
            return

        print(f"Found {len(products)} product(s) with corrupted image_url:")
        for p in products:
            fixed = p.image_url[len(BAD_PREFIX):]
            print(f"  ID={p.id}: {p.image_url!r}\n    -> {fixed!r}")
            p.image_url = fixed

        db.commit()
        print("Done. All image URLs fixed.")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    fix()
