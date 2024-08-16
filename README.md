**Genel Proje Özeti**

Bu projede, farklı coğrafi lokasyonlar arasında uçak rotaları oluşturmak ve bu rotaları görselleştirmek amacıyla Python programları geliştirildi. Kullanıcı, rotaları manuel olarak belirleyebilir veya belirli algoritmalar kullanarak rotaların otomatik olarak oluşturulmasını sağlayabilir. Ayrıca, H3 grid sistemini kullanarak rotaların etrafına hexagon şekiller çizildi ve bu şekiller folium kütüphanesi kullanılarak haritalar üzerine yerleştirildi.

**Projede Yer Alan Başlıca Kodlar:**
1. **Basit Uçuş Rotası Oluşturma:** Manuel olarak belirlenen noktalar arasında uçuş rotası oluşturulur ve folium haritası üzerinde gösterilir. Rotalar H3 grid sistemi ile desteklenmiştir.
2. **Büyük Daire Rotası:** İki lokasyon arasında büyük daire rotası hesaplanarak, en kısa mesafe uçuş rotası elde edilir ve harita üzerinde çizilir.
3. **API Kullanımı Olmayan Rota Çizimi:** Uçuş rotaları için herhangi bir API kullanmadan, belirli algoritmalar ile rota hesaplanır ve harita üzerinde görselleştirilir.
4. **FlightAware API Entegrasyonu:** Ücretli ve ücretli API seçenekleri olan sitelerle entegre edilmek üzere tasarlanmış kodlar bulunmaktadır.

**Kullanılan Teknolojiler:**
- **Folium:** Python’da harita görselleştirme kütüphanesi.
- **H3:** Hexagon grid sistemini kullanarak coğrafi verileri alt bölümlere ayırma.
- **Geopy:** Coğrafi hesaplamalar için kullanılan Python kütüphanesi.
- **Random:** Algoritmik olarak rota oluşturmak için kullanıldı.
