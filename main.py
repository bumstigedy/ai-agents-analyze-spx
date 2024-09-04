import pandas as pd
import datetime as dt
import os
import glob
#
from download_reports import download_files_from_folder
from merge_pdfs import merge_pdfs
from process_pdf import read_pdf_content
#
from crewai import Agent, Task, Crew
from ta_analysis_tool import TechnicalAnalysisTools
#
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
########------------------> INPUT FOLDER PATHS <------------------------
# reminded------->reset dropbox api------>
folder_paths = [
    "<insert first folder name>",
    "<insert second folder name>",
    "insert third folder name"]
########################################################################
# add model in case we want to change the llm model or the temperature #
# LLM_model=ChatOpenAI(model_name="gpt-4-turbo",temperature=0.7)
# use claude as it gives much better results

LLM_model = ChatAnthropic(
    model="claude-3-5-sonnet-20240620",
    temperature=0.7,
    timeout=None,
    max_retries=2,
)
#
# delete all existing pdf files 
# Get all PDF files in the current directory
pdf_files = glob.glob("*.pdf")

# Loop through the list of PDF files and delete them
for pdf_file in pdf_files:
    try:
        os.remove(pdf_file)
        print(f"Deleted: {pdf_file}")
    except OSError as e:
        print(f"Error: {pdf_file} : {e.strerror}")
#
# download files from dropbox 
    
for folder_path in folder_paths:
    try:
        download_files_from_folder(folder_path)
    except:
        print("doesn't look like that folder is here today :( ")
#
# merge all the pdf files into a single pdf
output_filename = "merged.pdf"
merge_pdfs(output_filename)
#############
# Function to save analysis to a file
def save_analysis_to_file(analysis, file_path):
    try:
        with open(file_path, 'w') as file:
            file.write(analysis)
        print(f"Analysis saved to {file_path}")
    except Exception as e:
        print(f"Error saving analysis to file: {e}")

# Read context from file
def read_context(filename):
    with open(filename, 'r') as file:
        return file.read()

# Get the context
ta_context = read_context('TA_context.txt')

# Create a Financial Analyst agent with context
TA_analyst = Agent(
    role='Technical Analyst',
    goal='Analyze S&P 500 technical indicators',
    backstory="""You're an experienced financial analyst specializing in technical analysis.  You have years of experience on wall street adn are a Certified Market
     Technicial or CMT You are good at distilling techincal market indicators into concise market summaries that traders can understand
     and act on""" + ta_context,
    tools=[TechnicalAnalysisTools()],
    llm =LLM_model
)
#################################################
pdf_path = "merged.pdf"
pdf_content = read_pdf_content(pdf_path)
# Create a Financial Analyst agent with context
hedge_fund_analyst = Agent(
    role='Financial/Fundamental Analyst',
    goal="""Please answer these questions:
            1. What are the impacts of flows on prices?
            2. What is the market outlook?
            3. Identify support and resistance levels.
            4. Identify any trade recommendations as well as risks.  Don't include risks from indicators being inaccurate.  
            5. Provide a detailed and insightful analysis based on the information given.""",
    backstory="""You are a highly experienced financial analyst providing analysis and recommendations to traders. You have years of experience at 
    hedge funds and working on Wall Street. Analyze and summarize the following market report:
                    """ + pdf_content,
    llm =LLM_model
                    #[:4000] # Limit content to 4000 characters to fit within token limits
    
)
####################################################################################################################################
# Create a writer agent
writer = Agent (
    role = "Professional Finance Short-Article Writer",
    goal = "Summarize market information from the hedge fund and technical analyst into concise actionable content.  ",
    backstory = """ You are a renowned financial writer a proven track record of summarizing the current market, risks, and identifying trading opportunities.  
    Your clients include professional buy side investors as well as retail investors and traders. """,
    verbose=True,
    allow_delegation=True,
    llm =LLM_model,
    max_iter=25,
    )

#######################################
# Define the TA analysis task
TA_analysis_task = Task(
    description="""Analyze the S&P 500 technical indicators and provide comprehensive insights. Consider the provided context in your analysis.  
    Identify overbought or oversold conditions and any bullish or bearish divergences. Cover the last year in your analysis, but give more focus on
    the past 20 days""",
    expected_output="""Concise summary of the current technical indicators and any trade recommendations.  Don't comment on technical indicators that are not present
    """,
    agent=TA_analyst
)
# Define the hedge fund analysis task
fund_analysis_task = Task(
    description="""Analyze what is currently driving markets, identify risks, and identify trading opportunities""",
    expected_output="""Concise summary of what is driving the markets, risks, and trade recommendations.  Do not mention the names of any 
    specific analysts or hedge funds or firms.  Flag any upcoming events that may move the markets.  Comment on monetary policy or the Fed/FOMC if applicable.    
    """,
    agent=hedge_fund_analyst
)
# Define the writer task
blog_task=Task(description = """ Write a short article that highlights the current market from a technical and fundamental basis.  Note the impact from
               flows on the market and the sentiment of the hedge fund articles.
           Make trade recommendations where possible and highlight risk to future or existing positions. 
           """,
           expected_output="""Full blog post of at least 3 paragraphs. Include input from the Technical Analyst and the Financial/Fundamental Analyst.  """,
           agent=writer
)
# Create a crew with the analyst and the task
crew = Crew(
    agents=[TA_analyst,hedge_fund_analyst, writer],
    tasks=[TA_analysis_task, fund_analysis_task,blog_task]
)

# Execute the analysis
result = crew.kickoff()

# Print the result
print(result)
date_t=str(pd.Timestamp.today().day) + "_"+str(pd.Timestamp.today().month)+"_"+str(pd.Timestamp.today().year)
save_analysis_to_file(result.raw, "analysis_{}.txt".format(date_t))
