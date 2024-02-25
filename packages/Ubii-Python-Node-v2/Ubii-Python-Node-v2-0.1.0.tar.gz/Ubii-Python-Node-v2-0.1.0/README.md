# Python client node v.2 for UBII
This is the package for thepython client node v2 for the UBII framework https://github.com/SandroWeber/ubii-node-python-v2

## Requirements and installation

- Tested for:
  - Linux and Windows
  - Python >= 3.7


## How to use 
- Import the UbiiClientNode module and instanciate the client node 
    ```python
  from UBII.ubii_client_node import UbiiClientNode
  
  node = UbiiClientNode('pythonNodev2', 'http://localhost:8102/services/binary', 'ws://localhost:8104')
 
- Use the node to make service calls, subscribe to topics, publish topic data 
  ```python
  request = ServiceRequest()
  request.topic = '/services/topic_list'
  response = self.node.call_service(request)
  
  
  topicDataRecord = TopicDataRecord()
  topicDataRecord.topic = 'testTopic'
  node.publish(topicDataRecord)
   
  def printTopicDataRecord(record):
    print(record)
   
  node.subscribeTopic('testTopic', printTopicDataRecord)
  
  
  node.stopNode()
  ```
- For more information on the module check the documentation

## Bugs

- There is a problem in python 3.9 and 3.10 where starting threads while the interpreter shuts down can lead to a RuntimeError: 'cannot schedule new futures after interpreter shutdown'. If this occurs one quck fix is to add a time.sleep to the end of the main file.