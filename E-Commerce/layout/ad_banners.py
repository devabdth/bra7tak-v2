class AdBanner:
	def __init__(
		self, id: str, title: dict, subtitle: dict, pricing: dict, action_link: str, card_action_link: str, action_text: dict, asset: str,
		background_color: str, subtitle_color: str, title_color: str, action_background_color: str, action_text_color: str
	):
		self.id= id
		self.title= title
		self.subtitle= subtitle
		self.pricing= pricing
		self.action_link= action_link
		self.action_text= action_text
		self.asset= asset
		self.background_color= background_color
		self.subtitle_color= subtitle_color
		self.title_color= title_color
		self.action_background_color= action_background_color
		self.action_text_color= action_text_color
		self.card_action_link= card_action_link

	def to_dict(self):
		return {
		"id": self.id,
		"title": self.title,
		"subtitle": self.subtitle,
		"pricing": self.pricing or "",
		"action_text": self.action_text or "",
		"action_link": self.action_link or "",
		"asset": self.asset or "",
		"background_color": self.background_color or "",
		"subtitle_color": self.subtitle_color or "",
		"title_color": self.title_color or "",
		"action_background_color": self.action_background_color or "",
		"action_text_color": self.action_text_color or "",
		"card_action_link": self.card_action_link or "",
		}