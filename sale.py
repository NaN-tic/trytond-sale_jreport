# This file is part sale_jreport module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool, PoolMeta
from trytond.modules.jasper_reports.jasper import JasperReport

__all__ = ['SaleReport']
__metaclass__ = PoolMeta


class SaleReport(JasperReport):
    __name__ = 'sale.sale'

    @classmethod
    def execute(cls, ids, data):
        pool = Pool()
        Config = pool.get('sale.configuration')
        config = Config(1)
        parameters = {
            'sale_qty_decimal': config.sale_qty_decimal or False
            }
        if 'parameters' in data:
            data['parameters'].update(parameters)
        else:
            data['parameters'] = parameters
        return super(SaleReport, cls).execute(ids, data)
