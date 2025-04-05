#include "esp_camera.h"
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

#define CAMERA_MODEL_AI_THINKER
#include "camera_pins.h"

// Configurações de rede
//CONFIG HERE
const char* ssid = "ESP32LAN";
const char* password = "abcdefgh";
const char* ipv4 = "192.168.212.154";
const int timeDelay = 500;
//CONFIG HERE END

String serverUrl = "http://" + String(ipv4) + ":8000/process-image/";

void setup() {
  Serial.begin(115200);
  Serial.setDebugOutput(true);
  Serial.println();

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

  if (config.pixel_format == PIXFORMAT_JPEG && psramFound()) {
    config.jpeg_quality = 10;
    config.fb_count = 2;
  } else {
    config.frame_size = FRAMESIZE_VGA;
    config.fb_location = CAMERA_FB_IN_DRAM;
  }

  sensor_t *s = esp_camera_sensor_get();
  if (s) {
      s->set_brightness(s, -2);  // Brilho (-2 a 2, padrão 0)
      s->set_contrast(s, -2);    // Contraste (-2 a 2, padrão 0)
      s->set_saturation(s, -2);  // Saturação (-2 a 2, padrão 0)
      s->set_special_effect(s, 2);
  }


  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x", err);
    return;
  }

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected");
}

void sendImageToServer() {
  camera_fb_t * fb = esp_camera_fb_get();
  if (!fb) {
    Serial.println("Falha ao capturar imagem");
    return;
  }

  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    WiFiClient client;

    http.begin(client, serverUrl);
    http.addHeader("Content-Type", "image/jpeg");

    int httpResponseCode = http.POST(fb->buf, fb->len);
    esp_camera_fb_return(fb);
    Serial.print("Código de resposta HTTP: ");
    Serial.println(httpResponseCode);

    if (httpResponseCode > 0) {
        String response = http.getString();
        Serial.println("Resposta do servidor:");
        Serial.println(response);

        // Criar buffer JSON
        StaticJsonDocument<200> doc;
        DeserializationError error = deserializeJson(doc, response);

        if (!error) {
            float max_val = doc["max_val"];
            int maxInt = static_cast<int>(max_val);
            
            Serial.print("Valor extraído: ");
            Serial.println(maxInt);
            if(maxInt >= 200) {
              //Vibrar motor
            }
        } else {
            Serial.println("Erro ao interpretar JSON");
        }
    } else {
        Serial.println("Erro na requisição");
    }
    
    http.end();
  } else {
    Serial.println("Wi-Fi não conectado");
  }
}

void loop() {
  sendImageToServer();
  delay(timeDelay);
}
