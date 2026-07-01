# ============================================= 
# 차시 9 예제: 선박 연료소비 예측 ML 모델
# =============================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing   import StandardScaler
from sklearn.metrics         import mean_squared_error, r2_score, mean_absolute_error

# 한글 폰트 설정 (Windows)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False
# ── 1. 데이터 로드 ────────────────────────────
df = pd.read_csv("ship_operational_data.csv")
print("데이터셋 크기:", df.shape)
print(df.describe().round(2))
# ── 2. 특성/목표 변수 분리 ────────────────────
features = ['speed_knot','draft_m','displacement_ton','wind_speed_ms','wave_height_m','engine_load_pct','trim_m']
target   = 'fuel_consumption_ton_day'
X = df[features]
y = df[target]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)
# ── 3. 스케일링 ──────────────────────────────
scaler  = StandardScaler()
X_train_sc = scaler.fit_transform(X_train)
X_test_sc  = scaler.transform(X_test)
# ── 4. 모델 학습 & 평가 ──────────────────────
models = {
    "선형 회귀": LinearRegression(),
    "랜덤 포레스트": RandomForestRegressor(n_estimators=100, random_state=42),
    "그래디언트 부스팅": GradientBoostingRegressor(n_estimators=100, random_state=42),
}
results = {}
for name, model in models.items():
    model.fit(X_train_sc, y_train)
    y_pred = model.predict(X_test_sc)
    mse    = mean_squared_error(y_test, y_pred)
    rmse   = np.sqrt(mse)
    mae    = mean_absolute_error(y_test, y_pred)
    r2     = r2_score(y_test, y_pred)
    cv_r2  = cross_val_score(model, scaler.transform(X), y, cv=5, scoring='r2').mean()
    results[name] = {"RMSE": rmse, "MAE": mae, "R²": r2, "CV R²": cv_r2}
    print(f"\n▶ {name}")
    print(f"  RMSE: {rmse:.3f} ton/day  MAE: {mae:.3f}  R²: {r2:.4f}  CV R²: {cv_r2:.4f}")
# ── 5. 특성 중요도 (랜덤 포레스트) ───────────
rf_model   = models["랜덤 포레스트"]
importances= pd.Series(rf_model.feature_importances_, index=features).sort_values(ascending=True)
# ── 6. 시각화 ─────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
# (1) 실제 vs 예측 (최우수 모델)
best_model = models["그래디언트 부스팅"]
y_pred_best= best_model.predict(X_test_sc)
axes[0].scatter(y_test, y_pred_best, c='steelblue', s=80, alpha=0.8)
axes[0].plot([y_test.min(), y_test.max()],             [y_test.min(), y_test.max()], 'r--', linewidth=1.5)
axes[0].set_xlabel("실제 연료소비 (ton/day)")
axes[0].set_ylabel("예측 연료소비 (ton/day)")
axes[0].set_title("그래디언트 부스팅: 실제 vs 예측")
axes[0].grid(True, alpha=0.3)
# (2) 특성 중요도
axes[1].barh(importances.index, importances.values, color='teal', alpha=0.8)
axes[1].set_xlabel("중요도"); axes[1].set_title("특성 중요도 (랜덤 포레스트)")
axes[1].grid(True, axis='x', alpha=0.3)
# (3) 속력별 연료소비 예측 곡선
speed_range = np.linspace(10, 18, 50)
mean_vals   = X.mean()
X_pred_list = []
for v in speed_range:
    row = mean_vals.copy(); row["speed_knot"] = v
    X_pred_list.append(row.values)
X_pred_df  = pd.DataFrame(X_pred_list, columns=features)
X_pred_arr = scaler.transform(X_pred_df)
y_pred_curve = best_model.predict(X_pred_arr)
axes[2].plot(speed_range, y_pred_curve, 'b-', linewidth=2)
axes[2].scatter(df["speed_knot"], df[target], alpha=0.5, color='orange', label='실측')
axes[2].set_xlabel("속력 (knots)"); axes[2].set_ylabel("연료소비 (ton/day)")
axes[2].set_title("속력에 따른 연료소비 예측"); axes[2].legend()
axes[2].grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("ml_fuel_prediction.png", dpi=150)
plt.show()