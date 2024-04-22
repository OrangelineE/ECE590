const mqtt = require('mqtt');
const client = mqtt.connect('mqtt://broker.emqx.io:1883');
const topic = 'ECE590_Final_Project_G2/S1/';
const message = 'Hello MQTT';

client.on('connect', () => {
  console.log(`Connected to broker`);
  client.publish(topic, message, { qos: 1 }, (error) => {
    if (error) {
      console.error(`Publish error: ${error}`);
    } else {
      console.log(`Message sent to topic ${topic}: ${message}`);
    }
    client.end(); // Close the connection
  });
});

client.on('error', (error) => {
  console.error(`Connection error: ${error}`);
  client.end();
});
