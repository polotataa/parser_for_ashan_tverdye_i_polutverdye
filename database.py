from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine, Float

# Создание engine and session
try:
    engine = create_engine('postgresql://Tata:p12345@localhost:5432/postgres')
    Session = sessionmaker(bind=engine)
    session = Session()
except Exception as e:
    print(f"Ошибка подключния к базе данных: {e}")

Base = declarative_base()


class Product(Base):
    __tablename__ = 'tverdye_i_polutverdye'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    link = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    old_price = Column(Float, nullable=True)
    brand = Column(String, nullable=False)

    def __repr__(self):
        return f"<Product(id={self.id}, title='{self.title}', link='{self.link}', price={self.price}, promo_price={self.promo_price}, brand='{self.brand}')>"

    def save(self):
        try:
            session.add(self)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Ошибка при сохранении product: {e}")

    def delete(self):
        try:
            session.delete(self)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error deleting product: {e}")

    @staticmethod
    def get_by_id(product_id):
        try:
            product = session.query(Product).get(product_id)
            return product
        except Exception as e:
            print(f"Error retrieving product: {e}")
            return None