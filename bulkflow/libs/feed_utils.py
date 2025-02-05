def feed_convert_field(field):
	if field in ['vendor', 'brand']:
		field = 'brand'
	if field in ['gtin', 'feed_gtin']:
		field = 'feed_gtin'
	if field in ['sale_price']:
		field = 'special_price.price'
	if field in ['manufacturer']:
		field = 'manufacturer.name'
	if field.startswith('c.'):
		field = field[2:]
		field = f'dict_attributes.{field}'
	if field in ['category']:
		field = 'category_name_list'
	if field in ['title']:
		field = 'name'
	return field