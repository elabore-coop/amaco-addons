# Copyright 2021 Elabore ()
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "amaco_odoo_customization",
    "version": "14.0.1.0.0",
    "author": "Elabore",
    "maintainer": "False",
    "website": "False",
    "license": "AGPL-3",
    "category": "False",
    "summary": "Customize the Amaco" "s Odoo Instance",
    "description": """
========================
amaco_odoo_customization
========================
This module customizes Amaco''s Odoo instance:
 - archive analytic account when lead is archived
 - add values to employee departure reasons
 - add team_id field in project model

Installation
============
Just install amaco_odoo_customization, all dependencies will be installed by default.

Known issues / Roadmap
======================

Bug Tracker
===========
Bugs are tracked on `GitHub Issues
<https://github.com/elabore-coop/elabore-odoo-addons/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed feedback.

Credits
=======

Images
------
* Elabore: `Icon <https://elabore.coop/web/image/res.company/1/logo?unique=f3db262>`_.

Contributors
------------
* Stéphan Sainléger <https://github.com/stephansainleger>

Funders
-------
The development of this module has been financially supported by:
* Elabore (https://elabore.coop)
* Amaco (https://amaco.org)

Maintainer
----------
This module is maintained by ELABORE.

""",
    # any module necessary for this one to work correctly
    "depends": [
        "base",
        "crm",
        "sale",
        "project",
        "sale_timesheet",
    ],
    "external_dependencies": {
        "python": [],
    },
    # always loaded
    "data": [
        "views/project.xml",
        "views/account_move_views.xml",
        "views/hr_expense_views.xml",
        "views/sale_order_views.xml",
    ],
    # only loaded in demonstration mode
    "demo": [],
    "js": [],
    "css": [],
    "qweb": [],
    "installable": True,
    # Install this module automatically if all dependency have been previously
    # and independently installed.  Used for synergetic or glue modules.
    "auto_install": False,
    "application": False,
}
