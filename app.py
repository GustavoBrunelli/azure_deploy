import pandas as pd
import numpy as np
import random
import streamlit as st

st.set_page_config( 
    #ref: https://docs.streamlit.io/library/api-reference/utilities/st.set_page_config
    page_title="Planning Tool - CoE Demo",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="https://symbols.getvecta.com/stencil_4/38_google-cloud-operations.092484e6da.svg"
    )

with st.sidebar:
    #not working st.image("https://drive.google.com/file/d/1boRbGXcUNXK8aexp8jI71moXhUdMPl9H/view?usp=sharing")
    st.title("App Settings")
    with st.expander("Login", expanded=True):
        Email = st.text_input('Enter your email:', type='password')
        Pass = st.text_input('Enter your password:', type='password')
        if not(len(Email)==40) and (len(Pass)==4):
            st.warning('Please enter your credentials!', icon='⚠️')
    Rev_edit_flag = not(st.checkbox('Edit Mode', value=True))
    if Rev_edit_flag == True:
        st.info('Read-Only mode.', icon="ℹ️")

def format_as_percent(value): #function to format to percent
    return f'{value:.1%}'
def rerun(): #rerun all
    st.session_state.rerun = True

#App titles
st.title("AOP Planning Tool")
st.write("This is a demo version - dummy data.")

tab1, tab2, tab3, tab4 = st.tabs(["Total AOP", "Direct AOP", "Indirect AOP", "Executive View"])
with tab1: #titles
    col1, col2, col3 = st.columns([2,2,1])
    with col1:
        st.write("Here you can adjust Rev data.")
    with col2:
        st.write("Here you can adjust Rev data.")
    with col3:
        st.write("Here you can adjust Mgn percent data.")
with tab2: #titles
    col4, col5= st.columns([1,1])
    with col4:
        st.write("Margin")
    with col5:
        st.write("Margin%")


if 'df' not in st.session_state: #will only run once
    st.session_state.rerun = False
    Region = ['Andean', 'Andean', 'Andean', 'Andean', 'Andean', 'Andean', 'Brazil', 'Brazil', 'Brazil', 'Brazil', 'Brazil', 'Brazil', 'Mexico', 'Mexico', 'Mexico', 'Mexico', 'Mexico', 'Mexico', 'NOLA', 'NOLA', 'NOLA', 'NOLA', 'NOLA', 'NOLA', 'South Cone', 'South Cone', 'South Cone', 'South Cone', 'South Cone', 'South Cone']
    LOB = ['Servers', 'Servers', 'Networking', 'Networking', 'EI', 'EI', 'Servers', 'Servers', 'Networking', 'Networking', 'EI', 'EI', 'Servers', 'Servers', 'Networking', 'Networking', 'EI', 'EI', 'Servers', 'Servers', 'Networking', 'Networking', 'EI', 'EI', 'Servers', 'Servers', 'Networking', 'Networking', 'EI', 'EI']
    Subregion = ['Colombia_Ecuador', 'Peru', 'Colombia_Ecuador', 'Peru', 'Colombia_Ecuador', 'Peru', 'Corporate', 'Enterprise', 'Corporate', 'Enterprise', 'Corporate', 'Enterprise', 'Corporate', 'Enterprise', 'Corporate', 'Enterprise', 'Corporate', 'Enterprise', 'Puerto Rico', 'Rest of NOLA', 'Puerto Rico', 'Rest of NOLA', 'Puerto Rico', 'Rest of NOLA', 'ARG_PRY_URY', 'Chile_Bolivia', 'ARG_PRY_URY', 'Chile_Bolivia', 'ARG_PRY_URY', 'Chile_Bolivia']
    Rev = [32, 17, 9, 12, 3, 2, 4, 2, 8, 32, 5, 1, 12, 23, 12, 2, 32, 7, 4, 31, 3, 21, 3, 21, 1, 12, 3, 18, 2, 26]
    Mgn = [3.84, 2.04, 1.08, 1.44, 0.36, 0.24, 0.48, 0.24, 0.96, 3.84, 0.6, 0.12, 1.44, 2.76, 1.44, 0.24, 3.84, 0.84, 0.48, 3.72, 0.36, 2.52, 0.36, 2.52, 0.12, 1.44, 0.36, 2.16, 0.24, 3.12]
    
    #creating dataset original
    st.session_state.df = pd.DataFrame({'Region': Region,'LOB': LOB,'Subregion': Subregion,'Rev': Rev,'Mgn': Mgn})

    #sample dataset for trendline
    sample_df = pd.DataFrame({"Trendline": [[random.randint(1, 100), random.randint(1, 100), random.randint(1, 100)] for _ in range(30)]})
    st.session_state.df = pd.concat([st.session_state.df, sample_df], axis=1)

    #creating dataset lob
    st.session_state.df_lob = st.session_state.df.drop("Subregion", axis=1).groupby(["Region", "LOB"]).sum().reset_index()
    st.session_state.df_lob = st.session_state.df_lob.sort_values(by='LOB', ascending=False)
    st.session_state.df_lob['Rev Mix'] = st.session_state.df_lob['Rev'] / st.session_state.df_lob.groupby('LOB')['Rev'].transform('sum')
    st.session_state.df_lob['Adj'] = 0
 
#calculated columns
st.session_state.df_lob['Rev non Adj'] = st.session_state.df_lob.apply(lambda row: row['Rev'] if row['Adj'] == 0 else None, axis=1)
st.session_state.df_lob['Mix Rev'] = st.session_state.df_lob['Rev non Adj']/st.session_state.df_lob.groupby('LOB')['Rev non Adj'].transform('sum')
st.session_state.df_lob['Auto Adj'] =  st.session_state.df_lob.groupby('LOB')['Adj'].transform('sum') * st.session_state.df_lob['Mix Rev'] *-1
st.session_state.df_lob['Rev Adjusted'] = st.session_state.df_lob.apply(lambda row: row['Rev']+row['Adj'] if row['Adj'] != 0 else row['Rev']+row['Auto Adj'], axis=1)
st.session_state.df_lob['Auto Adj'] = st.session_state.df_lob['Auto Adj'].replace(0, np.nan)

with tab1: #Total tab
    with col1:
        st.session_state.df_lob = st.session_state.df_lob.style.format({
            'Rev Mix': format_as_percent,
            'Mix Rev': format_as_percent,
            'Adj': '{:.3f}',
            'Rev Adjusted': '{:.3f}',
            'Auto Adj': '{:.3f}'})

        st.session_state.df_lob = st.data_editor(
            st.session_state.df_lob,
            on_change=rerun,
            column_config={
                "Adj": st.column_config.Column(required=True, disabled=Rev_edit_flag),
                "Trendline": st.column_config.LineChartColumn(y_min=0, y_max=100, width="small"),
                "Mgn": None, 
                "Rev non Adj": None, 
                "Mix Rev": None
                },
            disabled=["Region", "LOB", "Rev", "Auto Adj", "Rev Mix", "Rev non Adj", "Mix Rev", "Rev Adjusted"],
            hide_index=True,
            height=570,
            use_container_width=False)

        #info message
        unique_lobs_list = st.session_state.df_lob['LOB'].unique().tolist()
        warning_text = ""
        info_text = ""
        for lob in unique_lobs_list:
            df_for_check = st.session_state.df_lob[st.session_state.df_lob['LOB'] == lob]
            Rev_Adj_all_regions = not any(df_for_check['Adj'] == 0)
            Rev_Adj = df_for_check['Adj'].sum()*-1

            if Rev_Adj_all_regions == True:
                check = df_for_check['Rev Adjusted'].sum() - df_for_check['Rev'].sum()
                w_text = f'{lob} - All regions were manually adjusted. Remaining difference: {check}.'
                warning_text += w_text + "\n"
            elif Rev_Adj != 0:
                regions_adjusted = ' '.join(df_for_check.loc[df_for_check['Adj'] != 0, 'Region'])
                Regions_not_adjusted = ' '.join(df_for_check.loc[df_for_check['Adj'] == 0, 'Region'])
                i_text = (lob + ' - Revenue was manually adjusted (' + regions_adjusted + ') and ' +  "{:.2f}".format(Rev_Adj) + ' was automatically redistributed for remaining regions (' + Regions_not_adjusted + ') according to historical mix.')
                info_text += i_text + "\n"
        
        expander_flag = True if warning_text != "" or info_text != "" else False
        with st.expander("Automatic redistribution status:", expanded=expander_flag):
            if expander_flag == False:
                st.write("No changes were made.")
            if warning_text != "":
                st.warning("Automatic revenue redistribution deactivated for:", icon="⚠️")
                st.markdown(warning_text.replace('\n', '<br>'), unsafe_allow_html=True)
            if info_text != "":
                st.info("Revenue was automatically redistributed for:", icon="ℹ️")
                st.markdown(info_text.replace('\n', '<br>'), unsafe_allow_html=True)

        
if st.session_state.rerun == True:
    st.session_state.rerun = False
    st.experimental_rerun()












#st.warning('Automatic redistribution deactivated (all regions were manually adjusted).', icon="⚠️")
        #st.info('Revenue was manually adjusted (' + regions_adjusted + ') and ' +  "{:.2f}".format(Rev_Adj) + ' was automatically redistributed for remaining regions (' + Regions_not_adjusted + ') according to historical mix.', icon="ℹ️")



with tab2: #Data table (only test, not usefull now)
    with col4:
        st.write(st.session_state.df)
    with col5:
        chart_data = pd.DataFrame(np.random.randn(20, 3),columns=['a', 'b', 'c'])
        st.line_chart(chart_data)
    #with col4:
        #st.bar_chart(st.session_state.df[['Region', 'Rev', 'Rev Adjusted']].groupby('Region').sum())
        #st.line_chart(st.session_state.df[['Rev', 'Rev Adjusted']])
with tab4:
    url = "https://app.powerbi.com/reportEmbed?reportId=43ce1afb-3849-42a7-94fe-fdc3920641f9&autoAuth=true&ctid=945c199a-83a2-4e80-9f8c-5a91be5752dd"
    st.markdown(f'<iframe width="1140" height="900" src="{url}" frameborder="0" allowfullscreen></iframe>', unsafe_allow_html=True)
