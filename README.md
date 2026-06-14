# solidworks-auto-launcher

# YTU SolidWorks Auto-Launcher 🚀

Yıldız Technical University (YTU) öğrencileri için geliştirilmiş, GlobalProtect VPN bağlantısını ve SolidWorks başlatma sürecini tamamen otomatikleştiren, hata toleranslı (fault-tolerant) bir Python otomasyon aracıdır.

## 📌 Proje Amacı
SolidWorks kullanmak için her seferinde manuel olarak VPN açmak, şifre girmek, arayüzü beklemek ve programı başlatmak ciddi bir zaman kaybıdır. Bu proje, tüm bu süreci tek bir `.exe` dosyasına çift tıklayarak arka planda sessizce çözer. İşlem bitip SolidWorks kapatıldığında ise VPN bağlantısını otomatik olarak keser.

## ⚙️ Teknik Özellikler ve "Edge-Case" Çözümleri

Bu yazılım basit bir makro kaydedici değildir; içerisinde birçok çevresel değişkene karşı güvenlik ağları barındırır:

* **Dinamik Görüntü Ölçeklendirme (Universal Scaling):** Monitör çözünürlüğünüz veya Windows Ekran Ölçeklendirme (Display Scaling) oranınız (%100, %125, %150 vb.) ne olursa olsun, görüntü işleme (OpenCV/PIL) algoritmaları referans resimleri anlık olarak yeniden boyutlandırarak hedefini her ekranda bulur.
* **Hayalet Tıklama (Phantom Click & Hardware Block):** Otomasyon çalışırken kullanıcı faresini hareket ettirse bile sistem çökmez. `ctypes` kullanılarak donanımsal girişler (klavye/mouse) tıklama anında milisaniyelik olarak kilitlenir (`BlockInput`), hedef vurulur ve imleç kullanıcının bıraktığı yere iade edilir.
* **Akıllı Kaydırma (Smart Scrolling):** Düşük çözünürlüklü (ör: 800x600) ekranlarda "Disconnect" butonunun arayüzün altında (kaydırma çubuğunda) kalma ihtimaline karşı otomatik `Page Down` algoritması içerir.
* **Vur-Kaç Bağlantı Kesme (Hit & Run Disconnect):** Bildirim engellerine takılmamak için başarısız denemelerde arayüzü `ESC` ile temizler ve inatçı bir döngü ile hedefine ulaşana kadar tekrar dener.
* **UAC Otomasyonu:** Program çalıştırıldığı an Yönetici izinlerini otomatik olarak talep eder, kullanıcıyı ekstra ayar yapmaktan kurtarır.

## 🛠️ Kurulum ve Kullanım

1. `Releases` sekmesinden en güncel **SW_Baslatici.exe** dosyasını indirin.
2. Dosyayı masaüstünüze veya dilediğiniz bir klasöre koyun.
3. Çift tıklayarak çalıştırın. (Gerekli donanım kilitlerinin çalışması için Yönetici iznine "Evet" deyin).
4. Arkanıza yaslanın; program VPN'i bağlayacak ve SolidWorks'ü açacaktır. SolidWorks'ü kapattığınızda ise bağlantı kendi kendine kesilecektir.

## 💻 Geliştiriciler İçin
Eğer kodu kendi ortamınızda derlemek isterseniz:
1. Repoyu klonlayın.
2. Gerekli kütüphaneleri kurun: `pip install pyautogui pillow opencv-python pyinstaller`
3. Kodu `.exe` formatına dönüştürmek için terminale şu komutu yazın:
   `pyinstaller --onefile --noconsole --uac-admin --icon=sw_simgesi.ico SW_Baslatici.py`
