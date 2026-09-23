{
    "name": "Qooling Inbound Form",
    "version": "18.0.1.0.0",
    "category": "Operations",
    "summary": "Inbound Form record tool",
    "depends": ["base", "web", "stock"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "data/ir_sequence_data.xml",
        "views/inbound_form_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "wd_qooling_app/static/src/js/signature_field.js",
            "wd_qooling_app/static/src/xml/signature_field.xml",
        ],
    },
    "installable": True,
    "application": True,
    "license": "LGPL-3",
}
