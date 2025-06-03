import numpy as np

# Datos de entrada
R_A = 0.08  # Retorno esperado Activo A
s_A = 0.12  # Volatilidad Activo A
R_B = 0.12  # Retorno esperado Activo B
s_B = 0.20  # Volatilidad Activo B
rho_AB = 0.2  # Correlación entre A y B
R_f = 0.02  # Tasa libre de riesgo

# Inicialización de variables para almacenar el resultado óptimo
max_sharpe_ratio = -np.inf
optimal_w_A = 0
optimal_w_B = 0
optimal_portfolio_return = 0
optimal_portfolio_volatility = 0

# Iterar a través de posibles pesos para el Activo A
# Los pesos w_A irán desde 0 hasta 1 en incrementos de 0.001
# w_B será 1 - w_A

for w_A in np.arange(0, 1.001, 0.001):
    w_B = 1 - w_A

    # Calcular el retorno esperado de la cartera
    R_p = w_A * R_A + w_B * R_B

    # Calcular la volatilidad de la cartera
    s_p = np.sqrt(w_A**2 * s_A**2 + w_B**2 * s_B**2 + 2 * w_A * w_B * s_A * s_B * rho_AB)

    # Calcular el Ratio de Sharpe
    if s_p != 0:
        sharpe_ratio = (R_p - R_f) / s_p
    else:
        sharpe_ratio = -np.inf

    # Actualizar si encontramos un Ratio de Sharpe mayor
    if sharpe_ratio > max_sharpe_ratio:
        max_sharpe_ratio = sharpe_ratio
        optimal_w_A = w_A
        optimal_w_B = w_B
        optimal_portfolio_return = R_p
        optimal_portfolio_volatility = s_p

# Imprimir los resultados óptimos
output = f"""Resultados de la Optimización de Cartera:
-------------------------------------------------
Ratio de Sharpe Máximo: {max_sharpe_ratio:.4f}
Peso Óptimo Activo A (w_A): {optimal_w_A:.4f}
Peso Óptimo Activo B (w_B): {optimal_w_B:.4f}
Retorno Esperado de la Cartera Óptima: {optimal_portfolio_return:.4f}
Volatilidad de la Cartera Óptima: {optimal_portfolio_volatility:.4f}
"""
print(output)