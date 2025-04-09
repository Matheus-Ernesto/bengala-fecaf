#include "esp_camera.h"
#include <WiFi.h>
#include <ArduinoWebsockets.h>

using namespace websockets;

// Configurações de rede
// MODIFICAR ESTA PARTE PARA SUA REDE

// NOMDE DO SEU WIFI
const char* ssid = "CASA-2.4G";
// SUA SENHA DE WIFI
const char* password = "25122003";
// SEU IP, ONDE O SERVIDOR ESTA ABERTO
const char* websockets_server_host = "192.168.10.4";
// PORTA ESCOLHIDA PARA ABRIR O SERVIDOR
const uint16_t websockets_server_port = 8765;

// FIM Configurações de rede

WebsocketsClient client;

// Configurações
void setup() {
  // Iniciar transmissão de logs com o computador (se conectado por cabo USB)
  Serial.begin(115200);
  Serial.setDebugOutput(true);
  Serial.println();

  // Configuração da câmera
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = 5;
  config.pin_d1 = 18;
  config.pin_d2 = 19;
  config.pin_d3 = 21;
  config.pin_d4 = 36;
  config.pin_d5 = 39;
  config.pin_d6 = 34;
  config.pin_d7 = 35;
  config.pin_xclk = 0;
  config.pin_pclk = 22;
  config.pin_vsync = 25;
  config.pin_href = 23;
  config.pin_sccb_sda = 26;
  config.pin_sccb_scl = 27;
  config.pin_pwdn = 32;
  config.pin_reset = -1;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;
  config.fb_count = 1;
  // Modificar o campo abaixo para alterar a resolução de imagem 
  config.frame_size = FRAMESIZE_VGA;
  // Modificar a qualidade de foto - 0 = 100%; 31 = 50%; 63 = 0% (a imagem fica bem borrada no 63, recomendado 12)
  config.jpeg_quality = 12;

  // Inicialização do sensor e ajustes de imagem
  sensor_t *s = esp_camera_sensor_get();
  if (s) {
    s->set_brightness(s, 1);   // Brilho (-2 a 2)
    s->set_contrast(s, 2);     // Contraste (-2 a 2)
    s->set_saturation(s, 2);   // Saturação (-2 a 2)
  }

  // Inicializar câmera
  if (esp_camera_init(&config) != ESP_OK) {
    Serial.println("Falha na inicialização da câmera");
    return;
  }

  // Conectar ao Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi conectado");

  // Conectar ao servidor WebSocket
  if (client.connect(websockets_server_host, websockets_server_port, "/")) {
    Serial.println("Conectado ao servidor WebSocket");
  } else {
    Serial.println("Falha na conexão WebSocket");
  }

  // Callback para mensagens recebidas
  client.onMessage([](WebsocketsMessage message) {
    Serial.print("Resposta: ");
    Serial.println(message.data());
  });
}

// Repete infinitamente
void loop() {
  if (client.available()) {
    client.poll();
    // Tira e envia a foto ao servidor se disponível a conexão.
    camera_fb_t *fb = esp_camera_fb_get();
    if (!fb) {
      Serial.println("Falha ao capturar imagem");
      return;
    }
    Serial.println("Foto enviada");
    client.sendBinary((const char*)fb->buf, fb->len);
    // Limpa o buffer, removendo a foto da memória
    esp_camera_fb_return(fb);
  }
  // Essa parte pode ser reduzida de acordo com a velocidade do seu servidor e conexão.
  delay(500);
}