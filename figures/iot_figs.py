import plotly.graph_objs as go

cs = [
        [0.0,'#424ded'],
        [0.1,'#4283ed'],
        [0.2,'#42d0ed'],
        [0.3,'#42edae'],
        [0.4,'#78ed42'],
        [0.5,'#d6ed42'],
        [0.6,'#edde42'],
        [0.7,'#f4af41'],
        [0.8,'#f48541'],
        [0.9,'#f44741'],
        [1.0,'#f44298']
        ]

def fig_iot(dfs):
    data = []
    for df in dfs:
        data.append(
            go.Scatter(x=df['last_changed'], 
                            y=df['state'],
                            name=df['entity_id'][0],
                            line = dict(#color = 'rgb(255, 95, 63)',
                                shape='vh',
                                width = 3),
                            mode='lines')
            )

    layout = go.Layout(autosize=True)

    fig = dict(data=data, layout=layout)
    return fig

def fig_temp_hum(df_iot_temperature, df_iot_humidity):
    data = [
        go.Scatter(x=df_iot_temperature['timestamp'], 
            y=df_iot_temperature['value'],
            name='Temperature (C)',
            line = dict(color = 'rgb(255, 95, 63)',
                shape='vh',
                width = 3),
            mode='lines'),
        go.Scatter(x=df_iot_humidity['timestamp'], 
            y=df_iot_humidity['value'],
            name='Humidity (%)',
            line = dict(color = 'rgb(63, 127, 255)',
                shape='vh',
                width = 3),
            mode='lines'),
            ]

    layout = go.Layout(autosize=True)

    fig = dict(data=data, layout=layout)
    return fig

def swap_underscore(val):
    return float(val.replace('_','.'))

def figs_vib(df_iot_vib):
    df_iot_vib_hm = df_iot_vib.melt(id_vars=['timestamp'], value_vars=df_iot_vib.columns.drop(['truth','timestamp','topic','maj_pk','_id']))
    #df_iot_vib_hm['variable'] = df_iot_vib_hm['variable'].apply(swap_underscore)
    df_iot_vib_hm['variable'] = df_iot_vib_hm['variable'].astype('float')
    df_iot_vib_hm = df_iot_vib_hm[df_iot_vib_hm['variable'] > 50]

    data_qc = [
            go.Scatter(x=df_iot_vib['timestamp'], 
                            y=df_iot_vib['truth'],
                            name='Truth (Hz)',
                            line = dict(color = 'rgb(255, 95, 63)',
                                        width = 3),
                            mode='lines'),
            go.Scatter(x=df_iot_vib['timestamp'], 
                            y=df_iot_vib['maj_pk'],
                            name='Major Peak (Hz)',
                            line = dict(color = 'rgb(63, 127, 255)',
                                        width = 3),
                            mode='lines'),
            ]

    layout_qc = go.Layout(autosize=True)
    
    data_hm = [
            go.Heatmap(x=df_iot_vib_hm['timestamp'], 
                            y=df_iot_vib_hm['variable'],
                            z=df_iot_vib_hm['value'],
                            colorscale = cs,
                            connectgaps = True,
                            zsmooth = 'best',
            ),
    ]

    layout_hm = go.Layout(autosize=True)

    df_iot_vib_fft = df_iot_vib[:1].melt(id_vars=['timestamp'], value_vars=df_iot_vib.columns.drop(['truth','timestamp','topic','maj_pk','_id']))
    #df_iot_vib_fft['variable'] = df_iot_vib_fft['variable'].apply(swap_underscore)
    df_iot_vib_fft['variable'] = df_iot_vib_fft['variable'].astype('float')
    df_iot_vib_fft = df_iot_vib_fft[df_iot_vib_fft['value'] > 0]
    df_iot_vib_fft.sort_values('variable', inplace=True)
    
    df_iot_vib_fft1 = df_iot_vib[2:3].melt(id_vars=['timestamp'], value_vars=df_iot_vib.columns.drop(['truth','timestamp','topic','maj_pk','_id']))
    #df_iot_vib_fft['variable'] = df_iot_vib_fft['variable'].apply(swap_underscore)
    df_iot_vib_fft1['variable'] = df_iot_vib_fft1['variable'].astype('float')
    df_iot_vib_fft1 = df_iot_vib_fft1[df_iot_vib_fft1['value'] > 0]
    df_iot_vib_fft1.sort_values('variable', inplace=True)
    
    df_iot_vib_fft2 = df_iot_vib[4:5].melt(id_vars=['timestamp'], value_vars=df_iot_vib.columns.drop(['truth','timestamp','topic','maj_pk','_id']))
    #df_iot_vib_fft['variable'] = df_iot_vib_fft['variable'].apply(swap_underscore)
    df_iot_vib_fft2['variable'] = df_iot_vib_fft2['variable'].astype('float')
    df_iot_vib_fft2 = df_iot_vib_fft2[df_iot_vib_fft2['value'] > 0]
    df_iot_vib_fft2.sort_values('variable', inplace=True)
    

    data_fft = [
            go.Scatter(x=df_iot_vib_fft2['variable'], 
                            y=df_iot_vib_fft2['value'],
                            name='FFT_-2',
                            line = dict(color = 'rgb(244, 199, 65)',
                                        width = 3),
                            mode='lines'),
            go.Scatter(x=df_iot_vib_fft1['variable'], 
                            y=df_iot_vib_fft1['value'],
                            name='FFT_-1',
                            line = dict(color = 'rgb(244, 167, 66)',
                                        width = 3),
                            mode='lines'),
            go.Scatter(x=df_iot_vib_fft['variable'], 
                            y=df_iot_vib_fft['value'],
                            name='FFT_0',
                            line = dict(color = 'rgb(255, 95, 63)',
                                        width = 3),
                            mode='lines'),
    ]

    layout_fft = go.Layout(autosize=True)

    vib_qc = dict(data=data_qc, layout=layout_qc)
    vib_hm = dict(data=data_hm, layout=layout_hm)
    vib_fft = dict(data=data_fft, layout=layout_fft)

    return vib_hm, vib_fft, vib_qc