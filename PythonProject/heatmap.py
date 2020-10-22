import pycountry
import plotly.express as px
import pandas as pd


def main():
    covid_data = pd.read_csv("covid_19_clean_complete.csv")
    list_countries = covid_data['Country/Region'].unique().tolist()
    d_country_code = {}
    for country in list_countries:
        try:
            country_data = pycountry.countries.search_fuzzy(country)
            country_code = country_data[0].alpha_3
            d_country_code.update({country: country_code})

        except:
            d_country_code.update({country: ' '})

    for k, v in d_country_code.items():
        covid_data.loc[(covid_data["Country/Region"] == k), 'iso_alpha'] = v

    fig = px.choropleth(data_frame=covid_data,
                        locations="iso_alpha",
                        color="Confirmed",
                        hover_name="Country/Region",
                        color_continuous_scale='YlOrRd',
                        animation_frame="Date")

    fig.show()


if __name__ == '__main__':
    main()
