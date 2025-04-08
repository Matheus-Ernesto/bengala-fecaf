#include "esp_camera.h"
#include <WiFi.h>
#include <ArduinoWebsockets.h>
#include "base64.h"  // esta vem com a IDE Arduino

using namespace websockets;

#define CAMERA_MODEL_AI_THINKER
#include "camera_pins.h"

const char* ssid = "CASA-2.4G";
const char* password = "25122003";
const char* ws_server = "ws://192.168.10.4:8765";  // IP do seu PC com Python rodando

WebsocketsClient client;

void setupWiFi() {
  WiFi.begin(ssid, password);
  Serial.print("Conectando ao WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi conectado!");
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
}

void mandarFoto() {
  camera_fb_t * fb = esp_camera_fb_get();
  if (!fb) {
    Serial.println("Falha ao capturar imagem");
    return;
  }

  String imageBase64 = base64::encode(fb->buf, fb->len);
  client.send(imageBase64);
  Serial.println("Imagem enviada via WebSocket");

  esp_camera_fb_return(fb);
}

void setup() {
  Serial.begin(115200);
  setupWiFi();
  setupCamera();

  client.onEvent([](WebsocketsEvent e, String data){
    if (e == WebsocketsEvent::ConnectionOpened) {
      Serial.println("Conectado ao servidor WebSocket!");
    } else if (e == WebsocketsEvent::ConnectionClosed) {
      Serial.println("Desconectado do WebSocket.");
    } else if (e == WebsocketsEvent::GotPing) {
      Serial.println("Ping recebido!");
    }
  });

  client.onMessage([](WebsocketsMessage message){
    Serial.print("Mensagem do servidor: ");
    Serial.println(message.data());
  });

  client.connect(ws_server);
}

void loop() {
  client.poll();  // necessário para manter a conexão viva

  static unsigned long lastSent = 0;
  if (millis() - lastSent > 5000) {
    mandarFoto();
    lastSent = millis();
  }
}

