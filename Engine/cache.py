from collections import defaultdict


class MessageCache:

    def __init__(self):

        self.channels = defaultdict(dict)

    def add(self, message):

        self.channels[message.channel.id][message.id] = message

    def remove(self, channel_id, message_id):

        self.channels[channel_id].pop(message_id, None)

    def get_channel(self, channel_id):

        return list(self.channels[channel_id].values())

    def clear(self):

        self.channels.clear()