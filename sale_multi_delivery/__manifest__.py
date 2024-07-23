{
    "name": "Sale Multi Delivery",
    "version": "15.0.1.0.0",
    "summary": "This module is used to generate multiple delivery orders of each product from a sale order",
    "category": "sales",
    "author": "Nadeem Rizwan",
    "depends": ["base","sale", "stock"],
    "data": [
        "security/ir.model.access.csv",
        "views/delivery_order_view.xml",
    ],
    "license": "LGPL-3",
    "images": [],
    "installable": True,
    "auto_install": False,
    "application": True,
}
