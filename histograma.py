# plotando um histograma com o valor em cima certinho

def histograma(dado, variavel, bins, pos_x, pos_y):

	'''
	Retorna um histograma com o valor da moda
	dado = o dado em si
	variavel = nome da variável
	bins = quantidade de bins que você quer
	pos_x = posição x da legenda interna
	pos_y = posição y da legenda interna
	'''
	import matplotlib.pyplot as plt
	import seaborn as sns
	import numpy as np
	from matplotlib.patches import Rectangle

	fig, ax = plt.subplots(figsize=(12,10))
	plt.style.use('classic')
	fig.patch.set_color('white')

	histograma = sns.distplot(dado,norm_hist=True, bins=bins)
	ax.set_ylabel('Densidade', fontsize=12)
	ax.set_xlabel(f'{variavel}', fontsize=12)
	ax.set_title(f'Histograma de Densidade dos valores de {variavel}', fontsize=12)

	x,y = histograma.get_lines()[0].get_data()
	plt.axvline(x=x[np.argmax(y)],color='k',linestyle='--',linewidth=1)
	plt.text(x[np.argmax(y)],np.max(y),f'   {x[np.argmax(y)]:.2f} m',fontsize=22)
	

	textstr = (f'Máx = {dado.max():.2f}m\nMin = {dado.min():.2f}m\nMédia = {dado.mean():.2f}m\nMediana = {dado.median():.2f}m')
	props = dict(boxstyle='square', alpha=0.5, facecolor='none')

	ax.text(pos_x, pos_y, textstr, transform=ax.transAxes, fontsize=20,
	        verticalalignment='top', bbox=props)

	plt.grid()
	plt.show()

	# o scrpit ainda precisa de uns ajustes pra sair melhor o histograma, mas a ideia é essa
