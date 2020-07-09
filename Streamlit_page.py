import streamlit as st
import pandas as pd

def main():
    st.sidebar.image('LOGO_TONELLO.JPG', width=250)
    st.title('CFC Tonello')

    file  = st.sidebar.file_uploader('Arquivo das aulas (.csv)', type = 'csv')
    st.sidebar.image('https://media.giphy.com/media/KyBX9ektgXWve/giphy.gif', width=250)
    if file is not None:
        df = pd.read_csv(file)
        st.markdown('Número total de aulas dadas por todos os instrutores:')
        st.markdown(df.shape[0])
        st.markdown(' ')
    
        df['comeco_aula'] = df['Horário'].astype(str).str.slice(0,5)
        df['final_aula'] = df['Horário'].astype(str).str.slice(-5)
        df['comeco_aula'] = pd.to_datetime(df[['Data', 'comeco_aula']].agg(' '.join, axis=1), format='%d/%m/%Y %H:%M')
        df['final_aula'] = pd.to_datetime(df[['Data', 'final_aula']].agg(' '.join, axis=1), format='%d/%m/%Y %H:%M')

        df['tempo_aula'] = (df['final_aula'] - df['comeco_aula'])
        df['n_aula'] = df['tempo_aula'].astype('timedelta64[m]') / 50

        df = df.drop(['CFC','CPF do instrutor', 'CPF do aluno', 'Periodo'], axis=1)
        df = df.drop(['Data','Horário', 'tempo_aula', 'Biometria'], axis=1)

        df = df[['Instrutor', 'Categoria' , 'comeco_aula', 'final_aula', 'n_aula', 'Aluno', 'Veículo', 'KM', \
            'KM Inicial', 'KM Final', 'Status']]
        
        instrutores = list(df['Instrutor'].unique())
        
        instrutor = st.selectbox('Selecione um instrutor:', instrutores)
        df_instrutor = df[df['Instrutor'] == instrutor]
        
        total = df_instrutor.shape[0]
        df_instrutor = df_instrutor[df_instrutor['Status'].str.find('Cancelada') == -1]
        validas = df_instrutor.shape[0]

        
        st.write('Aulas canceladas:', total - validas)

        df_catB = df_instrutor[df_instrutor['Categoria'] == 'B']
        df_catA = df_instrutor[df_instrutor['Categoria'] == 'A']

        aulasB = df_catB['n_aula'].sum()
        st.write('Aulas categoria B:', aulasB)

        aulasA = df_catA['n_aula'].sum() * 0.5
        st.write('Aulas categoria A:', aulasA)

        st.write('Total:', (aulasB + aulasA))



        categorias = list(df['Categoria'].unique())
        cat = st.selectbox('Selecione uma categoria:', categorias)
        df_categorias = df_instrutor[df_instrutor['Categoria'] == cat]
        num = st.slider('Escolha o numero de aulas que deseja ver', min_value=5, max_value=df_categorias.shape[0])
        st.dataframe(df_categorias.head(num))
    
    else:
        st.subheader('Escolha o arquivo...')


if __name__ == '__main__':
    main()