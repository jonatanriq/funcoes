def rosa_ventos(dado_dir, dado_vel, titulo, nome):
	new_labels = ["E", "NE", "N", "NW", "W", "SW", "S", "SE"]

	ax = WindroseAxes.from_ax(theta_labels=new_labels)

	ax.bar(dado_dir, dado_vel,normed=True, opening=0.8, edgecolor='black') # outros parâmetros


	lgd = ax.set_legend(title=f'{titulo}',prop=dict(size=25), 
	                    bbox_to_anchor=(1.1, 0.6))

	plt.setp(lgd.get_texts(),
	         fontsize=20) 

	plt.savefig(f'{nome}.png',bbox_extra_artists=(lgd,), bbox_inches='tight')