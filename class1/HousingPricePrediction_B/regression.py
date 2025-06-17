import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import r2_score

def get_user_input():
    square_footages = []
    prices = []
    
    print("Enter house data (enter 'q' to finish):")
    print("Format: area,price (e.g.: 1500,300)")
    
    while True:
        user_input = input("> ")
        if user_input.lower() == 'q':
            break
        
        try:
            parts = user_input.split(',')
            if len(parts) != 2:
                raise ValueError("Please enter two comma-separated values")
            
            footage = float(parts[0].strip())
            price = float(parts[1].strip())
            
            if footage <= 0 or price <= 0:
                raise ValueError("Values must be greater than 0")
                
            square_footages.append(footage)
            prices.append(price)
            
        except ValueError as e:
            print(f"Input error: {e}. Please try again or enter 'q' to exit")
    
    if len(square_footages) < 3:
        print("At least 3 data points are required for analysis")
        return None, None
    
    return np.array(square_footages), np.array(prices)

def predict_price(size, model_type='linear'):
    if model_type == 'linear':
        return slope_linear * size + intercept_linear
    elif model_type == 'quadratic':
        return intercept_poly + coeffs_poly[1] * size + coeffs_poly[2] * (size**2)
    else:
        raise ValueError("Model type must be 'linear' or 'quadratic'")

X, y = get_user_input()
if X is None or y is None:
    exit()

X = X.reshape(-1, 1)

model_linear = LinearRegression()
model_linear.fit(X, y)

slope_linear = model_linear.coef_[0]
intercept_linear = model_linear.intercept_
r2_linear = r2_score(y, model_linear.predict(X))

poly = PolynomialFeatures(degree=2)
X_poly = poly.fit_transform(X)
model_poly = LinearRegression()
model_poly.fit(X_poly, y)

coeffs_poly = model_poly.coef_
intercept_poly = model_poly.intercept_
r2_poly = r2_score(y, model_poly.predict(X_poly))

plt.figure(figsize=(10, 6))

plt.scatter(X, y, color='blue', label='Data Points', zorder=2)

X_plot = np.linspace(X.min(), X.max(), 100).reshape(-1, 1)

y_linear_plot = model_linear.predict(X_plot)
plt.plot(X_plot, y_linear_plot, color='red', 
         label=f'Linear Regression: Price = {slope_linear:.3f} × Area + {intercept_linear:.1f}', zorder=1)

y_poly_plot = model_poly.predict(poly.transform(X_plot))
plt.plot(X_plot, y_poly_plot, color='green', linestyle='--', 
         label=f'Quadratic Regression: R²={r2_poly:.2f}', zorder=1)

plt.xlabel('Area (sq.ft)', fontsize=12)
plt.ylabel('Price ($1000s)', fontsize=12)
plt.title('House Price vs. Area', fontsize=14)
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

custom_size = float(input("\nEnter house area to predict (enter 0 to exit): "))

if custom_size <= 0:
    print("Area must be greater than 0")

            
price_linear = predict_price(custom_size, 'linear')
price_poly = predict_price(custom_size, 'quadratic')
        
print(f"\n--- Prediction Results ---")
print(f"Linear regression prediction ({custom_size} sq.ft): ${price_linear:.0f},000")
print(f"Quadratic regression prediction ({custom_size} sq.ft): ${price_poly:.0f},000")

