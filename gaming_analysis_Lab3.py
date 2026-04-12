import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler, StandardScaler

plt.style.use('default')
sns.set_palette('husl')
data_path = 'ITA105_Lab_3_Gaming.csv'

print('=== BÀI 4: NGƯỜI CHƠI TRỰC TUYẾN ===')

# 1. Khám phá, missing, phân phối
df = pd.read_csv(data_path)
print('Kích thước:', df.shape)
print('Head:\\n', df.head())
print('Missing:\\n', df.isnull().sum())
print('Stats:\\n', df.describe())
print('\\nNote: Có giá trị âm (gio_choi), cần xử lý nếu cần.')
print()

# 2. Trực quan hóa phân phối
columns = df.columns
fig, axes = plt.subplots(2, 2, figsize=(15, 10))
axes = axes.ravel()
for i, col in enumerate(columns):
    axes[i].hist(df[col], bins=20, alpha=0.7)
    axes[i].set_title(f'Phân phối {col}')
plt.tight_layout()
plt.savefig('gaming_hist_before.png', dpi=300)
plt.show()
print()

# 3. Chuẩn hóa
scaler_mm = MinMaxScaler()
df_mm = pd.DataFrame(scaler_mm.fit_transform(df), columns=columns)
print('MinMax stats:\\n', df_mm.describe())

scaler_z = StandardScaler()
df_z = pd.DataFrame(scaler_z.fit_transform(df), columns=columns)
print('ZScore stats:\\n', df_z.describe())
print()

# 4. Histogram so sánh
fig, axes = plt.subplots(2, 2, figsize=(18, 12))
axes = axes.ravel()
for i, col in enumerate(columns):
    axes[i].hist([df[col], df_mm[col], df_z[col]], label=['Raw', 'MinMax', 'ZScore'], alpha=0.6)
    axes[i].legend()
    axes[i].set_title(f'{col}')
plt.tight_layout()
plt.savefig('gaming_compare_hist.png', dpi=300)
plt.show()
print()

# 5. Thảo luận/nhận xét
print('=== THẢO LUẬN ===')
print('- Ngoại lệ: Người chơi "cày cuốc" cực (gio_choi>500, diem_tich_luy>15000).')
print('- MinMax bị ảnh hưởng nặng outliers (scale kéo về 1.0).')
print('- Z-Score ổn hơn, phân phối chuẩn cho clustering/KNN.')
print('- Cho clustering/KNN: Z-Score tốt vì outliers ít skew, Euclidean distance fair.')
print('- Xử lý âm: clip to 0 or investigate.')
print('Hoàn thành!') 
