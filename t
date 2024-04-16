import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
# Указатель, что график необходимо построить все в той же оболочке Jupyter, но теперь он выводится как обычная картинка
%matplotlib inline
 
df = pd.read_csv('./student_scores.csv')
df = df.sort_values(by = ['Hours', 'Scores']) # сортировка значений по Времени, далее по Оценкам
df.head()
 
df.describe()
 
df.plot(x = 'Hours', y = 'Scores', style = 'o')
plt.title('Часы и оценки')
plt.xlabel('Проведённое за учёбой время')
plt.ylabel('Успеваемость в процентах')
plt.show()
 
# Подготовка данных
X = df.iloc[:, :-1].values
y = df.iloc[:, 1].values
# Разбиение данных
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)
 
# Обучение модели
regressor = LinearRegression()
regressor.fit(X_train, y_train)
 
# Коэффициент b (y = m * x + b)
print(regressor.intercept_)
 
# Коэффициент m
print(regressor.coef_) # показывает на сколько процентов повысится успеваемость, если студент будет тратить на 1 час больше для обучения
 
# Прогнозирование
y_pred = regressor.predict(X_test)
 
df2 = pd.DataFrame({'Данные': y_test, 'Предсказанные': y_pred})
df2
 
# Отображение показателей ошибок
from sklearn import metrics
print('Mean Absolute Error (MAE):', metrics.mean_absolute_error(y_test, y_pred)) # среднее значение абсолютного значения ошибок.
print('Mean Squared Error (MSE):', metrics.mean_squared_error(y_test, y_pred)) # среднее значение квадратов ошибок
print('Root Mean Squared Error (RMSE):', np.sqrt(metrics.mean_squared_error(y_test, y_pred))) # квадратный корень из среднего значения квадратов ошибок
 
# Показатель RMSE со значением меньше 10% говорит о хорошей обученности модели
 
# Функция прямой по найденным коэффициентам
y = lambda x: regressor.coef_ * x + regressor.intercept_
x = np.linspace(1, 10, 10)
 
# Отображение графика линейной регрессии
df.plot(x = 'Hours', y = 'Scores', style = 'o')
plt.plot(x, y(x))
plt.title('Часы и оценки')
plt.xlabel('Проведённое за учёбой время')
plt.ylabel('Успеваемость в процентах')
plt.show()
 