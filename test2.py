with open('Groovy Script/loginForEmpl.groovy', 'r', encoding="utf-8") as f:
    old_data = f.read()

new_data = old_data.replace('Иванов', 'Родионов')

with open('Groovy Script/loginForEmpl.groovy', 'w', encoding="utf-8") as f:
    f.write(new_data)
