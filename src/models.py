from sqlalchemy import text, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy_utils.types import ChoiceType


class BaseModel(DeclarativeBase):
    pass


class User(BaseModel):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(25), unique=True)
    email: Mapped[str] = mapped_column(String(80), unique=True)
    password: Mapped[str] = mapped_column(nullable=True)
    is_staff: Mapped[bool] = mapped_column(default=False)
    is_active: Mapped[bool] = mapped_column(default=False)
    orders = relationship('Order', back_populates='user')

    # def __repr__(self):
    #     return f'<User {self.username}>'


class Order(BaseModel):
    ORDER_STATUSES = (
        ('PENDING', 'pending'),
        ('IN-TRANSIT', 'in-transit'),
        ('DELIVERED', 'delivered')
    )

    PIZZA_SIZES = (
        ('SMALL', 'small'),
        ('MEDIUM', 'medium'),
        ('LARGE', 'large'),
        ('EXTRA-LARGE', 'extra-large')
    )

    __tablename__ = 'orders'
    id: Mapped[int] = mapped_column(primary_key=True)
    quantity: Mapped[int] = mapped_column(nullable=False)
    order_status: Mapped[str] = mapped_column(String, default="PENDING")
    # order_status: Mapped[ChoiceType] = mapped_column(choices=ORDER_STATUSES, default="PENDING")
    pizza_size: Mapped[str] = mapped_column(String, default='SMALL')
    # pizza_size: Mapped[ChoiceType] = mapped_column(choices=PIZZA_SIZES, default='SMALL')
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    # user_id: Mapped[ChoiceType] = mapped_column(ForeignKey('user.id'))
    user = relationship('User', back_populates='orders')

    # def __repr__(self):
    #     return f"<Order {self.id}>"
