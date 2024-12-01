# Bollinger Bands Width Stock Scanner - NYSE, NASDAQ, B3 (Brazil) & BINANCE
The Bollinger Bands Width Stock Scanner is a technical analysis tool that can be used to identify potential price breakouts or breakdowns for (almost) all stocks at once on select exchanges (NYSE, NASDAQ & B3 in Brazil): By entering the desired value into the tool, one can filter out for stocks with tight prices that are about to rise or fall.

Find out more about using Bollinger Bands Width alongside your trading strategies here:
https://www.tradingview.com/support/solutions/43000501972-bollinger-bands-width-bbw/

## Requirements
Python 3.6 or newer.

## Local Installation via Docker
Before running inside a Docker container, a Docker image must be created. In the project directory run:

```bash
docker build -t bbw-stock-scanner .
```

```bash
docker run -d -p 8888:8080 bbw-stock-scanner
```

Then go to: http://localhost:8888

## Live Demo
You can try Bollinger Bands Width Stock Scanner online without installing Python at:
[https://bbw-stock-scanner-cs76jitc4q-rj.a.run.app/](https://bbw-stock-scanner-322498647605.southamerica-east1.run.app/)

## Recommended usage
The recommended values for the Bollinger Band Width indicator can vary depending on the time frame. For example:
- For daily scans, enter a value of 0.12 for BBW to get tight stocks.
- For 4-hour scans, the optimum value will be 0.04
- For hourly scans, enter a value of 0.02
- For 15 minutes, enter bbw value of 0.08

## Hosting
The demo app is currently hosted on Google Cloud Run.<br>
The sample app.yaml file contained in this repo will allow for Google App Engine deployments as well.

## Issues
If you found a bug or have a question, please open an issue. Email will not be replied.

## Warning
Trading is a risky activity, especially when done using an automated program.<br>
Never trade without checking results provided by the Bollinger Bands Width Scanner:<br>
Any monetary losses are not my fault.

## Author
Diogo Lessa

## License
Bollinger Bands Width Stock Scanner (bbw-stock-scanner) is available under the MIT license.
