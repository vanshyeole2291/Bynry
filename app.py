from flask import Flask, request, jsonify
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta

app = Flask(__name__)

# Dummy imports (replace with actual models and DB initialization in real app)
from models import db, Product, Inventory, Supplier, ProductSupplier, Sales

@app.route('/api/products', methods=['POST'])
def create_product():
    data = request.json
    required_fields = ['name', 'sku', 'price']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    try:
        price = float(data['price'])
    except ValueError:
        return jsonify({"error": "Price must be numeric"}), 400

    existing_product = Product.query.filter_by(sku=data['sku']).first()
    if existing_product:
        return jsonify({"error": "SKU already exists"}), 409

    try:
        product = Product(name=data['name'], sku=data['sku'], price=price)
        db.session.add(product)
        db.session.flush()

        if 'warehouse_id' in data:
            initial_quantity = data.get('initial_quantity', 0)
            inventory = Inventory(
                product_id=product.id,
                warehouse_id=data['warehouse_id'],
                quantity=initial_quantity
            )
            db.session.add(inventory)

        db.session.commit()
        return jsonify({"message": "Product created", "product_id": product.id}), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database integrity error"}), 500

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@app.route('/api/companies/<int:company_id>/alerts/low-stock', methods=['GET'])
def get_low_stock_alerts(company_id):
    cutoff_date = datetime.utcnow() - timedelta(days=30)

    results = db.session.query(
        Product.id.label("product_id"),
        Product.name.label("product_name"),
        Product.sku,
        Inventory.warehouse_id,
        Inventory.quantity.label("current_stock"),
        Product.low_stock_threshold.label("threshold"),
        Supplier.id.label("supplier_id"),
        Supplier.name.label("supplier_name"),
        Supplier.contact_email
    ).join(Inventory, Inventory.product_id == Product.id) \
     .join(Sales, Sales.product_id == Product.id) \
     .join(ProductSupplier, ProductSupplier.product_id == Product.id) \
     .join(Supplier, Supplier.id == ProductSupplier.supplier_id) \
     .filter(Inventory.quantity < Product.low_stock_threshold) \
     .filter(Sales.date >= cutoff_date) \
     .all()

    alerts = []
    for row in results:
        avg_daily_sales = 1
        days_until_stockout = row.current_stock / avg_daily_sales if avg_daily_sales else None

        alerts.append({
            "product_id": row.product_id,
            "product_name": row.product_name,
            "sku": row.sku,
            "warehouse_id": row.warehouse_id,
            "current_stock": row.current_stock,
            "threshold": row.threshold,
            "days_until_stockout": days_until_stockout,
            "supplier": {
                "id": row.supplier_id,
                "name": row.supplier_name,
                "contact_email": row.contact_email
            }
        })

    return jsonify({
        "alerts": alerts,
        "total_alerts": len(alerts)
    })


if __name__ == "__main__":
    app.run(debug=True)
