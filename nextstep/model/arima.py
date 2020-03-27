from statsmodels.tsa.arima_model import ARIMA
from pandas.plotting import autocorrelation_plot
from matplotlib import pyplot
from statsmodels.graphics.tsaplots import plot_pacf
from .base_model import base_model
import pandas as pd
import sys

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")


class arima(base_model):
    def __init__(self, config):
        super().__init__()
        self._config = config
        self._model = None
    
    def build_model(self, data):
        print('Building arima model.')

        size = int(len(data) * self._config['train_size'])
        data = data[self._config['label_column']].values
        train, test = data[:size].tolist(), data[size:]
        predictions = []
        for t in range(len(test)):
            model = ARIMA(train,
                        order=(self._config['lag'], self._config['differencing'], self._config['window_size']))
            fitted_model = model.fit()
            predicted = fitted_model.forecast()[0]
            predictions.append(predicted)
            train.append(test[t])

        print('Evaluating arima performance.')
        self.evaluation(test, predictions)

        model = ARIMA(data,
                      order=(self._config['lag'], self._config['differencing'], self._config['window_size']))
        model_fitted = model.fit()
        self._model = model_fitted
        return model
    
    def predict(self, X_new):
        return self._model.predict(X_new)

    def autocorrelation(self, data, number_of_time_step = 20):
        try:
            autocorrelation_plot(data[self._config['label_column']][:number_of_time_step])
            pyplot.show()
        except:
            print('Data time step is below 20, please specify paramter number of time step. to be below 20.')
        return None
    
    def partial_autocorrelation(self, data, lags = 20):
        try:
            plot_pacf(data[self._config['label_column']], lags = lags)
            pyplot.show()
        except:
            print('Data time step is below 20, please specify paramter lags to be below 20.')
        return None
    
    def residual_plot(self):
        df = pd.DataFrame(self._model.resid)
        df.plot()
        df.plot(kind='kde')
        pyplot.show()
        print("residual mean is {}".format(sum(self._model.resid)/len(self._model.resid)))
        return None
    
    def residual_density_plot(self):
        pd.DataFrame(self._model.resid).plot(kind='kde')
        pyplot.show()
        return None        
        
    
if __name__ == "__main__":
    import pandas as pd
    data = pd.read_csv("../../development/Feature_Mart/feature_mart_merged_1.csv")
    data = data

    parameter_tuning_config = {
        'number_of_time_step' : 30,
        'number_of_lags' : 30
        }
    
    user_config = {'lag' : 2,
                   'differencing' : 0,
                   'window_size' : 2,
                   'label_column' : 'USEP',
                   'train_size' : 0.8,
                   'seed' : 33}
    arima_shell = arima(user_config)
    data = data[-150:]
    arima_shell.autocorrelation(data)
    arima_shell.partial_autocorrelation(data)
    arima_shell.build_model(data)
    arima_shell.residual_plot()
    