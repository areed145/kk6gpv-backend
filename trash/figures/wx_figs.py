import plotly.graph_objs as go

def figs_wx(df_wx_raw, wind_temp):

	td_max = max(df_wx_raw['temp_f'].max(), df_wx_raw['dewpoint_f'].max()) + 1
	td_min = min(df_wx_raw['temp_f'].min(), df_wx_raw['dewpoint_f'].min()) - 1

	data_td = [
		go.Scatter(x=df_wx_raw.index,
			y=df_wx_raw['temp_f'],
			name='Temperature (F)',
			line=dict(color='rgb(255, 95, 63)', width=3),
			xaxis='x', yaxis='y',
			mode='lines'),
		go.Scatter(x=df_wx_raw.index,
			y=df_wx_raw['dewpoint_f'],
			name='Dewpoint (F)',
			line=dict(color='rgb(255, 127, 63)', width=3),
			xaxis='x', yaxis='y2',
			mode='lines'),
	]

	layout_td = go.Layout(autosize=True,
		height=200,
		yaxis=dict(domain=[0.02, 0.98],
			title='Temperature (F)',
			range=[td_min,td_max],
			fixedrange=True,
			titlefont=dict(color='rgb(255, 95, 63)')
		),
		yaxis2=dict(domain=[0.02, 0.98],
			title='Dewpoint (F)',
			overlaying='y',
			side='right',
			range=[td_min,td_max],
			fixedrange=True,
			titlefont=dict(color='rgb(255, 127, 63)')
		),
		xaxis=dict(type='date', fixedrange=True),
		margin=dict(r=50, t=30, b=30, l=60, pad=0),
		showlegend=False,
	)

	data_pr = [
		go.Scatter(x=df_wx_raw.index, 
			y=df_wx_raw['pressure_in'],
			name='Pressure (inHg)',
			line = dict(color = 'rgb(127, 255, 63)', width = 3),
			xaxis='x', yaxis='y',
			mode='lines'),
			go.Scatter(x=df_wx_raw.index, 
				y=df_wx_raw['relative_humidity'],
				name='Humidity (%)',
				line = dict(color = 'rgb(63, 127, 255)', width = 3),
				xaxis='x', yaxis='y2',
				mode='lines'),
	]

	layout_pr = go.Layout(autosize=True,
		height=200,
		yaxis=dict(domain=[0.02, 0.98],
			title='Pressure (inHg)',
			#range=[0,120],
			fixedrange=True,
			titlefont=dict(color='rgb(127, 255, 63)')
		),
		yaxis2=dict(domain=[0.02, 0.98],
			title='Humidity (%)',
			overlaying='y',
			side='right',
			#range=[0,120],
			fixedrange=True,
			titlefont=dict(color='rgb(63, 127, 255)')
		),
		xaxis=dict(type='date', fixedrange=True),
		margin=dict(r=50, t=30, b=30, l=60, pad=0),
		showlegend=False,
	)

	data_pc = [
		go.Scatter(x=df_wx_raw.index, 
			y=df_wx_raw['precip_1hr_in'],
			name='Precip (in/hr)',
			line = dict(color = 'rgb(31, 190, 255)', width = 3),
			xaxis='x', yaxis='y',
			mode='lines'),
		go.Scatter(x=df_wx_raw.index, 
			y=df_wx_raw['precip_cum_in'],
			name='Precip Cumulative (in)',
			line = dict(color = 'rgb(63, 255, 255)', width = 3),
			xaxis='x', yaxis='y2',
			mode='lines'),
	]

	layout_pc = go.Layout(autosize=True,
		height=200,
		yaxis=dict(domain=[0.02, 0.98],
			title='Precip (in/hr)',
			#range=[0,120],
			fixedrange=True,
			titlefont=dict(color='rgb(31, 190, 255)')
		),
		yaxis2=dict(domain=[0.02, 0.98],
			title='Precip Cumulative (in)',
			overlaying='y',
			side='right',
			#range=[0,120],
			fixedrange=True,
			titlefont=dict(color='rgb(63, 255, 255)')
		),
		xaxis=dict(type='date', fixedrange=True),
		margin=dict(r=50, t=30, b=30, l=60, pad=0),
		showlegend=False,
	)

	data_wd = [
		go.Scatter(x=df_wx_raw.index, 
			y=df_wx_raw['wind_degrees'],
			name='Wind Direction (degrees)',
			marker = dict(color = 'rgb(190, 63, 255)', size = 8, symbol='x'),
			xaxis='x', yaxis='y',
			mode='markers'),
		go.Scatter(x=df_wx_raw.index, 
			y=df_wx_raw['wind_gust_mph'] * 0.869,
			name='Wind Gust (kts)',
			line = dict(color = 'rgb(31, 190, 15)', width = 3),
			xaxis='x', yaxis='y2',
			mode='lines'),
		go.Scatter(x=df_wx_raw.index, 
			y=df_wx_raw['wind_mph'] * 0.869,
			name='Wind Speed (kts)',
			line = dict(color = 'rgb(127, 255, 31)', width = 3),
			xaxis='x', yaxis='y2',
			mode='lines'),
	]

	layout_wd = go.Layout(autosize=True,
		height=200,
		yaxis=dict(domain=[0.02, 0.98],
			title='Wind Direction (degrees)',
			range=[0,360],
			fixedrange=True,
			titlefont=dict(color='rgb(190, 63, 255)')
		),
		yaxis2=dict(domain=[0.02, 0.98],
			title='Wind Speed / Gust (kts)',
			overlaying='y',
			side='right',
			#range=[0,120],
			fixedrange=True,
			titlefont=dict(color='rgb(127, 255, 31)')
		),
		xaxis=dict(type='date', fixedrange=True),
		margin=dict(r=50, t=30, b=30, l=60, pad=0),
		showlegend=False,
	)

	data_su = [
		go.Scatter(x=df_wx_raw.index, 
			y=df_wx_raw['solar_radiation'],
			name='Solar Radiation (W/m<sup>2</sup>)',
			line = dict(color = 'rgb(255, 63, 127)', width = 3),
			xaxis='x', yaxis='y',
			mode='lines'),
		go.Scatter(x=df_wx_raw.index, 
			y=df_wx_raw['UV'],
			name='UV',
			line = dict(color = 'rgb(255, 190, 63)', width = 3),
			xaxis='x', yaxis='y2',
			mode='lines'),
	]

	layout_su = go.Layout(autosize=True,
		height=200,
		yaxis=dict(domain=[0.02, 0.98],
			title='Solar Radiation (W/m<sup>2</sup>)',
			#range=[0,120],
			fixedrange=True,
			titlefont=dict(color='rgb(255, 63, 127)')
		),
		yaxis2=dict(domain=[0.02, 0.98],
			title='UV',
			overlaying='y',
			side='right',
			#range=[0,120],
			fixedrange=True,
			titlefont=dict(color='rgb(255, 190, 63)')
		),
		xaxis=dict(type='date', fixedrange=True),
		margin=dict(r=50, t=30, b=30, l=60, pad=0),
		showlegend=False,
	)

	fig_td = dict(data=data_td, layout=layout_td)
	fig_pr = dict(data=data_pr, layout=layout_pr)
	fig_pc = dict(data=data_pc, layout=layout_pc)
	fig_wd = dict(data=data_wd, layout=layout_wd)
	fig_su = dict(data=data_su, layout=layout_su)

	return fig_td, fig_pr, fig_pc, fig_wd, fig_su