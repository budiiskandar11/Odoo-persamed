{
    "name"          : "Sale Form",
    "version"       : "1.0",
    "depends"       : ["sale","report_webkit"],
    "author"        : "Databit",
    "description"   : """This module is aim to add some new fields to:
                        - Sale Order""",
    "website"       : "https://www.databit.co.id/",
    "category"      : "Sales",
    "init_xml"      : [],
    "demo_xml"      : [],
    'test'          : [],
    "update_xml"    : [
                       "report/report_sale_order.xml",
                       "sale_workflow.xml",
                       "sale_view.xml",
                       ],
    "active"        : False,
    "installable"   : True,
}