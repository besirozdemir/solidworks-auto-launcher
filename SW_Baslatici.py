import subprocess
import time
import os
import pyautogui
import base64
import io
import traceback
import ctypes
from PIL import Image

pyautogui.FAILSAFE = False

# ==============================================================================
# BASE64 RESİM KODLARINI AŞAĞIDAKİ TIRNAKLARIN İÇİNE YAPIŞTIR
# ==============================================================================
CONNECT_RESIM_KODU = "iVBORw0KGgoAAAANSUhEUgAAANYAAAAfCAYAAACbBDNSAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAALESURBVHhe7drNThNRGMbx/3SPLWvLR0yskQVspS1udCGXUGJcsBNdS01wZSK9AcNKTEwYuAEFEgkSWrqWAAvQaKl7Adc4LuaMMzRDG2FO0uDzSyZpz9uembR9ct45qXNnwfMQkUSlWgdE5PIULBELFCwRCxQsEQsULBELFCwRCxQsEQsULBELFCxLnJhD/h+O/nmRPAeYLcHdSJqaezDxGU677NN2gC67pCtBK1bSMuCWIFWHogt5c3y6Dq/6u+sDzw2DOwIpLaeJ66bv+UqYKoCzB+UG/I6Mz72H6cjYeW1i8Phfa+3GW2t/607MmCRCrWCSMrA4Du+WYMU7v8VyMuCOw4D5Nde2YPq7H7pKCTbqMDMKjgNOE4pVv4VsV2ud012G1z/9a2itVbdgPQszZgX1zFjZXINcnlasJKWh/wS+dbhvqYxDdQUKpk08HYXKYPhlvOiDsSW/tpGF2YEONcefsxm0nx+gkIdbZkU6U3Nh7Rp8rcHLQ2jsQnERnilUiVKwEnQz3bmnyg1D8ResHYXhm9+FQl/43oUdCPqI9Sb0R+aNqwVzvm2YFeoINoF7GciN+LX5SBu6ug37bVZUuTwFK0EHx+D1wI1O+TqG/daxNOQ6ve8cHkAPvClBbcI/HqZhIG1eEHc+sUrBSlIDFk7gUcxOW/DUIwzRmaL58V9kFTk4Au8HjC2Gu5B517R3Xsz5xDoFK2FzO5C9DRVz7xPsuM2W4EkvfNmGzR64nwnrk0NQbV4wVQCHUM3C48icQZAPzPkmI9czNexvfgSir5dkKFhJa/ibAaejUI20Zqk6fDT3NeVlyD8I66k6PG+zedAub0Gtdc7aBDzt9QNTXoZs5HoGHX8FW21Cdgg2S7AUs8rKxWm7XcQCrVgiFihYIhYoWCIWKFgiFihYIhYoWCIWKFgiFihYIhYoWCIWKFgiFvwBBS3WcA69VP4AAAAASUVORK5CYII="
DISCONNECT_RESIM_KODU = "iVBORw0KGgoAAAANSUhEUgAAANQAAAAfCAYAAACf8eNvAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAALESURBVHhe7drNahpRGMbxv70AnRvQoYTaRShuG427QEWyb5FCU7Kr+7qLJLtk3+5CW0hDui+SQkmgU5N1CFk00ILjDRhvwC7mDDNORlFzuih5fpCF58zHIczD+57RzNPPoxEiYsWD5ICILE6BErFIgRKxSIESsUiBErFIgRKxSIESsUiBErFIgRKxKKNfSsyuuQ4vs4nBIWx8hV+xod0GZLrQ6oH+ufeLKtScvC6UD2HF/L3qw4cG1MIDHHAB1xk/739TLMFRCTLJCZlKgbqj6wvY6UO7ah6+Abw4hOcXqk73kVq+OTTXwb1MaeVcOKvAziEcm5bP78C7AdSq0M6b4/pQ9sy5DhzVg2qGqXytHowmjZvrnnahXbl9vWlzyXsdmLWRMud14aQQW3NiDTKdKpQNN+ADS8k2z4WtHGyELaIPz8zUbh38WPt44sAjYK8OXidqKUcV2HWj1qtdiM75kZ9tbuxeHaiuwuMp6/jjwXYf/Ktg/K3CNDMF6h8qOkAWHoYDvaCCFUtQHcJ+7EE9vgBKsDqE72H1APavYLUQfT64jM457Y/v1dLmbt1rAB6wljZn1nEdXVLmpEDZkIMC8DsWBMz+qtyFrQacN2AvVk24mfDgpo3noMgdXhBk4aNZw3kjeFPp5sxc2v1kYQqUBbUCZPrwLTlBUJXCVqtQiVq+MCS3pI2bh36Rtut6YPZTsTeTK6aNgwn3k4UpUHdULMFWHrbDFwBxDtQS+6olJ6hcXhY2YxWrWYrG12LnbC7DTz/6PLceeHl4k9zfmQqatg5ZnAI1p2oFzmLt06c8vDZv95JqT6BdN8eazf970xa2TMUKr+USVIpWB6rhOZa+IE5e87wBTROwSes49iG/HIx/0fdRM9NrcxGLVKFELFKgRCxSoEQsUqBELFKgRCxSoEQsUqBELFKgRCxSoEQsUqBELPoL26r5mXbgi7AAAAAASUVORK5CYII="

def check_vpn_status():
    """Yıldız Teknik ağından bağlantı alınıp alınmadığını kontrol eder."""
    try:
        result = subprocess.run(['ipconfig'], capture_output=True, text=True, errors='ignore', creationflags=subprocess.CREATE_NO_WINDOW)
        return "Ethernet 5" in result.stdout or "10.255." in result.stdout
    except Exception:
        return False

def get_image_from_base64(base64_string):
    image_bytes = base64.b64decode(base64_string)
    return Image.open(io.BytesIO(image_bytes))

def ekranda_resim_ara(orijinal_resim):
    """Sadece resmi arar ve bulursa koordinatını verir. Bulamazsa vakit kaybetmeden None döner."""
    olcek_oranlari = [
        1.0, 1.25, 1.5, 1.1, 1.2, 0.9, 0.8, 0.75, 
        1.75, 2.0, 2.25, 2.5, 3.0, 
        0.7, 0.6, 0.5, 1.3, 1.4, 1.6
    ]
    for oran in olcek_oranlari:
        yeni_boyut = (int(orijinal_resim.width * oran), int(orijinal_resim.height * oran))
        try:
            if hasattr(Image, 'Resampling'):
                olcekli = orijinal_resim.resize(yeni_boyut, Image.Resampling.LANCZOS)
            else:
                olcekli = orijinal_resim.resize(yeni_boyut, Image.ANTIALIAS)
                
            koordinat = pyautogui.locateCenterOnScreen(olcekli, confidence=0.8)
            if koordinat:
                return koordinat
        except Exception:
            pass
    return None

def hayalet_tiklama(koordinat):
    """Donanımsal kilit ile ışık hızında tıklar ve imleci eski yerine bırakır."""
    try:
        ctypes.windll.user32.BlockInput(True)
        eski_x, eski_y = pyautogui.position() 
        eski_pause = pyautogui.PAUSE
        pyautogui.PAUSE = 0.0 
        
        pyautogui.moveTo(koordinat)
        time.sleep(0.05) # İvme sönümleme
        pyautogui.click() 
        
        pyautogui.moveTo(eski_x, eski_y) 
        pyautogui.PAUSE = eski_pause 
    finally:
        ctypes.windll.user32.BlockInput(False)

def main():
    print("Mevcut bağlantı durumu kontrol ediliyor (Ön Kontrol)...")
    gp_path = r"C:\Program Files\Palo Alto Networks\GlobalProtect\PanGPA.exe"
    if not os.path.exists(gp_path):
        print("HATA: GlobalProtect belirtilen konumda bulunamadı!")
        return

    sanal_connect = get_image_from_base64(CONNECT_RESIM_KODU)
    sanal_disconnect = get_image_from_base64(DISCONNECT_RESIM_KODU)

    # ==========================================
    # 1. AŞAMA: VPN'E BAĞLANMA
    # ==========================================
    if check_vpn_status():
        print("VPN halihazırda bağlı! Doğrudan SolidWorks başlatılıyor...")
    else:
        print("Bağlanma aşaması başlatılıyor...")
        baglandi_mi = False
        
        for deneme in range(10):
            os.startfile(gp_path)
            time.sleep(2.5) 
            
            koordinat = ekranda_resim_ara(sanal_connect)
            if koordinat:
                print("   -> Connect butonu bulundu, tıklanıyor!")
                hayalet_tiklama(koordinat)
                
            # KULLANICININ ZEKASI: Tıklasa da tıklamasa da ESC'ye basıp ekranı temizle
            pyautogui.press('esc') 
            
            # Bağlantının kurulması için kısa bir süre bekle ve kontrol et
            time.sleep(4)
            if check_vpn_status():
                baglandi_mi = True
                break
                
        if not baglandi_mi:
            print("HATA: Tüm denemelere rağmen VPN bağlantısı kurulamadı.")
            return

    # ==========================================
    # 2. AŞAMA: SOLIDWORKS BAŞLATMA
    # ==========================================
    print("Bağlantı doğrulandı! SolidWorks başlatılıyor...")
    sw_path = r"C:\Program Files\SOLIDWORKS Corp\SOLIDWORKS\SLDWORKS.exe"
    try:
        process = subprocess.Popen([sw_path])
        print("SolidWorks kullanılıyor. Kapatana kadar arka planda bekleniyor...")
        process.wait() 
    except FileNotFoundError:
        print("HATA: SolidWorks bulunamadı.")
        return

    # ==========================================
    # 3. AŞAMA: DİSCONNECT (VUR-KAÇ DÖNGÜSÜ)
    # ==========================================
    print("SolidWorks kapatıldı. Hızlı Disconnect (Vur-Kaç) döngüsü başlıyor...")
    basarili_cikis = False
    
    for deneme in range(15): # Hızlı olduğu için deneme sayısını bol tutabiliriz
        if not check_vpn_status():
            basarili_cikis = True
            break
            
        print(f"[{deneme+1}/15] Arayüz çağrılıyor...")
        os.startfile(gp_path)
        time.sleep(2) # Arayüzün öne gelmesi için bekle
        
        # Küçük ekranlar için Akıllı Kaydırma (Garanti olsun diye hep yapıyoruz, zararı yok)
        pyautogui.press('pagedown')
        time.sleep(0.2)
        
        # Sadece hızlıca butonu ara
        koordinat = ekranda_resim_ara(sanal_disconnect)
        
        if koordinat:
            print("   -> Disconnect butonu bulundu, Hayalet Tıklama yapılıyor!")
            hayalet_tiklama(koordinat)
        else:
            print("   -> Buton bulunamadı (Bildirim engeli olabilir).")
            
        # İŞTE O SİHİRLİ DOKUNUŞ: Ne olursa olsun ESC'ye basıp masayı temizle!
        print("   -> ESC ile ekran/bildirim temizleniyor...")
        pyautogui.press('esc')
        
        # Tıklama sonrası bağlantının düşmesi için çok kısa bir süre bekle
        # Eğer düşmediyse döngü anında başa dönüp arayüzü tekrar açacak!
        time.sleep(1.5)

    # ==========================================
    # SONUÇ RAPORU
    # ==========================================
    if basarili_cikis:
        print("VPN bağlantısı başarıyla sonlandırıldı!")
    else:
        print("KRİTİK HATA: Kullanıcı müdahalesi veya bilinmeyen bir hata sebebiyle VPN açık kaldı!")

    print("Tüm işlemler tamamlandı. Program kapatılıyor.")
    time.sleep(3)

if __name__ == "__main__":
    main()
