print("$0" if (greeting := input("Greeting: ").lstrip().lower()).startswith("hello") else "$20" if greeting.startswith("h") else "$100")
