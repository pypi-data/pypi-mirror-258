import re
import threading
import time
from threading import Thread
from typing import Callable

import websockets
from proto.topicData.topicDataRecord_pb2 import TopicDataRecord, TopicDataRecordList
from websockets.sync.client import connect

from proto.topicData.topicData_pb2 import TopicData


class UbiiTopicDataClient:
    def __init__(self, endpoint, clientID, node):
        self.ws = connect(endpoint + '?clientID=' + clientID)
        self.endpoint = endpoint + '?clientID=' + clientID
        print("UbiiTopicDataClient.endpoint: ", self.endpoint)
        self.topicCallbacks: dict[str, list[Callable[[TopicDataRecord], None]]] = {}
        self.regexCallbacks: dict[str, list[Callable[[TopicDataRecord], None]]] = {}
        self.topicsToPublish = {}
        self.lockTopics = threading.Lock()
        self.lockRegex = threading.Lock()
        self.lockTopicsToPublish = threading.Lock()
        self.publishFrequency = 0.3
        self.running = True
        self.node = node

        t1 = Thread(target=self.__writeSocket, args=[])
        t1.daemon = True
        t1.start()
        t2 = Thread(target=self.__readSocket, args=[])
        t2.daemon = True
        t2.start()

    def publish(self, topicDataRecord: TopicDataRecord):
        with self.lockTopicsToPublish:
            self.topicsToPublish[topicDataRecord.topic] = topicDataRecord

    def __flush(self):
        try:
            while self.running:
                with self.lockTopicsToPublish:
                    records = list(self.topicsToPublish.values())
                    self.topicsToPublish.clear()
                if len(records) > 0:
                    topicDataToSend = TopicData()
                    topicDataList = TopicDataRecordList()
                    for rec in records:
                        topicDataList.elements.append(rec)

                    topicDataToSend.topic_data_record_list.CopyFrom(topicDataList)
                    msg = topicDataToSend.SerializeToString()
                    self.ws.send(msg)
                time.sleep(self.publishFrequency)

        except websockets.exceptions.WebSocketException as e:
            print('Error while publishing topicData to the masternode')
            print(e)
            self.node.events.onConnectionError(e)
        except Exception as e:
            self.node.events.onPublishError(e)
            print(e)

    def __writeSocket(self):
        self.__flush()

    def __readSocket(self):
        self.__recvMessage()

    def __recvMessage(self):
        try:
            with connect(self.endpoint) as socket:
                while self.running:
                    message = None
                    while True and self.running:
                        try:
                            message = socket.recv(2)
                            break
                        except TimeoutError:
                            if self.running:
                                print('timeout while recieving, trying again')

                    if message == "PING":
                        socket.send('PONG')
                    elif not message is None:
                        topicData = TopicData()
                        topicData.ParseFromString(message)

                        if topicData.HasField('topic_data_record'):
                            self.__invokeCallbacks(topicData.topic_data_record)

                        if topicData.HasField('topic_data_record_list'):
                            for record in topicData.topic_data_record_list.elements:
                                self.__invokeCallbacks(record)

                        if topicData.HasField('error'):
                            print('topicData receive error:')
                            print(topicData.error)



        except websockets.exceptions.WebSocketException as e:
            print('Error while receiving form the masternode')
            print(e)
            self.node.events.onConnectionError(e)

        except Exception as e:
            self.node.events.onReadError(e)
            print(e)

    def __sendData(self, data: str):
        try:
            self.ws.send(data)
        except websockets.exceptions.WebSocketException as e:
            print('Error sending topicdata to masternode')
            print(e)
            self.node.events.onConnectionError(e)

    async def sendTopicData(self, record: TopicData):
        msg = record.SerializeToString()
        self.__sendData(msg)

    def isSubscribed(self, topicRegex: str) -> bool:
        with self.lockTopics:
            isSub = topicRegex in self.topicCallbacks

        with self.lockRegex:
            return isSub or topicRegex in self.regexCallbacks

    def addTopicCallback(self, topic: str, callback: Callable[[TopicDataRecord], None]):
        with self.lockTopics:
            if not topic in self.topicCallbacks:
                self.topicCallbacks[topic] = []
            self.topicCallbacks[topic].append(callback)

    def addRegexCallback(self, regex: str, callback: Callable[[TopicDataRecord], None]):
        with self.lockRegex:
            if not regex in self.regexCallbacks:
                self.regexCallbacks[regex] = []
            self.regexCallbacks[regex].append(callback)

    def removeTopicCallback(self, topic: str, callback: Callable[[TopicDataRecord], None]):
        with self.lockTopics:
            if topic in self.topicCallbacks:
                listToRemoveFrom = self.topicCallbacks[topic]
                if not listToRemoveFrom is None:
                    if callback in listToRemoveFrom:
                        listToRemoveFrom.remove(callback)

    def removeRegexCallback(self, regex: str, callback: Callable[[TopicDataRecord], None]):
        with self.lockRegex:
            if regex in self.regexCallbacks:
                listToRemove = self.regexCallbacks[regex]
                if not listToRemove is None:
                    if callback in listToRemove:
                        listToRemove.remove(callback)

    def hasTopicDataCallbacks(self, topic: str) -> bool:
        if not self.isSubscribed(topic):
            return False
        with self.lockTopics:
            subs = self.topicCallbacks[topic]
            if (subs is None) or (not subs):
                return False
            return True

    def hasRegexCallbacks(self, regex: str):
        if not self.isSubscribed(regex):
            return False
        with self.lockRegex:
            subs = self.regexCallbacks[regex]
            if (subs is None) or (not subs):
                return False
            return True

    def stopNode(self):
        self.running = False
        self.ws.close()

    def removeTopicDataCallbacks(self, topic: str):
        with self.lockTopics:
            del self.topicCallbacks[topic]

    def removeAllRegexCallbacks(self, regex: str):
        with self.lockRegex:
            del self.regexCallbacks[regex]

    def __invokeCallbacks(self, record: TopicDataRecord):
        topic = record.topic
        with self.lockTopics:
            inTopics = topic in self.topicCallbacks
            if inTopics:
                for callback in self.topicCallbacks[topic]:
                    callback(record)

        with self.lockRegex:
            if not inTopics:
                for key, value in self.regexCallbacks.items():
                    if re.match(key, topic):
                        for callback in value:
                            callback(record)

    def setPublishFrequency(self, frequency):
        self.publishFrequency = frequency
