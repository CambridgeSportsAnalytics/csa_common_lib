import os

if os.getenv('LAMBDA_ENV') == None:
      from plotnine import *
      import pandas as pd
      
import numpy as np

def y_actual_means_graph(data,filepath):
    """
    Creates the barplot of Y actual means when Yhat is low and high and fit is low and high.
    data: Input dataframe of y_actual_means from a model_analysis result.
    filepath: The folder to save the plot in.
    """
    #Make the index a column so it can be plotted
    data.reset_index(drop=False,inplace=True)
    data = round(data,2)
    
    #insert blank rows to create spacing in graph
    blank1 = ['',np.nan]
    blank2 = [' ',np.nan]
    data.loc[0.5] = blank1
    data.loc[3.5] = blank2
    data = data.sort_index().reset_index(drop=True)

    #set up index to plot in the order we want
    data['index'] = pd.Categorical(data['index'],categories=list(reversed(data['index'])),ordered=True)
    
    #external graph parameters to be used in graph
    font_size = 10
    font_color = 'black'
    colors = ['#BFBFBF','#FFFFFF','#1F497D','#C0504D','#404040','#FFFFFF','#1F497D','#C0504D','#404040']
    color_mapping = dict(zip(data['index'],colors))
    data['alignment'] = data['Y Actual Mean'].apply(lambda x: 'left' if x > 0 else 'right')
    
    #create graph with the data
    plot = (ggplot(data,aes(x='index',y="Y Actual Mean",fill='index')) + #input data, sets the x and y axes
                    geom_bar(stat='identity',position='dodge') + #create bar plot
                    coord_flip() + #flips the coordinates so that the y axis is the categories and the x axis is the means
                    geom_hline(yintercept=0,color='black',size=0.5) + #add in y axis line
                    theme(
                          axis_text_x=element_blank(), #no x axis labels
                          axis_ticks=element_blank(), #take tick marks off axes
                          panel_grid=element_blank(), #turn off gridlines
                          panel_background=element_blank(), #no background on the plot area
                          axis_text_y = element_text(size=font_size,color=font_color), #set the font of the y axis so it matches bar labels
                          legend_position='none') + #turn off legend for fill colors
                    geom_text(
                              aes(label=data['Y Actual Mean'].apply(lambda x: f"{x:.2f}"), y='Y Actual Mean',ha=data['alignment']), #add bar labels, round to 2 decimals, set their aligments
                              va='center', #vertical alignment
                              position=position_dodge(width=0.9), #ensure the labels don't overlap
                              size=font_size,color=font_color) + #set font size to match y axis
                    scale_fill_manual(values=color_mapping) + #fill the bars with colors set above
                    labs(x='',y='',title='')) # turn off axis titles
    
    #Save plot to file path input
    plot_file = f"{filepath}\\y_actual_means_graph.png"
    plot.save(plot_file,width=14,height=8)
    
    return(plot_file)


def info_weighted_co_occurrence_graph(data,filepath):
    """
    Creates the barplot of info weighted co-occurrence when Yhat is low and high and fit is low and high.
    data: Input dataframe of info weighted co-occurrence from a model_analysis result.
    filepath: The folder to save the plot in.
    """
    #Make the index a column so it can be plotted    
    data.reset_index(drop=False,inplace=True)
    
    #insert blank rows to create spacing in graph
    blank1 = ['',np.nan]
    blank2 = [' ',np.nan]
    data.loc[2.5] = blank1
    data.loc[5.5] = blank2
    data = data.sort_index().reset_index(drop=True)

    #set up index to plot in the order we want
    data['index'] = pd.Categorical(data['index'],categories=list(reversed(data['index'])),ordered=True)
    
    #external graph parameters to be used in graph
    font_size = 10
    font_color = 'black'
    data['alignment'] = data['Informativeness Weighted Co-Occurrence'].apply(lambda x: 'left' if x > 0 else 'right')
    colors = ['#1F497D','#C0504D','#404040','#FFFFFF','#1F497D','#C0504D','#404040','#FFFFFF','#1F497D','#C0504D','#404040']
    color_mapping = dict(zip(data['index'],colors))

    #create graph with the data
    plot = (ggplot(data,aes(x='index',y="Informativeness Weighted Co-Occurrence",fill='index')) + #input data, sets the x and y axes
                    geom_bar(stat='identity',position='dodge') + #create bar plot
                    coord_flip() + #flips the coordinates so that the y axis is the categories and the x axis is the means
                    geom_hline(yintercept=0,color='black',size=0.5) + #add in y axis line
                    theme(
                          axis_text_x=element_blank(), #no x axis labels
                          axis_ticks=element_blank(), #take tick marks off axes
                          panel_grid=element_blank(), #turn off gridlines
                          panel_background=element_blank(), #no background on the plot area
                          axis_text_y = element_text(size=font_size,color=font_color), #set the font of the y axis so it matches bar labels
                          legend_position='none') + #turn off legend for fill colors
                    geom_text(aes(label=data['Informativeness Weighted Co-Occurrence'].apply(lambda x: f"{x:.2f}"), y='Informativeness Weighted Co-Occurrence',ha=data['alignment']), #add bar labels, round to 2 decimals, set their aligments
                              va='center', #vertical alignment
                              position=position_dodge(width=0.9), #ensure the labels don't overlap
                              size=font_size,color=font_color) + #set font size to match y axis
                    scale_fill_manual(values=color_mapping) + #fill the bars with colors set above
                    labs(x='',y='',title='')) # turn off axis titles
    
    #save plot image
    plot_file = f"{filepath}\\info_weighted_co_occurrence_graph.png"
    plot.save(plot_file,width=14,height=8)
    
    return(plot_file)

def variable_importance_graph(data,filepath):
    """
    Returns the variable importance graph plotted with medians and percentiles.
    data: Input dataframe of variable importance from a model_analysis result.
    filepath: The folder to save the plot in.
    """
    #make index a column so it can be plot
    data.reset_index(drop=False,inplace=True)
    
    #melt data to plot every point
    percentiles = ['5th Percentile','20th Percentile','50th Percentile','80th Percentile','95th Percentile']
    melted_data = data.melt(id_vars='index',value_vars=percentiles,var_name='Percentile',value_name='Value')
    order = data.sort_values(by='Median',ascending=False)['index'].to_list()
    melted_data['index'] = pd.Categorical(melted_data['index'], categories=order, ordered=True)

    #set y scale manually
    y_min = melted_data['Value'].min() - 0.001
    y_max = melted_data['Value'].max() + 0.001

    #set colors manually
    colors = ['#1F497D','#C0504D','#404040','#C0504D','#1F497D']
    color_mapping = dict(zip(percentiles,colors))

    #create line chart
    plot = (ggplot(melted_data, aes(x='index', y='Value', group='Percentile', color='Percentile')) + #set x and y and data to plot
                geom_line() + #add lines
                geom_point() + #add points alonge each line
                ylim(y_min, y_max) + #set y scale to the values set above
                theme(
                      axis_text_x=element_text(rotation=90), #rotate x axis labels 90 degrees
                      legend_position = 'bottom', 
                      legend_title = element_blank(), #no legend title
                      legend_box = 'horizontal', #make legend go horizontally across the bottom
                      panel_grid_major_y = element_blank(), #turn off y gridlines
                      panel_grid_minor_y = element_blank()) + #turn off y gridlines
                labs(x='',y='',title='') +
                scale_color_manual(values=color_mapping,limits=percentiles)
                )
    
    #save image to file
    plot_file = f"{filepath}\\variable_importance_graph.png"
    plot.save(plot_file,width=14,height=8)
    
    return(plot_file)

def heatmap_graph(data,test_set_names,X_cols,filepath):
    """
    Creates a heatmap of variable importance.
    """
    #Set up dataframe
    combi_compound = pd.DataFrame(np.vstack(data),index=test_set_names)
    combi_compound.columns = X_cols 
    
    #Melt the data to get in plottable form
    data_melt = combi_compound.reset_index().melt(id_vars=combi_compound.index.name,var_name='Variable',value_name="Value")
    data_melt.columns = ['index','Variable','Weight']
    
    #Sort order by median values of each variable
    median_values = data_melt.groupby('Variable')['Weight'].median().sort_values(ascending=False)
    data_melt['Variable'] = pd.Categorical(data_melt['Variable'],categories=median_values.index,ordered=True)
    
    #Make the heatmap
    plot = (ggplot(data_melt,aes(x='index',y='Variable',fill='Weight')) + #set up x, y, fill
                  geom_tile() +  #create heatmap
                  scale_fill_gradient2(low='red',mid='white',high='green',midpoint=np.median(data_melt['Weight'])) + #set fill scale
                  theme(axis_text_x = element_blank(), #no x axis text
                        axis_ticks_major_x = element_blank(), #no x axis ticks
                        axis_text_y=element_text(size=8)) + #y axis smaller font size to fit all variables
                  labs(x='',y='',title='') #turn off titles
            )
    
    #save image to file
    plot_file = f"{filepath}\\variable_heatmap.png"
    plot.save(plot_file,width=12,height=8)
    
    return(plot_file)
