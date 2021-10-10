from pymongo.collection import Collection
from config import client


class ChannelsDB:
    def __init__(self):
        self.channel_col = Collection(client['AnimeGallery'], 'channelsdata')
        
    def find(self, data):
        return self.channel_col.find_one(data)
    
    def full(self):
        return list(self.channel_col.find())

    def add(self, data):
        try:
            self.channel_col.insert_one(data)
        except:
            pass

    def remove(self, data):
        self.channel_col.delete_one(data)
