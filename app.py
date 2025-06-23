import panel as pn
import pandas as pd
import plotly.express as px
from datetime import datetime

pn.extension('plotly', sizing_mode='stretch_width')

# Load the cleaned dataset
df = pd.read_csv('teacher_workload_cleaned.csv')

# Custom CSS for advanced styling with enhanced suggestion box and footer
custom_css = """
body {
    background: linear-gradient(135deg, #1ABC9C 0%, #F1C40F 50%, #B39DDB 100%), url('data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100"%3E%3Ccircle cx="50" cy="50" r="20" fill="rgba(255, 215, 0, 0.1)" opacity="0.3"/%3E%3Cpath d="M10 10 L90 90 M10 90 L90 10" stroke="rgba(26, 188, 156, 0.2)" stroke-width="2"/%3E%3C/svg%3E');
    font-family: 'Helvetica', sans-serif;
    color: #2c3e50;
}
h1 {
    color: #ffffff;
    font-size: 2.5em; /* Reduced from 2.8em for balance */
    text-align: center;
    padding: 10px; /* Reduced from 15px for compactness */
    background: linear-gradient(90deg, #3498db 0%, #2980b9 70%, #1ABC9C 100%); /* Extended gradient for variety */
    border-radius: 12px; /* Slightly increased for softer edges */
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3); /* Enhanced shadow for depth */
    margin-bottom: 25px; /* Adjusted spacing */
    text-transform: uppercase; /* Added for emphasis */
    letter-spacing: 2px; /* Added for elegance */
}
.widget-box {
    background: linear-gradient(135deg, rgba(179, 157, 219, 0.2) 0%, rgba(241, 196, 15, 0.1) 50%, rgba(26, 188, 156, 0.15) 100%), url('data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="50" height="50" viewBox="0 0 50 50"%3E%3Ccircle cx="25" cy="25" r="10" fill="rgba(255, 215, 0, 0.05)" opacity="0.2"/%3E%3C/svg%3E');
    padding: 15px;
    border-radius: 10px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    margin: 10px 0;
}
.plotly-graph-div {
    background: linear-gradient(135deg, rgba(179, 157, 219, 0.15) 0%, rgba(241, 196, 15, 0.2) 50%, rgba(26, 188, 156, 0.1) 100%), url('data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="60" height="60" viewBox="0 0 60 60"%3E%3Cpath d="M10 50 L50 10 M10 10 L50 50" stroke="rgba(255, 215, 0, 0.15)" stroke-width="1" opacity="0.3"/%3E%3Ccircle cx="30" cy="30" r="5" fill="rgba(26, 188, 156, 0.1)"/%3E%3C/svg%3E');
    margin: 15px 0;
    border: 2px solid #3498db;
    border-radius: 10px;
    padding: 15px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}
.suggestion-box {
    background: linear-gradient(135deg, rgba(179, 157, 219, 0.2) 0%, rgba(241, 196, 15, 0.1) 50%, rgba(26, 188, 156, 0.15) 100%), url('data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="50" height="50" viewBox="0 0 50 50"%3E%3Ccircle cx="25" cy="25" r="10" fill="rgba(255, 215, 0, 0.05)" opacity="0.2"/%3E%3C/svg%3E');
    padding: 20px;
    border-left: 5px solid #2ecc71;
    border-radius: 10px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    margin: 20px 0;
    width: 100%;
    min-height: 200px;
}
.suggestion-box h3 {
    color: #2ecc71;
    font-size: 1.5em;
    margin-top: 0;
    font-weight: bold;
    text-transform: uppercase;
}
.suggestion-box p {
    font-size: 20px;
    line-height: 1.6;
    margin: 10px 0;
}
.footer {
    background: linear-gradient(135deg, #B39DDB 0%, #1ABC9C 100%);
    text-align: center;
    padding: 10px;
    border-top: 2px solid rgba(52, 152, 219, 0.5);
    margin-top: 20px;
    font-size: 0.9em;
    color: #ffffff;
    width: 100%;
    border-radius: 0 0 10px 10px;
    box-shadow: 0 -2px 6px rgba(0,0,0,0.1);
}
"""

# Apply custom CSS
pn.config.raw_css.append(custom_css)

# Create a dropdown widget for teacher selection with styling
teacher_select = pn.widgets.Select(name='Select Teacher', options=['All'] + list(df['Teacher_ID'].unique()), 
                                  width=350, sizing_mode='fixed', styles={'background': '#ecf0f1', 'padding': '10px', 'border-radius': '5px'})

# Function to update bar chart with annotations
def update_bar_chart(teacher):
    if teacher == 'All':
        filtered_df = df
    else:
        filtered_df = df[df['Teacher_ID'] == teacher]
    avg_hours = filtered_df.groupby('Task')['Hours_Spent'].mean().reset_index()
    fig = px.bar(avg_hours, x='Task', y='Hours_Spent', 
                 title='Average Hours per Task', 
                 labels={'Hours_Spent': 'Avg Hours', 'Task': 'Task'},
                 color='Task', color_discrete_sequence=px.colors.qualitative.Pastel1)
    fig.update_layout(
        margin=dict(l=40, r=40, t=60, b=40),
        showlegend=True,
        plot_bgcolor='rgba(179, 208, 219, 0.3)',  # Lightish teal-lavender blend
        paper_bgcolor='rgba(241, 216, 179, 0.3)',  # Lightish golden-lavender blend
        autosize=True
    )
    for i, row in avg_hours.iterrows():
        fig.add_annotation(x=row['Task'], y=row['Hours_Spent'],
                           text=f'{row["Hours_Spent"]:.1f} hrs',
                           showarrow=True, arrowhead=1)
    return pn.pane.Plotly(fig, sizing_mode='stretch_width')

# Function to create pie chart with custom theme
total_hours = df.groupby('Task')['Hours_Spent'].sum().reset_index()
pie_fig = px.pie(total_hours, names='Task', values='Hours_Spent', 
                 title='Workload Distribution by Task', 
                 color_discrete_sequence=px.colors.qualitative.Pastel1)
pie_fig.update_layout(
    margin=dict(l=40, r=40, t=60, b=40),
    plot_bgcolor='rgba(179, 208, 219, 0.3)',  # Lightish teal-lavender blend
    paper_bgcolor='rgba(241, 216, 179, 0.3)',  # Lightish golden-lavender blend
    autosize=True
)
pie_pane = pn.pane.Plotly(pie_fig, sizing_mode='stretch_width')

# Function to create scatter plot with trendline
scatter_fig = px.scatter(df[df['Task'] == 'grading'], x='Class_Size', y='Hours_Spent', 
                        title='Grading Hours vs. Class Size',
                        labels={'Class_Size': 'Class Size', 'Hours_Spent': 'Grading Hours'},
                        trendline='ols', color_discrete_sequence=['#3498db'])
scatter_fig.update_layout(
    margin=dict(l=40, r=40, t=60, b=40),
    plot_bgcolor='rgba(179, 208, 219, 0.3)',  # Lightish teal-lavender blend
    paper_bgcolor='rgba(241, 216, 179, 0.3)',  # Lightish golden-lavender blend
    autosize=True
)
scatter_pane = pn.pane.Plotly(scatter_fig, sizing_mode='stretch_width')

# Function to generate dynamic optimization suggestions
def update_suggestions(teacher):
    if teacher == 'All':
        filtered_df = df
    else:
        filtered_df = df[df['Teacher_ID'] == teacher]
    suggestions = ['### Optimization Suggestions']
    total_hours = filtered_df['Hours_Spent'].sum()
    grading_hours = filtered_df[filtered_df['Task'] == 'grading']['Hours_Spent'].sum() if not filtered_df[filtered_df['Task'] == 'grading'].empty else 0
    class_size = filtered_df['Class_Size'].mean() if not filtered_df.empty else 0

    if grading_hours > 7.82:
        suggestions.append('- Automate grading with Google Forms or Quizizz (~3–5 hrs saved).')
    if total_hours > 30:
        suggestions.append('- Delegate planning with Planboard (~1–2 hrs/week saved).')
    if class_size > 40 and grading_hours > 7:
        suggestions.append('- Reduce class size or add assistants (~1–2 hrs saved).')
    if not suggestions[1:]:
        suggestions.append('- No optimizations needed based on current data.')
    
    return pn.pane.Markdown('\n'.join(suggestions), css_classes=['suggestion-box'])

# Footer with credits and timestamp (hyperlink removed)
footer = pn.pane.Markdown(f'''
<footer class="footer">
    👨‍🏫 Developed by Samragya Banerjee |  
    📅 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S IST')}
</footer>
''')

# Layout the dashboard with optimized spacing
dashboard = pn.Column(
    pn.Row(pn.pane.Markdown('# Teacher Workload Optimization Dashboard', sizing_mode='stretch_width')),
    pn.Row(teacher_select, align='center', margin=(0, 0, 20, 0)),
    pn.Row(update_bar_chart(teacher_select.value), sizing_mode='stretch_width'),
    pn.Row(pie_pane, sizing_mode='stretch_width'),
    pn.Row(scatter_pane, sizing_mode='stretch_width'),
    pn.Row(update_suggestions(teacher_select.value), sizing_mode='stretch_width'),
    footer
)

# Serve the dashboard
dashboard.servable()

# Update charts and suggestions when teacher changes
def update_all(event):
    dashboard[2] = update_bar_chart(teacher_select.value)
    dashboard[5] = update_suggestions(teacher_select.value)

teacher_select.param.watch(update_all, 'value')