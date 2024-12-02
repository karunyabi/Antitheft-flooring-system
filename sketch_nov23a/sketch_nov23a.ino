#define PIEZO_PIN 34

void setup() {
  Serial.begin(115200);
  pinMode(PIEZO_PIN, INPUT);
}

void loop() {
  int knockValue = analogRead(PIEZO_PIN);
  if (knockValue > 1000) {  // Adjust threshold
    Serial.println("TRIGGER");
    delay(500);  // Prevent multiple triggers
  }
}
