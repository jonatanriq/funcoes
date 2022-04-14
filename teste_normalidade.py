def teste_normalidade(dado):
	from scipy.stats import normaltest
	alpha = 0.05
	k2, p = normaltest(dado)

	# se o valor p for maior do que alpha significa que a hipotese nula não pode ser rejeitada,
	# ou seja, a distribuição é normal
	if p < alpha:
	    print("A Hipótese Nula pode ser rejeitada")
	else:
	    print("A hipótese nula não pode ser rejeitada")