from statistics import mean
import statistics
from turtle import color, shape
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
from plotnine import ggplot, aes, geom_boxplot, geom_point, theme_bw, facet_wrap, labs, geom_smooth

Datos = pd.read_csv("Resumen_tres_temporadas.csv")
Datos2 = pd.read_csv("Resumen_tres_temporadas_cuali.csv")
Datos3 = pd.read_csv("Resumen_tres_temporadas_disc.csv")

print(Datos.shape)

print(Datos[0:9])
print(Datos3[0:9])

print(Datos.describe().transpose())
print(Datos3.describe().transpose())

print(Datos.Rendimiento[0:3])

par = sns.pairplot(Datos3, hue="Antecesor", x_vars=["Fsecado", "MSVicia", "PPEstival"], y_vars="Rendimiento")
plt.show()

#Analizar fecha de secado junto con precipitaciones estivales. Ya que en un año más seco se secó más temprano.
#Como consecuencia en el gráfico hay mucha diferencia

coef = np.polyfit(Datos["Fsecado"],Datos["Rendimiento"],1)
line_coef = np.poly1d(coef)
plt.plot(Datos['Fsecado'], line_coef(Datos["Fsecado"]))
plt.scatter(x=Datos["Fsecado"], y=Datos["Rendimiento"], color='red', alpha=0.5)
plt.show()

coef = np.polyfit(Datos3["Fsecado"],Datos3["Rendimiento"],1)
line_coef = np.poly1d(coef)
plt.plot(Datos3['Fsecado'], line_coef(Datos3["Fsecado"]))
plt.scatter(x=Datos3["Fsecado"], y=Datos3["Rendimiento"], color='red', alpha=0.5)
plt.show()

rendimiento_sobre_AUMaiz = Datos3["Rendimiento"]/Datos3["AUMaiz"]
fitted = np.polyfit(Datos3["Fsecado"],rendimiento_sobre_AUMaiz,1)
line_fitted = np.poly1d(fitted)
plt.plot(Datos3['Fsecado'], line_fitted(Datos3["Fsecado"]))
plt.scatter(x=Datos3["Fsecado"], y=rendimiento_sobre_AUMaiz, color='red', alpha=0.5)
plt.show()

aguaMz = Datos3["PPEstival"]*.75 + Datos3["AUMaiz"]
df = pd.DataFrame()
df['Rendimiento'] = Datos3['Rendimiento']
df['aguaMz'] = aguaMz
print(df)
df.corr(method='pearson')

fitted2 = np.polyfit(aguaMz,Datos3["Rendimiento"],1)
line_fitted2 = np.poly1d(fitted2)
plt.plot(aguaMz, line_fitted2(aguaMz))
plt.scatter(x= aguaMz, y= Datos3["Rendimiento"], color= 'blue')
plt.show()

rendimiento_en_agua = Datos3["Rendimiento"]/aguaMz
print(rendimiento_en_agua)
plt.scatter(x=Datos3["Fsecado"], y=rendimiento_en_agua, color='red', alpha=0.5)
plt.show()


print(Datos.corr(method="spearman"))

print(Datos.corr(method="pearson"))

fit = np.polyfit(x=Datos['MSVicia'], y=Datos['Rendimiento'], deg=1)
line_fit = np.poly1d(fit)
plt.plot(Datos['MSVicia'], line_fit(Datos["MSVicia"]))
plt.scatter(x=Datos["MSVicia"], y=Datos["Rendimiento"], color='red', alpha=0.25)
plt.title("Correlación de Pearson")
plt.show()


rend_ant = ggplot(Datos2) + aes(x="Fsecado", y="Rendimiento") + geom_boxplot() + geom_point(aes(size="Rendimiento", color="Antecesor"), alpha=0.7) + geom_smooth(alpha=0.7) + labs(title="Rendimientos según fecha de secado", x="Fecha de secado", y="Rendimiento", color="Antecesor") + facet_wrap("Fertilizante") + theme_bw()

rend_ant.save("rend_ant.png", dpi=600)