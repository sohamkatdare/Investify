import openai
import os
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_KEY')
openai.api_key = OPENAI_API_KEY

def summarize(prompt):
    reduced_prompt = ' '.join(prompt.replace('\n', ' ').split(' ')[:1600])
    augmented_prompt = "summarize this text to 500 words: " + reduced_prompt
    # raw_return = openai.Completion.create(model="text-davinci-003", prompt=augmented_prompt, temperature=.5, max_tokens=2000)["choices"][0]["text"].strip(' .')
    raw_return = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes and simplifies Investopedia articles through your complete knowledge of finance and investing."},
                {"role": "user", "content": augmented_prompt}, 
        ],
        max_tokens=1500,
    )['choices'][0]['message']['content'].strip(' .')
    incomplete = ''
    if raw_return[0] == raw_return[0].lower():
        incomplete = raw_return[:raw_return.index('.')+2]
    return raw_return.replace(incomplete, '') + '.'
if __name__ == '__main__':
    text = '''Pete Rathburn is a copy editor and fact-checker with expertise in economics and personal finance and over twenty years of experience in the classroom. Investopedia / Laura Porter 
    The Altman Z-score is the output of a credit-strength test that gauges a publicly traded manufacturing company's likelihood of bankruptcy. The Altman Z-score, a variation of the traditional z-score in statistics, is based on five financial ratios that can be calculated from data found on a company's annual 10-K report. It uses profitability, leverage, liquidity, solvency, and activity to predict whether a company has a high probability of becoming insolvent.
    
    NYU Stern Finance Professor Edward Altman developed the Altman Z-score formula in 1967, and it was published in 1968. Over the years, Altman has continued to reevaluate his Z-score. From 1969 until 1975, Altman looked at 86 companies in distress, then 110 from 1976 to 1995, and finally 120 from 1996 to 1999, finding that the Z-score had an accuracy of between 82% and 94%.
    
    In 2012, he released an updated version called the Altman Z-score Plus that one can use to evaluate public and private companies, manufacturing and non-manufacturing companies, and U.S. and non-U.S. companies. One can use Altman Z-score Plus to evaluate corporate credit risk. The Altman Z-score has become a reliable measure of calculating credit risk.
    
    One can calculate the Altman Z-score as follows:
    
    Altman Z-Score = 1.2A + 1.4B + 3.3C + 0.6D + 1.0E
    
    A score below 1.8 means it's likely the company is headed for bankruptcy, while companies with scores above 3 are not likely to go bankrupt. Investors can use Altman Z-scores to determine whether they should buy or sell a stock if they're concerned about the company's underlying financial strength. Investors may consider purchasing a stock if its Altman Z-Score value is closer to 3 and selling or shorting a stock if the value is closer to 1.8.
    
    In more recent years, however, a Z-Score closer to 0 indicates a company may be in financial trouble. In a lecture given in 2019 titled "50 Years of the Altman Score," Professor Altman himself noted that recent data has shown that 0—not 1.8—is the figure at which investors should worry about a company's financial strength. The two-hour lecture is available to view for free on YouTube.
    
    In 2007, the credit ratings of specific asset-related securities had been rated higher than they should have been. The Altman Z-score indicated that the companies' risks were increasing significantly and may have been heading for bankruptcy.

    Altman calculated that the median Altman Z-score of companies in 2007 was 1.81. These companies' credit ratings were equivalent to a B. This indicated that 50% of the firms should have had lower ratings, were highly distressed and had a high probability of becoming bankrupt.

    Altman's calculations led him to believe a crisis would occur and there would be a meltdown in the credit market. He believed the crisis would stem from corporate defaults, but the meltdown, which brought about the 2008 financial crisis, began with mortgage-backed securities (MBS). However, corporations soon defaulted in 2009 at the second-highest rate in history.
    The Altman Z-score, a variation of the traditional z-score in statistics, is based on five financial ratios that can be calculated from data found on a company's annual 10-K report. The formula for Altman Z-Score is 1.2*(working capital / total assets) + 1.4*(retained earnings / total assets) + 3.3*(earnings before interest and tax / total assets) + 0.6*(market value of equity / total liabilities) + 1.0*(sales / total assets). Investors can use Altman Z-score Plus to evaluate corporate credit risk. A score below 1.8 signals the company is likely headed for bankruptcy, while companies with scores above 3 are not likely to go bankrupt. Investors may consider purchasing a stock if its Altman Z-Score value is closer to 3 and selling, or shorting, a stock if the value is closer to 1.8. In more recent years, Altman has stated a score closer to 0 rather than 1.8 indicates a company is closer to bankruptcy. In 2007, Altman's Z-score indicated that the companies' risks were increasing significantly. The median Altman Z-score of companies in 2007 was 1.81, which is very close to the threshold that would indicate a high probability of bankruptcy. Altman's calculations led him to believe a crisis would occur that would stem from corporate defaults, but the meltdown, which brought about the 2008 financial crisis, began with mortgage-backed securities (MBS); however, corporations soon defaulted in 2009 at the second-highest rate in history. NYU Stern. "Predicting Financial Distress of Companies: Revisiting the Z-Score and Zeta Models," Page 18. Accessed Nov. 19, 2021. NYU Stern. "Professor Edward Altman Launches Digital App for Renowned Z-Score, "Altman Z-Score Plus." Accessed Nov. 19, 2021. NYU Stern. "Predicting Financial Distress of Companies: Revisiting the Z-Score and Zeta Models," Page 26. Accessed Nov. 19, 2021. NYU Stern. "A 50-Year Retrospective on Credit Risk Models, the Altman Z-Score Family of Models and Their Applications to Financial Markets and Managerial Strategies," Page 20. Accessed Nov. 19, 2021. NYU Stern. "Special Report on Defaults and Returns in the High-Yield Bond Market: The Year 2007 in Review and Outlook," Pages 9-13 and 27. Accessed Nov. 19, 2021 NYU Stern. "Special Report on Defaults and Returns in the High-Yield Bond Market: The Year 2007 in Review and Outlook," Pages 9-13 and 26. Accessed Nov. 19, 2021.  NYU Stern. "Special Report On Defaults and Returns in the High-Yield Bond and Distressed Debt Market: The Year 2009 in Review and Outlook," Page 3. Accessed Nov. 19, 2021. By clicking “Accept All Cookies”, you agree to the storing of cookies on your device to enhance site navigation, analyze site usage, and assist in our marketing efforts.'''
    summary = summarize(text)
    print(summary)