import numpy as np
from scipy.optimize import minimize

# Parámetros de los activos
retorno_a = 0.08
volatilidad_a = 0.12
retorno_b = 0.12
volatilidad_b = 0.20
correlacion = 0.2
tasa_libre_riesgo = 0.02

# Matriz de covarianza
covarianza = correlacion * volatilidad_a * volatilidad_b
matriz_covarianza = np.array([
    [volatilidad_a**2, covarianza],
    [covarianza, volatilidad_b**2]
])

def calcular_retorno_cartera(w_a):
    w_b = 1 - w_a
    return w_a * retorno_a + w_b * retorno_b

def calcular_volatilidad_cartera(w_a):
    w_b = 1 - w_a
    pesos = np.array([w_a, w_b])
    varianza_cartera = np.dot(pesos.T, np.dot(matriz_covarianza, pesos))
    return np.sqrt(varianza_cartera)

def calcular_ratio_sharpe(w_a):
    retorno_cartera = calcular_retorno_cartera(w_a)
    volatilidad_cartera = calcular_volatilidad_cartera(w_a)
    if volatilidad_cartera == 0:  # Evitar división por cero
        return -np.inf
    return (retorno_cartera - tasa_libre_riesgo) / volatilidad_cartera

# --- Cálculo para diferentes asignaciones de capital ---
pesos_a = np.linspace(0, 1, 100)
retornos_cartera = [calcular_retorno_cartera(w) for w in pesos_a]
volatilidades_cartera = [calcular_volatilidad_cartera(w) for w in pesos_a]
ratios_sharpe = [calcular_ratio_sharpe(w) for w in pesos_a]

# --- Optimización del Ratio de Sharpe ---
# Queremos maximizar el Ratio de Sharpe, que es equivalente a minimizar el negativo del Ratio de Sharpe
def negativo_ratio_sharpe(w_a):
    return -calcular_ratio_sharpe(w_a[0])

# Restricciones para los pesos (w_a entre 0 y 1)
bounds = ((0, 1),)

# Minimización utilizando scipy.optimize.minimize
# w0 es un punto de partida inicial para la optimización
resultado_optimizacion = minimize(negativo_ratio_sharpe, x0=[0.5], bounds=bounds)

w_a_optimo = resultado_optimizacion.x[0]
w_b_optimo = 1 - w_a_optimo

retorno_cartera_optimo = calcular_retorno_cartera(w_a_optimo)
volatilidad_cartera_optima = calcular_volatilidad_cartera(w_a_optimo)
ratio_sharpe_maximo = calcular_ratio_sharpe(w_a_optimo)

print(f"Pesos óptimos: A = {w_a_optimo:.4f}, B = {w_b_optimo:.4f}")
print(f"Retorno esperado de la cartera optimizada: {retorno_cartera_optimo:.4f}")
print(f"Volatilidad de la cartera optimizada: {volatilidad_cartera_optima:.4f}")
print(f"Ratio de Sharpe máximo: {ratio_sharpe_maximo:.4f}")