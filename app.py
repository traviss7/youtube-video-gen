import tkinter as tk
from tkinter import ttk, messagebox

try:
    from googleapiclient.discovery import build
except ImportError:
    build = None  # google-api-python-client is required

API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

class YouTubeSearcher:
    def __init__(self, api_key: str):
        self.api_key = api_key
        if build:
            self.youtube = build(API_SERVICE_NAME, API_VERSION, developerKey=api_key)
        else:
            self.youtube = None

    def search(self, query: str, max_results: int = 5):
        """Search for short videos matching the query."""
        if not self.youtube:
            return []
        request = self.youtube.search().list(
            q=query,
            part="id",
            type="video",
            videoDuration="short",
            maxResults=max_results,
        )
        search_response = request.execute()
        video_ids = [item['id']['videoId'] for item in search_response.get('items', [])]
        if not video_ids:
            return []
        details_request = self.youtube.videos().list(
            part="snippet,contentDetails",
            id=','.join(video_ids)
        )
        details_response = details_request.execute()
        results = []
        for item in details_response.get('items', []):
            snippet = item['snippet']
            details = item['contentDetails']
            results.append({
                'title': snippet.get('title'),
                'duration': details.get('duration'),
                'category': snippet.get('categoryId'),
                'channel': snippet.get('channelTitle'),
            })
        return results

class App(tk.Tk):
    def __init__(self, searcher: YouTubeSearcher):
        super().__init__()
        self.searcher = searcher
        self.title("YouTube Shorts Search")
        self.geometry("600x400")
        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        ttk.Label(frame, text="검색어:").grid(row=0, column=0, sticky=tk.W)
        self.query_var = tk.StringVar()
        query_entry = ttk.Entry(frame, textvariable=self.query_var)
        query_entry.grid(row=0, column=1, sticky=tk.EW)
        frame.columnconfigure(1, weight=1)

        search_button = ttk.Button(frame, text="검색", command=self.on_search)
        search_button.grid(row=0, column=2, padx=5)

        self.tree = ttk.Treeview(frame, columns=("title", "duration", "category", "channel"), show="headings")
        self.tree.heading("title", text="주제")
        self.tree.heading("duration", text="시간")
        self.tree.heading("category", text="대분류")
        self.tree.heading("channel", text="소분류")
        self.tree.grid(row=1, column=0, columnspan=3, sticky=tk.NSEW, pady=10)
        frame.rowconfigure(1, weight=1)

    def on_search(self):
        query = self.query_var.get().strip()
        if not query:
            messagebox.showwarning("경고", "검색어를 입력하세요")
            return
        self.tree.delete(*self.tree.get_children())
        results = self.searcher.search(query)
        for item in results:
            self.tree.insert('', tk.END, values=(item['title'], item['duration'], item['category'], item['channel']))

if __name__ == "__main__":
    API_KEY = "YOUR_API_KEY"  # Replace with your YouTube Data API key
    searcher = YouTubeSearcher(API_KEY)
    app = App(searcher)
    app.mainloop()
