import pygame
import random
import os

# PyGame Başlatma
pygame.init()
pygame.font.init()

# Ekran Ayarları
GENISLIK, YUKSEKLIK = 800, 600
pencere = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
pygame.display.set_caption("Space Defender - Cyber Edition")

# Renk Paleti
SIYAH = (10, 10, 18)
BEYAZ = (240, 240, 240)
KIRMIZI = (255, 60, 90)
YESIL = (46, 204, 113)
MAVI = (0, 210, 255)
SARI = (255, 215, 0)
TURUNCU = (255, 120, 0)
GRi = (100, 100, 120)

# --- SINIFLAR ---

class Oyuncu:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 44, 40)
        self.hiz = 7
        self.can = 3

    def ciz(self, ekran):
        # Motor Alevi (Hareketli animasyon hissi)
        alevin_boyu = random.randint(10, 18)
        pygame.draw.polygon(ekran, TURUNCU, [
            (self.rect.centerx - 6, self.rect.bottom),
            (self.rect.centerx + 6, self.rect.bottom),
            (self.rect.centerx, self.rect.bottom + alevin_boyu)
        ])
        
        # Gemi Gövdesi
        noktalar = [
            (self.rect.centerx, self.rect.top),
            (self.rect.left, self.rect.bottom),
            (self.rect.right, self.rect.bottom)
        ]
        pygame.draw.polygon(ekran, MAVI, noktalar)
        
        # Kanat Detayları & Kokpit
        pygame.draw.circle(ekran, SARI, (self.rect.centerx, self.rect.top + 16), 5)
        pygame.draw.line(ekran, BEYAZ, (self.rect.left, self.rect.bottom), (self.rect.centerx, self.rect.top), 2)
        pygame.draw.line(ekran, BEYAZ, (self.rect.right, self.rect.bottom), (self.rect.centerx, self.rect.top), 2)

    def hareket_et(self, tuslar):
        if (tuslar[pygame.K_LEFT] or tuslar[pygame.K_a]) and self.rect.left > 0:
            self.rect.x -= self.hiz
        if (tuslar[pygame.K_RIGHT] or tuslar[pygame.K_d]) and self.rect.right < GENISLIK:
            self.rect.x += self.hiz


class Mermi:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x - 3, y, 6, 16)
        self.hiz = -11

    def guncelle(self):
        self.rect.y += self.hiz

    def ciz(self, ekran):
        pygame.draw.rect(ekran, SARI, self.rect, border_radius=3)


class Dusman:
    def __init__(self):
        self.genislik = random.randint(35, 50)
        self.yukseklik = 30
        self.rect = pygame.Rect(
            random.randint(0, GENISLIK - self.genislik),
            random.randint(-150, -40),
            self.genislik,
            self.yukseklik
        )
        self.hiz = random.randint(2, 5)

    def guncelle(self):
        self.rect.y += self.hiz

    def ciz(self, ekran):
        pygame.draw.rect(ekran, KIRMIZI, self.rect, border_radius=6)
        # Düşman göz/ışık efekti
        pygame.draw.rect(ekran, SARI, (self.rect.x + 5, self.rect.y + 8, self.rect.width - 10, 4))


class SkorYonetici:
    def __init__(self, dosya="high_score.txt"):
        self.dosya = dosya
        self.yuksek_skor = self.oku()

    def oku(self):
        if os.path.exists(self.dosya):
            try:
                with open(self.dosya, "r") as f:
                    return int(f.read().strip())
            except:
                return 0
        return 0

    def kaydet(self, skor):
        if skor > self.yuksek_skor:
            self.yuksek_skor = skor
            with open(self.dosya, "w") as f:
                f.write(str(skor))


# --- ARAYÜZ / MENÜ FONKSİYONLARI ---

def metin_ciz(ekran, metin, boyut, x, y, renk=BEYAZ, ortala=True):
    font = pygame.font.SysFont("Trebuchet MS", boyut, bold=True)
    yazi = font.render(metin, True, renk)
    rect = yazi.get_rect()
    if ortala:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    ekran.blit(yazi, rect)


def baslangic_ekrani(pencere, skor_yonetici):
    yildizlar = [[random.randint(0, GENISLIK), random.randint(0, YUKSEKLIK)] for _ in range(60)]
    clock = pygame.time.Clock()
    
    bekliyor = True
    while bekliyor:
        clock.tick(60)
        pencere.fill(SIYAH)

        # Arka Plan Yıldızlar
        for yildiz in yildizlar:
            yildiz[1] += 0.5
            if yildiz[1] > YUKSEKLIK:
                yildiz[1] = 0
            pygame.draw.circle(pencere, GRi, yildiz, 1)

        # Başlık ve Alt Başlıklar
        metin_ciz(pencere, "SPACE DEFENDER", 52, GENISLIK // 2, 130, MAVI)
        metin_ciz(pencere, f"En Yüksek Skor: {skor_yonetici.yuksek_skor}", 22, GENISLIK // 2, 195, SARI)

        # Kontrol Kutusunu Çizme (Görsel Rehber)
        pygame.draw.rect(pencere, (25, 25, 45), (GENISLIK // 2 - 180, 240, 360, 190), border_radius=12)
        pygame.draw.rect(pencere, MAVI, (GENISLIK // 2 - 180, 240, 360, 190), width=2, border_radius=12)

        metin_ciz(pencere, "--- KONTROLLER ---", 20, GENISLIK // 2, 265, BEYAZ)
        metin_ciz(pencere, "Hareket:  [A] - [D]  veya  [←] - [→]", 18, GENISLIK // 2, 305, YESIL)
        metin_ciz(pencere, "Ateş Etme:  [ SPACE / BOŞLUK ]", 18, GENISLIK // 2, 345, YESIL)
        metin_ciz(pencere, "Oyunu Durdur:  [ P ]", 18, GENISLIK // 2, 385, TURUNCU)

        # Başlat Mesajı (Yanıp Sönen Efekt)
        if (pygame.time.get_ticks() // 500) % 2 == 0:
            metin_ciz(pencere, "BAŞLAMAK İÇİN [SPACE] TUŞUNA BASIN", 22, GENISLIK // 2, 480, BEYAZ)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bekliyor = False


# --- ANA OYUN DÖNGÜSÜ ---

def ana_oyun():
    clock = pygame.time.Clock()
    skor_yonetici = SkorYonetici()
    
    # Oyun Başlangıç Ekranını Çağır
    baslangic_ekrani(pencere, skor_yonetici)

    oyuncu = Oyuncu(GENISLIK // 2 - 22, YUKSEKLIK - 70)
    mermiler = []
    dusmanlar = []
    yildizlar = [[random.randint(0, GENISLIK), random.randint(0, YUKSEKLIK)] for _ in range(60)]
    
    skor = 0
    duraklatildi = False
    oyun_bitti = False

    calisiyor = True
    while calisiyor:
        clock.tick(60)

        # --- EVENT HANDLING ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                calisiyor = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not oyun_bitti and not duraklatildi:
                    mermiler.append(Mermi(oyuncu.rect.centerx, oyuncu.rect.top))

                if event.key == pygame.K_p and not oyun_bitti:
                    duraklatildi = not duraklatildi

                if event.key == pygame.K_r and oyun_bitti:
                    ana_oyun()
                    return

        # --- OYUN MANTIĞI ---
        if not oyun_bitti and not duraklatildi:
            tuslar = pygame.key.get_pressed()
            oyuncu.hareket_et(tuslar)

            # Düşman Üretimi
            if len(dusmanlar) < 7:
                dusmanlar.append(Dusman())

            # Mermi Güncelleme
            for mermi in mermiler[:]:
                mermi.guncelle()
                if mermi.rect.bottom < 0:
                    mermiler.remove(mermi)

            # Düşman Güncelleme ve Çarpışma
            for dusman in dusmanlar[:]:
                dusman.guncelle()

                # Ekrandan Çıkma (Can Kaybı)
                if dusman.rect.top > YUKSEKLIK:
                    dusmanlar.remove(dusman)
                    oyuncu.can -= 1
                    if oyuncu.can <= 0:
                        oyun_bitti = True
                        skor_yonetici.kaydet(skor)

                # Mermi Vurma
                for mermi in mermiler[:]:
                    if dusman.rect.colliderect(mermi.rect):
                        dusmanlar.remove(dusman)
                        mermiler.remove(mermi)
                        skor += 10
                        break

                # Gemimizle Çarpışma
                if dusman.rect.colliderect(oyuncu.rect):
                    dusmanlar.remove(dusman)
                    oyuncu.can -= 1
                    if oyuncu.can <= 0:
                        oyun_bitti = True
                        skor_yonetici.kaydet(skor)

        # --- ÇİZİM İŞLEMLERİ ---
        pencere.fill(SIYAH)

        # Arka Plan Yıldız Hareketi
        for yildiz in yildizlar:
            yildiz[1] += 1
            if yildiz[1] > YUKSEKLIK:
                yildiz[1] = 0
                yildiz[0] = random.randint(0, GENISLIK)
            pygame.draw.circle(pencere, BEYAZ, yildiz, 1)

        # Nesneleri Çizme
        oyuncu.ciz(pencere)
        for mermi in mermiler:
            mermi.ciz(pencere)
        for dusman in dusmanlar:
            dusman.ciz(pencere)

        # Üst Arayüz (HUD)
        metin_ciz(pencere, f"Skor: {skor}", 20, 15, 15, BEYAZ, ortala=False)
        metin_ciz(pencere, f"Rekor: {skor_yonetici.yuksek_skor}", 20, 15, 40, SARI, ortala=False)
        metin_ciz(pencere, f"Can: {'❤️ ' * oyuncu.can}", 18, GENISLIK - 130, 15, KIRMIZI, ortala=False)

        # Alt Kontrol İpucu
        metin_ciz(pencere, "[A/D - Sol/Sağ]  |  [SPACE - Ateş]  |  [P - Duraklat]", 14, GENISLIK // 2, YUKSEKLIK - 15, GRi)

        # Duraklatma Ekranı
        if duraklatildi:
            metin_ciz(pencere, "OYUN DURAKLATILDI", 36, GENISLIK // 2, YUKSEKLIK // 2, TURUNCU)

        # Game Over Ekranı
        if oyun_bitti:
            pygame.draw.rect(pencere, (0, 0, 0, 200), (0, 0, GENISLIK, YUKSEKLIK))
            metin_ciz(pencere, "GAME OVER", 48, GENISLIK // 2, YUKSEKLIK // 2 - 40, KIRMIZI)
            metin_ciz(pencere, f"Toplam Skor: {skor}", 24, GENISLIK // 2, YUKSEKLIK // 2 + 15, BEYAZ)
            metin_ciz(pencere, "Yeniden Başlamak İçin 'R' Tuşuna Basın", 20, GENISLIK // 2, YUKSEKLIK // 2 + 60, YESIL)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    ana_oyun()