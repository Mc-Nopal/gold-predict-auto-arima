import yfinance as yf
import pandas as pd
import numpy as np
from pmdarima import auto_arima
import datetime

def fetch_gold_history_yf(days=60, currency="USD"):
    try:
        if currency == "USD":
            df = yf.download("GC=F", period=f"{days}d", interval="1d", progress=False)
            if df.empty:
                df = yf.download("GLD", period=f"{days}d", interval="1d", progress=False)
            
            if isinstance(df.columns, pd.MultiIndex):
                prices = df[('Close', 'GC=F')] if ('Close', 'GC=F') in df.columns else df.iloc[:, 0]
            else:
                prices = df['Close']
                
            prices_per_gram = prices / 31.1035
            
        elif currency == "IDR":
            df_gold = yf.download("GC=F", period=f"{days}d", interval="1d", progress=False)
            df_rate = yf.download("USDIDR=X", period=f"{days}d", interval="1d", progress=False)
            
            p_usd = df_gold[('Close', 'GC=F')] if isinstance(df_gold.columns, pd.MultiIndex) else df_gold['Close']
            r_idr = df_rate[('Close', 'USDIDR=X')] if isinstance(df_rate.columns, pd.MultiIndex) else df_rate['Close']
            
            prices_per_gram = (p_usd / 31.1035) * r_idr
            
        else:
            df = yf.download("GC=F", period=f"{days}d", interval="1d", progress=False)
            prices = df.iloc[:, 0]
            prices_per_gram = prices / 31.1035
            
        df_result = pd.DataFrame({"Harga": prices_per_gram}).dropna()
        df_result.index = pd.to_datetime(df_result.index).normalize()
        df_result = df_result.asfreq('D', method='ffill')
        df_result.index.name = "Tanggal"
        
        return df_result

    except Exception as e:
        today = datetime.date.today()
        dates = [today - datetime.timedelta(days=i) for i in range(days)]
        prices = [1200000 + (i * 1000) for i in range(days)]
        df_fallback = pd.DataFrame({"Harga": prices}, index=pd.to_datetime(dates))
        df_fallback = df_fallback.asfreq('D', method='ffill')
        df_fallback.index.name = "Tanggal"
        return df_fallback

def predict_gold_arima(df, n_forecast_days=7):
    y = df["Harga"].dropna()
    
    # Jalankan Auto ARIMA
    model = auto_arima(y, seasonal=False, stepwise=True, suppress_warnings=True, error_action="ignore")
    
    # Hitung akurasi model
    fitted_vals = model.predict_in_sample()
    actuals = y.values
    mape = np.mean(np.abs((actuals - fitted_vals) / actuals)) * 100
    accuracy = max(0.0, 100.0 - mape)
    
    # Prediksi masa depan
    forecast = model.predict(n_periods=n_forecast_days)
    
    last_date = y.index[-1]
    future_dates = pd.date_range(start=last_date + datetime.timedelta(days=1), periods=n_forecast_days, freq='D')
    
    df_forecast = pd.DataFrame({
        "Prediksi_Harga_Gram": forecast
    }, index=future_dates)
    df_forecast.index.name = "Tanggal"
    
    return df_forecast, accuracy