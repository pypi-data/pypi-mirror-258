### Usage:
Once installed, import the module with: `import mc.mc_functions as mc`

### Module Functions:

- `publishMessage`: Used to publish messages to the Mosquitto Broker under a specified topic.  

- `subscribeToAll`: Used to subscribe to all communication topics under the Mosquitto Broker. Receives messages and saves them to a local directory named `messagingData` in JSON files according to the topic which the message was published under. (eg. `messagingData/navigation.json`). 

- `publishFile`: Publishes saved JSON to specified S3 bucket for secure storage and further analysis.

&ensp; Function Usage (note that all arguments should be passed as Strings):
&emsp; &emsp; &emsp;`publishMessage(messagingTopic, message, user, password, ec2ipv4Address)`

&emsp; &emsp; &emsp;`publishFile(topic, subTopic, bucketName, fileName)`

&emsp; &emsp; &emsp;`subscribeToAll(username, password, ec2ipv4Address)`
