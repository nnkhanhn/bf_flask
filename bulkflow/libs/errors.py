from bulkflow.libs.messages import Messages
from bulkflow.libs.utils import url_to_link, to_int


class Errors:
	URL_INVALID = 2601
	URL_NOT_FOUND = 2602
	URL_IS_LOCALHOST = 2603

	CHANNEL_NOT_CREATE = 2501
	CHANNEL_EXIST = 2502

	STATE_NOT_CREATE = 2401

	ACTION_INVALID = 2301

	EXCEPTION = 2201
	EXCEPTION_IMPORT = 2202

	PROCESS_NOT_CREATE = 2101
	RECONNECT_DIFFERENT_SITE = 2102

	SHOPIFY_SCOPE = 2701  # Thiếu scope
	SHOPIFY_VARIANT_LIMIT = 2702  # full variant
	SHOPIFY_API_INVALID = 2703  # full variant
	SHOPIFY_GET_PRODUCT_FAIL = 2704
	SHOPIFY_PRODUCT_NO_VARIANT = 2705
	SHOPIFY_URL_INVALID = 2706
	SHOPIFY_GET_ORDER_FAIL = 2707
	SHOPIFY_ORDER_NO_ITEM = 2708
	SHOPIFY_SCOPE_INVALID = 2709
	SHOPIFY_ORDER_ITEM_NOT_LINK = 2710
	SHOPIFY_ORDER_ITEM_OUT_STOCK = 2711
	SHOPIFY_NOT_FOUND_VARIANT_DEFAULT = 2712
	SHOPIFY_PRODUCT_NAME_MISSING = 2713
	SHOPIFY_PRODUCT_CREATE_ERROR = 2714
	SHOPIFY_PRODUCT_UPDATE_NEW_VARIANT_OPTION = 2715

	SHOPLINE_API_INVALID = 4000
	SHOPLINE_GET_PRODUCT_FAIL = 4001
	SHOPLINE_URL_INVALID = 4002
	SHOPLINE_ORDER_ITEM_OUT_STOCK = 4003
	SHOPLINE_ORDER_NO_ITEM = 4004
	SHOPLINE_NOT_FOUND_VARIANT_DEFAULT = 4005
	SHOPLINE_SCOPE = 4006  # Thiếu scope
	SHOPLINE_VARIANT_LIMIT = 4007  # full variant
	SHOPLINE_ORDER_ITEM_NOT_LINK = 4008

	WIX_API_INVALID = 3103
	WIX_GET_PRODUCT_FAIL = 3104
	WIX_IMPORT_VARIANT_FAIL = 3105

	WOOCOMMERCE_INVALID_SKU = 2902
	WOOCOMMERCE_ID_OR_SKU_REQUIRED = 2903
	WOOCOMMERCE_INVALID_URL = 2904
	WOOCOMMERCE_API_PERMISSION = 2905
	WOOCOMMERCE_ERROR_500 = 2906
	WOOCOMMERCE_ERROR_FIREWALL = 2907
	WOOCOMMERCE_CONNECT_FAIL = 2908
	WOOCOMMERCE_MOD_REWRITE = 2909
	WOOCOMMERCE_ERROR_503 = 2910
	WOOCOMMERCE_ERROR_504 = 2914
	WOOCOMMERCE_ERROR_406 = 2911
	WOOCOMMERCE_ERROR_401 = 2912
	WOOCOMMERCE_ERROR_BPS = 2913

	PRODUCT_DATA_INVALID = 2801
	PRODUCT_NOT_EXIST = 2802
	PRODUCT_NOT_EXPORT = 2803
	PRODUCT_NOT_CREATE = 2804
	PRODUCT_RATE_LIMIT = 2805

	CATEGORY_PARENT_NOT_CREATE = 2901

	CART_INFO_INVALID = 1101
	CART_NOT_CREATE_MIGRATION = 1102

	BIGCOMMERCE_API_PATH_INVALID = 1201
	BIGCOMMERCE_API_INVALID = 1202

	BONANZA_API_INVALID = 3901
	BONANZA_GET_PRODUCT_FAIL = 3902



	ETSY_API_INVALID = 1301
	ETSY_FAIL_API = 1303
	ETSY_GET_PRODUCT_FAIL = 1304
	ETSY_RATE_LIMIT = 1305
	ETSY_VARIANT_LIMIT = 1306
	ETSY_INVENTORY_VARIANT_FAIL = 1307
	ETSY_SHIPPING_ZIP_CODE = 1308

	FACEBOOK_INFO_INVALID = 1501
	FACEBOOK_FAIL_API = 1503
	FACEBOOK_CATALOG_INFO_IS_REQUIRED = 1504

	AMAZON_REQUEST_TIMEOUT = 1801
	AMAZON_API_INVALID = 1802
	AMAZON_PUSH_PRODUCT_ERROR = 1803
	AMAZON_GET_PRODUCT_ERROR = 1804
	AMAZON_GET_ORDER_ERROR = 1805
	AMAZON_ACCOUNT_INACTIVE = 1806
	AMAZON_INVALID_ASIN = 1807
	AMAZON_PRODUCT_EMPTY_TEMPLATE = 1808
	AMAZON_PRODUCT_INCOMPLETE = 1809

	GOOGLE_REQUEST_TIMEOUT = 1901
	GOOGLE_API_INVALID = 1902
	GOOGLE_REFRESH_ACCESS_TOKEN_ERROR = 1903
	GOOGLE_SKU_EMPTY = 1904
	GOOGLE_MERCHANT_ID_INVALID = 1905

	EBAY_API_INVALID = 2001
	EBAY_NOT_RESPONSE = 2002
	EBAY_CATEGORY_REQUIRED = 2003
	EBAY_PAYMENT_REQUIRED = 2012
	EBAY_SHIPPING_REQUIRED = 2013
	EBAY_MISSING_MPN = 2004
	EBAY_MISSING_BRAND = 2005
	EBAY_INVENTORY_API_REQUIRED = 2006
	EBAY_NAME = 2007
	EBAY_FREIGHT_SHIPMENT_TYPE = 2008
	EBAY_NOT_ALLOW_RELIST = 2009
	EBAY_RELIST_DUPLICATE = 2010
	EBAY_NOT_ALLOW_ENDED = 2011
	EBAY_NOT_ALLOW_RELIST_AUCTION = 2012
	EBAY_IMAGE_REQUIRED = 2013

	CHANNEL_NAME_REQUIRED = 1401
	SETUP_DATA_INVALID = 1402

	PROCESS_PRODUCT_NOT_EXIST = 1601
	PROCESS_ORDER_NOT_CREATE = 1602
	PROCESS_INVENTORY_NOT_CREATE = 1603

	SCHEDULER_NOT_EXIST = 1701
	SCHEDULER_PROCESS_ID_NOT_MATCH = 1702

	TEMPLATE_NOT_FOUND = 1901

	CM_NOT_CONNECT = 2001

	ORDER_RATE_LIMIT = 3001
	ORDER_NO_PRODUCT = 3002
	ORDER_DUPLICATE = 3003
	ORDER_STATUS_CANCELED = 3004
	ORDER_STATUS_UNPAID = 3005
	ORDER_PRODUCT_UNLINK = 3006

	SQUARESPACE_API_INVALID = 3200
	SQUARESPACE_NOT_STORE_PAGE = 3201

	CSV_FILE_NOT_MATCH = 3300
	CSV_FILE_MISSING_FIELD = 3301


	WISH_API_INVALID = 3401
	WISH_OPTION_VARIANT_TOO_MUCH = 3402
	WISH_OPTION_VARIANT = 3403
	WISH_OPTION_VARIANT_INVALID = 3405
	WISH_DESCRIPTION_REQUIRED = 3406
	WISH_SHIPPING_TEMPLATE_REQUIRED = 3407
	WISH_CATEGORY_REQUIRED = 3408

	WALMART_API_PATH_INVALID = 3501
	WALMART_VARIANT_LIMIT = 3502  # full variant
	WALMART_API_INVALID = 3503
	WALMART_GET_PRODUCT_FAIL = 3504
	WALMART_SCOPE = 3505
	WALMART_URL_INVALID = 3506
	WALMART_PUSH_PRODUCT_ERROR = 3507
	WALMART_SCOPE_INVALID = 3509
	WALMART_RATE_LIMIT = 3510
	WALMART_INTERNAL_ERROR = 3511
	WALMART_MISSING_PRODUCT_ID = 3512
	WALMART_MISSING_PRODUCT_SKU = 3513
	WALMART_MISSING_CATEGORY_TEMPLATE = 3514
	WALMART_MISSING_DESCRIPTION_IMAGES = 3515
	WALMART_ERROR_PARENT_PRODUCT = 3516
	WALMART_ACCESS_TOKEN_DENIED = 3517
	WALMART_FEED_ERROR = 3518
	WALMART_PRODUCT_ID_DUPLICATE = 3519
	WALMART_FIREWALL_BLOCKED = 3520
	WALMART_CA_API_INVALID = 3521
	WALMART_FEED_TIMEOUT = 3522
	WALMART_DESCRIPTION_LIMIT = 3523
	WALMART_SKU_DUPLICATE = 3524
	WALMART_CHAR_LIMIT = 3525
	WALMART_CATEGORY_UPGRADE = 3526
	WALMART_SYNC_SKU_MISMATCH = 3527

	ONBUY_SERVER_ERROR = 3600

	SHOPLAZZA_API_INVALID = 3700
	SHOPLAZZA_GET_PRODUCT_FAIL = 3701
	SHOPLAZZA_URL_INVALID = 3702
	SHOPLAZZA_ORDER_ITEM_OUT_STOCK = 3703
	SHOPLAZZA_ORDER_NO_ITEM = 3704
	SHOPLAZZA_NOT_FOUND_VARIANT_DEFAULT = 3705
	SHOPLAZZA_SCOPE = 3706
	SHOPLAZZA_VARIANT_LIMIT = 3707
	SHOPLAZZA_ORDER_ITEM_NOT_LINK = 3708
	SHOPLAZZA_PRODUCT_NAME_MISSED = 3709
	SHOPLAZZA_GET_ORDER_FAIL = 3710

	SQUAREPOS_API_INVALID = 9000
	SHOPWARE_API_INVALID = 9101
	SHOPWARE_CURRENCY_INVALID = 9102
	SHOPWARE_STORE_URL_INVALID = 9103

	OPENCART_CONNECTOR_BROKE = 10000
	OPENCART_SKU_EMPTY = 10001
	OPENCART_SKU_DUPLICATE = 10002
	CHANNEL_URL_IS_NOT_OPENCART_SITE = 10003
	def __init__(self):
		self.error_msg = self.error_message()


	def error_message(self):
		return {
			self.EBAY_MISSING_MPN: "when you specify Brand, MPN is required attribute.",
			self.EBAY_MISSING_BRAND: "when you specify MPN, Brand is required attribute.",
			self.EBAY_NAME: "EBAY_NAME",
			self.EBAY_FREIGHT_SHIPMENT_TYPE: "Your market does not support Freight Shipment. Please choose another shipment type and try again",
			self.EBAY_RELIST_DUPLICATE: "your product has been ended on eBay and may be relisted as another product with id {}, if so please delete the current product on LitCommerce and re-import the new product for the sync to continue",
			self.RECONNECT_DIFFERENT_SITE: "Please reconnect to the correct site you connected to.",
			self.WOOCOMMERCE_ERROR_500: f'We received an "Internal Server Error" error returned from your site. This prevented the connection from our system to your website. Please follow {url_to_link("https://help.litcommerce.com/en/article/how-to-increase-maximum-execution-time-memory-limit-for-woocommerce-15jbvt0", "the instructions")} or contact us for more solutions.',
			self.WOOCOMMERCE_ERROR_503: f"The WooCommerce server is temporarily unable to service your request due to maintenance downtime or capacity problems. Please follow {url_to_link('https://help.litcommerce.com/en/article/how-to-increase-maximum-execution-time-memory-limit-for-woocommerce-15jbvt0', 'the instructions')} or contact us for more solutions.",
			self.WOOCOMMERCE_ERROR_504: "we received '504 Gateway Time-out' error from your woocommerce site. This could be because your product has too many images or variations that your site can't handle. Please contact us for a solution.",
			self.WOOCOMMERCE_ERROR_406: "The WooCommerce server returns http status 406 with content: An appropriate representation of the requested resource could not be found on this server. This error was generated by Mod_Security. Please disabled Mod_Security and try again or contact us for more solutions.",
			self.WOOCOMMERCE_ERROR_401: "Your website is currently disconnected from our system. Please go to {} => Reconnect and try again.",
			self.WOOCOMMERCE_ERROR_BPS: "Your site is being protected by the plugin 'BulletProof Security'. Please disable to be able to connect to litcommerce",
			self.SHOPIFY_SCOPE_INVALID: "Please enter api password with sufficient permissions: read_products,write_products,write_inventory,read_locations",
			self.SHOPIFY_ORDER_ITEM_NOT_LINK: "The order has an unlinked product. Please check again.",
			self.SHOPIFY_ORDER_ITEM_OUT_STOCK: "There is a product out of stock in your order. Please update your inventory before clicking Update Order.",
			self.EBAY_NOT_RESPONSE: "no response from eBay. Please try again later",
			self.EBAY_CATEGORY_REQUIRED: "Primary Category is required. Please select a category before trying again",
			self.EBAY_NOT_ALLOW_RELIST_AUCTION: "EBAY_NOT_ALLOW_RELIST_AUCTION",
			self.EBAY_PAYMENT_REQUIRED: "EBAY_PAYMENT_REQUIRED",
			self.EBAY_SHIPPING_REQUIRED: "EBAY_SHIPPING_REQUIRED",
			self.EBAY_NOT_ALLOW_RELIST: "Your product has been Ended on eBay and the Auto Relist option is currently not enabled. Therefore, we cannot relist products. Please relist the product to continue syncing",
			self.EBAY_NOT_ALLOW_ENDED: "Out Of Stock Control is enable",
			self.EBAY_IMAGE_REQUIRED: "Product images are required.",
			self.WOOCOMMERCE_INVALID_URL: "The url you just entered doesn't seem to be woocommerce. Please check again",
			self.GOOGLE_SKU_EMPTY: 'sku is empty.',
			self.AMAZON_ACCOUNT_INACTIVE: 'Due to limited amazon account activity, your ability to create listings has been disabled.',
			self.SHOPIFY_ORDER_NO_ITEM: 'Order no products',
			self.SHOPIFY_NOT_FOUND_VARIANT_DEFAULT: 'SHOPIFY_NOT_FOUND_VARIANT_DEFAULT',
			self.SHOPIFY_PRODUCT_NAME_MISSING: 'SHOPIFY_PRODUCT_NAME_MISSING',
			self.SHOPIFY_PRODUCT_CREATE_ERROR: 'SHOPIFY_PRODUCT_CREATE_ERROR',
			self.SHOPIFY_PRODUCT_UPDATE_NEW_VARIANT_OPTION: 'SHOPIFY_PRODUCT_UPDATE_NEW_VARIANT_OPTION',
			self.ETSY_INVENTORY_VARIANT_FAIL: 'At least One product must have a quantity greater than 0',
			self.WOOCOMMERCE_API_PERMISSION: 'Api Invalid. The Api you provide must have read/write permission',
			self.URL_INVALID: 'Url invalid. Please enter the correct url',
			self.URL_IS_LOCALHOST: "Unfortunately, you can't perform connect from localhost! You should upload your site to a live server for the connector to work",
			self.CHANNEL_NOT_CREATE: 'This channel failed to create',
			self.CHANNEL_EXIST: 'You have already connected that channel',
			self.STATE_NOT_CREATE: 'State failed to create',
			self.ACTION_INVALID: 'Invalid action',
			self.EXCEPTION: 'There was an error. Please try again or contact us for a solution.',
			self.PROCESS_NOT_CREATE: 'Process failed to create',
			self.SHOPIFY_SCOPE: 'SHOPIFY_SCOPE',
			self.SHOPIFY_VARIANT_LIMIT: 'SHOPIFY_VARIANT_LIMIT',
			# self.SHOPIFY_API_INVALID: f'Please follow {url_to_link("https://help.litcommerce.com/en/article/how-can-i-get-shopify-api-key-18re237/?bust=1705458294109","these instructions")} and enter the API Password accurately. Note that the API Password is not the password used to log in to your Shopify account.',
			self.SHOPIFY_API_INVALID: f'SHOPIFY_API_INVALID.',
			self.SHOPIFY_GET_PRODUCT_FAIL: 'SHOPIFY_GET_PRODUCT_FAIL',
			self.SHOPIFY_PRODUCT_NO_VARIANT: 'SHOPIFY_PRODUCT_NO_VARIANT',
			self.PRODUCT_DATA_INVALID: 'PRODUCT_DATA_INVALID',
			self.PRODUCT_NOT_EXIST: 'PRODUCT_NOT_EXIST',
			self.CATEGORY_PARENT_NOT_CREATE: 'CATEGORY_PARENT_NOT_CREATE',
			self.CART_INFO_INVALID: 'CART_INFO_INVALID',
			self.BIGCOMMERCE_API_PATH_INVALID: 'BIGCOMMERCE_API_PATH_INVALID',
			self.BIGCOMMERCE_API_INVALID: 'BIGCOMMERCE_API_INVALID',
			self.BONANZA_API_INVALID: 'BONANZA_API_INVALID',
			self.CART_NOT_CREATE_MIGRATION: 'CART_NOT_CREATE_MIGRATION',
			self.CHANNEL_NAME_REQUIRED: 'Channel name required',
			self.SETUP_DATA_INVALID: 'SETUP_DATA_INVALID',
			self.SQUARESPACE_API_INVALID: 'SQUARESPACE_API_INVALID',
			self.PRODUCT_NOT_EXPORT: 'PRODUCT_NOT_EXPORT',
			self.PRODUCT_NOT_CREATE: 'PRODUCT_NOT_CREATE',
			self.SHOPIFY_URL_INVALID: 'Please enter the correct url (https://storeid.myshopify.com)',
			self.ETSY_SHIPPING_ZIP_CODE: 'Invalid ZIP/Postal Code. Please go to Store Manager > Settings > Shipping Settings > click on Shipping Label Options at the top and edit your selected shipping profile.',
			self.ETSY_FAIL_API: 'Error returned from Etsy',
			self.ETSY_API_INVALID: 'Error returned from info channel Etsy',
			self.ETSY_GET_PRODUCT_FAIL: 'ETSY_GET_PRODUCT_FAIL',
			self.ETSY_RATE_LIMIT: "Has exceeded the limit of calling request to api. Please wait another 30 minutes",
			self.FACEBOOK_INFO_INVALID: 'Error returned from info channel Facebook',
			self.FACEBOOK_FAIL_API: 'Error returned from Facebook',
			self.FACEBOOK_CATALOG_INFO_IS_REQUIRED: 'FACEBOOK_CATALOG_INFO_IS_REQUIRED',
			self.PROCESS_PRODUCT_NOT_EXIST: 'PROCESS_PRODUCT_NOT_EXIST',
			self.SCHEDULER_NOT_EXIST: 'SCHEDULER_NOT_EXIST',
			self.SCHEDULER_PROCESS_ID_NOT_MATCH: 'SCHEDULER_PROCESS_ID_NOT_MATCH',
			self.SHOPIFY_GET_ORDER_FAIL: 'SHOPIFY_GET_ORDER_FAIL',
			self.WOOCOMMERCE_INVALID_SKU: 'Your sku already exists on woocommerce. Please import products from woocommerce to LitC and link them, or edit the sku to continue importing.',
			self.WOOCOMMERCE_ID_OR_SKU_REQUIRED: 'Product ID or SKU is required',
			self.PROCESS_INVENTORY_NOT_CREATE: 'PROCESS_INVENTORY_NOT_CREATE',
			self.AMAZON_REQUEST_TIMEOUT: 'AMAZON_REQUEST_TIMEOUT',
			self.AMAZON_API_INVALID: 'AMAZON_API_INVALID',
			self.AMAZON_PUSH_PRODUCT_ERROR: 'AMAZON_PUSH_PRODUCT_ERROR',
			self.AMAZON_GET_PRODUCT_ERROR: 'AMAZON_GET_PRODUCT_ERROR',
			self.AMAZON_GET_ORDER_ERROR: 'AMAZON_GET_ORDER_ERROR',
			self.AMAZON_PRODUCT_EMPTY_TEMPLATE: 'Please fill in the required information on the OFFER, SEO, and LISTING DETAILS tabs before clicking "Save & Publish to Amazon." Besides, the more information you provide, the higher the chance your products will be published on Amazon.',
			self.AMAZON_INVALID_ASIN: 'AMAZON_INVALID_ASIN',
			self.AMAZON_PRODUCT_INCOMPLETE: 'Listing has not been completely configured. Please update your product data and try again. If you need further assistance, please contact our support.',
			self.GOOGLE_REQUEST_TIMEOUT: 'GOOGLE_REQUEST_TIMEOUT',
			self.GOOGLE_API_INVALID: 'Google api invalid. Please try again later.',
			self.GOOGLE_REFRESH_ACCESS_TOKEN_ERROR: 'GOOGLE_REFRESH_ACCESS_TOKEN_ERROR',
			self.EBAY_API_INVALID: 'Error returned from Ebay',
			self.CM_NOT_CONNECT: "Can't connect to cm server",
			self.TEMPLATE_NOT_FOUND: "TEMPLATE_NOT_FOUND",
			self.ORDER_RATE_LIMIT: Messages.ORDER_RATE_LIMIT_TITLE,
			self.PRODUCT_RATE_LIMIT: Messages.PRODUCT_RATE_LIMIT_TITLE,
			self.ORDER_NO_PRODUCT: 'ORDER_NO_PRODUCT',
			self.ORDER_STATUS_CANCELED: 'ORDER_STATUS_CANCELED',
			self.ORDER_STATUS_UNPAID: 'ORDER_STATUS_UNPAID',
			self.ORDER_PRODUCT_UNLINK: 'ORDER_PRODUCT_UNLINK',
			self.URL_NOT_FOUND: 'URL_NOT_FOUND',
			self.EXCEPTION_IMPORT: 'There was an error while importing. Please try again later',
			self.WIX_IMPORT_VARIANT_FAIL: 'WIX_IMPORT_VARIANT_FAIL',
			self.ETSY_VARIANT_LIMIT: 'Etsy only allows products with up to 70 variants. Please hide some variants before importing.',
			self.SQUARESPACE_NOT_STORE_PAGE: 'Your store does not have a store page enabled. Please enable at least one store page.',
			self.WOOCOMMERCE_ERROR_FIREWALL: 'We detect this website is under {} Firewall. Please temporarily turn off the firewall for the api to work properly, or contact us for more solutions.',
			self.WOOCOMMERCE_CONNECT_FAIL: f'We are unable to connect to your website. If you are using the Cloudflare Web Application Firewall, please follow {url_to_link("https://help.litcommerce.com/en/article/solution-when-your-websites-firewall-blocks-litcommerce-i2ub8p","these instructions")} to establish a connection.',
			self.CSV_FILE_NOT_MATCH: 'The file you provided does not match the structure of the sample file.',
			self.CSV_FILE_MISSING_FIELD: 'The file you provided is missing a field: {}',
			self.WOOCOMMERCE_MOD_REWRITE: 'We are unable to connect to your api. Please enable mod_rewrite before trying again',
			self.GOOGLE_MERCHANT_ID_INVALID: 'Merchant id you provided is incorrect. Please check again',
			self.WISH_API_INVALID: 'WISH_API_INVALID',
			self.WIX_API_INVALID: 'WIX_API_INVALID',
			self.WISH_OPTION_VARIANT_TOO_MUCH: 'Your product has too many options for variation. Wish only accepts variations with 2 options: size, color.',
			self.WISH_OPTION_VARIANT: 'Your product is missing the Size or Color option. Wish only accepts variations with 2 options: size, color.',
			self.WISH_OPTION_VARIANT_INVALID: '{} attributes do not match.. Wish only accepts variations with 2 options: size, color.',
			self.WISH_DESCRIPTION_REQUIRED: 'Description is required',
			self.WISH_SHIPPING_TEMPLATE_REQUIRED: 'WISH_SHIPPING_TEMPLATE_REQUIRED',
			self.WISH_CATEGORY_REQUIRED: 'Primary category is required. Please select a category before trying again.',
			self.WALMART_URL_INVALID: 'Please enter the correct URL Walmart.',
			self.WALMART_API_INVALID: 'The Walmart Client Id and Client Secret are invalid. Please check and try again.',
			self.WALMART_CA_API_INVALID: 'The Walmart Consumer ID and Private Key are invalid. Please check and try again.',
			self.WALMART_VARIANT_LIMIT: 'WALMART_VARIANT_LIMIT',
			self.WALMART_GET_PRODUCT_FAIL: 'WALMART_GET_PRODUCT_FAIL',
			self.WALMART_SCOPE_INVALID: 'Access token denied. Please check permissions and give LitCommerce full access permissions to work properly. Please wait a moment and try again if you were recently give permissions.',
			self.WALMART_PUSH_PRODUCT_ERROR: 'WALMART_PUSH_PRODUCT_ERROR',
			self.WALMART_RATE_LIMIT: 'You have reached the limit of Walmart\'s API. Please wait another 30 minutes to try again.',
			self.WALMART_INTERNAL_ERROR: 'The Walmart servers have some problems. Please wait a moment and try again.',
			self.WALMART_MISSING_PRODUCT_ID: 'The Product Identifier is missing. Enter one of those: EAN/UPC/GTIN/ISBN and try again.',
			self.WALMART_MISSING_PRODUCT_SKU: 'Walmart requires a product SKU. Please update your product and try again.',
			self.WALMART_MISSING_DESCRIPTION_IMAGES: 'Walmart requires a description and product images. Please update your product and try again.',
			self.WALMART_MISSING_CATEGORY_TEMPLATE: 'The product needs a category. Select a category in the the Category tab. You can using Templates & Recipes sidebar to apply category to multiple listings at once.',
			self.WALMART_ERROR_PARENT_PRODUCT: 'There is a problem with variant products. Click the `+` button to get the error for each product variant.',
			self.WALMART_ACCESS_TOKEN_DENIED: 'Access token denied. Please set all permissions as "Full Access" and try again.',
			self.WALMART_FIREWALL_BLOCKED: 'The request is blocked by Walmart\'s firewall. Please contact support for help.',
			self.WALMART_FEED_ERROR: 'There was an error when upload feed. Please try again or contact us for a solution.',
			self.WALMART_PRODUCT_ID_DUPLICATE: 'The {} code already exists in another product in your store catalog with a different SKU. You can use SKU Override option to update the SKU code. Alternatively, you may opt for a different {} code.',
			self.WALMART_FEED_TIMEOUT: 'Walmart Timeout: The Walmart system is not available during ingestion. Please wait for at least an hour and try again. If the problem persists, contact us for a solution.',
			self.WALMART_DESCRIPTION_LIMIT: 'Product descriptions exceed the 4000 character limit. This limit includes HTML characters. Please try again with a shorter description.',
			self.WALMART_SKU_DUPLICATE: 'You are using the same SKU code for multiple products. Please use different SKU code and try again.',
			self.WALMART_CHAR_LIMIT: 'The character count in the "{}" field has exceeded the allowed limit. Limit: {}, Actual: {}.',
			self.WALMART_CATEGORY_UPGRADE: 'WALMART_CATEGORY_UPGRADE',
			self.WALMART_SYNC_SKU_MISMATCH: 'WALMART_SYNC_SKU_MISMATCH',
			self.SQUAREPOS_API_INVALID: 'SQUAREPOS_API_INVALID',
			self.SHOPLINE_API_INVALID: 'SHOPLINE_API_INVALID',
			self.SHOPLINE_GET_PRODUCT_FAIL: 'SHOPLINE_GET_PRODUCT_FAIL',
			self.SHOPLINE_URL_INVALID: 'Please enter the correct url (https://storeid.myshopline.com)',
			self.SHOPLINE_ORDER_ITEM_OUT_STOCK: "There is a product out of stock in your order. Please update your inventory before clicking Update Order.",
			self.SHOPLINE_ORDER_NO_ITEM: 'Order no products',
			self.ONBUY_SERVER_ERROR: "OnBuy's server is experiencing an issue and is unable to process the current request. Please try again or contact support for assistance.",
			self.SHOPLINE_NOT_FOUND_VARIANT_DEFAULT: 'SHOPLINE_NOT_FOUND_VARIANT_DEFAULT',
			self.SHOPLINE_SCOPE: 'SHOPLINE_SCOPE',
			self.SHOPLINE_VARIANT_LIMIT: 'SHOPLINE_VARIANT_LIMIT',
			self.SHOPWARE_API_INVALID: 'Authentication information is incorrect. Please try again.',
			self.SHOPWARE_CURRENCY_INVALID: 'SHOPWARE_CURRENCY_INVALID',
			self.SHOPWARE_STORE_URL_INVALID: 'Store URL is invalid. Please try again.',
			self.OPENCART_CONNECTOR_BROKE: 'Opencart connector not working or not installed. Please contact support for assistance',
			self.OPENCART_SKU_EMPTY: 'SKU is empty, please enter SKU to continue',
			self.OPENCART_SKU_DUPLICATE: 'SKU is duplicated',
			self.CHANNEL_URL_IS_NOT_OPENCART_SITE: "The provided channel URL is not recognized as an OpenCart site. Check the URL for accuracy and ensure it is accessible.",
			self.SHOPLAZZA_API_INVALID: "SHOPLAZZA_API_INVALID",
			self.SHOPLAZZA_GET_PRODUCT_FAIL: "SHOPLAZZA_GET_PRODUCT_FAIL",
			self.SHOPLAZZA_URL_INVALID: "SHOPLAZZA_URL_INVALID",
			self.SHOPLAZZA_ORDER_ITEM_OUT_STOCK: "SHOPLAZZA_ORDER_ITEM_OUT_STOCK",
			self.SHOPLAZZA_ORDER_NO_ITEM: "SHOPLAZZA_ORDER_NO_ITEM",
			self.SHOPLAZZA_NOT_FOUND_VARIANT_DEFAULT: "Shoplazza does not support import orders containing products that do not exist on Shoplazza store. You can create products on your Shoplazza store before syncing the order back to your Shoplazza store.",
			self.SHOPLAZZA_SCOPE: "SHOPLAZZA_SCOPE",
			self.SHOPLAZZA_VARIANT_LIMIT: "SHOPLAZZA_VARIANT_LIMIT",
			self.SHOPLAZZA_ORDER_ITEM_NOT_LINK: "SHOPLAZZA_ORDER_ITEM_NOT_LINK",
			self.SHOPLAZZA_PRODUCT_NAME_MISSED: "SHOPLAZZA_PRODUCT_NAME_MISSED",
			self.SHOPLAZZA_GET_ORDER_FAIL: 'SHOPIFY_GET_ORDER_FAIL',
		}


	def get_msg_error(self, error_code, default = None):
		if not default:
			default = error_code
		if not error_code:
			return ''
		return self.error_msg.get(to_int(error_code), default)