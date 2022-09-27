from config.suppliers import SUPPLIERS, OZON_SUPPLIERS


def get_suppliers_list_ozon(suppliers: list = None):
    """
    getting suppliers list from constants
    :param suppliers: suppliers names. If None -> gets all suppliers
    :return:
    """
    if suppliers is None:
        return OZON_SUPPLIERS.values()

    result = []
    for supplier_name in suppliers:
        if type(supplier_name) == str:
            if SUPPLIERS.get(supplier_name) is not None:
                result.append(OZON_SUPPLIERS.get(supplier_name))

    return result


def get_suppliers_list(suppliers: list = None):
    """
    getting suppliers list from constants
    :param suppliers: suppliers names. If None -> gets all suppliers
    :return:
    """
    if suppliers is None:
        return SUPPLIERS.values()

    result = []
    for supplier_name in suppliers:
        if type(supplier_name) == str:
            if SUPPLIERS.get(supplier_name) is not None:
                result.append(SUPPLIERS.get(supplier_name))

    return result


if __name__ == '__main__':
    print(get_suppliers_list(['sff']))
#
