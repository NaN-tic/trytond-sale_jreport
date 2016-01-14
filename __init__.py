# This file is part sale_jreport module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from .configuration import *
from .sale import *


def register():
    Pool.register(
        Configuration,
        SaleConfigurationCompany,
        module='sale_jreport', type_='model'),
    Pool.register(
        SaleReport,
        module='sale_jreport', type_='report')
