menu = {
    "Baja Taco": 4.25,
    "Burrito": 7.50,
    "Bowl": 8.50,
    "Nachos": 11.00,
    "Quesadilla": 8.50,
    "Super Burrito": 8.50,
    "Super Quesadilla": 9.50,
    "Taco": 3.00,
    "Tortilla Salad": 8.00
}

total: float = 0.0
while True:
    try:
        total += menu[food] if (food := input("Item: ").lower().title()) in menu else 0.0
        if food in menu:
            print(f"Total: ${total:.2f}")
    except (EOFError):
        print("\n")
        break
