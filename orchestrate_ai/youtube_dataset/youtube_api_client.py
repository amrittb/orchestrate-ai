import urllib3
import simplejson as json

class Client:

	def __init__(self, api_key):
		self.api_key = api_key
		urllib3.disable_warnings()

	"""Returns playlist items
	
	"""
	def get_playlist_items(self, playlist_id):
		http = urllib3.PoolManager()

		item_ids = []

		next_page_token = None
		page = 1

		print("Fetching playlist items for playlist_id", playlist_id)

		while True:
			response = http.request("GET", self.get_playlist_items_api_url(playlist_id, next_page_token))
			json_response = json.loads(response.data)

			total_results = json_response["pageInfo"]["totalResults"]
			per_page = json_response["pageInfo"]["resultsPerPage"]

			total_pages = (total_results // per_page) + 1

			print("Fetched ", len(json_response['items']), " items on page ", page, "out of ", total_pages, " pages")

			for item in json_response["items"]:
				item_ids.append(item["contentDetails"]["videoId"])

			if total_results <= len(item_ids):
				break
			else:
				page += 1
				next_page_token = json_response["nextPageToken"]

		return item_ids

	def get_playlist_items_api_url(self, playlist_id, next_page_token = None):
		url = "https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults=50&playlistId="+ playlist_id +"&key=" + self.api_key

		if next_page_token is not None:
			url = url + "&pageToken=" + next_page_token

		return url