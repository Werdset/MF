import json

orders = json.load(open('orders.json', 'r'))
new_orders = []
for order in orders.copy():
	print(order['pk'])
	new_orders.append(order)
	if 'order' in new_orders[-1]['model']:
		del new_orders[-1]['fields']['sex']
		del new_orders[-1]['fields']['excluding_weekday']
		del new_orders[-1]['fields']['is_called']
		del new_orders[-1]['fields']['dishes_monday']

json.dump(new_orders, open('new_orders.json', 'w'))
