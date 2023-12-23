from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    type = Column(Integer)
    name = Column(String)
    attack = Column(Integer)
    defense = Column(Integer)
    rarity = Column(Integer)
    stack_size = Column(Integer)
    
    inventory_id = Column(Integer, ForeignKey('inventory.id'))
    inventory = relationship("Inventory", back_populates="item")

class Player(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True)
    description = Column(String)
    backstory = Column(String)
    appearance = Column(String)
    age = Column(Integer)
    level = Column(Integer)
    exp = Column(Integer)
    unassigned_points = Column(Integer)
    current_health = Column(Integer)
    max_health = Column(Integer)
    current_mana = Column(Integer)
    max_mana = Column(Integer)
    strength = Column(Integer)
    dexterity = Column(Integer)
    intelligence = Column(Integer)
    luck = Column(Integer)
    charisma = Column(Integer)
    wisdom = Column(Integer)
    constitution = Column(Integer)
    mining = Column(Integer)
    fishing = Column(Integer)
    cooking = Column(Integer)
    weapon_r = Column(Integer)
    weapon_l = Column(Integer)
    helm = Column(Integer)
    chest = Column(Integer)
    arms = Column(Integer)
    legs = Column(Integer)
    ring_r = Column(Integer)
    ring_l = Column(Integer)
    amulet = Column(Integer)

    inventory_id = Column(Integer, ForeignKey('inventory.id'))
    inventory = relationship("Inventory", back_populates="player")

class Inventory(Base):
    __tablename__ = 'inventory'

    id = Column(Integer, primary_key=True)
    stack_size = Column(Integer)

    item = relationship("Item", back_populates="inventory", uselist=False)
    player = relationship("Player", back_populates="inventory", uselist=False)

if Base.metadata.tables == {}:
    Base.metadata.create_all(create_engine('sqlite:///database.db'))


class Database:
    def __init__(self, connection_url):
        self.engine = create_engine(connection_url, echo=True)
        self.Session = sessionmaker(bind=self.engine)

    def create_item(self, type, name, attack, defense, rarity, stack_size):
        item = Item(type=type, name=name, attack=attack, defense=defense, rarity=rarity, stack_size=stack_size)
        with self.Session() as session:
            session.add(item)
            session.commit()

    def get_all_items(self):
        with self.Session() as session:
            return session.query(Item).all()

    def update_item(self, item_id, **new_values):
        with self.Session() as session:
            item = session.query(Item).get(item_id)
            if item:
                for key, value in new_values.items():
                    setattr(item, key, value)
                session.commit()
                return True
            return False

    def delete_item(self, item_id):
        with self.Session() as session:
            item = session.query(Item).get(item_id)
            if item:
                session.delete(item)
                session.commit()
                return True
            return False

    def create_player(self, id, **attributes):
        player = Player(id=id, **attributes)
        with self.Session() as session:
            session.add(player)
            session.commit()

    def get_all_players(self):
        with self.Session() as session:
            return session.query(Player).all()

    def get_player(self, player_id):
        with self.Session() as session:
            return session.query(Player).get(player_id)

    def update_player(self, player_id, **new_values):
        with self.Session() as session:
            player = session.query(Player).get(player_id)
            if player:
                for key, value in new_values.items():
                    setattr(player, key, value)
                session.commit()
                return True
            return False

    def delete_player(self, player_id):
        with self.Session() as session:
            player = session.query(Player).get(player_id)
            if player:
                session.delete(player)
                session.commit()
                return True
            return False

    def create_inventory(self, stack_size, item_id, player_id):
        inventory = Inventory(stack_size=stack_size, item_id=item_id, player_id=player_id)
        with self.Session() as session:
            session.add(inventory)
            session.commit()

    def get_all_inventories(self):
        with self.Session() as session:
            return session.query(Inventory).all()

    def update_inventory(self, inventory_id, **new_values):
        with self.Session() as session:
            inventory = session.query(Inventory).get(inventory_id)
            if inventory:
                for key, value in new_values.items():
                    setattr(inventory, key, value)
                session.commit()
                return True
            return False

    def delete_inventory(self, inventory_id):
        with self.Session() as session:
            inventory = session.query(Inventory).get(inventory_id)
            if inventory:
                session.delete(inventory)
                session.commit()
                return True
            return False
