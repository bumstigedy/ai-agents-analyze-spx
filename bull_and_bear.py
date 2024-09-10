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
from ta_analysis_tool_ticker import TechnicalAnalysisTools
#
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
########------------------> INPUT FOLDER PATHS <------------------------
# reminded------->reset dropbox api------>
folder_paths = [
    "/current/2024/september/sep 7/goldman/s&t",
    "/current/2024/september/sep 7/bofa"
    ]
########################################################################
# add model in case we want to change the llm model or the temperature #
# LLM_model=ChatOpenAI(model_name="gpt-4-turbo",temperature=0.7)

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
symbols_context = read_context('symbols.txt')
# Create a Financial Analyst agent with context
TA_analyst = Agent(
    role='Technical Analyst',
    goal='Analyze technical indicators for a given ticker or symbol.',
    backstory="""You're an experienced financial analyst specializing in technical analysis.  You have years of experience on wall street adn are a Certified Market
     Technicial or CMT You are good at distilling techincal market indicators into concise market summaries that traders can understand
     and act on.  You recommend stops based on key support and resistance levels.  """ + ta_context + symbols_context,
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
# Create a bullish trade recommendation
bull = Agent (
    role = "Buy side analyst",
    goal = """Utilize market information from the hedge fund and technical analyst to identify a bullish trade recommendation.  Identify potential entry points
      and stops based on support levels from technical analysis.  """,
    backstory = """ You are a renowned buy side analyst with a proven track record of identifying bullish trade recommendations.
     You have years of experience working on wall street. """,
    verbose=True,
    allow_delegation=True,
    llm =LLM_model,
    max_iter=25,
    )
####################################################################################################################################
# Create a bullish trade recommendation
bear = Agent (
    role = "Buy side analyst",
    goal = """Utilize market information from the hedge fund and technical analyst to identify a bearish trade recommendation. Identify potential entry points
     and stops based on resistance levels from technical analysis """,
    backstory = """ You are a renowned buy side analyst with a proven track record of identifying bearish trade recommendations.
     You have years of experience working on wall street. """,
    verbose=True,
    allow_delegation=True,
    llm =LLM_model,
    max_iter=25,
    )
########
# Create a bullish trade recommendation
writer = Agent (
    role = "Professional technical writer",
    goal = """Write a concise summary of the trade recommendations from the bull and the bear.  Use the fundemantal and technical analysts to identify
    trade recommendations, entry points, and stops.  You will need to tell the technical analyst which tickers or symbols need analysis""",
    backstory = """ You are a renowned financial writer with an ability to clearly summarize trade recommendations.   """,
    verbose=True,
    allow_delegation=True,
    llm =LLM_model,
    max_iter=25,
    )


#######################################
# Define the TA analysis task
TA_analysis_task = Task(
    description="""Analyze the S&P 500 technical indicators """,
    expected_output="""Identify trade recommendations, entry points, and stops.""",
    agent=TA_analyst
)
# Define the hedge fund analysis task
fund_analysis_task = Task(
    description="""Analyze what is currently driving markets, identify risks, and identify trading opportunities""",
    expected_output="""Identify trade recommendations and risks.    """,
    agent=hedge_fund_analyst
)
# Define the writer task
trades_task=Task(description = """ Identify one bullish and one bearish trade.  For each trade recommend an entry point from technical analysis, 
                 a stop from technical analysis, and any risks identified from fundamental or technical analysis. """,
           expected_output="""Concise summary of trades.  """,
           agent=writer
)
# Create a crew with the analyst and the task
crew = Crew(
    agents=[TA_analyst,hedge_fund_analyst, bull, bear, writer],
    tasks=[TA_analysis_task, fund_analysis_task,trades_task]
)

# Execute the analysis
result = crew.kickoff()

# Print the result
print(result)
date_t=str(pd.Timestamp.today().month) + "_"+str(pd.Timestamp.today().day)+"_"+str(pd.Timestamp.today().year)
save_analysis_to_file(result.raw, "trades_{}.txt".format(date_t))