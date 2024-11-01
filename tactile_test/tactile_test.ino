void setup() {
    Serial.begin(9600); // シリアル通信を9600bpsで開始
}

void loop() {
    int valueA0 = analogRead(A0); // A0ポートの値を取得
    int valueA1 = analogRead(A1); // A1ポートの値を取得
    int valueA2 = analogRead(A2);
    int valueA3 = analogRead(A3);
    int valueA4 = analogRead(A4);
    int valueA5 = analogRead(A5);
    int valueA6 = analogRead(A6);
    int valueA7 = analogRead(A7);
    // 値をシリアルポートに送信
    Serial.print(valueA0);
    Serial.print(",");
    Serial.print(valueA1);
    Serial.print(",");
    Serial.print(valueA2);
    Serial.print(",");
    Serial.print(valueA3);
    Serial.print(",");
    Serial.print(valueA4);
    Serial.print(",");
    Serial.print(valueA5);
    Serial.print(",");
    Serial.print(valueA6);
    Serial.print(",");
    Serial.println(valueA7);
    
    delay(200); // 0.2秒待つ
}
