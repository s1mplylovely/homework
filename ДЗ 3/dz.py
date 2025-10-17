class Negative(Exception):
    pass


class Product:
    def __init__(self, name: str, price, stock: int):
        self.name = name
        self.price = price
        self.stock = stock

    def __str__(self):
        return f"{self.name} {self.price} {self.stock}"

    def update_stock(self, quantity: int):
        try:
            test(self.stock + quantity)
            self.stock += quantity
            return True
        except Negative as e:
            print(e)


class Order:
    def __init__(self):
        self.products = {}

    def __str__(self):
        order = "Заказ:\n"
        for product, quantity in self.products.items():
            order += f"{product.name} {product.price} {quantity}\n"
        return order.removesuffix("\n")

    def add_product(self, product: Product, quantity: int):
        if product.update_stock(-quantity):
            self.products[product] = quantity
        else:
            print(f"Товара '{product.name}' не достаточно на складе")

    def calculate_total(self):
        sum = 0
        for product, quantity in self.products.items():
            sum += product.price*quantity
        return sum

    def return_product(self, product: Product, quantity: int):
        product.update_stock(quantity)

    def remove_product(self, product: Product, quantity: int):
        try:
            if (self.products[product] - quantity) <= 0:
                self.return_product(product, self.products[product])
                del self.products[product]
            else:
                self.return_product(product, quantity)
                self.products[product] -= quantity
        except KeyError:
            print(f"Товара '{product.name}' нет в заказе")


class Store:
    def __init__(self):
        self.products = []

    def add_product(self, product: Product):
        self.products.append(product)

    def list_products(self):
        print("Товары в магазине:")
        for product in self.products:
            print(product)

    def create_order(self):
        return Order()


def test(x):
    if (x < 0):
        raise Negative("Ошибка")


# Создаем магазин
store = Store()

# Создаем товары
product1 = Product("Ноутбук", 1000, 5)
product2 = Product("Смартфон", 500, 10)

# Добавляем товары в магазин
store.add_product(product1)
store.add_product(product2)

# Список всех товаров
store.list_products()

# Создаем заказ
order = store.create_order()

# Добавляем товары в заказ
order.add_product(product1, 2)
order.add_product(product2, 3)

# Заказ
print(order)

# Выводим общую стоимость заказа
total = order.calculate_total()
print(f"Общая стоимость заказа: {total}")

# Проверяем остатки на складе после заказа
print("~После заказа~")
store.list_products()

# Меняем количество товара в заказе
order.remove_product(product1, 2)  # удаляем product1 из заказа
order.remove_product(product2, 1)

# Проверяем заказ после изменения количества товара в заказе
print("~После изменения количества товара в заказе~")
print(order)

# Проверяем остатки на складе после изменения количества товара в заказе
store.list_products()