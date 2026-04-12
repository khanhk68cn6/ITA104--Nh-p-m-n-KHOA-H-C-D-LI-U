import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler, StandardScaler

plt.style.use('default')
sns.set_palette('husl')
data_path = 'ITA105_Lab_3_Finance.csv'

print('=== BÀI 3: CHỈ SỐ CÔNG TY ===')

# 1. Khám phá
df = pd.read_csv(data_path)
print('Kích thước:', df.shape)
print('Head:\\n', df.head())
print('Stats:\\n', df.describe())
print()

# 2. Boxplot scale/outliers
columns = df.columns
fig, axes = plt.subplots(2, 2, figsize=(15, 10))
axes = axes.ravel()
for i, col in enumerate(columns):
    sns.boxplot(y=df[col], ax=axes[i])
    axes[i].set_title(col)
plt.tight_layout()
plt.savefig('finance_box_before.png', dpi=300)
plt.show()
print('Outliers: doanh_thu >5000 (công ty cực lớn).')
print()

# 3. Chuẩn hóa
scaler_mm = MinMaxScaler()
df_mm = pd.DataFrame(scaler_mm.fit_transform(df), columns=columns)
print('MinMax stats:\\n', df_mm.describe())

scaler_z = StandardScaler()
df_z = pd.DataFrame(scaler_z.fit_transform(df), columns=columns)
print('ZScore stats:\\n', df_z.describe())
print()

# 4. Scatter doanh_thu vs loi_nhuan
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
pairs = [('doanh_thu_musd', 'loi_nhuan_musd')]
labs = ['Raw', 'MinMax', 'ZScore']
dfs = [df, df_mm, df_z]
for i, (colx, coly) in enumerate(pairs):
    axes[i].scatter(dfs[i][colx], dfs[i][coly], alpha=0.6)
    axes[i].set_xlabel(colx)
    axes[i].set_ylabel(coly)
    axes[i].set_title(f'Scatter {labs[i]}')
plt.tight_layout()
plt.savefig('finance_scatter_compare.png', dpi=300)
plt.show()
print()

# 5. Nhận xét/Thảo luận
print('=== NHẬN XÉT ===')
print('- Ngoại lệ lớn (doanh_thu 5000-10000): MinMax không phù hợp (kéo tất cả về gần 0-1, outliers dominate).')
print('- Z-Score tốt hơn.')
print('- Cho Linear Regression/KNN tài chính: Z-Score (standardizes variance, robust outliers, good for distance-based KNN).')
print('- MinMax chỉ nếu cần bounded [0,1] và no heavy outliers.')
print('Hoàn thành!')
