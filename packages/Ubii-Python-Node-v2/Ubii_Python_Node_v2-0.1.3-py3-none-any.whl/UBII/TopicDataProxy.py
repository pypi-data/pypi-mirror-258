from typing import Callable

from proto.topicData.topicDataRecord_pb2 import TopicDataRecord

from typing import List

from UBII.TopicDataBuffer import TopicDataBuffer, SubscriptionToken, SubscriptionTokenTYPE
from UBII.UbiiNetworkClient import UbiiNetworkClient


class TopicDataProxy:
    def __init__(self, topicDataBuffer: TopicDataBuffer, networkClient: UbiiNetworkClient, node):
        self.topicDataBuffer: TopicDataBuffer = topicDataBuffer
        self.networkClient = networkClient
        self.node = node

    def subscribeTopic(self, topic: str, callback: Callable[[TopicDataRecord], None]) -> SubscriptionToken:
        subscriptions = self.getTopicSubscriptionTokens(topic)
        if subscriptions is None or not subscriptions:
            self.networkClient.subscribeTopic(topic, self.onTopicDataRecord)

        return self.topicDataBuffer.subscribeTopic(topic, callback)

    def subscribeRegex(self, regex: str, callback: Callable[[TopicDataRecord], None]) -> SubscriptionToken:
        subscriptions = self.getRegexSubscriptionTokens(regex)
        if subscriptions is None or not subscriptions:
            self.networkClient.subscribeRegex(regex, self.onTopicDataRecord)

        return self.topicDataBuffer.subscribeRegex(regex, callback)

    def unsubscribe(self, token: SubscriptionToken) -> bool:
        bufferUnsubscribe = self.topicDataBuffer.unsubscribe(token)
        if bufferUnsubscribe:
            if token.type == SubscriptionTokenTYPE.TOPIC:
                subList = self.getTopicSubscriptionTokens(token.topic)
                if (subList is None) or (not subList):
                    self.networkClient.unsubscribe(token.topic, self.onTopicDataRecord)

            elif token.type == SubscriptionTokenTYPE.REGEX:
                subList = self.getRegexSubscriptionTokens(token.topic)
                if (subList is None) or (not subList):
                    self.networkClient.unsubscribeRegex(token.topic, self.onTopicDataRecord)

            return True

        return False

    def remove(self, topic: str):
        self.topicDataBuffer.remove(topic)

    def pull(self, topic: str) -> TopicDataRecord:
        return self.topicDataBuffer.pull(topic)

    def getTopicSubscriptionTokens(self, topic: str) -> List[SubscriptionToken]:
        return self.topicDataBuffer.getTopicSubscriptionTokens(topic)

    def getRegexSubscriptionTokens(self, regex: str) -> List[SubscriptionToken]:
        return self.topicDataBuffer.getRegexSubscriptionTokens(regex)

    def onTopicDataRecord(self, record: TopicDataRecord):
        self.topicDataBuffer.publish(record)

    def setPublishFrequency(self, frequency):
        self.networkClient.setPublishFrequency(frequency)

    def stopNode(self):
        self.networkClient.stopNode()
