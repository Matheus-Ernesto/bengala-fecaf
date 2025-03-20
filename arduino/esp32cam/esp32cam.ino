#include "esp_camera.h"
#include <WiFi.h>
#include <HTTPClient.h>

#define CAMERA_MODEL_AI_THINKER  // Altere para o modelo correto, se necessário
#include "camera_pins.h"

const char* ssid = "CASA-2.4G"; // Coloque seu SSID
const char* password = "25122003"; // Coloque sua senh
//const char* serverUrl = "http://192.168.10.3:8000/process-image/"; // Endereço do FastAPI
const char* serverUrl = "192.168.10.3"; // Endereço do FastAPI
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
  config.frame_size = FRAMESIZE_128X128;  // Reduz para 640x480 (menor tamanho de arquivo)
  config.jpeg_quality = 12; // Aumenta a compressão, reduzindo qualidade e tamanho do arquivo
  config.fb_count = 1;

  if (config.pixel_format == PIXFORMAT_JPEG && psramFound()) {
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
    WiFiClient client;
    if (client.connect(serverUrl, 8000)) {  // Altere para HTTPS se necessário
      Serial.println("Enviando foto...");
      
      // Monta a requisição HTTP manualmente
      client.print("POST /process-image/ HTTP/1.1\r\n");
      client.print("Host: " + String(serverUrl) + "\r\n");
      client.print("Content-Type: image/jpeg\r\n");
      client.print("Content-Length: " + String(fb->len) + "\r\n");
      client.print("Connection: close\r\n\r\n");

      // Envia os dados da imagem
      client.write(fb->buf, fb->len);

      // Fecha a conexão imediatamente (sem esperar resposta)
      client.stop();
      Serial.println("Foto enviada!");
    } else {
      Serial.println("Falha ao conectar ao servidor");
    }
  } else {
    Serial.println("Wi-Fi não conectado");
  }

  esp_camera_fb_return(fb);
}

void loop() {
  sendImageToServer(); // Envia a imagem ao servidor Flask
  delay(17); // Ajuste o intervalo conforme necessário

}
