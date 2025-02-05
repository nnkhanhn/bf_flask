from bulkflow.libs.utils import *

class GraphQLQuery:
	""" This class and its subclasses are used to generate GraphQL queries for Shopify API.
	Try organizing the query and mutation order: schema -> query -> mutation
	"""
	def __init__(self):
		# limit, cursor,..
		pass


class AccountQL(GraphQLQuery):
	def graphql_get_locations_schema(self, is_strip = False):
		locations_schema = f"""{{
			node {{
				id
				name
				isActive
				isFulfillmentService
				address {{
					formatted	
				}}
			}}
		}}"""
		if is_strip:
			locations_schema = locations_schema.strip('{} ')
		return locations_schema

	def mutation_webhook_delete(self):
		graph_query = """
		mutation webhookSubscriptionDelete($id: ID!) {
			webhookSubscriptionDelete(id: $id) {
			userErrors { field message }
			deletedWebhookSubscriptionId
			}
		}
		"""

		return graph_query

	def mutation_webhook_create(self):
		graphql_query = """
		mutation WebhookSubscriptionCreate($topic: WebhookSubscriptionTopic!, $webhookSubscription: WebhookSubscriptionInput!) {
			webhookSubscriptionCreate(topic: $topic, webhookSubscription: $webhookSubscription) {
			userErrors { field message }
			webhookSubscription {
				id
				topic
				apiVersion { handle supported }
				format
				createdAt
			}
			}
		}
		"""

		return graphql_query

	def query_webhooks_get(self):
		graph_query = """
		query WebhookSubscriptionList {
			webhookSubscriptions(first: 50) {
			edges {
				node {
				id
				topic
				endpoint {
					__typename
					... on WebhookHttpEndpoint { callbackUrl }
					... on WebhookEventBridgeEndpoint { arn }
					... on WebhookPubSubEndpoint { pubSubProject pubSubTopic }
				}
				createdAt
				updatedAt
				apiVersion { handle }
				format
				includeFields
				metafieldNamespaces
				}
			}
			}
		}
		"""

		return graph_query

	def query_access_scopes(self):
		graph_query = """
		query AccessScopeList {
			currentAppInstallation {
				accessScopes { handle }
			}
		}			
		"""

		return graph_query

	def query_get_countries(self):
		graph_query = """ 
		query DeliveryZoneList {
			deliveryProfiles(first: 100) {
			edges {
				node {
				id
				profileLocationGroups {
					locationGroup { id }
				locationGroupZones(first: 100) {
					edges {
						node {
						zone {
							id
							name
							countries {
							id
							name
							code { countryCode }
							provinces { name code }
							}
						}
						}
					}
					}
				}
				}
			}
			}
		}
		"""

		return graph_query

	def query_shop_info(self):
		graphql_query = """
		query ShopInfo {
			shop {
				contactEmail
				createdAt
				description
				email
				id
				name
				primaryDomain { host id url}
				resourceLimits { locationLimit maxProductOptions maxProductVariants redirectLimitReached }
				shopOwnerName
				timezoneOffset
				unitSystem
				updatedAt
				url
			}
		}	
			"""

		return graphql_query

	def query_locations(self):
		query_graph = f"""query GetLocations {{
			locations(first: 10, includeInactive: false, includeLegacy: true) {{
				edges {self.graphql_get_locations_schema()}	
			}}	
		}}
		"""
		return query_graph


class ProductQL(GraphQLQuery):
	def __init__(self):
		super().__init__()
		self.IMAGE_LIMIT = 40
		pass

	def graphql_get_product_schema(self, include_variant = False):
		"""flags something here"""
		product_schema = (f"""{{
			id
			title
			category
			{{
				id
				fullName

			}}
			compareAtPriceRange
			{{
				maxVariantCompareAtPrice
				{{
					amount
					currencyCode
				}}
				minVariantCompareAtPrice
				{{
					amount
					currencyCode
				}}
			}}
			createdAt""" + f"""
			collections(first: 20) {{
				edges {{
					node {{
				""" + f'{self.graphql_get_collection_schema(True)}' + f"""
			}}  
				}}
			}}
			descriptionHtml
			handle
			hasOnlyDefaultVariant
			""" + f"""{
		'' if not include_variant else
		f'''
				variants(first: 100, sortKey: POSITION) {{edges {{node {self.graphql_get_product_variant_schema()}}}}}'''
		}""" + f"""
			media(first: 50, sortKey: POSITION)
			{{
				nodes
				{{
					alt
					mediaContentType
					id
					... on MediaImage {{
						preview {{
							image {{
								url
							}}
						}}   
					}}
					...on ExternalVideo
					{{
						originUrl
					}}
					...on Video
					{{
						originalSource
						{{
							url
							width
							height
							fileSize
							format
							mimeType
						}}
						filename
					}}
				}}
			}}
			metafields(first: 100)
			{{
				""" + f'{self.graphql_get_metafields_schema(True)}' + f"""
			}}
			options
			{{
				id
				name
				optionValues
				{{
					hasVariants
					id
					name
					swatch
					{{
						color
						image
						{{
							alt
							createdAt
							id
							image
							{{
								url
							}}

						}}
					}}
				}}
			}}
			productType
			publishedAt
			seo
			{{
				description
				title
			}}
			status
			tags
			totalInventory
			tracksInventory
			updatedAt
			vendor
		}}""")

		return product_schema

	def graphql_get_product_variant_schema(self, is_strip = False):
		variant_schema = (f"""{{
				availableForSale
				barcode
				compareAtPrice
				createdAt
				id
				image {{
					altText
					height
					id
					url
				}}
				inventoryItem {{
					id
					inventoryLevels(first: 10) {{
						edges {{
							node {{
								id
								location {{
									id
									name    
								}}   
								quantities(names: ["available"]) {{
									name
									quantity    
								}}
							}}   
						}}
					}}
					measurement {{
						weight {{
							unit
							value
						}}
					}}
					sku
					tracked
					unitCost {{
						amount
					}}
					updatedAt
				}}
				inventoryPolicy
				inventoryQuantity
				metafields(first: 50) {{
					""" + f'{self.graphql_get_metafields_schema(is_strip = True)}'
							+ f"""
				}}
				position
				price
				selectedOptions {{
					name    
					value
				}}
				sku
				title
				updatedAt
		}}""")
		if is_strip:
			variant_schema = variant_schema.strip('{} ')
		return variant_schema

	def graphql_get_collection_schema(self, is_strip = False):
		collection_schema = """{
			id
			title
			ruleSet {
				appliedDisjunctively	
			}	
		}"""
		if is_strip:
			collection_schema = collection_schema.strip('{} ')
		return collection_schema

	def graphql_get_metafields_schema(self, is_strip = False):
		metafields_schema = f"""{{
			nodes {{
				id
				value
				key
				type
				namespace 
				definition {{
					name
				}}
			}}
		}}"""
		if is_strip:
			metafields_schema = metafields_schema.strip('{} ')
		return metafields_schema

	def schema_collection(self, is_strip = False):
		collection_schema = """{
			id
			title
			ruleSet {
				appliedDisjunctively	
			}	
		}"""
		if is_strip:
			collection_schema = collection_schema.strip('{} ')
		return collection_schema

	def mutation_metafields_delete(self):
		query = """mutation metafieldsDelete($metafields: [MetafieldIdentifierInput!]!) {
					metafieldsDelete(metafields: $metafields) {
					deletedMetafields { 
						key
						namespace
						ownerId
					}
					userErrors {
						field 
						message 
						} 
					} 
				}
				"""
		return query

	def mutation_media_stage_upload(self):
		graph_query = """
			mutation StagedUploadsCreate ($input: [StagedUploadInput!]!) {
				stagedUploadsCreate(input: $input) {
					stagedTargets {
						resourceUrl
						url
						parameters {
							name
							value
						}
					}
					userErrors {
						field
						message
					}
				}
			}
		"""

		return graph_query

	def mutation_product_delete(self):
		graph_query = f"""mutation DeleteProductByID($ProductID: ID!){{
			productDelete(input: {{id: $ProductID}}, synchronous: false) {{
				deletedProductId
				userErrors {{
					field	
					message
				}}
			}}
		}}
		"""

		return graph_query

	def mutation_product_create(self, image_limit = None):
		if not image_limit:
			image_limit = self.IMAGE_LIMIT
		query = '''mutation LitCCreateProduct($product: ProductCreateInput!, $images: [CreateMediaInput!]!){
					productCreate(product: $product, media: $images) {
					product {
						id
						media(first: ''' + to_str(image_limit) + ''') {
						nodes {
							id
						}
						}
					},
					userErrors {
					field
					message
				}
					}
				}'''

		return query

	def mutation_product_category_update(self):
		query = '''mutation updateProductCategory ($ProductID: ID!, $CategoryID: ID!){
			productUpdate(product: {id: $ProductID, category: $CategoryID}) {
			product {
				id
			}
			}
		}
		'''

		return query

	def mutation_product_media_create(self):
		graph_query = """
			mutation ProductCreateMedia ($product_id: ID!, $media: [CreateMediaInput!]!) {
				productCreateMedia(
					productId: $product_id,
					media: $media
				) {
					media {
						alt
						mediaContentType
						status
						id
					}
				}
			}
		"""
		return graph_query

	def mutation_product_media_delete(self):
		mutation_query = """ mutation productDeleteMedia($mediaIds: [ID!]!, $productId: ID!) {
			productDeleteMedia(mediaIds: $mediaIds, productId: $productId) {
			deletedMediaIds
			deletedProductImageIds
			mediaUserErrors {
				field
				message
			}
			product {
				id
				title
				media(first: 10) {
				nodes {
					alt
					mediaContentType
					status
				}
				}
			}
			}
		}		
		"""
		return mutation_query

	def mutation_product_update(self, image_limit = None):
		if not image_limit:
			image_limit = self.IMAGE_LIMIT

		query_update_product = '''mutation LitCUpdateProduct($product: ProductUpdateInput!, $images: [CreateMediaInput!]!){
						productUpdate(product: $product, media: $images) {
						product {
							id
							media(first: ''' + to_str(image_limit) + ''') {
							nodes {
								id
							}
							}
							variants(first: 100, sortKey: POSITION) {
							edges {
								node {
									id
									title
									selectedOptions {
										name
										value
									}
									inventoryPolicy 
									inventoryQuantity
								} 
							} 
							}
						},
						userErrors { field message }
						}
					}'''
		return query_update_product

	def mutation_product_variants_bulk_create(self):
		query_create = '''mutation ChannelupdateProductVariantsBulkCreate($productId: ID!, $variants: [ProductVariantsBulkInput!]!, $strategy: ProductVariantsBulkCreateStrategy!) {
					productVariantsBulkCreate(productId: $productId, variants: $variants, strategy: $strategy) {
					productVariants {
						id
						position
						image {
						id
						url 
						}
						selectedOptions {
						name
						value
						}
						inventoryItem {
						id
						inventoryLevels(first: 5) {
							edges {
								node {
									id 
									location {
										id
										name  
									}
								} 
							} 
						} 
					}
				}
				userErrors {
					field
					message
				}
			}
		}'''
		return query_create

	def mutation_product_variants_bulk_update(self):
		query_update = """
			mutation productVariantsBulkUpdate($productId: ID!, $variants: [ProductVariantsBulkInput!]!) {
				productVariantsBulkUpdate(productId: $productId, variants: $variants) {
				product {
					id
				}
				productVariants {
					id
					media(first: 20) {
					nodes {
						id
						alt
						mediaContentType  
					}
					}
					inventoryItem {
					id
					inventoryLevels(first: 5) {
						edges {
							node {
								id 
								location {
									id
									name  
								}
							} 
						} 
					} 
				}
					metafields(first: 2) {
					edges {
						node {
						namespace
						key
						value
						}
					}
					}
				}
				userErrors {
					field
					message
				}
				}
			}
		"""
		return query_update

	def mutation_inventory_update(self, inventory_id, tracked):
		track_query = f"""mutation ChannelSyncInventoryLevel {{
				inventoryItemUpdate(id: "{inventory_id}", input: {{tracked: {tracked} }}) {{
					inventoryItem {{
					id
					tracked
					}}
					userErrors {{
					field
					message
					}}
				}}
				}}"""
		return track_query

	def mutation_inventory_set_quantities(self):
		query = """ mutation inventorySetQuantities($input: InventorySetQuantitiesInput!) {
			inventorySetQuantities(input: $input) {
				inventoryAdjustmentGroup {
					app {
						appStoreAppUrl
					}
					reason
					referenceDocumentUri
					changes {
						name
						delta
						quantityAfterChange
					}
				}
				userErrors {
					code
					field
					message
				}
			}
		}
		"""
		return query

	def mutation_inventory_adjust_quantities(self):
		graph_query = """ mutation inventoryAdjustQuantities($input: InventoryAdjustQuantitiesInput!) {
				inventoryAdjustQuantities(input: $input) {
				inventoryAdjustmentGroup {
					createdAt
					reason
					referenceDocumentUri
					changes { name delta }
				}
				userErrors { field message }
				}
			} """
		return graph_query

	def mutation_channel_sync_inventory_level(self):
		bulk_variant = """
			mutation channelSyncInventoryLevel($productId: ID!, $variants: [ProductVariantsBulkInput!]!) {
				productVariantsBulkUpdate(productId: $productId, variants: $variants) {
				productVariants {
					id
				}
				userErrors {
					field
					message
				}
				}
			}
		"""
		return bulk_variant

	def mutation_channel_sync_product(self):
		query_update_product = '''mutation ChannelSyncProduct($product: ProductUpdateInput!){
						productUpdate(product: $product) {
							product {
								id
								status
							}
						}
					}'''
		return query_update_product

	def mutation_channel_sync_product_variant(self):
		price_query = """
			mutation channelSyncProductVariantsBulkUpdate($productId: ID!, $variants: [ProductVariantsBulkInput!]!) {
				productVariantsBulkUpdate(productId: $productId, variants: $variants) {
				productVariants {
					id
					price
					compareAtPrice
				}
				userErrors {
					field
					message
				}
				}
			}
		"""
		return price_query

	def mutation_product_sync_title_description(self):
		update_query = """mutation SyncProductTitleDescription($product_info: ProductUpdateInput!){
			productUpdate(product: $product_info) {
				product {
					id
					descriptionHtml	
				}
				userErrors {
					field
					message	
				}
			}	
		}"""

		return update_query

	def mutation_variant_sync_title(self):
		query_variant = """mutation channelSyncTitleVariantUpdate($productId: ID!, $variants: [ProductVariantsBulkInput!]!) {
				productVariantsBulkUpdate(productId: $productId, variants: $variants) {
				product {
					id
				}
				productVariants {
					id
				}
				userErrors {
					field
					message
				}
				}
			}
		"""

		return query_variant

	def mutation_product_media_update(self):
		query = """
			mutation productUpdateMedia($media: [UpdateMediaInput!]!, $productId: ID!)
				{
					productUpdateMedia(media: $media, productId: $productId)
					{
						media { alt }
					}
				}
		"""
		return query

	def mutation_product_media_reorder(self):
		graph_query = """
					mutation ProductReorderMedia($id: ID!, $moves: [MoveInput!]!) {
						productReorderMedia(
							id: $id
							moves: $moves
						) {
							job {
								done
								id
							}
							userErrors {
								field
								message
							}
							mediaUserErrors {
								code
								field
								message
							}
						}
					}
					"""

		return graph_query

	def mutation_metaobject_create(self):
		query = """
		mutation CreateMetaobject($metaobject: MetaobjectCreateInput!) {
			metaobjectCreate(metaobject: $metaobject) {
				metaobject {
					id
				}
				userErrors {
					field
					message
					code
				}
			}
		}
		"""
		return query

	def mutation_collection_add_products(self):
		query = """mutation collectionAddProductsV2($id: ID!, $productIds: [ID!]!) {
			collectionAddProductsV2(id: $id, productIds: $productIds) {
			job {
				done
				id
			}
			userErrors {
				field
				message
			}
			}
		}
		"""
		return query

	def mutation_collection_delete(self):
		query = """ mutation CollectionDelete($collectionID: ID!) {
			collectionDelete(input: {id: $collectionID}) {
				deletedCollectionId
				userErrors { field message }
			}
		}
		"""
		return query

	def mutation_collection_remove_product(self):
		query = """mutation collectionRemoveProducts($id: ID!, $productIds: [ID!]!) {
				collectionRemoveProducts(id: $id, productIds: $productIds) {
				job {
					done
					id
				}
				userErrors { field message }
				}
			}
		"""
		return query

	def mutation_product_status_update(self):
		graph_query = f"""
			mutation UpdateProductStatus($ProductID: ID!, $ProductStatus: ProductStatus) {{
				productUpdate(input: {{
					id: $ProductID,
					status: $ProductStatus	
				}})
				{{
					product {{
						id
						title
						status	
					}}	
					userErrors {{
						field	
						message
					}}
				}}	
			}}
		"""

		return graph_query

	def mutation_collection_create(self):
		graph_query = """
		mutation CollectionCreate($input: CollectionInput!) {
			collectionCreate(input: $input) {
			userErrors {
				field
				message
			}
			collection {
				id
				title
				descriptionHtml
				handle
				sortOrder
				ruleSet {
				appliedDisjunctively
				rules {
					column
					relation
					condition
				}
				}
			}
			}
		}
		"""

		return graph_query

	def query_collections_count(self):
		graphql_query = """
			query GetCollectsCount($collection_query: String) {
				collectionsCount(query: $collection_query) { count }
			}
			"""

		return graphql_query

	def query_collections(self, next_cursor = None):
		query_default = 'first: $limit, query: $collection_query'
		if next_cursor:
			query_default = f"""first: $limit, after:"{next_cursor}", query: $collection_query"""

		graphql_query = f"""query CollectionList($collection_query: String, $limit: Int) {{
			collections({query_default}) {{
				edges {{
						node {{
							id
							legacyResourceId
							title
							templateSuffix
						}}
					}}
					pageInfo {{ hasNextPage endCursor }}
				}}
			}}"""

		return graphql_query

	def query_products_in_specific_collection(self):
		query = f"""query GetProductsInCollection($collectionId: ID!) {{
				collection(id:	$collectionId) {{
					productsCount {{
						count	
					}}
					products(first:	250) {{
						edges {{
							node
								{self.graphql_get_product_schema()}
							}}
						pageInfo {{
							endCursor	
						}}
					}}
				}}
			}}
		"""
		return query

	def query_product_collections(self):
		query = """query GetProductCollections($productId: ID!) {
			product(id: $productId) {
			id
			collections(first: 25) {
				edges {
				node {
				""" + f'{self.schema_collection(True)}' + """
				}
				}
			}
			}
		}"""

		return query

	def query_get_product_media(self, image_limit = None):
		if not image_limit:
			image_limit = self.IMAGE_LIMIT

		query = """
			query GetProductImagesAndMedia($productId: ID!) {
				product(id: $productId) {
					images(first:""" + to_str(image_limit) + """) {
						edges {
							node {
								altText
								id
								url
							}
						}
					}
					media(first:""" + to_str(image_limit) + """, sortKey: POSITION) {
						edges {
							node {
								id
								mediaContentType
								... on MediaImage {
									image {
										altText
										id
										url
									}
									mediaContentType
									originalSource {
										fileSize
									}
								}
								... on Video {
									sources {
										fileSize
										format
										url	
									}
								}
							}
						}
					}
				}
			}
			"""
		return query

	def query_products_count(self, query_in_query):
		query = f"""
		{{
			productsCount(query: "{query_in_query}") {{
				count
			}}
		}}
		"""
		return query

	def query_get_product_by_id(self):
		graph_query = f"""query GetProductByID($ProductID: ID!){{
			node(id: $ProductID) {{
				...on Product
				{self.graphql_get_product_schema(include_variant = True)}
			}}
		}}
		"""

		return graph_query

	def query_get_products(self, arguments = '', next_cursor = '', query_in_query = ''):
		if not arguments and not next_cursor:
			arguments = """first: 25, reverse: true, sortKey: UPDATED_AT"""
		if next_cursor:
			query = f""" query {{
				products({arguments}, after: "{next_cursor}") {{	
					edges {{
						node 
							{self.graphql_get_product_schema()}
					}}
					pageInfo {{
						hasNextPage
						endCursor
					}}  
				}}
			}}
			"""
		else:
			query = f""" query {{
				products({arguments}, query: "{query_in_query}") {{	
					edges {{
						node 
							{self.graphql_get_product_schema()}
					}}
					pageInfo {{
						hasNextPage
						endCursor
					}}  
				}}
			}}
			"""

		return query

	def query_get_variant_by_id(self):
		graph_query = f"""
		query GetVariantByID($VariantID: ID!) {{
			productVariant(id: $VariantID) {{
				{self.graphql_get_product_variant_schema(is_strip = True)}	
			}}	
		}}"""

		return graph_query

	def query_get_variant_metafields(self, pre_query):
		query = '''query GetVariantMetafields{  {
			productVariants('''+pre_query+''', first: 10) {
				pageInfo {
				hasNextPage
			}
			edges {
				cursor
			}
			nodes {
				metafields(first: 50) {
				nodes {
					value
					key
					definition {
					name
				}
				}
				},
				id
			}
			}
		}
		'''
		return query

	def query_get_products_ext(self):
		query = f'''query GetProductsByExt($ProductIDs:[ID!]!)
				{{
				nodes(ids: $ProductIDs) {{
				...on Product {{
					id
					category {{
					id
					fullName
				}}
				media(first: 20) {{
					nodes {{
					... on ExternalVideo {{
						id
						originUrl
					}}
					... on Video {{
						id
						originalSource {{
						url
						width
						height
						fileSize
						format
						mimeType
						}}
						filename
					}}
					}}
				}}
				variants(first: 100, sortKey: POSITION) {{
					edges {{
						node {{
						{self.graphql_get_product_variant_schema(is_strip = True)}
						}}
					}}
					pageInfo {{
						hasNextPage
						endCursor
					}}
				}}
				metafields(first: 100) {{
					nodes {{
					type
					value
					key
					definition {{
					name
				}}
					}}
				}}
				}}
				}}
			}}'''

		return query

	def query_metaobjects(self):
		metaobject_info_query = """ query GetMetaobject($id: ID!) {
			metaobjectDefinition(id: $id) {
				fieldDefinitions {
					key
					required
					type {
						name
					}
				}
				type
				displayNameKey
				metaobjects(first: 100) {
					nodes {
						displayName
						fields {
							key
							value
						}
						id
					}
				}
			}
		}"""
		return metaobject_info_query

	def query_metafield_definitions(self, owner_type = 'PRODUCT'):
		query = '''query metafield_definitions{
			metafieldDefinitions(ownerType: ''' + owner_type + ''', first: 100) {
			nodes {
				name
				key
				namespace
				type {
					valueType
					name
				}
				validations {
					type
					value
					name
				}
			}
			}
		}
		'''
		return query

	def query_get_metafield_by_id(self, metaobject_id):
		query = f"""
		query {{
			metaobject(id: "{metaobject_id}") {{
			id
			fields {{
				key
				value
				type
			}}
			}}
		}}
		"""
		return query

	def query_sale_channels(self):
		query = '''query channels {
			channels(first: 100) {
			nodes {
				handle
				id
				name
			}
			}
		}
				'''
		return query

class OrderQL(GraphQLQuery):
	def __init__(self):
		super().__init__()
		pass

	def fragment_moneybag_input(self, amount, currency):
		return {'shopMoney': {'amount': amount, 'currencyCode': currency}}

	def graphql_get_order_schema(self, is_strip = False):
		order_schema = f"""{{
			id
			billingAddress {{
				{self.graphql_fragment_mailing_address()}	
			}}
			createdAt
			cancelledAt
			currencyCode
			customer {{
				id
				defaultAddress {{
					{self.graphql_fragment_mailing_address()}
				}}
				email
				firstName
				lastName
				note
			}}
			displayFinancialStatus
			displayFulfillmentStatus
			discountCodes
			email
			fulfillmentOrders(first: 5) {{
				nodes {{
					id
					assignedLocation {{
						location {{ id }}
					}}
					status
					lineItems(first: 100) {{
						nodes {{
							id
							inventoryItemId
							remainingQuantity
							totalQuantity
						}}
					}}
				}}					
			}}
			fulfillments(first: 50) {{
				id
				createdAt
				trackingInfo {{
				company
				url
				number
				}}
				fulfillmentLineItems(first: 50) {{
				nodes {{ 
					id
					lineItem {{
						product {{ id }}
						quantity	
					}}
				}} 
				}}
			}}
			lineItems(first: 50) {{
				nodes {{
				id
				product {{
					id	
					hasOnlyDefaultVariant
				}}
				variant {{
					id
					displayName	
					selectedOptions {{
						name
						value
					}}
				}}
				originalUnitPriceSet {{
				{self.graphql_fragment_money_bag()} 
				}}
				originalTotalSet {{
				{self.graphql_fragment_money_bag()}
				}}
				totalDiscountSet {{
				{self.graphql_fragment_money_bag()}
				}}
				taxLines(first:5) {{
				priceSet {{
					{self.graphql_fragment_money_bag()} 
				}} 
				rate
				ratePercentage
				}} 
				lineItemGroup {{
				id
				variantId
				variantSku

				}}
				sku
				name
				quantity
				}}
			}}
			name
			paymentGatewayNames
			shippingAddress {{
				{self.graphql_fragment_mailing_address()}
			}}
			shippingLines(first: 1) {{
				nodes {{
				id
				title
				originalPriceSet {{
					{self.graphql_fragment_money_bag()}	
				}}
				}}
			}}
			subtotalPriceSet {{ {self.graphql_fragment_money_bag()} }}
			tags
			taxesIncluded
			totalDiscountsSet {{ {self.graphql_fragment_money_bag()} }}
			totalShippingPriceSet {{ {self.graphql_fragment_money_bag()} }}
			totalTaxSet {{ {self.graphql_fragment_money_bag()} }}
			totalPriceSet {{ {self.graphql_fragment_money_bag()} }}
			transactions(first: 10) {{
				id	
				kind
				amountSet {{ {self.graphql_fragment_money_bag()} }} 
			}}
			note
			updatedAt
		}}"""
		if is_strip:
			order_schema = order_schema.strip('{} ')
		return order_schema

	def graphql_fragment_money_bag(self):
		return f"""
			presentmentMoney {{
				amount
				currencyCode
			}}
			shopMoney {{
				amount
				currencyCode
			}}
		"""

	def graphql_fragment_mailing_address(self):
		return f"""
			firstName
			lastName
			address1
			address2
			city
			country
			countryCodeV2
			province
			provinceCode
			zip
			phone
			company
		"""

	def mutation_transaction_create(self):
		graph_query = """
		mutation TransactionCreate($input: OrderCaptureInput!) {
			orderCapture(input: $input) {
			transaction {
				accountNumber
				createdAt
				errorCode
				formattedGateway
				gateway
				id
				kind
				status
				user { id }
			}
			userErrors { field message }
			}
		}	
		"""
		return graph_query

	def mutation_order_update_metafield(self):
		graph_query = """
			mutation updateOrderMetafields($input: OrderInput!) {
				orderUpdate(input: $input) {
				order {
					id
					metafields(first: 10) {
					edges {
						node {
						id
						namespace
						key
						value
						}
					}
					}
				}
				userErrors {
					message
					field
				}
				}
			}
		"""
		return graph_query

	def mutation_order_create(self):
		graph_query = """mutation OrderImport($order: OrderCreateOrderInput!, $options: OrderCreateOptionsInput) {
			orderCreate(order: $order, options: $options) {
			userErrors {
				field
				message
			}
			order {
				id
				createdAt
				displayFinancialStatus
				displayFulfillmentStatus
				name
				totalTaxSet {
				shopMoney {
					amount
					currencyCode
				}
				}
				lineItems(first: 5) {
				nodes {
					variant {
					id
					}
					id
					title
					quantity
					taxLines {
					title
					rate
					priceSet {
						shopMoney {
						amount
						currencyCode
						}
					}
					}
				}
				}
			}
			}
		}"""

		return graph_query

	def mutation_fulfillment_order_move(self):
		graph_query_move = """
		mutation fulfillmentOrderMove($id: ID!, $newLocationId: ID!, $lineItems: [FulfillmentOrderLineItemInput!]!) {
			fulfillmentOrderMove(id: $id, newLocationId: $newLocationId, fulfillmentOrderLineItems: $lineItems) {
			movedFulfillmentOrder { id status }
			remainingFulfillmentOrder { id status }
			userErrors { field message }
			}
		}
		"""
		return graph_query_move

	def mutation_order_refund_create(self):
		graph_query = """mutation RefundCreate($input: RefundInput!) {
			refundCreate(input: $input) {
			refund {
				id
				totalRefundedSet { presentmentMoney { amount currencyCode }
				}
			}
			userErrors { field message }
			}
		}
		"""
		return graph_query

	def mutation_fulfillment_cancel(self):
		graph_query = """mutation fulfillmentCancel($id: ID!) {
			fulfillmentCancel(id: $id) {
			fulfillment { id status }
			userErrors { field message }
			}
		}"""

		return graph_query

	def mutation_order_transaction_capture(self):
		"""order transaction create"""
		graph_query = """mutation CaptureOrderTransaction($input: OrderCaptureInput!) {
			orderCapture(input: $input) {
			transaction {
				id
				kind
				status 
			}
			userErrors { field message }
			}
		}"""
		return graph_query

	def mutation_fulfillment_create(self):
		graph_query = """ 
		mutation fulfillmentCreate($fulfillment: FulfillmentInput!, $message: String) {
			fulfillmentCreate(fulfillment: $fulfillment, message: $message) {
			fulfillment {
				id
				trackingInfo(first: 5) { number url company }
			}
			userErrors { field message }
			}
		}
		"""

		return graph_query

	def mutation_order_cancel(self):
		graph_query = """mutation OrderCancel($orderId: ID!, $notifyCustomer: Boolean, $reason: OrderCancelReason!, $refund: Boolean!, $restock: Boolean!) {
			orderCancel(orderId: $orderId, notifyCustomer: $notifyCustomer, reason: $reason, refund: $refund, restock: $restock) {
			job { done id }
			orderCancelUserErrors { code field message }
			}
		}"""
		return graph_query

	def query_get_order_transactions(self):
		graph_query = """
		query GetOrderTransactions($orderId: ID!) {
			order(id: $orderId) {
			id
			transactions { id amount kind status }
			}
		}
		"""

		return graph_query

	def query_get_order_fulfillements(self):
		fulfill_query = """query GetOrderFullfillment($id: ID!, $limit: Int){
			order(id: $id) {
				fulfillmentOrders(first: $limit) {
					nodes { id }
				}	
			}	
		}"""
		return fulfill_query

	def query_get_order_fulfillment_by_id(self):
		graph_query = """ query GetFulfillmentOrderById($id: ID!) {
			fulfillmentOrder(id: $id) {
			id
			assignedLocation {
				location {
				id
				}
			} 
			status
			lineItems(first: 100) {
				nodes {
				id
				inventoryItemId
				remainingQuantity
				totalQuantity
				}
			}
			}
		}
		"""
		return graph_query

	def query_get_inventory_level_location(self):
		graph_query = """query GetInventoryLevelLocation($id: ID!) {
			inventoryItem(id: $id) {
			id
			inventoryLevels(first: 5) {
				nodes {
					location {
					id
					name
					}
					quantities(names: "available") {
					id
					name
					quantity 
					}
				}
			}
			}
		} """
		return graph_query

	def query_orders_count(self):
		graph_query = """query GetOrderCount($query: String) {
			ordersCount(query: $query) {
			count
			}
		}
		"""

		return graph_query

	def query_get_order_by_id(self):
		graph_query = f"""query GetOrderByID($id: ID!){{
			node(id: $id) {{ ...on Order {self.graphql_get_order_schema(is_strip = False)} }}
		}}
		"""

		return graph_query

	def query_get_orders(self, end_cursor = None):
		if end_cursor is not None:
			graph_query = f"""query GetOrders($end_cursor: String, $first: Int) {{
				orders(first: $first, after: $end_cursor, sortKey: UPDATED_AT) {{
				edges {{
					node {{ {self.graphql_get_order_schema(is_strip = True)} }}
				}}
				pageInfo {{ hasNextPage endCursor }}
				}}
			}}"""
		else:
			graph_query = f"""query GetOrders($query: String, $first: Int) {{
				orders(first: $first, query: $query, sortKey: UPDATED_AT) {{
				edges {{
					node {{ {self.graphql_get_order_schema(is_strip = True)} }}
				}}
				pageInfo {{ hasNextPage endCursor }}
				}}
			}}"""

		return graph_query

