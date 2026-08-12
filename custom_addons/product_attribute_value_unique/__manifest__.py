{
    'name': 'Product Attribute Value Unique Constraint',
    'version': '18.0.1.0.0',
    'category': 'Sales/Sales',
    'summary': 'Prevent duplicate attribute values under the same attribute',
    'description': """
        Ensures that each product attribute value name is unique within its
        attribute (e.g. "50" cannot be defined twice under "Boy_Bağlantı Elemanları").
    """,
    'depends': ['product'],
    'data': [],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
