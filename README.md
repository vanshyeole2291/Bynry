# Bynry Backend Case Study Solution

This repository contains my solution for the **Backend Engineering Intern Case Study** assigned by **Bynry Inc**.  
It includes:
- Part 1: Code Review & Debugging
- Part 2: Database Design
- Part 3: API Implementation

---

## Part 1: Code Review & Fixes

### Issues Identified
1. **No SKU uniqueness check** allows duplicate products  
2. **Product creation tied to a single warehouse** violates multi-warehouse requirement  
3. **Missing validation for required fields** causes runtime errors if inputs are missing  
4. **No transaction handling** can leave an inconsistent state with partial commits  
5. **Price type not enforced** allows incorrect values  
6. **Assumes `initial_quantity` always provided** breaks if missing  

---

### Corrected Flask Endpoint
```python
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
            inventory = Inventory(product_id=product.id,
                                  warehouse_id=data['warehouse_id'],
                                  quantity=initial_quantity)
            db.session.add(inventory)

        db.session.commit()
        return jsonify({"message": "Product created", "product_id": product.id}), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database integrity error"}), 500

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
```
