# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.modules.product_price_list.price_list import Null
from trytond.pool import PoolMeta
from trytond.transaction import Transaction


class PriceList(metaclass=PoolMeta):
    __name__ = 'product.price_list'

    def get_context_formula(self, product, quantity, uom, pattern=None):
        context = super().get_context_formula(
            product, quantity, uom, pattern=pattern)
        kit_unit_price = Transaction().context.get('kit_unit_price')
        context['names']['kit_unit_price'] = (
            kit_unit_price if kit_unit_price else Null())
        return context


class PriceListLine(metaclass=PoolMeta):
    __name__ = 'product.price_list.line'

    @classmethod
    def __setup__(cls):
        super().__setup__()
        cls.formula.help += (
            '\n- kit_unit_price: the unit_price calculated for a kit with '
            'List Price Method "Sum of component sale prices"')
