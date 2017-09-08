wireless_template = """config wifi-device  radio0
	option type     mac80211
	option channel  {}
	option hwmode	11g
	option path	\'platform/qca955x_wmac\'
	option htmode	HT20
	# REMOVE THIS LINE TO ENABLE WIFI:
	#option disabled 1

config wifi-iface
	option device   radio0
	option network  lan
	option mode     ap
	option ssid     {}
	option encryption none"""