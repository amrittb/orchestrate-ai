import simplejson as json

class Generator:

	""" Creates VideoListGenerator

	"""
	def __init__(self, filename, api_client):
		self.filename = filename
		self.api_client = api_client
		self.cache_filename = "cached_playlist.json"

		self.parse_json()

	""" Parses file into json
	
	Opens the file and loads json data by parsing the string
	"""
	def parse_json(self):
		with open(self.filename) as data_file:
			self.json_data = json.load(data_file)

	"""Returns video list for given instrument and emotion
	
	"""
	def get_video_list(self, instrument_name, emotion_label, force_refresh = False):
		instrument_playlist_id = self.json_data["instruments"][instrument_name]["playlistId"]
		emotion_playlist_id = self.json_data["emotions"][emotion_label]["playlistId"]

		instrument_playlist_items, is_instrument_playlist_cached = self.get_cached_playlist_items(instrument_playlist_id)		
		
		emotion_playlist_items, is_emotion_playlist_cached = self.get_cached_playlist_items(emotion_playlist_id)		

		if (not is_instrument_playlist_cached) or force_refresh:
			print("Fetching Video list for playlist of instrument: '",instrument_name,"'")		
			instrument_playlist_items = self.api_client.get_playlist_items(instrument_playlist_id)
			self.cache_playlist_items(instrument_playlist_id, instrument_playlist_items)
		else:
			print("Using cached list for instrument: '",instrument_name,"'")		

		if (not is_emotion_playlist_cached) or force_refresh:
			print("Fetching Video list for playlist of emotion: '",emotion_label,"'")		
			emotion_playlist_items = self.api_client.get_playlist_items(emotion_playlist_id)
			self.cache_playlist_items(emotion_playlist_id, emotion_playlist_items)
		else:
			print("Using cached list for emotion: '",emotion_label,"'")

		video_list = list(set(instrument_playlist_items).intersection(emotion_playlist_items))

		return video_list

	"""Returns cached playlist items
	
	Returns cached playlist items from json file
	"""
	def get_cached_playlist_items(self, playlist_id):
		try:
			data_file = open(self.cache_filename,"r")

			cached_json_data = json.load(data_file)

			data_file.close()

			return cached_json_data[playlist_id], (cached_json_data[playlist_id] != None)
		except:
			data_file = open(self.cache_filename,"w")

			data_file.close()

			return [], False

	"""Caches Playlist items
	
	Stores playlist items in a json file
	"""
	def cache_playlist_items(self, playlist_id, playlist_items):
		try:
			data_file = open(self.cache_filename,"r")

			cached_json_data = json.load(data_file)

			data_file.close()
		except:
			cached_json_data = {}

		cached_json_data[playlist_id] = playlist_items

		with open(self.cache_filename,"w") as data_file:
			data_file.write(json.dumps(cached_json_data))
