# AI Agents for S&P 500 Market Analysis and Stock Trading Recommendations

## Overview

This project utilizes AI agents to perform comprehensive market analysis on the S&P 500 index and individual stocks. It combines technical analysis, fundamental analysis from hedge fund reports, and AI-powered insights to provide a holistic view of the market and generate trading recommendations.

## Live Demo

Check out our live demo showcasing an example conversation between AI agents:

[https://bumstigedy.github.io/ai-agents-analyze-spx/](https://bumstigedy.github.io/ai-agents-analyze-spx/)

## Features

- Automated downloading of hedge fund reports from Dropbox
- PDF processing and merging capabilities
- Technical analysis using popular indicators (RSI, MACD, Moving Averages) for S&P 500 and individual stocks
- Fundamental analysis based on hedge fund reports
- AI-powered market summary and trade recommendations
- Daily analysis output with timestamps
- Bullish and bearish trade recommendations for individual stocks

## Project Structure

- `main.py`: Orchestrates the S&P 500 analysis process
- `bull_and_bear.py`: Generates daily bullish and bearish trade recommendations for individual stocks
- `download_reports.py`: Downloads hedge fund reports from Dropbox
- `merge_pdfs.py`: Merges multiple PDF files into a single document
- `process_pdf.py`: Extracts text content from PDF files
- `ta_analysis_tool.py`: Performs technical analysis on S&P 500 data
- `ta_analysis_tool_ticker.py`: Performs technical analysis on any given stock ticker
- `TA_context.txt`: Knowledge base for technical analysis and indicators
- `symbols.txt`: List of stock symbols and their descriptions

## How It Works

### S&P 500 Analysis (main.py)

1. The system downloads the latest hedge fund reports from specified Dropbox folders.
2. PDF reports are merged and processed to extract textual content.
3. Technical analysis is performed on S&P 500 data using various indicators.
4. AI agents analyze both technical and fundamental data:
   - A Technical Analyst agent interprets the technical indicators.
   - A Financial/Fundamental Analyst agent examines the hedge fund reports.
   - A Professional Finance Writer agent synthesizes insights from both analyses.
5. The final output is a comprehensive market analysis, including current trends, potential risks, and trade recommendations.

### Individual Stock Recommendations (bull_and_bear.py)

1. The system downloads and processes hedge fund reports similar to the S&P 500 analysis.
2. Technical analysis is performed on individual stocks using the `ta_analysis_tool_ticker.py`.
3. AI agents collaborate to generate trade recommendations:
   - A Technical Analyst agent analyzes technical indicators for given tickers.
   - A Financial/Fundamental Analyst examines hedge fund reports for market insights.
   - A Buy-side Analyst identifies bullish trade opportunities.
   - Another Buy-side Analyst identifies bearish trade opportunities.
   - A Professional Technical Writer synthesizes the information into concise trade recommendations.
4. The output includes one bullish and one bearish trade recommendation, complete with entry points, stops, and associated risks.

## AI Agents

### Technical Analyst
- **Role**: Analyze S&P 500 and individual stock technical indicators
- **Backstory**: An experienced financial analyst specializing in technical analysis with years of Wall Street experience and CMT certification
- **Tools**: TechnicalAnalysisTools (custom tool for calculating and interpreting technical indicators)

### Financial/Fundamental Analyst
- **Role**: Analyze hedge fund reports and provide fundamental market insights
- **Backstory**: Highly experienced financial analyst with years of experience at hedge funds and on Wall Street

### Buy-side Analysts (Bull and Bear)
- **Role**: Identify bullish and bearish trade opportunities based on technical and fundamental analysis
- **Backstory**: Renowned buy-side analysts with proven track records in identifying profitable trade recommendations

### Professional Finance Short-Article Writer / Technical Writer
- **Role**: Summarize market information and trade recommendations into concise, actionable content
- **Backstory**: Renowned financial writer with a proven track record of summarizing market conditions, risks, and trading opportunities for professional and retail investors

## Crew Tasks

The AI agents work together as crews to produce comprehensive market analyses and trade recommendations. Their tasks include:

1. Analyzing S&P 500 and individual stock technical indicators
2. Examining current market drivers, identifying risks, and spotting trading opportunities based on hedge fund reports
3. Generating bullish and bearish trade recommendations with specific entry points and stops
4. Synthesizing information into concise, actionable reports

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
4. Update the `folder_paths` in `main.py` and `bull_and_bear.py` with your Dropbox folder names
5. Run `main.py` to start the S&P 500 analysis process
6. Run `bull_and_bear.py` to generate daily trade recommendations

## Output

- S&P 500 analysis results are saved daily in the format: `analysis_DD_MM_YYYY.txt`
- Trade recommendations are saved daily in the format: `trades_MM_DD_YYYY.txt`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[Add your chosen license here]

## Disclaimer

This project is for educational and research purposes only. Always consult with a qualified financial advisor before making investment decisions. The trade recommendations generated by this system should not be considered as financial advice.
