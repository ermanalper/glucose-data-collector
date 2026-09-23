# 🩸 Glucose Data Collector

*Türkçe versiyonu için aşağı kaydırın*

A **self-hosted** Python backend service that centrally manages glucose (blood sugar) data received via Dexcom Share, Nightscout, or directly through a push webhook.

## 🛡️ Why Self-Hosted?
The project connects directly with Nightscout and Dexcom Share. Since the passwords obtained from the user are used directly within the backend to connect to these services, being unable to hash the passwords poses a significant security risk. For this reason, the project was designed to be completely self-hosted, allowing everyone to ensure their own security on their own servers.

## ✨ Features and Architecture
The system has different client types to fetch glucose data. The client to be used is selected via the `get_glucose_provider()` function inside `dependencies`.

*   **Pull Clients (Dexcom Share & Nightscout):** Fetches data periodically using a timer. The timer can be adjusted in `scheduler.py` (or tested using the `IS_DEVELOPMENT` boolean in `config.py`). 
    *   *Important Note:* When using Dexcom, you must enter your actual "Publisher" account, not your "Follow" account.
*   **Push Client:** Listens to a webhook endpoint. When a new glucose value arrives, it logs it into the system.
*   **Dexcom-Go-Worker:** If your Dexcom username appears as a *phone number*, standard Pull Clients will likely not work. In this case, you can use the `dexcom-go-worker` service. As long as this service is configured and running, it pulls data from Dexcom and forwards it to the Push Client. (Make sure you select the Push Client in the backend `dependencies` settings when using this method).
*   **Simulation Client:** A pull-based test client that you can use during the development process. It provides a fake/new glucose value to the system with every timer tick.

## 🔔 Alarms and Tracking (SSE, Insulin, Meal)
*   **SSE Alarms:** As new glucose values are generated, they are evaluated within the `glucose.py` model to determine if they are "normal", "warning", or "critical". Then, alarms are sent to frontends listening to the SSE (Server-Sent Events) tunnel from the `/api/v1/events/stream` endpoint in `alarm_service.py`.
*   **Meal and Insulin:** There are specific endpoints available to track the meals consumed and insulin doses administered by the patient.

## 📱 Frontend Examples
You can find a few frontend examples working integrated with this backend on my profile:
*   **ESP32 Buzzer:** Physical hardware that beeps with a specific melody when an alarm is received.
*   **Android Mobile Application:** An interface where you can monitor the glucose graph, compare it with other days, add meals/insulin, and run test protocols for other frontends in the SSE tunnel (e.g., the ESP32 buzzer hardware). You can also integrate your own frontends or test protocols into the system.

## 🚀 Installation and Setup

1. **Pull the Project:** 
   Download the project to your computer or server via Git (pull/clone).
2. **Configuration:** 
   Complete your `.env` and `docker-compose.yml` configurations in the root directory (You can copy the generated `.env.example` file and fill it in).
3. **Client Selection:** 
   Go to the `dependencies` folder in the backend source code and select the client type you will use.
4. **Timer Setup:** 
   If you are going to use a pull client, adjust the timer in `scheduler.py` (You can also tweak this timer using the `IS_DEVELOPMENT` boolean in the `config.py` file).
5. **Launch:** 
   Decide where you will host the project and spin up the services using Docker Compose.
6. **Security (Recommendation):** 
   If you are going to expose the server to the internet, it will be highly beneficial to protect the backend by using the NPM (Nginx Proxy Manager) service in your Docker Compose configuration instead of exposing it directly.

## ⚠️ Disclaimer and Important Warnings

*   **No Medical Validity:** This project is NOT a professional medical device or software with medical validity. It is for personal tracking and hobby purposes only. It cannot be used in treatment processes or critical life decisions. *Use it at your own risk.*
*   **Rate Limiting / Ban Risk:** Sending requests to services like Dexcom Share, Nightscout, or similar platforms too frequently (at short intervals) can result in you being temporarily or permanently blocked (banned) from those platforms and losing access to your glucose data for a while. Be sure to take this into account when setting your timer.

---
---

# 🩸 Glucose Data Collector (Türkçe)

Dexcom Share, Nightscout veya doğrudan push webhook üzerinden aldığı glukoz (kan şekeri) verilerini merkezi olarak yöneten **self-hosted** bir Python backend servisidir.

## 🛡️ Neden Self-Hosted?
Proje, Nightscout ve Dexcom Share ile doğrudan bağlantı kurar. Kullanıcıdan alınan şifreler, backend içinde doğrudan bu servislere bağlanmak için kullanıldığından şifreleri hashleyememek büyük bir güvenlik sorununa sebep olur. Bu yüzden proje tamamen self-hosted olarak tasarlandı; böylece herkes kendi sunucusunda kendi güvenliğini sağlayabilir.

## ✨ Özellikler ve Mimari
Sistem, glukoz verilerini almak için farklı istemci (client) türlerine sahiptir. Kullanılacak client, `dependencies` içindeki `get_glucose_provider()` fonksiyonundan seçilir.

*   **Pull Clients (Dexcom Share & Nightscout):** Bir timer ile periyodik olarak veri çeker. `scheduler.py` içinden timer ayarlanabilir (veya `config.py` içindeki `IS_DEVELOPMENT` boolean değeri ile test yapılabilir). 
    *   *Önemli Not:* Dexcom kullanırken "Follow" hesabınızı değil, asıl "Publisher" hesabınızı girmelisiniz.
*   **Push Client:** Bir webhook endpoint'ini dinler. Yeni bir glukoz değeri geldiğinde sisteme girişini yapar.
*   **Dexcom-Go-Worker:** Eğer Dexcom kullanıcı adınız bir *telefon numarası* olarak gözüküyorsa standart Pull Client'lar muhtemelen çalışmayacaktır. Bu durumda `dexcom-go-worker` servisini kullanabilirsiniz. Bu servis yapılandırıldığı sürece Dexcom'dan veriyi çeker ve Push Client'a atar. (Bu yöntemi kullanırken backend `dependencies` ayarlarında Push Client seçtiğinizden emin olun).
*   **Simulation Client:** Geliştirme sürecinde kullanabileceğiniz, her timer tick'i ile sisteme sahte/yeni bir glukoz değeri veren pull tabanlı bir test istemcisidir.

## 🔔 Alarmlar ve Takip (SSE, İnsülin, Öğün)
*   **SSE Alarmları:** Yeni glukoz değerleri oluştukça `glucose.py` modeli içinde bu değerlerin "normal", "warning" veya "critical" olduğu belirlenir. Ardından `alarm_service.py` içinde `/api/v1/events/stream` endpoint'inden SSE (Server-Sent Events) tünelini dinleyen frontend'lere alarmlar gönderilir.
*   **Öğün ve İnsülin:** Hasta tarafından tüketilen öğünlerin (meal) ve uygulanan insülin dozlarının takibini yapabileceğiniz özel endpointler mevcuttur.

## 📱 Frontend Örnekleri
Profilimde bu backend ile entegre çalışan birkaç frontend örneği bulabilirsiniz:
*   **ESP32 Buzzer:** Alarm geldiğinde belirli bir melodide öten fiziksel donanım.
*   **Android Mobil Uygulaması:** Glukoz grafiğini izleyebildiğiniz, başka günlerle karşılaştırma yapabildiğiniz, öğün/insülin ekleyebildiğiniz ve SSE tünelindeki diğer frontendlerin (örneğin ESP32 buzzer donanımı) test protokollerini çalıştırabileceğiniz bir arayüz. Kendi frontendlerinizi veya test protokollerinizi de sisteme dahil edebilirsiniz.

## 🚀 Kurulum ve Ayağa Kaldırma

1. **Projeyi Çekin:** 
   Projeyi Git üzerinden (pull/clone) bilgisayarınıza veya sunucunuza indirin.
2. **Yapılandırma:** 
   Kök dizindeki `.env` ve `docker-compose.yml` yapılandırmalarınızı tamamlayın (Oluşturulan `.env.example` dosyasını kopyalayıp içini doldurabilirsiniz).
3. **Client Seçimi:** 
   Backend kaynak kodunda `dependencies` klasörüne gidip kullanacağınız client türünü seçin.
4. **Timer Ayarı:** 
   Pull client kullanacaksanız `scheduler.py` içinden timer'ı ayarlayın (`config.py` dosyasındaki `IS_DEVELOPMENT` boolean'ı ile de bu timer üzerinde oynamalar yapabilirsiniz).
5. **Başlatma:** 
   Projeyi nerede kaldıracağınıza karar verdikten sonra Docker Compose ile servisleri ayağa kaldırın.
6. **Güvenlik (Öneri):** 
   Eğer sunucuyu internete açacaksanız, backend'i doğrudan açmak yerine Docker Compose yapılandırmanızdaki NPM (Nginx Proxy Manager) servisini kullanarak korumanız oldukça yararlı olacaktır.

## ⚠️ Sorumluluk Reddi (Disclaimer) ve Önemli Uyarılar

*   **Tıbbi Geçerlilik Yoktur:** Bu proje, tıbbi geçerliliği olan profesyonel bir tıbbi cihaz veya yazılım DEĞİLDİR. Sadece kişisel takip ve hobi amaçlıdır. Tedavi süreçlerinde veya hayati kararlarda kullanılamaz. *Use it at your own risk.*
*   **Rate Limiting / Ban Riski:** Dexcom Share, Nightscout veya benzeri platformlara çok sık (kısa aralıklarla) istek atmak, o platformlardan geçici veya kalıcı olarak engellenmenize (ban yemenize) ve glukoz verinize bir süre erişememenize neden olabilir. Timer ayarlarınızı yaparken bu durumu mutlaka göz önünde bulundurun.