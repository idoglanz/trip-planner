import xml.etree.ElementTree as ET
import pandas as pd
from app.groceries import GroceryItem, GroceryList


def rename_units(units):
    if units == 'קילוגרמים':
        return 'ק״ג'
    elif units == 'גרמים':
        return 'גרם'
    elif units == 'ליטרים':
        return 'ליטר'
    elif units == 'מיליליטרים':
        return 'מ״ל'
    else:
        return units

def map_item_to_grocery_item(item) -> GroceryItem:
    """
    Map xml item to GroceryItem
    """
    name = item.find('ItemName').text
    price = item.find('ItemPrice').text
    units = item.find('UnitQty').text
    quantity = item.find('Quantity').text
    uuid = item.find('ItemCode').text

    if float(quantity) == 0:
        if units == 'קילוגרמים':
            quantity = '1'
        elif units == 'גרמים':
            quantity = '100'
    
    units = rename_units(units)

    return GroceryItem(name, price, units, quantity, uuid)


def parse_xml(xml_file):
    """
    Parse xml file and return a list of dictionaries containing the data
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()
    groceries = GroceryList('Shufersal')

    for i, child in enumerate(root):
        if child.tag == 'ChainId':
            groceries.chain_id = child.text
        elif child.tag == 'StoreId':
            groceries.store_id = child.text
        elif child.tag == 'Items':
            for sub_child in child:
                if sub_child.tag == 'Item':
                    groceries.add_item(map_item_to_grocery_item(sub_child))
                    
    # filter out all items with price over 100
    print(f'Number of items before filtering: {len(groceries.items)}')
    groceries.items = [item for item in groceries.items if float(item.price) < 100]
    print(f'Number of items after filtering: {len(groceries.items)}')
    return groceries



if __name__ == "__main__":
    groceries_list = parse_xml('./data/price_lists/PriceFull7290027600007-413-202307110340')
    print(groceries_list.items[0])
