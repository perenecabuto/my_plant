#define ON HIGH
#define OFF LOW
#define WATER_PUMP 6
#define MOISTER_PIN A1

int sensorValue = 0;
int dryLimit = 600;
boolean autoIrrigationStarted = false;

uint32_t irrigationInterval = 5000UL;
uint32_t currMillis = 0;
uint32_t irrigateMillis = 0;
uint8_t pumpStatus = OFF;

void setup() {
  Serial.begin(9600);
  pinMode(WATER_PUMP, OUTPUT);
}

void loop() {
  sensorValue = 1023 - analogRead(MOISTER_PIN);
  currMillis = millis();

  printStatus();

  if (isToStartAutoIrrigation()) {
    irrigateMillis = currMillis;
    autoIrrigationStarted = true;
    startIrrigation();
  }

  if (isToStartManualIrrigation()) {
    irrigateMillis = currMillis;
    autoIrrigationStarted = false;
    startIrrigation();
  }

  if (autoIrrigationStarted && !isDry()) {
      stopIrrigation();
  }

  if (irrigationFinished()) {
    irrigateMillis = currMillis;
    stopIrrigation();
  }

  delay(100);
}

void printStatus() {
  Serial.print(sensorValue);
  Serial.print(',');
  Serial.println(pumpStatus == ON ? "WORKING" : "IDLE");
}

char getMessage() {
  if (Serial.available())
    return Serial.read();

  return NULL;
}

void startIrrigation() {
  if (pumpStatus == ON) return;

  digitalWrite(WATER_PUMP, ON);
  pumpStatus = ON;
}

void stopIrrigation() {
  if (pumpStatus == OFF) return;

  digitalWrite(WATER_PUMP, OFF);
  pumpStatus = OFF;
}

boolean irrigationFinished() {
 return pumpStatus == ON && cycleIntervalFinished();
}

boolean isDry() {
 return sensorValue <= dryLimit;
}

boolean isToAutoIrrigate() {
 return isDry() && cycleIntervalFinished();
}

boolean isToStartAutoIrrigation() {
  return pumpStatus == OFF && isToAutoIrrigate();
}

boolean isToStartManualIrrigation() {
 return getMessage() == 'i';
}

boolean cycleIntervalFinished() {
  return currMillis - irrigateMillis >= irrigationInterval;
}
