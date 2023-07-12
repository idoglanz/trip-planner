
from dataclasses import dataclass
import pandas as pd

@dataclass
class GroceryItem:
    name: str
    price: float
    units: str
    quantity: float
    uuid: str = None

    def to_dict(self):
        return {
            'uuid': self.uuid,
            'name': self.name,
            'price': self.price,
            'units': self.units,
            'quantity': self.quantity
        }
    
class GroceryList:
    def __init__(self, name):
        self.name = name
        self.items = []
        self.chain_id = None
        self.store_id = None 
        self._df = None
        self._uuid_mapping = None
    
    def add_item(self, item):
        self.items.append(item)

    def get_row_by_name(self, name):
        return self.df.loc[self.df['name'].str.contains(name)]

    def get_row_by_uuid(self, uuid):
        return self.df.loc[uuid]
        
    def get_uuid_from_name_price(self, name_price):
        return self.name_price_to_uuid_map[name_price]


    def __repr__(self):
        return f'{self.name}: {self.items}'
    
    @property
    def name_price_to_uuid_map(self):
        if self._uuid_mapping is None:
            self._uuid_mapping =  {row['name-price']: uuid for uuid, row in self.df.iterrows()}
        
        return self._uuid_mapping
        
    @property
    def df(self):
        if self._df is None:
            self._df = pd.DataFrame([item.to_dict() for item in self.items])
            self._df['name-price'] = self._df['name'] + ' - ' + self._df['price'].astype(str) + '₪' + ' - ' + self._df['quantity'] + ' ' + self._df['units']
            self._df.set_index('uuid', inplace=True)

        return self._df