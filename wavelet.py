def wavelet_analysis(dataset, significancia, j, d):
  '''
  Retorna as imagens do plot de wavelet. Utiliza o pacote pwcwt e a metodologia de plot foi extraída da metodologia do Prof. André Belem 

  dataset = dataset que você vai usar
  significancia = significancia estatistica que voce deseja usar (ex. 0.95 ou 0.70)
  j = potencias / quanto maior o valor maior a escala de tempo máxima
  d = denominador das sub-oitavas / quanto maior mais sub-oitavas voce quer
  '''  
  
  # primeiro importa o que vamos usar
  import pycwt as wavelet
  from pycwt.helpers import find
  import numpy as np

  # algumas definições
  title = 'Diferenças entre ZScore'
  label = 'ZScore'
  units = '-'
  t0 = 0
  dt = 1 # quero em dia [MUITO IMPORTANTE!]

  dat = np.array(dataset) # simplesmente converte o meu Dataframe para um array usando o numpy
  # artificialmente cria o vetor de tempo em decyears (pode ser que tenha outra maneira mais eficiente de fazer isso)
  N = dat.size
  t = np.arange(0, N) * dt + t0

  p = np.polyfit(t - t0, dat, 1) # usando o polyfit para normalizar o dado
  dat_notrend = dat - np.polyval(p, t - t0)
  std = dat_notrend.std()  # Standard deviation
  var = std ** 2  # Variance
  dat_norm = dat_notrend / std  # Normalized dataset

  mother = wavelet.Morlet(6) # Segundo grindsted, 6 é o valor mais adequado para extração de recursos
  s0 = 1 * dt  # escala da wavelet
  dj = 1/d  #  sub-oitavas por oitavas
  J =  j / dj  #  potências de dois com sub-oitavas dj
  alpha, _, _ = wavelet.ar1(dat)  # Lag-1 autocorrelação para ruído vermelho !!!! muito importante !!!!!

  wave, scales, freqs, coi, fft, fftfreqs = wavelet.cwt(dat, dt, dj, s0, J, mother) # usando o dado não normalizado
  #wave, scales, freqs, coi, fft, fftfreqs = wavelet.cwt(dat, dt, dj, s0, J,mother)
  iwave = wavelet.icwt(wave, scales, dt, dj, mother) * std

  power = (np.abs(wave)) ** 2
  fft_power = np.abs(fft) ** 2
  period = 1 / freqs

  mysig = significancia
  signif, fft_theor = wavelet.significance(1.0, dt, scales, 0, alpha,
                                          significance_level=mysig, #<---- veja 
                                          wavelet=mother)
  sig95 = np.ones([1, N]) * signif[:, None]
  sig95 = power / sig95

  glbl_power = power.mean(axis=1)
  dof = N - scales  # Correction for padding at edges
  glbl_signif, tmp = wavelet.significance(var, dt, scales, 1, alpha,
                                          significance_level=mysig, dof=dof, #<---- veja
                                          wavelet=mother)

  sel = find((period >= period.min()) & (period <= period.max()))
  Cdelta = mother.cdelta
  scale_avg = (scales * np.ones((N, 1))).transpose()
  scale_avg = power / scale_avg  # As in Torrence and Compo (1998) equation 24
  scale_avg = var * dj * dt / Cdelta * scale_avg[sel, :].sum(axis=0)
  scale_avg_signif, tmp = wavelet.significance(var, dt, scales, 2, alpha,
                                              significance_level=mysig, #<---- veja
                                              dof=[scales[sel[0]],
                                                    scales[sel[-1]]],
                                              wavelet=mother)
  
  from matplotlib import pyplot

  

  # Prepare the figure
  pyplot.close('all')
  pyplot.ioff()
  figprops = dict(figsize=(12, 8), dpi=72)
  fig = pyplot.figure(**figprops)

  # Primeiro sub-gráfico, a anomalia da série temporal original e 
  # wavelet inversa.
  ax = pyplot.axes([0.1, 0.75, 0.65, 0.2])
  lns1 = ax.plot(t, dat, 'k', linewidth=1.5,label='original')
  ax2 = ax.twinx()

  lns2 = ax2.plot(t, iwave, '-', linewidth=1.5, color='r',label='inverse wavelet')
  # added these three lines
  lns = lns1+lns2
  labs = [l.get_label() for l in lns]
  ax.legend(lns, labs, loc=0)

  ax.set_title('a) {}'.format(title))
  ax.set_ylabel(r'{} [{}]'.format(label, units))

  # Segundo sub-gráfico, o espectro de potência da wavelet normalizada e significância
  # linhas de contorno niveladas e cone da área hachurada de influencia. Observe aquele período
  # escala é logarítmica.
  bx = pyplot.axes([0.1, 0.37, 0.65, 0.28], sharex=ax)
  levels = [0.0625, 0.125, 0.25, 0.5, 1, 2, 4, 8, 16] # escala em log2!
  bx.contourf(t, np.log2(period), np.log2(power), np.log2(levels),
              extend='both', cmap=pyplot.cm.rainbow) # aplica log2 em toda
  extent = [t.min(), t.max(), 0, max(period)]
  bx.contour(t, np.log2(period), sig95, [-99, 1], colors='k', linewidths=2,
            extent=extent)
  bx.fill(np.concatenate([t, t[-1:] + dt, t[-1:] + dt,
                            t[:1] - dt, t[:1] - dt]),
          np.concatenate([np.log2(coi), [1e-9], np.log2(period[-1:]),
                            np.log2(period[-1:]), [1e-9]]),
          'k', alpha=0.3, hatch='x')
  bx.set_title('b) {} Wavelet Power Spectrum ({})'.format(label, mother.name))
  bx.set_ylabel('Period (Hours)')
  #
  Yticks = 2 ** np.arange(np.ceil(np.log2(period.min())),
                            np.ceil(np.log2(period.max())))
  bx.set_yticks(np.log2(Yticks))
  bx.set_yticklabels(Yticks)#

  # Terceiro sub-gráfico, wavelet global e espectros de potência de Fourier e teóricos
  # espectro de ruído. Observe que a escala do período é logarítmica.
  cx = pyplot.axes([0.77, 0.37, 0.2, 0.28], sharey=bx)
  cx.plot(glbl_signif, np.log2(period), 'k--')
  cx.plot(var * fft_theor, np.log2(period), '--', color='#cccccc')
  cx.plot(var * fft_power, np.log2(1./fftfreqs), '-', color='#cccccc',
          linewidth=1.)
  cx.plot(var * glbl_power, np.log2(period), 'k-', linewidth=1.5)
  cx.set_title('c) Global Wavelet Spectrum')
  cx.set_xlabel(r'Power [({})^2]'.format(units))
  cx.set_xlim([0, glbl_power.max() + var])
  cx.set_ylim(np.log2([period.min(), period.max()]))
  cx.set_yticks(np.log2(Yticks))
  cx.set_yticklabels(Yticks)
  pyplot.setp(cx.get_yticklabels(), visible=False)

  # Quarto sub-gráfico, o espectro de ondas médias da escala.
  dx = pyplot.axes([0.1, 0.07, 0.65, 0.2], sharex=ax)
  dx.axhline(scale_avg_signif, color='k', linestyle='--', linewidth=1.)
  dx.plot(t, scale_avg, 'k-', linewidth=1.5)
  dx.set_title(f'd) {period.min():.2f}--{period.max():.2f} day scale-averaged power')
  dx.set_xlabel('Time (Hours)')
  dx.set_ylabel(r'Average variance [{}]'.format(units))
  ax.set_xlim([t.min(), t.max()])

  pyplot.show()

  # esse código sai as imagens perfeitas, se necessitar de algum ajuste, tem que ser feito antes aqui.
