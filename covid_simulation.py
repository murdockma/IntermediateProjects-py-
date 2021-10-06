import numpy as np
import pandas as pd
import altair as alt

class CovidSimulation():
    
    def __init__(self,p_covid_treat, p_covid_control, totalN):
#         self.p_covid = p_covid
#         self.N= N
        self.p_covid_treat = p_covid_treat
        self.p_covid_control = p_covid_control
        self.totalN = totalN

    def sample(self, p_covid, N):

        return np.random.choice([0, 1], N, p=[1-p_covid,p_covid])

    def make_data_frame(self):

        treatment = self.sample(self.p_covid_treat, int(self.totalN/2))
        control = self.sample(self.p_covid_control, int(self.totalN/2))

        N_covid_control = np.sum(control) # np.sum([0, 1, 0, 0, 1, 1]) = 3
        N_no_covid_control = control.size - N_covid_control

        N_covid_treatment = np.sum(treatment)  # np.sum([0, 1, 0, 1, 1, 1]) = 4
        N_no_covid_treatment = treatment.size - N_covid_treatment

        group = ["treatment", "treatment", "control", "control"]
        covid = [True, False, True, False]
        count = [N_covid_treatment, N_no_covid_treatment, N_covid_control, N_no_covid_control]
        
        return pd.DataFrame({"group": group, "count": count, "covid": covid})
    
    def make_plot(self,df):
        treat = df[df["group"] == "treatment"]
        control = df[df["group"] == "control"] 

        treat_chart = alt.Chart(treat).mark_bar().encode(
        x='covid',
        y='count'
        ).properties(title="treatment")

        control_chart = alt.Chart(control).mark_bar().encode(
            x='covid',
            y='count'
        ).properties(title="control")

        return treat_chart | control_chart

    def make_plot_2(self,df):

        plot2 = df[df["covid"] == True][["group", "count"]]#selecting the group and count

        max_ = max(plot2["count"]) #pulling max count from count column of dataframe
        plot2["is_max"] = plot2["count"] == max_  #adding is_max column and is True if count is max (adding a new feature to dataframe)

        _chart = alt.Chart(plot2).mark_bar().encode(
            x='group',
            y='count',
            color="is_max",
            tooltip="count"
        ).properties(title="# covid", width=50, height=100)

        return _chart
      
      
      
    
# make_plot_2 is simply a better visual representation of the charts... 

# ways to run this 

## intialize our instance with specified probabilities, assign a variable (df) to the make_data_frame instance, 
## pass the data frame through our make_plot method (can do make_plot_1 or 2)
inst = CovidSimulation(p_covid_treat=.1, p_covid_control=.11, totalN=100000)
df = inst.make_data_frame()
inst.make_plot_2(df)

# Way to run several tests to identify trends / abnormalities
## interate through any range (range is number of simulations), assign variable to make data_frame method, 
## pass data frame through make_plot and assign a varible to the instance, append plots and use hconcat to display all at once
all_ = []
for j in range(8):
    df = inst.make_data_frame() # creating dataframe
    plot1 = inst.make_plot_2(df) 
    all_.append(plot1) 

alt.hconcat(*all_) 


