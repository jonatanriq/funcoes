
# plotando um histograma com o valor em cima certinho

def histograma():
	import matplotlib.pyplot as plt
	import seaborn as sns
	import numpy as np
	from matplotlib.patches import Rectangle


	boia = dados 

	fig, ax = plt.subplots(figsize=(10,10))
	plt.style.use('classic')
	fig.patch.set_color('white')

	histograma = sns.distplot(boia.Hsig[boia.index < '2020-01'],norm_hist=True)
	ax.set_ylabel('Densidade', fontsize=12)
	ax.set_xlabel('Altura Significativa de Onda', fontsize=12)
	ax.set_title('Histograma de Densidade dos valores de altura significativa de onda - Boia RJ4 (SiMCosta) ', fontsize=12)

	x,y = histograma.get_lines()[0].get_data()
	plt.axvline(x=x[np.argmax(y)],color='k',linestyle='--',linewidth=1)
	plt.text(x[np.argmax(y)],np.max(y),f'   {x[np.argmax(y)]:.2f} m',fontsize=22)
	

	textstr = (f'Máx = {boia.Hsig.max():.2f}m\nMin = {boia.Hsig.min():.2f}m\nMédia = {boia.Hsig.mean():.2f}m\nMediana = {boia.Hsig.median():.2f}m')
	props = dict(boxstyle='square', alpha=0.5, facecolor='none')

	ax.text(0.66, 0.985, textstr, transform=ax.transAxes, fontsize=20,
	        verticalalignment='top', bbox=props)

	plt.grid()
	plt.show()