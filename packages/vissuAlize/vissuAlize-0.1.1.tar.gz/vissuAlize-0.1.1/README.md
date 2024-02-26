# vissuAlize

`vissuAlize`, Python için yüksek seviyeli bir veri görselleştirme kütüphanesidir. Matplotlib ve Seaborn'un güçlü özelliklerini bir araya getirerek, kullanıcı dostu bir arayüz sunar. Veri bilimi projelerinizde hızlı ve etkili görselleştirmeler oluşturmanıza olanak tanır.

## Özellikler

- Çeşitli görselleştirme türleri: bar plotlar, scatter plotlar, line plotlar ve daha fazlası.
- Seaborn ve Matplotlib tabanlı estetik ve interaktif grafikler.
- Kolay kullanım ve esnek API.
- Çoklu veri seti desteği ve kategorik veri analizi için özel görselleştirmeler.

## Kurulum

`vissuAlize`'ı pip kullanarak kolayca kurabilirsiniz:

```bash
pip install vissuAlize
```

## Kullanım Örnekleri

`vissuAlize` ile görselleştirme yapmak basit ve doğrudandır. İşte bazı temel kullanım örnekleri:

Bar Plot Oluşturma:

```python
import vissuAlize as viss
import pandas as pd

# Veri setini yükle
data = pd.read_csv('your_dataset.csv')

# Bar plot oluştur
viss.bar(x='category', y='value', data=data, title="Örnek Bar Plot")
```

Scatter Plot Oluşturma:

```python
# Scatter plot oluştur
viss.scatter(x='x_column', y='y_column', data=data, title="Örnek Scatter Plot")
```

Bu basit örnekler, `vissuAlize`'ın nasıl kullanılacağına dair bir fikir vermektedir. Daha fazla bilgi ve örnek için dokümantasyonumuzu ziyaret edin.

## Katkıda Bulunma

`vissuAlize`'a katkıda bulunmak istiyorsanız, lütfen Katkıda Bulunma Rehberi'ni okuyun. Her türlü katkı, büyük ya da küçük, takdirle karşılanır!

## Lisans

`vissuAlize`, MIT Lisansı altında lisanslanmıştır. Detaylar için LICENSE dosyasına bakın.
