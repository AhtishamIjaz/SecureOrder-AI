from fastmcp import FastMCP
import sqlite3
import os
from schema import OrderCreateSchema

# Initialize MCP Server
mcp = FastMCP("SecureOrder-Vault")
DB_PATH = os.path.join(os.path.dirname(__file__), "../data/orders.db")

@mcp.tool()
def search_inventory(query: str = None, max_price: float = None) -> str:
    """Search the company database for products by name or price."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    sql = "SELECT name, price, description, stock FROM products WHERE 1=1"
    params = []
    
    if query:
        sql += " AND (name LIKE ? OR description LIKE ?)"
        params.extend([f"%{query}%", f"%{query}%"])
    if max_price:
        sql += " AND price <= ?"
        params.append(max_price)
        
    cursor.execute(sql, params)
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        return "No products found matching those criteria."
    
    results = "\n".join([f"- {r[0]}: ${r[1]} | {r[2]} (In Stock: {r[3]})" for r in rows])
    return f"🛡️ SecureOrder Inventory:\n{results}"

@mcp.tool()
def place_secure_order(customer_name: str, product_id: int, quantity: int, address: str) -> str:
    """Strictly places an order. Requires validated customer details."""
    try:
        # Pydantic Validation (Industrial Guard)
        data = OrderCreateSchema(
            customer_name=customer_name, 
            product_id=product_id, 
            quantity=quantity, 
            shipping_address=address
        )
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Get Price from DB (Don't trust the LLM for price!)
        cursor.execute("SELECT price, name FROM products WHERE id = ?", (data.product_id,))
        res = cursor.fetchone()
        
        if not res: return "Error: Product ID not found."
        
        total = res[0] * data.quantity
        
        cursor.execute('''
            INSERT INTO orders (customer_name, product_id, quantity, total_price, status)
            VALUES (?, ?, ?, ?, 'Confirmed')
        ''', (data.customer_name, data.product_id, data.quantity, total))
        
        order_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return f"✅ SUCCESS: Order #{order_id} for {res[1]} placed. Total: ${total}."
    except Exception as e:
        return f"❌ SECURITY BLOCK: {str(e)}"

if __name__ == "__main__":
    mcp.run()