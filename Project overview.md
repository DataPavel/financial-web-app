## Project Definition

### Project Overview

For the last decade, I was working in the finance department of different companies. One of the functions of the finance department is to provide periodic results to management and shareholders. Finance specialists usually present the results as a huge amount of different and difficult excel tables with long and not user-friendly formulas. However, management and shareholders require a less difficult representation of data. Therefore, other tools may be considered when presenting the results of company activity.

In this project, I will be trying to come up with a format for a management report, which can be easy to read and access by shareholders through the corporate website. The data I will be using is dummy data, but it can be replaced with a real one.

### Problem Statement

The problem which needs to be solved is a lack of convenient means of communication of financial data to shareholders. The solution will be a corporate dashboard web application displaying financial data.

### Metrics

The report should be easy to access and not difficult to read. It is difficult to come up with an appropriate metric. Let's say that if the report can be accessed through the internet, it is easy to access and if the report shows appropriate visualizations (ie axis are labeled, there is a title, appropriate graph for a particular data)
## Methodology

### Data Preprocessing

No data preprocessing is necessary, because dummy data is taken

### Implementation

The web application is implemented using the Dash package. The application takes data from the `data` folder which should be updated. After updating the data, the report automatically updated accordingly. 
The performance data represents a data frame with the following columns: Date, Company, Studio, Project, Category, Country, Country_code, OS, Counterparty, Amount_USD.   
The cash balance data represents a data frame with the following columns: Date, Company, Cash balance.

### Refinement
The main complication that occurred during the coding process is the implementation of conditional dropdowns. I took the code of Gabri-al from GitHub as a starting point. As a result, you can choose a legal entity and the next dropdown with the studio will be updated accordingly. The same flow with the project dropdown. However, if you choose studio or project first, the first two dropdowns will not be updated. I left this for future thinking.

## Results
### Justification

The final results are discussed in detail. Explain the exploration as to why some techniques worked better than others, or how improvements were made are documented.
The web application gives a comprehensive snapshot of how a company is doing at a particular point in time from different angles. The information is provided by the legal entity, studio, and project. The application includes such metrics as available cash, profit, revenue, marketing, and development.  

Profit:
- Profit by month  
- Cumulative profit  
- Profit by project  

Revenue:  
- Revenue by month  
- Revenue by country  
- Revenue by category  
- Each category of revenue by counterparty  

Marketing:  
- Marketing by month  
- Marketing by country  
- Marketing by counterparty  

Development:  
- Development by month  
- Development by country  
- Development by category  
- Each category of Development by counterparty
 
## Conclusion
### Reflection

In conclusion, I can say that the application is successfully implemented and provides the necessary insights for shareholders and management about how the company is doing. The application is accessible through a website and provides summary data that is easy to read.  During the development of the application I encountered many difficulties such as the implementation of conditional dropdowns.

### Improvement

There is some improvement that should be implemented at a later date. The main improvement is adding to the app functionality that allows downloading underlying data from the application in case someone will want to inspect it in detail. The easiest solution is to create a button near each graph that will allow the extraction of the underlying data. One of the main downsides of the application is that it displays properly only from a PC or laptop. When you open the application from a mobile phone device, the visualizations do not display correctly.







