import yfinance as yf
import pandas as pd
import talib
from crewai_tools import BaseTool
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TechnicalAnalysisTools(BaseTool):
    name: str = "Analyze Stock Technical Indicators"
    description: str = "Analyzes stock technical indicators and provides insights."

    def __init__(self, **data):
        super().__init__(**data)

    def _run(self, symbol: str = "^GSPC", period: str = "1y") -> str:
        """Analyzes stock technical indicators and provides insights."""
        logger.info(f"Starting analysis for symbol: {symbol}, period: {period}")
        
        valid_periods = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
        if period not in valid_periods:
            logger.error(f"Invalid period: {period}")
            return f"Error: Invalid period '{period}'. Valid periods are: {', '.join(valid_periods)}"

        try:
            logger.info("Downloading data from Yahoo Finance")
            data = yf.download(symbol, period=period)

            if data.empty:
                logger.error(f"No data available for symbol: {symbol}, period: {period}")
                return f"Error: No data available for symbol '{symbol}' and period '{period}'"

            logger.info("Calculating technical indicators")
            data['RSI'] = talib.RSI(data['Close'])
            data['MACD'], data['MACD_Signal'], _ = talib.MACD(data['Close'])
            data['SMA_200'] = talib.SMA(data['Close'], timeperiod=200)
            data['SMA_50'] = talib.SMA(data['Close'], timeperiod=50)
            data['SMA_20'] = talib.SMA(data['Close'], timeperiod=20)

            csv_filename = f"{symbol}_technical_analysis.csv"
            logger.info(f"Saving data to {csv_filename}")
            data.to_csv(csv_filename)

            result = f"Technical analysis data for {symbol} has been saved to {csv_filename}."
            result += f"\n\nData summary:\n{data.describe()}"
            result += f"\n\nLast 5 rows of data:\n{data.tail()}"

            logger.info("Analysis completed successfully")
            return result

        except Exception as e:
            logger.exception(f"Error occurred while analyzing {symbol}")
            return f"Error occurred while analyzing {symbol}: {str(e)}"

# Usage example:
# tool = TechnicalAnalysisTools()
# result = tool.run(symbol="AAPL", period="6mo")
# print(result)