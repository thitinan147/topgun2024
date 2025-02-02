import paho.mqtt.client as mqtt
import psycopg2
import json

conn = psycopg2.connect(
    dbname="your_dbname",
    user="your_username",
    password="your_password",
    host="your_host",
    port="your_port"
)
cur = conn.cursor()

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    client.subscribe("test/topic")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    data = json.loads(msg.payload.decode('utf-8'))
    for item in data:
        sound = item['sound']
        timestamp = item['timestamp']
        # บันทึกข้อมูลลงในฐานข้อมูล
        cur.execute("INSERT INTO mqtt_messages (sound, timestamp) VALUES (%s, %s)", (sound, timestamp))
    conn.commit()

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.connect("host.docker.internal", 1883, 60)

mqttc.loop_forever()

cur.close()
conn.close()