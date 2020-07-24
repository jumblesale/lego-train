#include <WiFi.h>
#include "PoweredUpHub.h"

const char* ssid     = "KabelBox-0C64";
const char* password = "19286188759601606190";

const char* host = "192.168.0.9";
const uint16_t port = 9876;

PoweredUpHub myHub;
PoweredUpHub::Port _port = PoweredUpHub::Port::A;

bool socketConnected = false;
WiFiClient client;

void setup()
{
    Serial.begin(115200);
    delay(10);

    Serial.println();
    Serial.println();
    Serial.print("Connecting to ");
    Serial.println(ssid);

    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }

    Serial.println("");
    Serial.println("WiFi connected");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());

    myHub.init();
}

void loop()
{
    if(false == socketConnected) {
        socketConnected = connect();
        if(false == socketConnected) {
          Serial.println("Connection failed");
          return;
        } else {
          Serial.println();
          Serial.println("Handhsake succeeded, waiting for commands");
        }
    }

    if (myHub.isConnecting()) {
      myHub.connectHub();
      if (myHub.isConnected()) {
        Serial.println("Connected to HUB");
        myHub.setLedColor(GREEN);
      } else {
        Serial.println("Failed to connect to HUB");
      }
    }

    parseMessage(readMessage());
    
    delay(10);
}

bool connect() {
    Serial.println();
    Serial.print("Not connected, attempting to connect to ");
    Serial.print(host);
    Serial.print(":");
    Serial.print(port);
    Serial.println();
    
    if (!client.connect(host, port)) {
        Serial.println("Connection failed");
        return false;
    }

    if(!performHandshake()) {
        return false;
    }

    return true;
}

bool performHandshake() {
    String line = readMessage();
    if(String("hello?") != line) {
      Serial.println();
        Serial.print("Expected \"hello?\" but received ");
        if (String("") == line) {
            Serial.print("nothing");
        } else {
            Serial.print(line);
        }
        Serial.println();
        Serial.println("Retrying...");
        return false;
    }
    sendMessage(String("hello"));
    return true;
}

String readMessage() {
    String line = client.readStringUntil('\r');
    if(line.length() > 0) {
        Serial.println("Received message: ");
        Serial.print(line);
        Serial.println("");
    }
    return line;
}

void sendMessage(String s) {
    Serial.println();
    Serial.print("Sending message: ");
    Serial.print(s);
    Serial.println();
    client.print(s);
}

void parseMessage(String message) {
    if (message.length() == 0) {
        return;
    }
    message.toUpperCase();
    if (String("YELLOW") == message) {
        myHub.setLedColor(YELLOW);
    } else if (String("RED") == message) {
        myHub.setLedColor(RED);
    } else if (String("BLUE") == message) {
        myHub.setLedColor(BLUE);
   } else if (String("GO") == message) {
        myHub.setMotorSpeed(_port, 15);
    } else if (String("STOP") == message) {
        myHub.stopMotor(_port);
    } else {
        Serial.println("no se");
    }
}
