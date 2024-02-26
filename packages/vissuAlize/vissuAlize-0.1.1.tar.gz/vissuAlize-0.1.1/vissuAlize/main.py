import matplotlib.pyplot as plt
import seaborn as sns
from pandas.plotting import parallel_coordinates

class vissuAlize:
    @staticmethod
    def bar(x, y, title="Title", xlabel="X-axis", ylabel="Y-axis",
            figsize=(8, 6), color='maroon', orientation='vertical', **kwargs):
        """
        Çubuk grafik çizimi için bir fonksiyon.

        Parametreler:
        - x: x eksenindeki değerler (kategori isimleri veya sayılar).
        - y: y eksenindeki değerler.
        - title: Grafiğin başlığı.
        - xlabel: X ekseninin etiketi.
        - ylabel: Y ekseninin etiketi.
        - figsize: Grafiğin boyutu, (genişlik, yükseklik) formatında.
        - color: Çubukların rengi.
        - orientation: Çubukların yönü, 'vertical' veya 'horizontal'.
        - **kwargs: Matplotlib bar fonksiyonuna aktarılacak ekstra anahtar kelime argümanları.
        """
        plt.figure(figsize=figsize)
        if orientation == 'vertical':
            plt.bar(x, y, color=color, **kwargs)
        else:
            plt.barh(x, y, color=color, **kwargs)

        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.show()

    @staticmethod
    def plot(x, y, titleName="Title", rowName="Row", columnName="Column",
             figsize=(8, 6), color='maroon', width=0.4, kind="line", **kwargs):
        if kind == "line":
            plt.figure(figsize=figsize)
            plt.plot(x, y, color=color, **kwargs)
            plt.title(titleName)
            plt.xlabel(columnName)
            plt.ylabel(rowName)
            plt.show()
        elif kind == "bar":
            plt.figure(figsize=figsize)
            plt.bar(x, y, color=color, width=width, **kwargs)
            plt.title(titleName)
            plt.xlabel(columnName)
            plt.ylabel(rowName)
            plt.show()

    @staticmethod
    def scatter(x, y, title="Title", xlabel="X-axis", ylabel="Y-axis",
                figsize=(8, 6), color='blue', marker='o', **kwargs):
        """
        Saçılım grafiği çizimi için bir fonksiyon.

        Parametreler:
        - x, y: Veri noktalarının x ve y koordinatları.
        - title: Grafiğin başlığı.
        - xlabel, ylabel: Eksenlerin etiketleri.
        - figsize: Grafiğin boyutu, (genişlik, yükseklik) formatında.
        - color: Noktaların rengi.
        - marker: Noktaların şekli.
        - **kwargs: Matplotlib scatter fonksiyonuna aktarılacak ekstra anahtar kelime argümanları.
        """
        plt.figure(figsize=figsize)
        plt.scatter(x, y, color=color, marker=marker, **kwargs)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.show()

    @staticmethod
    def histogram(data, bins=10, title="Title", xlabel="Value", ylabel="Frequency",
                  figsize=(8, 6), color='green', **kwargs):
        """
        Histogram çizimi için bir fonksiyon.

        Parametreler:
        - data: Histogramı oluşturacak veri.
        - bins: Histogramdaki kutu sayısı.
        - title: Grafiğin başlığı.
        - xlabel, ylabel: Eksenlerin etiketleri.
        - figsize: Grafiğin boyutu, (genişlik, yükseklik) formatında.
        - color: Kutuların rengi.
        - **kwargs: Matplotlib hist fonksiyonuna aktarılacak ekstra anahtar kelime argümanları.
        """
        plt.figure(figsize=figsize)
        plt.hist(data, bins=bins, color=color, **kwargs)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.show()

    @staticmethod
    def boxplot(data, title="Title", xlabel="Categories", ylabel="Values",
                figsize=(8, 6), color="skyblue", **kwargs):
        """
        Boxplot çizimi için bir fonksiyon.

        Parametreler:
        - data: Boxplot için veri. Pandas DataFrame, listelerin listesi veya benzeri olabilir.
        - title: Grafiğin başlığı.
        - xlabel, ylabel: Eksenlerin etiketleri.
        - figsize: Grafiğin boyutu, (genişlik, yükseklik) formatında.
        - color: Kutunun rengi (eğer seaborn kullanılıyorsa, bu parametre seaborn stil parametrelerine eklenebilir).
        - **kwargs: Matplotlib veya seaborn boxplot fonksiyonuna aktarılacak ekstra anahtar kelime argümanları.
        """
        plt.figure(figsize=figsize)
        if isinstance(data, list):
            plt.boxplot(data, patch_artist=True, boxprops=dict(facecolor=color), **kwargs)
        elif isinstance(data, pd.DataFrame):
            sns.boxplot(data=data, color=color, **kwargs)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.show()

    @staticmethod
    def heatmap(data, title="Title", figsize=(10, 8), cmap="viridis", annot=False, **kwargs):
        """
        Heatmap çizimi için bir fonksiyon.

        Parametreler:
        - data: Heatmap için veri matrisi. Pandas DataFrame olmalı ve her hücre bir değeri temsil etmelidir.
        - title: Grafiğin başlığı.
        - figsize: Grafiğin boyutu, (genişlik, yükseklik) formatında.
        - cmap: Kullanılacak renk paleti.
        - annot: Eğer True ise, her hücrenin içine değerler yazdırılır.
        - **kwargs: Seaborn heatmap fonksiyonuna aktarılacak ekstra anahtar kelime argümanları.
        """
        plt.figure(figsize=figsize)
        sns.heatmap(data, cmap=cmap, annot=annot, **kwargs)
        plt.title(title)
        plt.show()

    @staticmethod
    def lineplot(x, y, title="Title", xlabel="X-axis", ylabel="Y-axis",
                 figsize=(10, 6), color='blue', linestyle='-', linewidth=2, **kwargs):
        """
        Çizgi grafiği çizimi için bir fonksiyon.

        Parametreler:
        - x, y: Veri noktalarının x ve y koordinatları.
        - title: Grafiğin başlığı.
        - xlabel, ylabel: Eksenlerin etiketleri.
        - figsize: Grafiğin boyutu, (genişlik, yükseklik) formatında.
        - color: Çizginin rengi.
        - linestyle: Çizgi stili ('-', '--', '-.', ':').
        - linewidth: Çizgi kalınlığı.
        - **kwargs: Matplotlib plot fonksiyonuna aktarılacak ekstra anahtar kelime argümanları.
        """
        plt.figure(figsize=figsize)
        plt.plot(x, y, color=color, linestyle=linestyle, linewidth=linewidth, **kwargs)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.show()

    @staticmethod
    def pie(sizes, labels, colors=None, explode=None, title="Title", startangle=90, autopct='%1.1f%%', figsize=(8, 8),
            **kwargs):
        """
        Pasta grafiği çizimi için bir fonksiyon.

        Parametreler:
        - sizes: Her bir dilimin büyüklüğü, genellikle toplamın yüzdesi olarak.
        - labels: Her dilimin etiketi.
        - colors: Dilimlerin renkleri, liste şeklinde. Opsiyonel.
        - explode: Belirli dilimlerin 'patlatılması' için değerler, dilimden uzaklaşma miktarını belirler. Opsiyonel.
        - title: Grafiğin başlığı.
        - startangle: İlk dilimin başlangıç açısı.
        - autopct: Dilimlerin üzerinde gösterilecek yüzde formatı.
        - figsize: Grafiğin boyutu, (genişlik, yükseklik) formatında.
        - **kwargs: Matplotlib pie fonksiyonuna aktarılacak ekstra anahtar kelime argümanları.
        """
        plt.figure(figsize=figsize)
        plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct=autopct, startangle=startangle, **kwargs)
        plt.title(title)
        plt.axis('equal')  # Eşit oranlı bir pie chart yapısı sağlar.
        plt.show()

    @staticmethod
    def violinplot(data, x=None, y=None, hue=None, title="Title", xlabel="X-axis", ylabel="Y-axis",
                   figsize=(10, 6), palette="muted", split=False, inner="quartile", **kwargs):
        """
        Violinplot çizimi için bir fonksiyon.

        Parametreler:
        - data: Görselleştirilecek veri seti. Pandas DataFrame'i olabilir.
        - x, y: Veri setindeki sütun isimleri. `x` kategorik değişken, `y` ise sayısal değişken olmalıdır.
        - hue: Kategorik değişkenler arasında renk ayrımı yapmak için kullanılır.
        - title: Grafiğin başlığı.
        - xlabel, ylabel: Eksenlerin etiketleri.
        - figsize: Grafiğin boyutu, (genişlik, yükseklik) formatında.
        - palette: Kullanılacak renk paleti.
        - split: Eğer True ise, hue parametresi kullanıldığında iki yarım violin bir arada gösterilir.
        - inner: Violin içinde gösterilecek bilgi tipi ("box", "quartile", "point", "stick", None).
        - **kwargs: Seaborn violinplot fonksiyonuna aktarılacak ekstra anahtar kelime argümanları.
        """
        plt.figure(figsize=figsize)
        sns.violinplot(data=data, x=x, y=y, hue=hue, palette=palette, split=split, inner=inner, **kwargs)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.show()

    def pairplot(data, hue=None, palette="muted", markers="o", height=2.5, aspect=1, **kwargs):
        """
        Çok değişkenli veri ilişkilerini görselleştirmek için pairplot çizimi.

        Parametreler:
        - data: Görselleştirilecek veri seti. Pandas DataFrame'i olmalı.
        - hue: Kategorik değişkenler arasında renk ayrımı yapmak için kullanılır.
        - palette: Kullanılacak renk paleti.
        - markers: Scatterplotlarda kullanılacak marker türleri.
        - height: Her bir subplot'un yüksekliği.
        - aspect: Yükseklik ve genişlik oranı.
        - **kwargs: Seaborn pairplot fonksiyonuna aktarılacak ekstra anahtar kelime argümanları.
        """
        g = sns.pairplot(data, hue=hue, palette=palette, markers=markers, height=height, aspect=aspect, **kwargs)
        g.fig.suptitle("Pairplot of the Dataset", y=1.02)  # Başlık ekleme ve konumlandırma
        plt.show()

    @staticmethod
    def timeseries(data, x, y, title="Time Series Plot", xlabel="Time", ylabel="Value",
                   figsize=(12, 6), color='blue', linestyle='-', linewidth=2, **kwargs):
        """
        Zaman serisi verilerini görselleştirmek için bir fonksiyon.

        Parametreler:
        - data: Görselleştirilecek veri seti. Pandas DataFrame'i olmalı ve zaman serisi indekse sahip olmalı.
        - x: Zaman serisi verisinin zaman/saat bilgisini içeren sütun.
        - y: Görselleştirilecek değerleri içeren sütun(lar).
        - title: Grafiğin başlığı.
        - xlabel, ylabel: Eksenlerin etiketleri.
        - figsize: Grafiğin boyutu, (genişlik, yükseklik) formatında.
        - color: Çizginin rengi.
        - linestyle: Çizgi stili ('-', '--', '-.', ':').
        - linewidth: Çizgi kalınlığı.
        - **kwargs: Matplotlib plot fonksiyonuna aktarılacak ekstra anahtar kelime argümanları.
        """
        plt.figure(figsize=figsize)
        if isinstance(y, list):
            for column in y:
                plt.plot(data[x], data[column], linestyle=linestyle, linewidth=linewidth, label=column, **kwargs)
            plt.legend()
        else:
            plt.plot(data[x], data[y], color=color, linestyle=linestyle, linewidth=linewidth, **kwargs)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.show()



    @staticmethod
    def geo_map(geo_data, title="Geographic Map", figsize=(10, 10), color='lightblue', edgecolor='black', **kwargs):
        """
        Coğrafi verileri görselleştirmek için bir harita fonksiyonu.

        Parametreler:
        - geo_data: Görselleştirilecek coğrafi veri seti. Geopandas GeoDataFrame'i olmalı.
        - title: Haritanın başlığı.
        - figsize: Haritanın boyutu, (genişlik, yükseklik) formatında.
        - color: Harita üzerindeki alanların doldurulma rengi.
        - edgecolor: Sınırların rengi.
        - **kwargs: Geopandas plot fonksiyonuna aktarılacak ekstra anahtar kelime argümanları.
        """
        fig, ax = plt.subplots(1, 1, figsize=figsize)
        geo_data.plot(ax=ax, color=color, edgecolor=edgecolor, **kwargs)
        ax.set_title(title)
        plt.show()

    ######################################################################################################################

    @staticmethod
    def parallel_coordinates(data, class_column, cols=None, color=None, title="Parallel Coordinates Plot",
                             figsize=(12, 6), **kwargs):
        """
        Çok boyutlu veri setlerini paralel koordinatlar kullanarak görselleştirmek için bir fonksiyon.
        """
        plt.figure(figsize=figsize)
        if cols:  # Eğer spesifik sütunlar belirtilmişse, sadece bu sütunları içeren bir DataFrame oluştur.
            data = data[cols + [class_column]]
        parallel_coordinates(data, class_column, color=color, **kwargs)
        plt.title(title)
        plt.show()

    @staticmethod
    def distplot(data, column, bins=30, kde=True, color="blue", title="Distribution Plot", **kwargs):
        """
        Veri dağılımını hem histogram hem de KDE ile gösterir.
        """
        plt.figure(figsize=(8, 6))
        sns.distplot(data[column], bins=bins, kde=kde, color=color, **kwargs)
        plt.title(title)
        plt.show()

    @staticmethod
    def countplot(data, column, palette="muted", title="Count Plot", **kwargs):
        """
        Kategorik bir değişkendeki her kategorinin sayısını gösterir.
        """
        plt.figure(figsize=(8, 6))
        sns.countplot(x=column, data=data, palette=palette, **kwargs)
        plt.title(title)
        plt.show()

    @staticmethod
    def jointplot(data, x, y, kind='scatter', color="blue", title="Joint Plot", **kwargs):
        """
        İki değişken arasındaki dağılımı ve her bir değişkenin kendi dağılımını gösterir.
        """
        g = sns.jointplot(x=x, y=y, data=data, kind=kind, color=color, **kwargs)
        g.fig.suptitle(title, y=1.03)  # Suptitle ile başlığı ayarla
        plt.show()

    @staticmethod
    def pairplot(data, hue=None, palette="muted", title="Pair Plot", **kwargs):
        """
        DataFrame'deki her sayısal sütun çifti için scatter plotlar ve histogramlar oluşturur.
        """
        g = sns.pairplot(data, hue=hue, palette=palette, **kwargs)
        g.fig.suptitle(title, y=1.03)  # Suptitle ile başlığı ayarla
        plt.show()

    @staticmethod
    def heatmap(data, annot=True, cmap='viridis', title="Heatmap", **kwargs):
        """
        Veri matrisini renk kodlaması kullanarak görselleştirir.
        """
        plt.figure(figsize=(10, 8))
        sns.heatmap(data.corr(), annot=annot, cmap=cmap, **kwargs)
        plt.title(title)
        plt.show()
    @staticmethod
    def kdeplot(data, column, shade=True, color="red", title="KDE Plot", xlabel=None, ylabel=None, **kwargs):
        """
        Kernel Density Estimate (KDE) plot çizer.
        """
        plt.figure(figsize=(8, 6))
        sns.kdeplot(data[column], shade=shade, color=color, **kwargs)
        plt.title(title)
        if xlabel:
            plt.xlabel(xlabel)
        if ylabel:
            plt.ylabel(ylabel)
        plt.show()

    @staticmethod
    def updated_violinplot(data, x=None, y=None, hue=None, split=True, inner="quart", palette="muted", title="Violin Plot", xlabel=None, ylabel=None, **kwargs):
        """
        Güncellenmiş violinplot, veri dağılımının yoğunluğunu daha detaylı gösterir.
        """
        plt.figure(figsize=(10, 6))
        sns.violinplot(data=data, x=x, y=y, hue=hue, split=split, inner=inner, palette=palette, **kwargs)
        plt.title(title)
        if xlabel:
            plt.xlabel(xlabel)
        if ylabel:
            plt.ylabel(ylabel)
        plt.show()

    @staticmethod
    def swarmplot(data, x, y, hue=None, color="blue", title="Swarm Plot", xlabel=None, ylabel=None, **kwargs):
        """
        Swarmplot, kategorik veriler için nokta grafiği çizer ve üst üste binmeyi önler.
        """
        plt.figure(figsize=(10, 6))
        sns.swarmplot(x=x, y=y, data=data, hue=hue, color=color, **kwargs)
        plt.title(title)
        if xlabel:
            plt.xlabel(xlabel)
        if ylabel:
            plt.ylabel(ylabel)
        plt.show()

    @staticmethod
    def facet_grid(data, row, col, plot_kind="scatter", palette="muted", title=None, **kwargs):
        """
        FacetGrid kullanarak, veri setini satır ve sütunlara göre bölümlere ayırır ve her bölüm için belirlenen çizim türünü uygular.
        """
        g = sns.FacetGrid(data, row=row, col=col, palette=palette, **kwargs)
        if plot_kind == "scatter":
            g = g.map(plt.scatter, "x", "y")
        elif plot_kind == "kde":
            g = g.map(sns.kdeplot, "x", "y")
        if title:
            g.fig.suptitle(title, y=1.03)
        g.add_legend()
        plt.show()
