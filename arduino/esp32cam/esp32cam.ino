#include "esp_camera.h"
#include <WiFi.h>
#include <HTTPClient.h>

#define CAMERA_MODEL_AI_THINKER  // Altere para o modelo correto, se necessário
#include "camera_pins.h"

// Configurações de rede
const char* ssid = "ESP32LAN"; // Coloque seu SSID
const char* password = "abcdefgh"; // Coloque sua senh
const char* serverUrl = "http:/192.168.56.1/api/sendPhotos.php"; // URL do servidor Flask

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
  config.frame_size = FRAMESIZE_SVGA;  // Reduz para 640x480 (menor tamanho de arquivo)
  config.jpeg_quality = 12; // Aumenta a compressão, reduzindo qualidade e tamanho do arquivo
  config.fb_count = 1;

  if (config.pixel_format == PIXFORMAT_JPEG && psramFound()) {
    config.jpeg_quality = 10;
    config.fb_count = 2;
  } else {
    config.frame_size = FRAMESIZE_VGA;  // Reduz para 640x480 (menor tamanho de arquivo)
    config.fb_location = CAMERA_FB_IN_DRAM;
  }

  sensor_t *s = esp_camera_sensor_get();
  if (s) {
      s->set_brightness(s, 1);  // Brilho (-2 a 2, padrão 0)
      s->set_contrast(s, 2);    // Contraste (-2 a 2, padrão 0)
      s->set_saturation(s, 2);  // Saturação (-2 a 2, padrão 0)
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
    http.begin(serverUrl);
    http.addHeader("Content-Type", "image/jpeg");

    int httpResponseCode = http.POST(fb->buf, fb->len);
    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println("Resposta do servidor:");
      Serial.println(response);
    } else {
      Serial.print("Erro na requisição: ");
      Serial.println(httpResponseCode);
    }
    http.end();
  } else {
    Serial.println("Wi-Fi não conectado");
  }

  esp_camera_fb_return(fb);
}

void loop() {
  sendImageToServer(); // Envia a imagem ao servidor Flask
  delay(500); // Ajuste o intervalo conforme necessário
}
