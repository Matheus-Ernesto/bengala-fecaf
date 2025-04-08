#include "esp_camera.h"
#include <WiFi.h>
#include <WebSocketsClient.h>
#include <ArduinoJson.h>

#define CAMERA_MODEL_AI_THINKER
#include "camera_pins.h"

const char* ssid = "CASA-2.4G";
const char* password = "25122003";
const char* host = "192.168.10.4";
const uint16_t port = 8000;
const char* wsPath = "/ws";
const int timeDelay = 1000;

WebSocketsClient webSocket;

void setupWiFi() {
  WiFi.begin(ssid, password);
  Serial.print("Conectando ao WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi conectado");
}

void setupCamera() {
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sccb_sda = SIOD_GPIO_NUM;
  config.pin_sccb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;
  config.frame_size = FRAMESIZE_VGA;
  config.jpeg_quality = 12;
  config.fb_count = 1;
  config.fb_location = CAMERA_FB_IN_PSRAM;

  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Erro ao inicializar câmera: 0x%x", err);
    while (true) delay(100);
  }

  sensor_t *s = esp_camera_sensor_get();
  s->set_brightness(s, -2);
  s->set_contrast(s, -2);
  s->set_saturation(s, -2);
  s->set_special_effect(s, 2);
}

void webSocketEvent(WStype_t type, uint8_t* payload, size_t length) {
  switch (type) {
    case WStype_CONNECTED:
      Serial.println("[WS] Conectado ao servidor WebSocket");
      break;
    case WStype_DISCONNECTED:
      Serial.println("[WS] Desconectado do WebSocket");
      break;
    case WStype_TEXT:
      Serial.println("[WS] Mensagem recebida: " + String((char*)payload));
      break;
    case WStype_BIN:
      Serial.println("[WS] Binário recebido (não tratado)");
      break;
    default:
      break;
  }
}

void setupWebSocket() {
  webSocket.begin(host, port, wsPath);
  webSocket.onEvent(webSocketEvent);
  webSocket.setReconnectInterval(5000);
}

void setup() {
  Serial.begin(115200);
  Serial.setDebugOutput(true);
  Serial.println();

  setupWiFi();
  setupCamera();
  setupWebSocket();
}

void loop() {
  webSocket.loop();

  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("[ERRO] Wi-Fi desconectado, tentando reconectar...");
    setupWiFi();
    return;
  }

  if (!webSocket.isConnected()) {
    Serial.println("[ERRO] WebSocket desconectado, aguardando reconexão...");
    delay(1000);
    return;
  }

  camera_fb_t *fb = esp_camera_fb_get();
  if (!fb) {
    Serial.println("[ERRO] Falha ao capturar imagem");
    return;
  }

  Serial.println("[INFO] Enviando imagem via WebSocket...");
  webSocket.sendBIN(fb->buf, fb->len);
  esp_camera_fb_return(fb);

  delay(timeDelay);
}