"""
Migration script - Thêm các cột còn thiếu vào database Neon.
Chạy lệnh: python migrate.py
"""
from sqlalchemy import text, inspect
from Core.database import engine


def column_exists(inspector, table_name, column_name):
    try:
        cols = [c['name'] for c in inspector.get_columns(table_name)]
        return column_name in cols
    except Exception:
        return False


def table_exists(inspector, table_name):
    return table_name in inspector.get_table_names()


def run_migration():
    inspector = inspect(engine)

    migrations = []

    # ──────────────────────────────────────────────
    # 1. users.phone_number
    # ──────────────────────────────────────────────
    if table_exists(inspector, 'users') and not column_exists(inspector, 'users', 'phone_number'):
        migrations.append(
            "ALTER TABLE users ADD COLUMN phone_number VARCHAR(50);"
        )
        print("[PENDING] users.phone_number")
    else:
        print("[OK] users.phone_number")

    # ──────────────────────────────────────────────
    # 2. order_items.product_detail_id
    # ──────────────────────────────────────────────
    if table_exists(inspector, 'order_items') and not column_exists(inspector, 'order_items', 'product_detail_id'):
        migrations.append(
            "ALTER TABLE order_items ADD COLUMN product_detail_id INTEGER REFERENCES product_details(id);"
        )
        print("[PENDING] order_items.product_detail_id")
    else:
        print("[OK] order_items.product_detail_id")

    # ──────────────────────────────────────────────
    # 3. order_items.price
    # ──────────────────────────────────────────────
    if table_exists(inspector, 'order_items') and not column_exists(inspector, 'order_items', 'price'):
        migrations.append(
            "ALTER TABLE order_items ADD COLUMN price FLOAT;"
        )
        print("[PENDING] order_items.price")
    else:
        print("[OK] order_items.price")

    # ──────────────────────────────────────────────
    # 4. orders.location_id
    # ──────────────────────────────────────────────
    if table_exists(inspector, 'orders') and not column_exists(inspector, 'orders', 'location_id'):
        migrations.append(
            "ALTER TABLE orders ADD COLUMN location_id INTEGER REFERENCES locations(id);"
        )
        print("[PENDING] orders.location_id")
    else:
        print("[OK] orders.location_id")

    # ──────────────────────────────────────────────
    # 5. products.supplier_id
    # ──────────────────────────────────────────────
    if table_exists(inspector, 'products') and not column_exists(inspector, 'products', 'supplier_id'):
        migrations.append(
            "ALTER TABLE products ADD COLUMN supplier_id INTEGER REFERENCES suppliers(id);"
        )
        print("[PENDING] products.supplier_id")
    else:
        print("[OK] products.supplier_id")

    # ──────────────────────────────────────────────
    # 6. products.stock
    # ──────────────────────────────────────────────
    if table_exists(inspector, 'products') and not column_exists(inspector, 'products', 'stock'):
        migrations.append(
            "ALTER TABLE products ADD COLUMN stock INTEGER;"
        )
        print("[PENDING] products.stock")
    else:
        print("[OK] products.stock")

    # ──────────────────────────────────────────────
    # 7. products.image_url
    # ──────────────────────────────────────────────
    if table_exists(inspector, 'products') and not column_exists(inspector, 'products', 'image_url'):
        migrations.append(
            "ALTER TABLE products ADD COLUMN image_url VARCHAR(500);"
        )
        print("[PENDING] products.image_url")
    else:
        print("[OK] products.image_url")

    # ──────────────────────────────────────────────
    # 8. product_details.unit_id
    # ──────────────────────────────────────────────
    if table_exists(inspector, 'product_details') and not column_exists(inspector, 'product_details', 'unit_id'):
        migrations.append(
            "ALTER TABLE product_details ADD COLUMN unit_id INTEGER REFERENCES units(id);"
        )
        print("[PENDING] product_details.unit_id")
    else:
        print("[OK] product_details.unit_id")

    # ──────────────────────────────────────────────
    # 9. product_details.sales_price
    # ──────────────────────────────────────────────
    if table_exists(inspector, 'product_details') and not column_exists(inspector, 'product_details', 'sales_price'):
        migrations.append(
            "ALTER TABLE product_details ADD COLUMN sales_price INTEGER;"
        )
        print("[PENDING] product_details.sales_price")
    else:
        print("[OK] product_details.sales_price")

    # ──────────────────────────────────────────────
    # 10. product_details.quantity
    # ──────────────────────────────────────────────
    if table_exists(inspector, 'product_details') and not column_exists(inspector, 'product_details', 'quantity'):
        migrations.append(
            "ALTER TABLE product_details ADD COLUMN quantity INTEGER;"
        )
        print("[PENDING] product_details.quantity")
    else:
        print("[OK] product_details.quantity")

    # ──────────────────────────────────────────────
    # 11. users.login_method_id
    # ──────────────────────────────────────────────
    if table_exists(inspector, 'users') and not column_exists(inspector, 'users', 'login_method_id'):
        migrations.append(
            "ALTER TABLE users ADD COLUMN login_method_id INTEGER REFERENCES login_methods(id);"
        )
        print("[PENDING] users.login_method_id")
    else:
        print("[OK] users.login_method_id")

    # ──────────────────────────────────────────────
    # 5. Tạo các ENUM types nếu chưa có
    # ──────────────────────────────────────────────
    enum_migrations = [
        "DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'payment_method_enum') THEN CREATE TYPE payment_method_enum AS ENUM ('CASH', 'VNPAY', 'MOMO', 'PAYPAL'); END IF; END $$;",
        "DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'payment_status_enum') THEN CREATE TYPE payment_status_enum AS ENUM ('PENDING', 'SUCCESS', 'FAILED'); END IF; END $$;",
        "DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'shipment_status_enum') THEN CREATE TYPE shipment_status_enum AS ENUM ('PENDING', 'PICKED_UP', 'IN_TRANSIT', 'DELIVERED', 'CANCELLED'); END IF; END $$;",
    ]

    # ──────────────────────────────────────────────
    # 6. cart_items.product_detail_id
    # ──────────────────────────────────────────────
    if table_exists(inspector, 'cart_items') and not column_exists(inspector, 'cart_items', 'product_detail_id'):
        migrations.append(
            "ALTER TABLE cart_items ADD COLUMN product_detail_id INTEGER REFERENCES product_details(id);"
        )
        print("[PENDING] cart_items.product_detail_id")
    else:
        print("[OK] cart_items.product_detail_id")

    # ──────────────────────────────────────────────
    # 7. Tạo các bảng mới nếu chưa tồn tại
    # ──────────────────────────────────────────────
    new_tables = []

    if not table_exists(inspector, 'login_methods'):
        new_tables.append("""
CREATE TABLE IF NOT EXISTS login_methods (
    id SERIAL PRIMARY KEY,
    name VARCHAR,
    code VARCHAR
);
""")
        print("[PENDING] CREATE TABLE login_methods")
    else:
        print("[OK] login_methods table")

    if not table_exists(inspector, 'locations'):
        new_tables.append("""
CREATE TABLE IF NOT EXISTS locations (
    id SERIAL PRIMARY KEY,
    address VARCHAR,
    is_default BOOLEAN,
    user_id INTEGER REFERENCES users(id)
);
""")
        print("[PENDING] CREATE TABLE locations")
    else:
        print("[OK] locations table")

    if not table_exists(inspector, 'units'):
        new_tables.append("""
CREATE TABLE IF NOT EXISTS units (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);
""")
        print("[PENDING] CREATE TABLE units")
    else:
        print("[OK] units table")

    if not table_exists(inspector, 'suppliers'):
        new_tables.append("""
CREATE TABLE IF NOT EXISTS suppliers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(255) UNIQUE,
    address VARCHAR(500)
);
""")
        print("[PENDING] CREATE TABLE suppliers")
    else:
        print("[OK] suppliers table")

    if not table_exists(inspector, 'product_details'):
        new_tables.append("""
CREATE TABLE IF NOT EXISTS product_details (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id),
    unit_id INTEGER REFERENCES units(id),
    description TEXT,
    price INTEGER,
    sales_price INTEGER,
    quantity INTEGER
);
""")
        print("[PENDING] CREATE TABLE product_details")
    else:
        print("[OK] product_details table")

    if not table_exists(inspector, 'image_products'):
        new_tables.append("""
CREATE TABLE IF NOT EXISTS image_products (
    id SERIAL PRIMARY KEY,
    product_detail_id INTEGER REFERENCES product_details(id),
    image_url VARCHAR
);
""")
        print("[PENDING] CREATE TABLE image_products")
    else:
        print("[OK] image_products table")

    if not table_exists(inspector, 'payments'):
        new_tables.append("""
CREATE TABLE IF NOT EXISTS payments (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id),
    payment_method payment_method_enum,
    amount INTEGER,
    status payment_status_enum
);
""")
        print("[PENDING] CREATE TABLE payments")
    else:
        print("[OK] payments table")

    if not table_exists(inspector, 'shipments'):
        new_tables.append("""
CREATE TABLE IF NOT EXISTS shipments (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id),
    shipper VARCHAR,
    status shipment_status_enum,
    position VARCHAR
);
""")
        print("[PENDING] CREATE TABLE shipments")
    else:
        print("[OK] shipments table")

    # ──────────────────────────────────────────────
    # Chạy tất cả migration
    # ──────────────────────────────────────────────
    all_sqls = enum_migrations + new_tables + migrations

    if not all_sqls:
        print("\n[DONE] Tat ca cot va bang deu da ton tai. Khong can migration.")
        return

    print(f"\n[START] Bat dau chay {len(all_sqls)} migration(s)...")
    with engine.connect() as conn:
        for sql in all_sqls:
            try:
                conn.execute(text(sql.strip()))
                print(f"  [OK] {sql.strip()[:80]}")
            except Exception as e:
                print(f"  [ERR] Error: {e}")
        conn.commit()

    print("\n[DONE] Migration hoan tat!")


if __name__ == "__main__":
    run_migration()
