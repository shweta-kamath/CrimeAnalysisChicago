from shiny import App, render, ui, reactive
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas
import os
import datetime as dt

crimetypes = ['Crime',
       'Arson', 'Assault', 'Battery', 'Burglary',
       'Concealed Carry License Violation', 'Crim Sexual Assault',
       'Criminal Damage', 'Criminal Sexual Assault', 'Criminal Trespass',
       'Deceptive Practice', 'Gambling', 'Homicide', 'Human Trafficking',
       'Interference With Public Officer', 'Intimidation', 'Kidnapping',
       'Liquor Law Violation', 'Motor Vehicle Theft', 'Narcotics',
       'Non - Criminal', 'Non-Criminal', 'Non-Criminal (Subject Specified)',
       'Obscenity', 'Offense Involving Children', 'Other Narcotic Violation',
       'Other Offense', 'Prostitution', 'Public Indecency',
       'Public Peace Violation', 'Ritualism', 'Robbery', 'Sex Offense',
       'Stalking', 'Theft', 'Weapons Violation']

safetytypes = ['All Community Members', 'African American Community',
               'Asian American Community', 'Hispanic Community', 'White Community',
               'All Other Races Community']

path = r'/Users/aditishankar/Documents//GitHub/DP2/final-project-crime_analysis_chicago_finalproject' # Change accordingly
os.chdir(path)
scatter_data = pd.read_csv('Data/scatter_data.csv')

test = pd.read_csv('Data/Crimes_2011_to_2021.csv')

app_ui = ui.page_fluid(
    ui.row(ui.column(12, ui.h2('How do Crimes impact Safety Perceptions? The Relation of Crime and Safety in Chicago'),
                         ui.h3('...a look into crime counts and safety scores in different police districts in the Chicago area.'),
                         align='left')),
    ui.row(ui.column(12, ui.p('Aditi Shankar, Harish Sai, Shweta Kamath'),
                         ui.hr(),
                         align='right')),           
    ui.row(ui.column(4, ui.p('Almost expectedly, crime and safety perceptions do seem to have a link. The crime choropleth shows that, across the years, the crime rates are worse in the South and West sides of the city. Incidentally, in these areas, safety perceptions are also lower than the rest of the city.'),
                         align='left',
                         offset=0.5),
            ui.column(4, ui.input_slider(id = 'years',
                                         label = 'Years', 
                                         min = 2011, max = 2021, value = 1, sep = "")),
            ui.column(4, ui.input_slider(id = 'safetyyears',
                        label = 'Years', 
                        min = 2018, max = 2021, value = 1, sep = ""))),
    ui.row( ui.column(4, ui.p('On dissecting safety scores by communities, we see that African Americans and Asians feel the least safe in Chicago, especially in South, West and South-West areas.'),
                         align='left',
                         offset=0.2),
            ui.column(4, ui.input_select(id = 'chars',
                                         label = 'Total or Primary Crime Type:',
                                         choices= crimetypes)),
            ui.column(4, ui.input_select(id = 'sentiment',
                                         label = 'Total or Ethnic Community:',
                                         choices= safetytypes))),
    ui.row( ui.column(4, ui.p('Historically, these are the areas that are known to be at the end of police brutality which could explain reduced safety perception.'),
                         ui.p('Moreover, regardless of crime type, there is a disproportionate number of incidents in the South and West sides. Especially bad is assualt, which has repeatedly seen over 1400 cases a year in the Southern police districts.'),
                         ui.p('Interestingly, if we toggle the L train routes, we see the the South Side has less access to the trains. While the red line makes it part of the south, it mostly remains uncovered by the L.'),
                         ui.p("Districts in the North had comparatively low levels of crime, and higher safety scores across all communities. This is maintained across the years in our analysis, as well as for all the different kinds of crime."),
                         align='left',
                         offset=0.2),
            ui.column(4, ui.output_plot("chars"),
                         align='center'),
            ui.column(4, ui.output_plot("sentiment"),
                         align='center')),
    ui.row(ui.column(12, ui.input_switch(id = 'trains',
                                        label = 'Switch on for L-Train Lines'),
                    align = 'right')),
    ui.row( ui.column(12, ui.h5("Correlation between crime and perception of safety"),
              align='left')),
            ui.column(12, ui.input_select(id='scatter',
                                        label='Please pick a district',
                                        choices=['1','2','3','4','5','6','7','8','9','10','11','12','14','15','16','17','18','19','20','22','24','25']),
                        align='center'),
            
    ui.row( ui.column(6, ui.output_plot(id='scatter'),
                         align='left'),
            ui.column(6, ui.p("Regressing mean safety scores on actual crime on a monthly basis at a district level indicated a weak correlation of -0.0077. A possible explanation of this could be that safety perceptions are hard to change even with relative changes in crime."),
                         ui.p("We can explore this by plotting the relationship between the variables by selecting different districts from the dropdown. Across selections, we generally observe somewhat of a scattered relationship for the police districts."),
                         ui.p("Investigation of micro-level characteristics beyond actual crime is required for more comprehensive insight on what impacts safety perceptions."))) 
)


def server(input, output, session):
    @reactive.Calc
    def get_cta_data():

        df_rails = geopandas.read_file('Data/CTA_RailLines/CTA_RailLines.shp')
        return df_rails

    @reactive.Calc
    def get_crime_data():

        df_police = geopandas.read_file('Data/PoliceDistrict/PoliceDistrict.shp')
        df_police = df_police.rename(columns={"DIST_NUM":"District"})
        df_police['District'] = df_police['District'].astype('int')
        crimes = pd.read_csv('Data/Crimes_2011_to_2021.csv')
        crimes = crimes.dropna(subset=['District'])
        crimes['District'] = crimes['District'].astype('int')

        counts = crimes.groupby(['Year', 'District']).size()
        counts = counts.reset_index(name='Crime') 

        filtered = crimes[['District', 'Year', 'Primary Type']]
        typedivided = pd.pivot_table(filtered, index=['Year','District'], columns="Primary Type", aggfunc=len, fill_value=0)
        typedivided = typedivided.reset_index()

        final_crimes = counts.merge(typedivided, on=['Year', 'District'], how='right')
        final_crimes.columns = map(str.title, final_crimes.columns)
        final_crimes = df_police.merge(final_crimes, on = 'District', how = 'inner')
        final_crimes = final_crimes.reset_index()

        return final_crimes

    @reactive.Calc
    def get_safety_data():

        senti = pd.read_csv('Data/Police_Sentiment_Scores.csv')
        senti = senti.dropna(subset=['DISTRICT'])
        senti['DISTRICT'] = senti['DISTRICT'].astype('int')

        senti['START_DATE'] = pd.to_datetime(senti['START_DATE'])
        senti['year'] = senti['START_DATE'].dt.year
        senti = senti.sort_values(by=['year'])
        senti = senti.groupby(['year', 'DISTRICT']).mean()
        senti = senti.reset_index()
        senti = senti[senti['year'] < 2022]
        senti = senti[senti['year'] > 2017]
        senti = senti.rename(columns={"DISTRICT":"District"})
        senti.columns = map(str.title, senti.columns)
        senti = senti.rename(columns={"S_Race_African_American":"African American Community",
                                      "S_Race_Asian_American":"Asian American Community",
                                      "S_Race_Hispanic":"Hispanic Community",
                                      "S_Race_White":"White Community",
                                      "S_Race_Other":"All Other Races Community",
                                      "Safety":"All Community Members"})

        df_police = geopandas.read_file('Data/PoliceDistrict/PoliceDistrict.shp')
        df_police = df_police.rename(columns={"DIST_NUM":"District"})
        df_police['District'] = df_police['District'].astype('int')
        
        sentiment = df_police.merge(senti, on = 'District', how = 'inner')

        return sentiment
        
    @output
    @render.plot
    def chars():

        df = get_crime_data()
        df_cta = get_cta_data()

        def get_col(l): # for colours of L trains *from Prof Levy's Code*
            if 'Blue' in l:
                return 'b'
            elif 'Red' in l:
                return 'r'
            elif 'Purple' in l:
                return 'purple'
            elif 'Brown' in l:
                return 'brown'
            elif 'Yellow' in l:
                return 'yellow'
            elif 'Green' in l:
                return 'green'
            elif 'Pink' in l:
                return 'pink'
            elif 'Orange' in l:
                return 'orange'
        color_dict = {l:get_col(l) for l in df_cta['LINES'].unique()}
        color_dict

        fig, ax = plt.subplots(figsize=(16,16))

        for year, variable in zip([input.years()], [input.chars()]): # changing according to the input variables
            df[df['Year'] == year].plot(ax=ax, color='white', edgecolor='black');
            df[df['Year'] == year].plot(ax=ax, column=variable, legend=True)
            ax.set_title(f'Counting the total cases of\n{variable}\nin Chicago Police Districts in {year}.')
            if input.trains() == True:
                for line in df_cta['LINES']:
                    c = color_dict[line]
                    df_cta[df_cta['LINES'] == line].plot(ax = ax, color = c, alpha=1, linewidth=1) # adding a layer if toggle is 'on'
        ax.axis('off')
        return ax;

    @output
    @render.plot
    def sentiment():

        df = get_safety_data()
        df_cta = get_cta_data()

        def get_col(l): # for colours of L trains *from Prof Levy's Code*
            if 'Blue' in l:
                return 'b'
            elif 'Red' in l:
                return 'r'
            elif 'Purple' in l:
                return 'purple'
            elif 'Brown' in l:
                return 'brown'
            elif 'Yellow' in l:
                return 'yellow'
            elif 'Green' in l:
                return 'green'
            elif 'Pink' in l:
                return 'pink'
            elif 'Orange' in l:
                return 'orange'
        color_dict = {l:get_col(l) for l in df_cta['LINES'].unique()}
        color_dict

        fig, ax = plt.subplots(figsize=(16,16))

        for year, variable in zip([input.safetyyears()], [input.sentiment()]): # changing according to the input variables
            df[df['Year'] == year].plot(ax=ax, color='white', edgecolor='black');
            df[df['Year'] == year].plot(ax=ax, column=variable, legend=True)
            ax.set_title(f'Safety Perceptions for \n{variable}\nin Chicago Police Districts in {year}')
            if input.trains() == True:
                for line in df_cta['LINES']:
                    c = color_dict[line]
                    df_cta[df_cta['LINES'] == line].plot(ax = ax, color = c, alpha=1, linewidth=1) # adding a layer if toggle is 'on'
        ax.axis('off')
        return ax;

    @output
    @render.plot  
    def scatter():
        fig, ax = plt.subplots()
        df_scatter = scatter_data[scatter_data['District']==int(input.scatter())]
        ax = sns.scatterplot(data=df_scatter, x="crime", y="SAFETY")
        ax.set_ylabel('Mean safety scores (monthly)')
        ax.set_xlabel('Crime count (monthly)')
        ax.set_title(f'Relationship between crime counts and safety scores\nin police district {input.scatter()}')
        return ax
    
app = App(app_ui, server) 

# Source: 
    # DP 2 lecture and lab  13 and 14 slides
