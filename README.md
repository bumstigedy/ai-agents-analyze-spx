# AI Agents for S&P 500 Market Analysis

## Overview

This project utilizes AI agents to perform comprehensive market analysis on the S&P 500 index. It combines technical analysis, fundamental analysis from hedge fund reports, and AI-powered insights to provide a holistic view of the market.

## Live Demo

Check out our live demo showcasing an example conversation between AI agents:

[https://bumstigedy.github.io/ai-agents-analyze-spx/](https://bumstigedy.github.io/ai-agents-analyze-spx/)

## Features

- Automated downloading of hedge fund reports from Dropbox
- PDF processing and merging capabilities
- Technical analysis using popular indicators (RSI, MACD, Moving Averages)
- Fundamental analysis based on hedge fund reports
- AI-powered market summary and trade recommendations
- Daily analysis output with timestamps

## Project Structure

- `main.py`: Orchestrates the entire analysis process
- `download_reports.py`: Downloads hedge fund reports from Dropbox
- `merge_pdfs.py`: Merges multiple PDF files into a single document
- `process_pdf.py`: Extracts text content from PDF files
- `ta_analysis_tool.py`: Performs technical analysis on S&P 500 data
- `TA_context.txt`: Knowledge base for technical analysis and indicators

## How It Works

1. The system downloads the latest hedge fund reports from specified Dropbox folders.
2. PDF reports are merged and processed to extract textual content.
3. Technical analysis is performed on S&P 500 data using various indicators.
4. AI agents analyze both technical and fundamental data:
   - A Technical Analyst agent interprets the technical indicators.
   - A Financial/Fundamental Analyst agent examines the hedge fund reports.
   - A Professional Finance Writer agent synthesizes insights from both analyses.
5. The final output is a comprehensive market analysis, including current trends, potential risks, and trade recommendations.

## AI Agents

### Technical Analyst
- **Role**: Analyze S&P 500 technical indicators
- **Backstory**: An experienced financial analyst specializing in technical analysis with years of Wall Street experience and CMT certification
- **Tools**: TechnicalAnalysisTools (custom tool for calculating and interpreting technical indicators)
- **Knowledge Base**: Comprehensive information on technical analysis and indicators (provided in TA_context.txt)

### Financial/Fundamental Analyst
- **Role**: Analyze hedge fund reports and provide fundamental market insights
- **Backstory**: Highly experienced financial analyst with years of experience at hedge funds and on Wall Street
- **Knowledge Base**: Content from downloaded and processed hedge fund reports

### Professional Finance Short-Article Writer
- **Role**: Summarize market information from both analysts into concise, actionable content
- **Backstory**: Renowned financial writer with a proven track record of summarizing market conditions, risks, and trading opportunities for professional and retail investors

## Crew Task

The AI agents work together as a crew to produce a comprehensive market analysis. Their tasks include:

1. Analyzing S&P 500 technical indicators and providing insights
2. Examining current market drivers, identifying risks, and spotting trading opportunities based on hedge fund reports
3. Synthesizing information from both analyses into a concise, actionable blog post

## Development Process

The majority of the coding for this project was done using Claude Dev within Visual Studio Code, leveraging AI assistance for efficient development and problem-solving.

## Dependencies

- pandas
- yfinance
- talib
- crewai
- langchain_openai
- langchain_anthropic

## Setup and Usage

1. Clone the repository
2. Install the required dependencies
3. Set up your Dropbox API credentials
4. Update the `folder_paths` in `main.py` with your Dropbox folder names
5. Run `main.py` to start the analysis process

## Output

The analysis results are saved daily in the format: `analysis_DD_MM_YYYY.txt`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[Add your chosen license here]

## Disclaimer

This project is for educational and research purposes only. Always consult with a qualified financial advisor before making investment decisions.
